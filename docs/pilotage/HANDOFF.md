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
