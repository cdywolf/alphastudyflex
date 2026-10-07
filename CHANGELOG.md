# 0.2.0 — Chapitre Volcanisme (2026-10-07)

- Deuxième chapitre pilote : le volcanisme, avec 3 compétences, 3 séances et 20 questions (6 de diagnostic, 8 d’entraînement dont une réponse rédigée, 6 de bilan). Toutes sont en brouillon : la validation enseignant reste à faire.
- Nouvelle source déclarée : corrigé d’exercices sur les volcans (18 sources).
- Serveur multi-chapitres : diagnostic, séances, bilan, tableau de bord et préparation calculés par chapitre ; les tentatives portent leur chapitre (migration de schéma 2, les tentatives existantes restent en tectonique).
- Prérequis entre chapitres signalés à l’élève, jamais imposés.
- Schéma original d’une coupe de volcan, numéroté ; sa description accessible ne donne pas les réponses.
- Les identifiants de questions, séances et règles de la tectonique sont inchangés : les validations déjà publiées restent valides.
- Correctif : le motif de l’identifiant de connexion était refusé par les navigateurs récents.

# 0.1.1 — Encodage Windows

- Lecture et écriture UTF-8 explicites pour les contenus pédagogiques et le corpus.
- Les données, comptes et résultats existants sont conservés. Les anciennes tentatives gardent leur snapshot ; leurs éventuels caractères déjà altérés ne sont pas modifiés automatiquement.

# Historique

## 0.1.0 — 2026-10-01

Première itération depuis zéro :

- Inventaire des 17 documents, extraction des 503 pages PDF et 921 blocs Word.
- Conservation des tableaux Word et rôle explicite de chaque source.
- Huit règles pédagogiques rattachées aux références ; séparation lycée / 2AC.
- Premier parcours de tectonique : 19 questions, 3 séances, diagnostic et bilan.
- Comptes, validation enseignant, indices suivis et correction humaine d’une réponse ouverte.
- SQLite local et PostgreSQL distant ; export du corpus séparé du dépôt.
- Configuration GitHub Actions et déploiement Render Free avec Neon.

Limites : aucune IA générative connectée, corpus pas encore intégralement validé, autres chapitres non ouverts, interface de consultation du corpus textuelle.

## Prochaine itération proposée

- Auditer les pages de tectonique et leurs visuels, corriger les erreurs documentaires et finaliser la matrice acquis / activités / évaluations.
- Relier les illustrations aux questions et aux passages validés.
- Brancher le tutorat RAG sur le corpus validé avec un budget et un fournisseur choisis, puis tester sa fidélité et ses refus hors source.
