# TFC — Chauffage d'un biodigesteur

Auteur : Jason Mukombela
Université de Kinshasa — Faculté polytechnique
L3 Génie mécanique

## Objet

Étude et dimensionnement d'un système d'apport thermique
pour un biodigesteur en vue d'améliorer la cinétique
de digestion et la production de biogaz.

## Contenu

- calculs/ : scripts Python, paramètres, tests et résultats.
- ansys/ : fichiers du cas Fluent final.
- figures/ : illustrations et résultats numériques.
- documentation/ : mémoire et documents associés.

## Exécuter le dimensionnement

Python 3.10 ou supérieur, sans bibliothèque externe.

Depuis la racine du dépôt :

    cd calculs/dimensionnement_ch2
    python dimensionnement.py
    python sensibilite.py
    python audit_chapitre2.py
    python -m unittest -v

Les scripts ont été reconstruits et vérifiés à partir
du chapitre 2 du mémoire.

## Simulation Fluent

Le calcul présenté porte sur le démarrage thermique
jusqu'à 100 secondes physiques.

Le dossier ansys contient le fichier de cas et le fichier
de données correspondants. Leur récupération nécessite Git LFS.

## Portée des résultats

Le dimensionnement analytique et les résultats Fluent
sont distingués.

La simulation ne démontre pas la montée complète à 35 °C
ni un gain biologique propre au dispositif.