# Architecture de la première itération

Un processus FastAPI sert les fichiers de l’interface et l’API sur la même origine. Les sessions sont des jetons aléatoires stockés sous forme d’empreinte en base. Le navigateur reçoit uniquement un cookie HttpOnly, SameSite Strict, sécurisé en hébergement.

La base est SQLite pour l’exécution locale et PostgreSQL via psycopg lorsque DATABASE_URL est défini. Les requêtes sont paramétrées. Les changements de publication sont journalisés, les tentatives portent un snapshot du corrigé et les soumissions sont sérialisées pour éviter les doubles réponses. Le code de démarrage bloque SQLite en hébergement Render.

## Responsabilités

- `content/` : version du curriculum, des questions, des sources et des règles. Modifier un contenu exige une nouvelle validation.
- `app/engine.py` : statuts descriptifs, preuves, prise en compte des indices et ordre du plan avec prérequis.
- `app/main.py` : routes, droits, validation des entrées et orchestration.
- `app/db.py` : schéma version 1 et accès aux deux moteurs.
- `tools/ingest.py` : traitement local des originaux avec reprise, empreinte et statut.
- `tools/sync_corpus.py` : import des résultats dans la base distante.

## Frontières pédagogiques

Les documents bruts ne sont jamais des instructions exécutables. Aucun texte extrait n’est directement fourni à l’élève par un moteur génératif dans la v0.1. Les textes et questions du pilote sont préparés, puis doivent être validés. Le schéma de sources contient le niveau et l’autorisation d’usage potentiel côté élève ; cela ne vaut pas validation.

Le domaine « méthode » ne peut atteindre le statut consolidé par les seuls QCM : une réponse ouverte autonome corrigée positivement est nécessaire. Les autres seuils sont des règles de prototype, explicitement visibles dans le code. Ils ne constituent pas une estimation psychométrique validée.

Le plan peut faire remonter un prérequis insuffisant avant une compétence dépendante. La comparaison diagnostic/final reste descriptive : six questions ne permettent pas d’attribuer un gain d’apprentissage causal à la plateforme.

## Évolutions à prévoir

Avant un pilote réel élargi : gestion des établissements et classes, récupération de compte, politique de conservation, sauvegardes vérifiées, surveillance, limitations d’usage distribuées et revue sécurité. L’authentification actuelle utilise une seule cohorte et une limitation en mémoire adaptée à un seul processus ; la prévention distribuée des abus reste à ajouter.

Pour le tutorat : interface de fournisseur de modèle, corpus de contenus validés, index multimodal avec filtres niveau/chapitre, citations vérifiables, coût et latence suivis, tests d’injection et de fidélité. Les réponses rédigées resteront revues par un enseignant tant que l’évaluation automatique n’aura pas été validée sur un jeu annoté.
