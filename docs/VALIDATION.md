# Validation de l’itération 0.1.0

Vérification locale le 1 octobre 2026, Python 3.12.

- 12 tests d’intégration réussis avec SQLite : parcours complet, publication et invalidation, réponses non divulguées pendant l’évaluation, séparation des rôles et des élèves, doubles soumissions, aides, prérequis, sessions, origine des requêtes, inscriptions, consultation du corpus distant, installation initiale et refus de SQLite en hébergement.
- Vérification structurelle : 17 sources, 19 questions et 8 règles ; équilibre des dimensions entre diagnostic et bilan final ; références du contenu élève limitées au niveau 2AC.
- Analyse syntaxique JavaScript réussie.
- 503 pages PDF et 921 blocs Word extraits. La couverture est un indicateur d’extraction, pas une validation scientifique ou pédagogique.

## Limites de ces vérifications

Le workflow GitHub Actions est configuré pour rejouer les tests avec PostgreSQL 17. Cette exécution n’a pas été effectuée dans cet environnement : la création du processus PostgreSQL local est indisponible. La première CI doit donc réussir avant un pilote distant.

La vérification visuelle dans un navigateur n’a pas pu être réalisée : le navigateur téléchargé ne peut pas démarrer en raison des restrictions système sur ses sockets. La syntaxe du JavaScript et les routes serveur ont été vérifiées ; un contrôle de l’interface sur ordinateur et mobile reste à faire.

Aucun déploiement sur Render/Neon et aucun push GitHub n’ont été effectués. Les configurations et procédures sont livrées. Les sources originales n’ont pas été publiées.

Les validations enseignantes utilisées dans les tests sont fictives, isolées et absentes de la livraison. Le pilote demande une validation pédagogique humaine de ses questions avant de les rendre accessibles aux élèves. Aucun gain d’apprentissage n’est revendiqué.

Un avertissement de dépréciation de Starlette concerne son client de test HTTPX ; il ne fait pas échouer les tests.
