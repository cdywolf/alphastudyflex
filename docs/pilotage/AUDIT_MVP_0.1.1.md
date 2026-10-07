# Audit du MVP existant (dépôt cdywolf/alphastudyflex, v0.1.1, commit cc7fd8d)

Audit en lecture seule du 2026-10-07. Rien n'a été modifié dans le dépôt.

## Constaté (vérifié)
- 2 commits (« Codex », 2026-10-01/02), tag v0.1.0. ~450 lignes Python/JS (app/ 420, web/app.js 34), très compactes.
- FastAPI servant API + frontend statique ; SQLite en local, PostgreSQL (Neon) si `DATABASE_URL` ; `render.yaml` plan free ; CI GitHub Actions.
- Contenus en JSON : `content/questions.json` (19 questions), `curriculum.json`, `pedagogy.json`, `sources.json` (17 sources).
- Parcours Tectonique des plaques : diagnostic 6 questions, 3 séances, 7 exercices, évaluation finale 6 questions ; indices progressifs suivis ; correction humaine d'une réponse ouverte ; plan tenant compte des prérequis.
- Validation enseignant des questions avant ouverture ; journal de revue ; snapshot du corrigé par tentative.
- Sécurité : sessions par jeton haché, cookie HttpOnly SameSite Strict, mots de passe hachés, requêtes paramétrées, code d'installation.
- Tests : `python -m pytest -q` → **13 passed** (Python 3.13, 2026-10-07).
- Aucune IA générative, aucun média audio/vidéo.

## Écarts avec les exigences (docs/REQUIREMENTS.md)
| Exigence | État dans le MVP |
|---|---|
| REQ-019/020 multi-écoles, classes, rôles direction/admin | absent : une seule cohorte, rôles student/teacher |
| REQ-001 multimodal (image, audio, vidéo) | absent (schémas préparés seulement) |
| REQ-017/018 tutorat IA sourcé, budget | absent |
| REQ-026 sauvegarde/restauration | absent |
| Migrations | schéma v1 créé par `CREATE TABLE IF NOT EXISTS` ; pas d'outil de migration |
| Corpus | extraction propre au dépôt (17 sources, OCR français seulement) ; notre extraction J0 couvre 22 fichiers avec OCR fra+ara |
| Volcanisme | « en préparation » |

## Points à vérifier avant de bâtir dessus
- Lecture complète de `app/main.py` (239 lignes denses) : autorisations route par route.
- Concordance des 17 sources du dépôt avec nos D01-D22.
- Seuils pédagogiques codés dans `app/engine.py` (règles de prototype, à documenter).
