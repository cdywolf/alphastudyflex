# État du projet

Dernière mise à jour : 2026-10-07 (session 1).

## Objectif et périmètre actuels
Jalon **J0 Cadrage & corpus** pour SVT 2AC (hypothèse H-1). Tranche verticale choisie : Volcanisme (DEC-003, proposée).

## Fait (avec preuves)
- Inventaire de 22 fichiers : empreinte, pages, producteur → `tools/inventory_raw.tsv`, `docs/DOCUMENT_REGISTER.md`.
- Extraction page à page (natif + OCR fra+ara) → `corpus/pages/Dxx/pNNN.{txt,json}` ; statut → `docs/DOCUMENT_COVERAGE.md`,
  `corpus/coverage_pages.csv`. Commande : `python3 tools/build_register.py` (régénère registre et couverture).
- Documents de mémoire créés (voir `CLAUDE.md`).
- Relevé de 6 écarts/erreurs probables (E-01 à E-06).
- Carte d'alignement des sources Volcanisme (partielle) → `pedagogy/volcanisme/sources.md`.

## Fait le 2026-10-07 (suite)
- Graphe de compétences Volcanisme v0.1 (4 prérequis, 8 connaissances, 7 compétences, 7 erreurs fréquentes) → `pedagogy/volcanisme/competences.yaml`.
- 13 items de diagnostic + règles auditables → `pedagogy/volcanisme/diagnostic_items.yaml`. Non validés ; 4 médias à produire.

## En cours
- T-003 couverture : la revue humaine/échantillonnage OCR n'est pas faite.
- T-005 carte Volcanisme : bornes de pages D13/D15 à confirmer.

## Rien de tout cela n'existe encore
Aucun code produit, aucun test produit, aucune validation enseignant, aucun déploiement, aucune opération externe.

## Divergence découverte le 2026-10-07 11:05 UTC
Le dépôt `cdywolf/alphastudyflex` n'est pas vide : il contient un MVP v0.1.1 (commits « Codex » des 1er-2 octobre 2026) :
FastAPI + SQLite/PostgreSQL (Neon), parcours Tectonique des plaques (19 questions, 3 séances), comptes, validation enseignant,
13 tests pytest **passants** (exécutés le 2026-10-07 : `python -m pytest -q` → 13 passed), render.yaml, CI GitHub Actions.
Candy avait indiqué « pas de code POC » : décision demandée (bâtir dessus ou repartir de zéro).
Push depuis la session refusé : l'app GitHub Claude n'est pas installée sur le dépôt.

## Bloquants
- GitHub non connecté au projet : Candy doit connecter son compte et créer le dépôt vide `cdywolf/alphastudyflex` (T-011).
- Plafond fixé : 25 $/mois (DEC-014). La clé API sera demandée à Candy au moment des premiers appels réels.
Réponses reçues le 2026-10-07 : voir DEC-007 à DEC-013.

## Prochaines actions ordonnées
1. Intégrer les réponses de Candy dans `DECISIONS.md`.
2. T-005 : finaliser les bornes de pages ; lire intégralement les pages Volcanisme et prérequis.
3. Revue enseignant du graphe et des items (Candy transmet à l'enseignant référent).
4. J2 : squelette FastAPI + Supabase (local d'abord) dès que le dépôt existe.
5. T-010 : vérifier la documentation officielle de l'API Claude (modalités, tarifs, données).
6. Si Q5 accordée : créer le dépôt, migrer, CI.

## Opérations externes effectuées
Aucune. (Installation locale de tesseract dans le conteneur éphémère uniquement.)
