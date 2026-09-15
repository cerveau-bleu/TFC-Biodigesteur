"""Compare des valeurs imprimées du PDF aux calculs ; tolérance d'arrondi explicite."""
from pathlib import Path
from dimensionnement import calculer, ecrire_csv

# clé, valeur imprimée, demi-unité du dernier chiffre affiché, référence PDF
REFERENCES = [
 ('volume_total_m3',.649565,.0000005,'2.11'),
 ('volume_gaz_m3',.129913,.0000005,'2.11'),
 ('volume_tube_m3',.006267,.0000005,'2.12'),
 ('volume_utile_m3',.513385,.0000005,'2.13'),
 ('trh_j',25.67,.005,'2.14'),
 ('K_enveloppe_W_K',3.00250,.000005,'2.17'),
 ('pertes_enveloppe_W',45.04,.005,'tableau pertes'),
 ('alimentation_kWh_j',.3483,.00005,'2.19'),
 ('maintien_W',59.55,.005,'2.21'),
 ('longueur_helice_m',30.1699,.00005,'2.23'),
 ('surface_active_m2',1.51650,.000005,'2.24'),
 ('debit_eau_kg_s',.00992,.000005,'2.27'),
 ('C_eau_W_K',41.4656,.00005,'2.27'),
 ('vitesse_eau_m_s',.06496,.000005,'2.28'),
 ('Re',1382,.5,'2.28'),
 ('hw_W_m2K',164.7,.05,'2.29'),
 ('resistance_fixe_m2K_W',.0091704,.00000005,'2.31'),
 ('U_W_m2K',34.281,.0005,'2.32'),
 ('UA_W_K',51.99,.005,'2.32'),
 ('G_W_K',29.630,.0005,'2.35'),
 ('puissance_consigne_W',296.30,.005,'2.35'),
 ('sortie_eau_C',37.85,.005,'2.35'),
 ('De',211.04,.005,'2.36'),
 ('f_Darcy',.09179,.000005,'2.37'),
 ('dp_helice_Pa',414.0,.05,'2.38'),
 ('dp_droits_Pa',34.6,.05,'2.39'),
 ('dp_total_Pa',3490.5,.05,'2.5.4'),
 ('dp_selection_Pa',4363,.5,'2.41'),
 ('hauteur_selection_m',.448,.0005,'2.41'),
 ('capacite_J_K',2210950,5,'2.43'),
 ('equilibre_C',42.70,.005,'2.6.1'),
 ('demarrage_h',20.35,.005,'2.6.1'),
 ('temperature_apres_apport_C',34.416,.0005,'2.45'),
 ('recuperation_h',1.38,.005,'2.6.2'),
 ('total_previsionnel_kWh_j',2.15,.005,'2.6.3'),
]


def main():
    r=calculer(); lignes=[]
    for cle, ref, tol, eq in REFERENCES:
        ecart=r[cle]-ref
        lignes.append(dict(grandeur=cle,reference=eq,pdf=ref,recalcul=r[cle],
                           ecart=ecart,tolerance_arrondi=tol,
                           conforme_arrondi=abs(ecart)<=tol+1e-10))
    Path('resultats').mkdir(exist_ok=True)
    ecrire_csv('resultats/audit_valeurs.csv',lignes)
    n=sum(x['conforme_arrondi'] for x in lignes)
    print(f'{n}/{len(lignes)} valeurs conformes à la précision imprimée.')
    if n != len(lignes):
        raise SystemExit(1)


if __name__=='__main__':
    main()
