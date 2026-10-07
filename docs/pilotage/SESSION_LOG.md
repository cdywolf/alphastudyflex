# Journal des sessions

## 2026-10-07 — session 1 (fil « Ma plateforme éducative version SVT »)
- Lecture du brief de Candy. Lecture/inventaire des 22 fichiers de `svt/`.
- Constat : corpus 2AC parcours international option français ; référentiels IPSE = lycée ; 7 fichiers scannés.
- Installation de tesseract (fra, ara) dans le conteneur ; extraction page à page de 22 documents.
- Création de CLAUDE.md et docs/* ; backlog J0-J8 ; 8 questions à Candy.
- Choix proposé de la tranche Volcanisme (DEC-003).
- Réponses de Candy (DEC-007 à DEC-014) ; hébergement gratuit analysé ; graphe Volcanisme v0.1 et 13 items de diagnostic.
- Dépôt connecté : MVP 0.1.1 existant découvert ; Candy choisit de continuer dessus (DEC-015).
- Pilotage poussé dans `docs/pilotage/` (commit d0be0e1). Version 0.2.0 : chapitre Volcanisme (20 questions brouillon, 3 séances, schéma original), serveur multi-chapitres, migration de schéma 2.
- Tests : 19 passés sous SQLite et sous PostgreSQL local ; `check_content.py` OK ; essai navigateur du diagnostic Volcanisme (téléphone 390 px) sans erreur JS.
- Correctifs trouvés à l'essai : numéros du schéma invisibles (CSS), motif d'identifiant refusé par Chrome récent.
