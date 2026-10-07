# AlphaStudyFlex — instructions de travail pour Claude

Plateforme éducative SaaS B2B pour établissements scolaires (premier marché : Maroc).
Périmètre actif : **SVT uniquement**. Physique-chimie et mathématiques = extensions futures, sans travaux actifs.
Porteur : Candy Aho (data science / BI, Python, LLM, RAG, backend). Langue de travail : français.

## À lire en reprise (dans cet ordre)
1. `docs/pilotage/PROJECT_STATE.md` — état réel, jalon en cours, prochaines actions.
2. `docs/pilotage/HANDOFF.md` — texte de reprise et pièges connus.
3. Puis seulement la spécification utile à la tâche (voir index ci-dessous).

## Sources de vérité
| Sujet | Fichier |
|---|---|
| Vision, hypothèses du pilote | `docs/pilotage/PROJECT_BRIEF.md` |
| Exigences numérotées (REQ-xxx) et traçabilité | `docs/pilotage/REQUIREMENTS.md` |
| Décisions et raisons (DEC-xxx) | `docs/pilotage/DECISIONS.md` |
| Inventaire des fichiers sources (Dxx) | `docs/pilotage/DOCUMENT_REGISTER.md` |
| Statut page par page | `docs/pilotage/DOCUMENT_COVERAGE.md` + `corpus/pages/<Dxx>/pNNN.{txt,json}` |
| Pédagogie, compétences, évaluation | `docs/pilotage/PEDAGOGY_AND_ASSESSMENT.md` |
| Architecture | `docs/pilotage/ARCHITECTURE.md` |
| Agents produit (pas l'équipe de construction) | `docs/pilotage/AGENT_ROLES_AND_CONTRACTS.md` |
| Sécurité, données de mineurs | `docs/pilotage/SECURITY_AND_PRIVACY.md` |
| Tests et évaluation IA | `docs/pilotage/TEST_AND_EVALUATION_PLAN.md` |
| Pilote et commercial | `docs/pilotage/COMMERCIAL_AND_PILOT_PLAN.md` |
| Risques | `docs/pilotage/RISK_REGISTER.md` |
| Jalons et tâches (T-xxx) | `docs/pilotage/BACKLOG.md` |
| Journal des sessions | `docs/pilotage/SESSION_LOG.md` |

Documents sources originaux : `/mnt/project-files/svt/` (lecture seule, ne jamais modifier).
Code : ce dépôt. Pilotage : `docs/pilotage/`. Corpus extrait (hors dépôt, droits) : `/mnt/project-files/alphastudyflex/corpus/` dans le projet Claude.

## Règles de travail
- Ne jamais inventer : document lu, test réussi, validation enseignant, intégration, conformité, déploiement.
- Statuts obligatoires : proposé → implémenté → testé → validé enseignant → déployé.
- Toute affirmation pédagogique est sourcée (Dxx, page). Contenu incertain = jamais canonique.
- Aucune dépense externe, création de dépôt, push ou déploiement sans accord explicite de Candy.
- Aucun secret ni donnée élève réelle dans ces fichiers.
- Mettre à jour `PROJECT_STATE.md`, `HANDOFF.md` et `SESSION_LOG.md` après chaque jalon et avant toute opération longue.
- Fichier partagé : relire juste avant de modifier, modifications courtes.

## Environnement (constaté le 2026-10-07)
- Conteneur cloud éphémère : les outils installés disparaissent entre sessions. `/mnt/project-files` persiste.
- OCR : `sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-fra tesseract-ocr-ara`
  puis `OMP_THREAD_LIMIT=1` (sinon 4 OCR parallèles se bloquent mutuellement).
- Le dossier partagé ne conserve pas le bit exécutable : lancer les scripts avec `bash script.sh`.
- Extraction : `bash tools/extract_pages.sh <Dxx> <pdf> corpus/pages` (idempotente, reprend où elle s'est arrêtée).

## Code existant (0.2.0)
- `docs/ARCHITECTURE.md` décrit le code actuel ; `docs/pilotage/ARCHITECTURE.md` décrit la cible proposée.
- Tests : `python -m pytest -q` (19 tests au 2026-10-07, SQLite et PostgreSQL). Lancement : voir README.md.
- Audit de reprise : `docs/pilotage/AUDIT_MVP_0.1.1.md`.
