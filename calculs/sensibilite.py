"""Reproduit les sensibilités §2.7 et exporte des trajectoires analytiques."""
from dataclasses import replace
from math import exp, isfinite
from pathlib import Path
from dimensionnement import Parametres, calculer, ecrire_csv
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('resultats'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    p = Parametres()
    for nom, champ, valeurs, sorties in [
        ('hb','hb_W_m2K',[10,20,30,50,100],['U_W_m2K','puissance_consigne_W','demarrage_h','recuperation_h']),
        ('rho','rho_b_kg_m3',[980,1000,1050],['debit_suspension_m3_j','trh_j','marge_volume_m3']),
        ('cp','cp_b_J_kgK',[3600,3950,4180],['alimentation_kWh_j','demarrage_sensible_kWh']),
        ('isolation','isolant_m',[0.05,0.08,0.10],['K_enveloppe_W_K','pertes_enveloppe_W']),
    ]:
        lignes = []
        for v in valeurs:
            r = calculer(replace(p, **{champ:v}))
            lignes.append({champ:v, **{k:r[k] for k in sorties}})
        ecrire_csv(args.out/f'sensibilite_{nom}.csv',lignes)
    # Seuil mathématique pour les délais moyens : ne valide pas hb réel.
    bas, haut = 10., 100.
    for _ in range(60):
        milieu = (bas+haut)/2
        r = calculer(replace(p,hb_W_m2K=milieu))
        if r['demarrage_h'] <= 36 and r['recuperation_h'] <= 2:
            haut = milieu
        else:
            bas = milieu
    ecrire_csv(args.out/'seuil_delais.csv',[{'hb_seuil_W_m2K':haut,
        'puissance_consigne_W':calculer(replace(p,hb_W_m2K=haut))['puissance_consigne_W']}])
    lignes = []
    for hb in [10,20,30,50,100]:
        r = calculer(replace(p,hb_W_m2K=hb))
        for i in range(241):
            t_h = i/4
            t = t_h*3600
            T = r['equilibre_C']+(p.initiale_C-r['equilibre_C'])*exp(-(r['G_W_K']+r['K_enveloppe_W_K'])*t/r['capacite_J_K'])
            lignes.append({'hb_W_m2K':hb,'temps_h':t_h,'temperature_non_regulee_C':T})
    ecrire_csv(args.out/'chauffe_analytique_non_regulee.csv',lignes)
    print(f'Sensibilités exportées ; seuil des deux délais : hb = {haut:.4f} W/(m² K).')


if __name__ == '__main__':
    main()
