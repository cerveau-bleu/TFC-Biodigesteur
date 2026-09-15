"""Reproduction du chapitre 2 de TFC_Jason_MUKOMBELA.pdf.

Python >= 3.10, bibliothèque standard uniquement. Unités dans les noms.
Modèle moyen de prédimensionnement, sans validation biologique ou mécanique.
Les constantes par défaut sont celles du PDF fourni, non des mesures.
"""
from dataclasses import dataclass, asdict, replace
from math import pi, sqrt, log, exp, expm1, isfinite, inf
from pathlib import Path
import argparse
import csv
import json


@dataclass(frozen=True)
class Parametres:
    dechets_kg_j: float = 10.0
    eau_dilution_kg_j: float = 10.0
    rho_b_kg_m3: float = 1000.0
    cp_b_J_kgK: float = 4180.0
    trh_cible_j: float = 25.0
    fraction_gaz: float = 0.20
    rapport_H_D: float = 1.5
    diametre_cuve_m: float = 0.820
    metal_m: float = 0.002
    isolant_m: float = 0.080
    lambda_isolant_W_mK: float = 0.040
    ponts_W_K: float = 0.50
    tube_exterieur_m: float = 0.016
    tube_interieur_m: float = 0.014
    diametre_helice_m: float = 0.600
    tours: int = 16
    pas_m: float = 0.050
    axe_bas_m: float = 0.080
    raccord_immerge_m: float = 1.0
    raccord_externe_m: float = 4.0
    lambda_cuivre_W_mK: float = 380.0
    debit_eau_L_min: float = 0.60
    rho_eau_kg_m3: float = 992.0
    cp_eau_J_kgK: float = 4180.0
    mu_eau_Pas: float = 0.000653
    lambda_eau_W_mK: float = 0.630
    Nu_reference: float = 3.66
    hb_W_m2K: float = 50.0
    encrassement_externe_m2K_W: float = 0.002
    encrassement_interne_m2K_W: float = 0.0002
    zeta_accessoires: float = 20.0
    dp_generateur_Pa: float = 2000.0
    dp_reglage_Pa: float = 1000.0
    reserve_pompe: float = 0.25
    hauteur_pompe_m: float = 0.50
    gravite_m_s2: float = 9.81
    capacite_aux_J_K: float = 65000.0
    ambiance_C: float = 20.0
    initiale_C: float = 20.0
    intrant_C: float = 20.0
    consigne_C: float = 35.0
    entree_eau_C: float = 45.0
    pertes_boucle_W: float = 25.0
    pompe_electrique_W: float = 5.0
    generateur_W: float = 1200.0
    # Illustrations uniquement : aucune caractérisation attribuée à Ley Luyi.
    fraction_MS_dechets: float = 0.20
    fraction_MV_MS: float = 0.90
    fraction_volume_inactif: float = 0.05

    def verifier(self):
        fractions = ('fraction_gaz', 'fraction_MS_dechets', 'fraction_MV_MS',
                     'fraction_volume_inactif')
        temperatures = ('ambiance_C', 'initiale_C', 'intrant_C', 'consigne_C', 'entree_eau_C')
        zeros = ('eau_dilution_kg_j', 'ponts_W_K', 'raccord_immerge_m',
                 'raccord_externe_m', 'encrassement_externe_m2K_W',
                 'encrassement_interne_m2K_W', 'zeta_accessoires',
                 'dp_generateur_Pa', 'dp_reglage_Pa', 'reserve_pompe',
                 'capacite_aux_J_K', 'pertes_boucle_W', 'pompe_electrique_W')
        for k, v in asdict(self).items():
            if not isinstance(v, (int, float)) or not isfinite(v):
                raise ValueError(f'{k}: nombre fini requis')
            if k in fractions:
                if not 0 <= v < 1:
                    raise ValueError(f'{k}: valeur attendue dans [0,1[')
            elif k in temperatures:
                if v <= -273.15:
                    raise ValueError(f'{k}: température non physique')
            elif v < 0 or (v == 0 and k not in zeros):
                raise ValueError(f'{k}: valeur positive requise')
        if self.tours != int(self.tours):
            raise ValueError('Le nombre de tours doit être entier')
        if self.tube_interieur_m >= self.tube_exterieur_m:
            raise ValueError('Diamètre intérieur du tube >= extérieur')
        if self.consigne_C <= self.initiale_C:
            raise ValueError('Ce script traite une montée vers une consigne supérieure')
        if self.entree_eau_C <= self.consigne_C:
            raise ValueError("L'eau chaude doit dépasser la consigne")


def white_darcy(Re, di, Ds):
    """Eq. 2.37 ; White, Darcy. Refuse les extrapolations hors domaine."""
    ratio = di / Ds
    De = Re * sqrt(ratio)
    if Re <= 0 or Re >= 2000:
        raise ValueError('Référence laminaire des raccords : exiger 0 < Re < 2000')
    if not (3.878e-4 < ratio < 0.066 and 11.6 < De < 2000):
        raise ValueError('Hors domaine de White retenu au chapitre 2')
    return (64 / Re) / (1 - (1 - (11.6 / De)**0.45)**(1 / 0.45))


