# Évaluation du dimensionnement du chapitre 2

Document examiné : TFC_Jason_MUKOMBELA.pdf, chapitre 2, pages imprimées 16–26.
Évaluation du 14 septembre 2026. Les nombres ci-dessous sont des recalculs,
pas des mesures. Le verdict porte sur un avant-projet thermique et hydraulique.

## Verdict

Le calcul est arithmétiquement cohérent sous ses hypothèses. Il mérite d'être
conservé comme prédimensionnement conditionnel. Il ne suffit pas à valider
la fabrication, le chauffage homogène ni l'amélioration de production de gaz.
La faiblesse dominante est l'incertitude sur le transfert côté suspension,
plutôt qu'une erreur de calcul de puissance ou de volume.

| Grandeur | Recalcul | Valeur du chapitre |
|---|---:|---:|
| Volume net de suspension | 513,3850 L | 513,385 L |
| TRH nominal | 25,6693 j | 25,67 j |
| Longueur de l'hélice | 30,16990 m | 30,1699 m |
| Surface active | 1,516504 m² | 1,51650 m² |
| Conductance des pertes | 3,002497 W/K | 3,00250 W/K |
| Pertes à 35 °C | 45,03746 W | 45,04 W |
| Besoin moyen cuve + alimentation | 59,55135 W | 59,55 W |
| Reynolds eau | 1381,594 | 1382 |
| U extérieur | 34,28132 W/(m² K) | 34,281 |
| Puissance transférée à 35 °C | 296,30053 W | 296,30 W |
| Sortie d'eau à la consigne | 37,85431 °C | 37,85 °C |
| Perte de pression avant réserve | 3490,513 Pa | 3490,5 Pa |
| Hauteur après réserve | 0,44835 m | 0,448 m |
| Démarrage 20–35 °C | 20,34778 h | 20,35 h |
| Récupération après alimentation | 1,37672 h | 1,38 h |
| Consommation prévisionnelle continue | 2,14923 kWh/j | 2,15 kWh/j |

L'audit CSV détaille les écarts et les tolérances d'arrondi. Les tableaux de
sensibilité du chapitre sont recalculés séparément.

## Points solides

Le volume extérieur déplacé par le tube est bien retiré de la suspension.
Les raccords immergés déplacent du liquide mais ne sont pas crédités dans
la surface active : choix prudent et explicite. À 980 kg/m³, la faible marge
volumique est correctement signalée. Le niveau estimé après soutirage reste
au-dessus du sommet de l'hélice.

La sortie d'eau est calculée via le bilan de l'échangeur, au lieu d'être
imposée indépendamment de la puissance. Le facteur de frottement est un
facteur de Darcy. Le modèle de White est utilisé dans son domaine nominal.
Les budgets d'accessoires, du générateur et des ponts thermiques sont
clairement distingués de mesures. La nécessité de régulation est reconnue.

## Corrections et précisions utiles dans le mémoire

1. **Énergie du démarrage.** Les 9,21229 kWh sont l'énergie sensible seule.
   En intégrant les pertes du même modèle pendant 20,34778 h, on obtient
   0,53921 kWh de pertes d'enveloppe et **9,75150 kWh reçus**. Avec les
   provisions continues 25 W + 5 W, le total électrique idéalisé serait
   environ 10,362 kWh, avant préchauffe séparée et sous les hypothèses de
   conversion déclarées. Il ne faut pas qualifier 9,212 kWh de consommation
   électrique totale de démarrage.

2. **Récupération.** La formule du chapitre refroidit fictivement les
   auxiliaires avec la suspension, puis utilise Ceff : elle donne 1,37672 h.
   Si l'énergie retirée est exactement celle du remplacement de 20 kg et
   les auxiliaires restent chauds avant redistribution, la moyenne énergétique
   initiale est 35 − Ealim/Ceff ; le même modèle donne **1,33765 h**.
   L'écart est faible (environ 2,34 min) et la convention prudente du chapitre
   est annoncée. Aucun de ces délais ne prouve une homogénéité locale.

3. **Seuil de transfert.** Les critères moyens (<36 h et <2 h) sont tous deux
   satisfaits au-delà d'environ **hb=24,9544 W/(m² K)** dans ce modèle.
   La puissance correspondante à 35 °C est environ **217,35 W**. La valeur
   hb=30 et la puissance 239,27 W du chapitre constituent donc une cible avec
   marge, pas le minimum mathématique exact. Conserver cette cible prudente.

4. **Surévaluation par l'eau.** Le « environ 6 % » compare les cp à masse
   fixée : 4180/3942 − 1 = 6,04 %. À volume identique, le changement de rho
   doit aussi être inclus. Le scénario de mélange donne rho≈1023,687 kg/m³
   et une surévaluation de rho*cp d'environ 3,58 %. Préciser la base de la
   comparaison plutôt que généraliser les 6 % à toute la capacité de cuve.

5. **Unité de hauteur.** La formule H=Δp/(rho_eau*g) donne une hauteur du
   fluide circulant (rho=992). Pour une mCE conventionnelle basée sur
   1000 kg/m³, la conversion est environ 0,4448 m. Le choix de 0,50 m garde
   une marge dans les deux cas. Vérifier la courbe débit–hauteur du produit.

6. **Organisation du chapitre.** La section 2.1 annonce déjà le dimensionnement
   mais contient surtout l'introduction. La renommer « Objet et démarche du
   dimensionnement » éviterait le doublon avec la section 2.3.

## Limites physiques à conserver clairement

- hb=50 et les résistances d'encrassement ne sont pas mesurés. À hb=10,
  les délais deviennent 57,94 h et 4,65 h : les objectifs ne sont plus tenus.
- Nu=3,66 représente le tube droit laminaire établi à paroi isotherme.
  Ce choix ne démontre pas une borne rigoureuse pour l'ensemble réel.
- Le coefficient de perte simplifie le gaz, les coins, le support et les
  échanges superficiels. Le budget de ponts thermiques doit être vérifié.
- Les 65 kJ/K auxiliaires et la moyenne unique n'établissent pas les
  températures individuelles du cuivre, de l'eau et de la cuve non agitée.
- Le générateur de 1,2 kW est compatible avec le plafond calculé du serpentin
  et 25 W de pertes ; cela ne vérifie pas sa régulation, la préchauffe ni
  les performances d'un produit réel.
- MS et MV/MS du chapitre sont illustratifs. La caractérisation Excel de
  Ley Luyi n'est pas contenue dans les entrées de ces scripts. Il faudra
  vérifier sa provenance et ses unités avant de remplacer ces hypothèses.
- L'épaisseur 2 mm, le fond plat, les appuis et la pression du gaz nécessitent
  une étude mécanique distincte. Le cuivre nécessite une vérification de
  compatibilité et de durabilité dans le milieu réel.
- La CFD exploite une puissance constante et un domaine simplifié. Elle
  n'a pas validé les 20,35 h, la récupération ou la production biologique.

## Vérification logicielle

Les tests vérifient les bilans volume/énergie, les valeurs nominales arrondies,
des tendances physiques, une intégration RK4 indépendante de l'équation
différentielle et le rejet d'entrées hors domaine. Ces tests vérifient le
logiciel et la reproduction du modèle ; ils ne valident pas ses hypothèses.

Sources de relations vérifiées :
https://fluids.readthedocs.io/fluids.friction.html#fluids.friction.helical_laminar_fd_White
et https://ht.readthedocs.io/en/latest/ht.conv_internal.html.
