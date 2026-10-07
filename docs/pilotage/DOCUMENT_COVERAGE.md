# Matrice de couverture documentaire

Généré le 2026-10-07 par `tools/build_register.py`. Détail page par page : `corpus/coverage_pages.csv`.
Chaîne : document → pages → extraction → contrôle qualité → compétences → ressources/évaluations → statut.
Un décompte de pages ne prouve pas une extraction parfaite : les pages « revue humaine » et un échantillon des autres doivent être vérifiés.

| ID | Pages attendues | Pages traitées (au moment de la génération) | Texte natif | OCR | Conf. OCR moy. | Pages à revoir | Contrôle qualité | Exploitation pédagogique |
|---|---|---|---|---|---|---|---|---|
| D01 | 6 | 6 | 6 | 0 | — | 0 | non échantillonné | non analysé |
| D02 | 4 | 4 | 4 | 0 | — | 0 | non échantillonné | non analysé |
| D03 | 3 | 3 | 0 | 3 | 93 | 0 | non échantillonné | non analysé |
| D04 | 2 | 2 | 0 | 2 | 94 | 0 | non échantillonné | non analysé |
| D05 | 2 | 2 | 0 | 2 | 93 | 0 | non échantillonné | non analysé |
| D06 | 1 | 1 | 1 | 0 | — | 0 | non échantillonné | non analysé |
| D07 | 3 | 3 | 3 | 0 | — | 0 | non échantillonné | non analysé |
| D08 | 2 | 2 | 0 | 2 | 94 | 0 | non échantillonné | non analysé |
| D09 | 3 | 3 | 0 | 3 | 94 | 0 | non échantillonné | non analysé |
| D10 | 3 | 3 | 0 | 3 | 93 | 1 | non échantillonné | non analysé |
| D11 | 90 | 90 | 85 | 5 | 86 | 1 | non échantillonné | non analysé |
| D12 | 82 | 82 | 75 | 7 | 88 | 4 | non échantillonné | non analysé |
| D13 | 77 | 77 | 0 | 77 | 91 | 3 | non échantillonné | non analysé |
| D14 | 77 | 77 | 0 | 77 | 90 | 2 | non échantillonné | non analysé |
| D15 | 53 | 53 | 0 | 53 | 88 | 3 | non échantillonné | non analysé |
| D16 | 53 | 53 | 0 | 53 | 85 | 3 | non échantillonné | non analysé |
| D17 | 14 | 14 | 14 | 0 | — | 0 | non échantillonné | non analysé |
| D18 | 27 | 27 | 22 | 5 | 87 | 4 | non échantillonné | non analysé |
| D19 | 11 | 11 | 10 | 1 | 90 | 1 | non échantillonné | non analysé |
| D20 | doc entier | 1 | 1 | 0 | — | 0 | non échantillonné | non analysé |
| D21 | doc entier | 1 | 1 | 0 | — | 0 | non échantillonné | non analysé |
| D22 | 17 | 17 | 14 | 3 | 93 | 2 | non échantillonné | non analysé |

## Erreurs, contradictions et écarts relevés (T-006, à faire valider par un enseignant)

| Réf. | Source | Constat | Statut |
|---|---|---|---|
| E-01 | D11 guide Almoufid, ch.3 séquence 1, tâche 1 (PDF p.42) | Lave visqueuse du Saint Helens annoncée à « à peu près 350 °C ». D12 p036 attribue ces 350 °C à la nuée ardente, pas à la lave : confusion probable lave / nuée ardente. Le même « 350 °C » est donné pour les eaux hydrothermales en PDF p.44 (cohérent). | à valider |
| E-02 | D11, ch.3 (PDF p.42-44) | « volcans explosives et intrusives », « basalte andésitique » : terminologie incohérente (intrusif ≠ effusif ; andésite ≠ basalte). | à valider |
| E-03 | D18 Naciri, ch.4 « Formation des chaînes de montagnes » (PDF p.25-26) | Deux sections titrées « Formation de chaîne de subduction » ; la seconde traite de l'Himalaya, chaîne de **collision** (le texte le dit ensuite). Titre erroné. | à valider |
| E-04 | D18 | Nombreuses fautes de frappe (« blog » pour bloc, « océane ») : non canonique pour citations élèves. | constaté |
| E-05 | Découpage | Volcanisme et roches magmatiques : chapitres séparés (D11, D13, D17) ou fusionnés (D12). Le graphe de compétences doit être indépendant du découpage éditeur. | constaté |
| E-06 | D20/D21 | Référentiels lycée, hors niveau 2AC. | constaté |