def temps_chauffe_s(C, G, K, eau, air, debut, fin):
    """Solution exacte eq. 2.44 ; inf si la consigne n'est pas atteignable."""
    if C <= 0 or G <= 0 or K < 0:
        raise ValueError('C > 0, G > 0, K >= 0 requis')
    if fin <= debut:
        return 0.0
    equilibre = (G * eau + K * air) / (G + K)
    if fin >= equilibre:
        return inf
    return C / (G + K) * log((equilibre - debut) / (equilibre - fin))


def calculer(p=Parametres()):
    """Equations 2.1 à 2.45 ; résultats non arrondis pour les calculs en chaîne."""
    p.verifier()
    m_j = p.dechets_kg_j + p.eau_dilution_kg_j
    q_j = m_j / p.rho_b_kg_m3
    D, do, di, Ds = (p.diametre_cuve_m, p.tube_exterieur_m,
                     p.tube_interieur_m, p.diametre_helice_m)
    H = D * p.rapport_H_D
    Hl = (1 - p.fraction_gaz) * H
    section = pi * D**2 / 4
    Vt = section * H
    L = p.tours * sqrt((pi * Ds)**2 + p.pas_m**2)
    droits = p.raccord_immerge_m + p.raccord_externe_m
    Vtube = pi * do**2 / 4 * (L + p.raccord_immerge_m)
    Vu = (1 - p.fraction_gaz) * Vt - Vtube
    radial = (D - Ds - do) / 2
    haut = p.axe_bas_m + p.tours * p.pas_m + do / 2
    niveau_retrait = Hl - q_j / section  # approximation, comme au chapitre
    if Vu <= q_j or radial <= 0 or p.pas_m <= do or p.axe_bas_m <= do/2 or haut >= Hl:
        raise ValueError('Géométrie incompatible : volume, jeu, pas ou immersion')
    Ao = pi * do * L
    r1 = D / 2 + p.metal_m
    r2 = r1 + p.isolant_m
    Klat = 2 * pi * p.lambda_isolant_W_mK * H / log(r2 / r1)
    Kdisque = p.lambda_isolant_W_mK * pi * r2**2 / p.isolant_m
    K = Klat + 2 * Kdisque + p.ponts_W_K
    pertes = K * (p.consigne_C - p.ambiance_C)
    Ealim = m_j * p.cp_b_J_kgK * (p.consigne_C - p.intrant_C)
    Qv = p.debit_eau_L_min * 1e-3 / 60
    mw = p.rho_eau_kg_m3 * Qv
    Cw = mw * p.cp_eau_J_kgK
    v = 4 * Qv / (pi * di**2)
    Re = p.rho_eau_kg_m3 * v * di / p.mu_eau_Pas
    De = Re * sqrt(di / Ds)
    f = white_darcy(Re, di, Ds)
    hw = p.Nu_reference * p.lambda_eau_W_mK / di
    Rfixe = (p.encrassement_externe_m2K_W + do / (2*p.lambda_cuivre_W_mK)
             * log(do/di) + do/di * (1/hw + p.encrassement_interne_m2K_W))
    U = 1 / (1/p.hb_W_m2K + Rfixe)
    UA = U * Ao
    efficacite = -expm1(-UA/Cw)
    G = Cw * efficacite
    Q35 = G * (p.entree_eau_C - p.consigne_C)
    sortie = p.entree_eau_C - Q35/Cw
    dyn = p.rho_eau_kg_m3 * v**2 / 2
    dphel = f * L/di * dyn
    dpdroits = 64/Re * droits/di * dyn
    dpsing = p.zeta_accessoires * dyn
    dp = dphel + dpdroits + dpsing + p.dp_generateur_Pa + p.dp_reglage_Pa
    dpsel = dp * (1+p.reserve_pompe)
    masse = p.rho_b_kg_m3 * Vu
    C = masse * p.cp_b_J_kgK + p.capacite_aux_J_K
    Tinf = (G*p.entree_eau_C + K*p.ambiance_C)/(G+K)
    t = temps_chauffe_s(C,G,K,p.entree_eau_C,p.ambiance_C,p.initiale_C,p.consigne_C)
    Trec = p.consigne_C - m_j/masse * (p.consigne_C-p.intrant_C)
    trec = temps_chauffe_s(C,G,K,p.entree_eau_C,p.ambiance_C,Trec,p.consigne_C)
    # Alternative cohérente si les auxiliaires restent initialement à la consigne.
    Trec_aux = p.consigne_C - Ealim/C
    trec_aux = temps_chauffe_s(C,G,K,p.entree_eau_C,p.ambiance_C,Trec_aux,p.consigne_C)
    maintien = pertes + Ealim/86400
    E_sensible = C*(p.consigne_C-p.initiale_C)
    if isfinite(t):
        int_T = Tinf*t + (p.initiale_C-Tinf)*C/(G+K)*(-expm1(-(G+K)*t/C))
        E_pertes = K*(int_T-p.ambiance_C*t)
        E_recue = G*(p.entree_eau_C*t-int_T)
    else:
        E_pertes = E_recue = inf
    return dict(
        debit_suspension_m3_j=q_j, volume_min_m3=q_j*p.trh_cible_j,
        diametre_sans_tube_m=(4*q_j*p.trh_cible_j/((1-p.fraction_gaz)*pi*p.rapport_H_D))**(1/3),
        hauteur_m=H, niveau_m=Hl, volume_total_m3=Vt,
        volume_gaz_m3=p.fraction_gaz*Vt, volume_tube_m3=Vtube,
        volume_utile_m3=Vu, trh_j=Vu/q_j, marge_volume_m3=Vu-q_j*p.trh_cible_j,
        trh_volume_actif_j=(1-p.fraction_volume_inactif)*Vu/q_j,
        ms_suspension_fraction=p.dechets_kg_j*p.fraction_MS_dechets/m_j,
        cov_illustrative_kgMV_m3_j=p.dechets_kg_j*p.fraction_MS_dechets*p.fraction_MV_MS/Vu,
        longueur_helice_m=L, longueur_hydraulique_m=L+droits, surface_active_m2=Ao,
        jeu_radial_m=radial, jeu_vertical_m=p.pas_m-do, sommet_tube_m=haut,
        niveau_apres_retrait_m=niveau_retrait, immersion_apres_retrait_m=niveau_retrait-haut,
        K_lateral_liquide_W_K=Klat*(1-p.fraction_gaz), K_lateral_gaz_W_K=Klat*p.fraction_gaz,
        K_disque_W_K=Kdisque, K_enveloppe_W_K=K, pertes_enveloppe_W=pertes,
        alimentation_kWh_j=Ealim/3.6e6, maintien_W=maintien, cuve_kWh_j=maintien*24/1000,
        total_previsionnel_kWh_j=(maintien+p.pertes_boucle_W+p.pompe_electrique_W)*24/1000,
        debit_eau_kg_s=mw, C_eau_W_K=Cw, vitesse_eau_m_s=v, Re=Re, De=De,
        hw_W_m2K=hw, resistance_fixe_m2K_W=Rfixe, U_W_m2K=U, UA_W_K=UA, G_W_K=G,
        puissance_consigne_W=Q35, sortie_eau_C=sortie, DT_log_K=Q35/UA,
        f_Darcy=f, pression_dynamique_Pa=dyn, dp_helice_Pa=dphel,
        dp_droits_Pa=dpdroits, dp_accessoires_Pa=dpsing, dp_total_Pa=dp,
        dp_selection_Pa=dpsel, hauteur_selection_m=dpsel/(p.rho_eau_kg_m3*p.gravite_m_s2),
        pompe_hydraulique_W=p.rho_eau_kg_m3*p.gravite_m_s2*p.hauteur_pompe_m*Qv,
        capacite_J_K=C, masse_suspension_kg=masse, equilibre_C=Tinf,
        demarrage_h=t/3600, recuperation_h=trec/3600,
        temperature_apres_apport_C=Trec, recuperation_auxiliaires_chauds_h=trec_aux/3600,
        demarrage_sensible_kWh=E_sensible/3.6e6, demarrage_pertes_kWh=E_pertes/3.6e6,
        demarrage_chaleur_recue_kWh=E_recue/3.6e6,
        puissance_initiale_W=G*(p.entree_eau_C-p.initiale_C),
        plafond_initial_serpentin_W=Cw*(p.entree_eau_C-p.initiale_C),
        marge_generateur_W=p.generateur_W-Cw*(p.entree_eau_C-p.initiale_C)-p.pertes_boucle_W,
        pression_hydrostatique_Pa=p.rho_b_kg_m3*p.gravite_m_s2*Hl)


def ecrire_csv(path, lignes):
    with Path(path).open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, help='JSON partiel ou complet des paramètres')
    parser.add_argument('--out', type=Path, default=Path('resultats'))
    args = parser.parse_args()
    p = Parametres(**json.loads(args.config.read_text(encoding='utf-8'))) if args.config else Parametres()
    r = calculer(p)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'parametres_utilises.json').write_text(json.dumps(asdict(p),indent=2),encoding='utf-8')
    # JSON strict : null pour une cible inaccessible ; CSV conserve inf explicitement.
    (args.out/'resultats.json').write_text(json.dumps({k:v if isfinite(v) else None for k,v in r.items()},indent=2,allow_nan=False),encoding='utf-8')
    ecrire_csv(args.out/'resultats.csv',[{'grandeur':k,'valeur':v} for k,v in r.items()])
    for k in ('volume_utile_m3','trh_j','puissance_consigne_W','maintien_W','demarrage_h','recuperation_h','hauteur_selection_m'):
        print(f'{k}: {r[k]:.8g}')
    print('Hypothèses de conception ; ne constitue pas une validation du dispositif.')


if __name__ == '__main__':
    main()
