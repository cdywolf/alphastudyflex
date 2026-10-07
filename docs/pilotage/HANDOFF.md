# Reprise

## Texte à coller dans une nouvelle session
Reprends la construction d'AlphaStudyFlex à partir des fichiers de `/mnt/project-files/alphastudyflex/`
(ou du dépôt s'il existe). Lis d'abord CLAUDE.md, docs/PROJECT_STATE.md et docs/HANDOFF.md. Vérifie leur cohérence
avec les fichiers et les derniers résultats. Résume brièvement l'état, les divergences et la prochaine tâche, puis
poursuis sans recommencer les étapes validées. Les consignes, décisions et critères d'acceptation déjà documentés
restent applicables. Ne répète aucune opération externe sans avoir vérifié son état.

## Pièges connus
- Le conteneur est éphémère : réinstaller tesseract (commande dans CLAUDE.md) avant toute nouvelle OCR.
- Le dossier partagé perd le bit exécutable : `bash tools/extract_pages.sh …`.
- 4 OCR parallèles sans `OMP_THREAD_LIMIT=1` = >1 min/page.
- Les titres décoratifs des manuels scannés (D13-D16) sont mal reconnus par l'OCR : ne pas s'y fier pour les bornes de chapitre, regarder l'image.
- Les numéros de page cités sont des pages PDF, sauf mention contraire.
- Code : dépôt `cdywolf/alphastudyflex` cloné dans `/home/claude/alphastudyflex` (à recloner si le conteneur est neuf). Installer `pip install -r requirements.lock`.
- Tests PostgreSQL locaux : `sudo service postgresql start` puis `TEST_DATABASE_URL=postgresql://asf:asf-test-only@localhost:5432/asf_test python -m pytest -q` (rôle et base de test à recréer si le conteneur est neuf).
- Ne jamais modifier un contenu de tectonique sans le vouloir : l'empreinte de révision change et la validation enseignant publiée devient caduque.
- Essai navigateur : Playwright Python avec `executable_path='/opt/pw-browsers/chromium'` ; ne pas lancer `playwright install`. Ne pas utiliser `pkill -f` avec un motif présent dans sa propre commande (tue le shell).
- Le CSS `.figure text` impose la couleur du texte SVG : utiliser une classe (ex. `.num`) pour un texte de couleur différente.
