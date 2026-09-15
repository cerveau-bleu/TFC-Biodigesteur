# Dimensionnement du biodigesteur — chapitre 2

Scripts reconstruits et vérifiés le 14 septembre 2026 à partir du chapitre 2
de `TFC_Jason_MUKOMBELA.pdf` fourni par Jason Mukombela (pages imprimées 16–26).
Ils reproduisent le modèle analytique du mémoire. Ils ne sont pas présentés
comme les scripts historiques ayant produit le document initial.

## Exécution sous Windows, macOS ou Linux

Python 3.10 ou plus récent. Aucune bibliothèque externe à installer.
Décompresser le dossier, ouvrir un terminal dans ce dossier puis :

```sh
python dimensionnement.py
python sensibilite.py
python audit_chapitre2.py
python -m unittest -v
```

Si Windows utilise le lanceur `py`, remplacer `python` par `py`.
Dans VS Code, ouvrir le dossier puis Terminal > Nouveau terminal.

Les sorties sont dans `resultats/` : CSV ouvrables dans Excel, JSON avec unités
dans les noms, tableaux de sensibilité, trajectoires thermiques analytiques.
Les CSV utilisent un point décimal et une virgule séparatrice : utiliser
l'import de données d'Excel si l'ouverture directe ne sépare pas les colonnes.

## Modifier un scénario

```sh
python dimensionnement.py --config exemple_config.json --out resultats_hb30
```

Les noms de paramètres acceptés figurent dans `Parametres` et dans
`resultats/parametres_utilises.json`. Les champs absents reprennent le cas nominal.
Le script de sensibilité et l'audit utilisent délibérément le cas du chapitre 2,
indépendamment du scénario personnalisé. Les unités sont SI, sauf les champs
explicitement en L/min, kg/j, jours, heures, kWh ou degrés Celsius.

## Fichiers

- `dimensionnement.py` : géométrie, TRH, COV illustrative, isolation, besoins
  thermiques, échangeur, hydraulique, démarrage et récupération.
- `sensibilite.py` : variations de hb, rho, cp, isolation ; seuil des délais.
- `audit_chapitre2.py` : comparaison aux valeurs imprimées, tolérance d'arrondi.
- `test_dimensionnement.py` : conservation du volume et de l'énergie,
  intégration RK4 indépendante, cas limites et rejet de paramètres invalides.
- `EVALUATION.md` : conclusions techniques et améliorations proposées.

Les fichiers générés peuvent être écrasés lors d'une nouvelle exécution : utiliser
`--out` pour conserver des variantes du calcul principal ou des sensibilités.

## Hypothèses essentielles

10 kg/j de déchets + 10 kg/j d'eau ; consigne 35 °C, eau chaude 45 °C,
ambiance 20 °C, référence aqueuse ; pas d'agitateur. hb=50 W/(m² K) est une
hypothèse. Nu=3,66 est une référence de tube droit à paroi isotherme, pas une
corrélation de convection validée pour le serpentin et le digestat.

Les champs MS=20 % et MV/MS=90 % sont des exemples du chapitre. Aucune donnée
du fichier de caractérisation transmis par Ley Luyi n'a été importée ici.
Ces valeurs ne doivent pas être renommées « mesures ».

Le modèle suppose un apport permanent d'eau à 45 °C et une température moyenne
unique. Les trajectoires exportées sont **non régulées** : elles dépassent 35 °C
mathématiquement, sans représenter un fonctionnement réel souhaitable.
Les calculs à 20,35 h ne sont pas des sorties Fluent. La puissance constante
de 296,2935 W du cas Fluent est distincte de la loi variable de l'échangeur.

Les débits invalidant les hypothèses laminaires ou le domaine de White sont
refusés. Le script n'est pas un dimensionneur universel pour tous les fluides.
Un délai infini est exporté en `null` dans le JSON si la consigne est inaccessible.

## Références des relations

La traçabilité principale est la numérotation 2.1–2.45 du PDF fourni.
Sources techniques vérifiées le 14 septembre 2026 :

- White, Darcy et domaine : https://fluids.readthedocs.io/fluids.friction.html#fluids.friction.helical_laminar_fd_White
- Nu constant, tube droit laminaire : https://ht.readthedocs.io/en/latest/ht.conv_internal.html

Aucun des paquets `fluids` ou `ht` n'est requis pour exécuter les scripts.
Leur documentation sert à vérifier les relations explicitement implémentées.

Pour une publication GitHub, conserver ce README et l'évaluation avec le code.
Le PDF source, les fichiers ANSYS et les données de tiers ne sont pas inclus.
