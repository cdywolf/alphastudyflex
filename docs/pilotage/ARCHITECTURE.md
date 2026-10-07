# Architecture — v0 (proposée, non décidée)

Statut : **proposé** le 2026-10-07. Décision attendue au jalon J2, après réponses Q5/Q6.

## Principes
Monolithe modulaire, base relationnelle unique, stockage objet, workers asynchrones. Pas de microservices ni
Kubernetes sans besoin démontré. Logique pédagogique, orchestration IA et infrastructure séparées en modules.
Matière, niveau, langue et école sont des données (pas du code) pour permettre les extensions (REQ-032).

## Options comparées (à confirmer)
| Sujet | Option retenue proposée | Alternatives | Raison |
|---|---|---|---|
| Backend | Python + FastAPI | Django ; Node/NestJS | Compétence de Candy, écosystème IA/RAG, typage Pydantic |
| Base | PostgreSQL + Row Level Security par `school_id` | Base par école ; schéma par école | RLS = seconde barrière en plus des filtres applicatifs ; coût faible au pilote |
| Recherche | PostgreSQL : plein texte + `pgvector` (hybride) dans la même base, même RLS | Base vectorielle dédiée | Corpus pilote petit (quelques milliers de segments) ; une seule frontière d'isolation |
| Fichiers/médias | Stockage objet compatible S3, préfixe par école, URLs signées courtes | Disque local | Médias volumineux, streaming HLS/MP4 |
| Tâches | File dans PostgreSQL (ex. procrastinate) | Redis + Celery | Moins de composants ; idempotence et reprise transactionnelles |
| Frontend | PWA React (TypeScript) mobile d'abord | Application native | Un seul code, hors-ligne partiel, coût |
| IA | Couche fournisseur abstraite ; Claude via API backend | Modèles locaux | À chiffrer (T-010) ; pas de clé disponible à ce jour |
| Audio | STT et TTS via services remplaçables | — | Claude ne fait pas nativement STT/TTS (à vérifier T-010) |
| Vidéo | ffmpeg : transcodage, sous-titres, détection de scènes, images clés choisies par changement de scène + transcript | Envoi intégral à un modèle | Coût, traçabilité temporelle |

## Modules prévus
`tenancy` (écoles, années, classes, inscriptions) · `identity` (auth, rôles, MFA) · `curriculum` (disciplines,
niveaux, compétences, graphe) · `sources` (documents, versions, pages, segments, médias, droits) ·
`content` (ressources, activités, états de publication) · `assessment` (items, tentatives, preuves, profils) ·
`planning` (plans, validations enseignant) · `tutoring` (sessions, indices) · `ai` (fournisseurs, prompts
versionnés, budgets, traces) · `reporting` · `audit`.

## Hébergement du MVP démo (vérifié le 2026-10-07 sur les pages officielles)
| Service | Offre gratuite constatée | Contrainte pour nous |
|---|---|---|
| Render web service | 750 h d'instance/mois ; mise en veille après 15 min sans trafic, ~1 min de réveil ; disque éphémère | Réveiller avant une démo ; aucun fichier local persistant |
| Render Postgres free | 1 Go, **expire 30 jours après création** | Écarté |
| Render static site | gratuit | Frontend PWA |
| Supabase free | 500 Mo Postgres (pgvector disponible), 1 Go stockage, 50 000 MAU, **pause après 1 semaine d'inactivité**, 2 projets | Base + fichiers + médias légers ; relancer avant démo |
| Vercel Hobby | « non-commercial, personal use only » | Écarté pour un projet de startup |
Sources : render.com/docs/free, supabase.com/pricing, vercel.com/docs/plans/hobby.
Isolation : RLS PostgreSQL par école, même sur l'offre gratuite. Données de démo uniquement (aucune donnée élève réelle sur l'offre gratuite).

## Coûts IA (tarifs API Claude au 2026-09-25, par million de tokens entrée/sortie)
Claude Opus 5.5 : 4 $ / 20 $ · Claude Sonnet 5.5 : 2 $ / 10 $ · Claude Haiku 4.5 : 1 $ / 5 $. Cache en lecture moins cher.
Estimation (hypothèse : tour de tutorat ≈ 3 000 tokens d'entrée dont contexte en cache + 400 de sortie) :
≈ 0,02 $/tour avec Opus 5.5, ≈ 0,01 $ avec Sonnet 5.5, ≈ 0,005 $ avec Haiku 4.5. Phase démo (quelques centaines de tours) : quelques dollars.
Pilote 70 élèves × 2 séances/semaine × 15 tours × 4 semaines ≈ 8 400 tours/mois : ≈ 170 $ (Opus 5.5), 85 $ (Sonnet 5.5), 40 $ (Haiku 4.5).
Choix de modèle par tâche : décision de Candy, à mesurer sur le jeu d'évaluation (non décidé).
Audio : synthèse vocale des explications publiées pré-générée hors ligne (moteur open source, coût nul à l'exécution) ;
transcription des réponses orales : option à décider (service payant plafonné, ou navigateur avec avertissement de confidentialité).

## Hors code pour l'instant
Rien n'est implémenté hors outillage d'extraction (`tools/extract_pages.sh`).
