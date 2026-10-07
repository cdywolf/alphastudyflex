# AlphaStudyFlex

Un MVP pédagogique de SVT pour la deuxième année collégiale au Maroc.

**Itération 0.2.0 : deux chapitres pilotes, tectonique des plaques et volcanisme.** Les 20 questions du volcanisme sont des brouillons à faire valider par l’enseignant avant tout usage élève. Le code peut être déployé sur Render Free avec une base PostgreSQL Neon Free ; aucun déploiement de la 0.2.0 n’a été fait. Le tutorat génératif reste à développer.

## Ce qui fonctionne

- Comptes élève et enseignant, sessions conservées côté serveur et mots de passe hachés.
- Premier compte enseignant créé en ligne avec un code d’installation à usage initial unique, ou localement par CLI.
- Inscription élève avec code d’invitation lorsque l’application est hébergée.
- Validation enseignant des questions et de leurs supports avant ouverture de chaque chapitre (19 en tectonique, 20 en volcanisme).
- Chapitres pilotes indépendants : chaque chapitre a son diagnostic, ses séances et son bilan ; un prérequis d’un autre chapitre est signalé à l’élève sans être bloquant.
- Diagnostic de 6 questions, 3 séances et 7 questions d’entraînement, puis évaluation finale de 6 questions distinctes.
- Explications préparées, indices progressifs, enregistrement des aides utilisées et correction humaine d’une réponse rédigée.
- Plan personnel tenant compte des résultats et des prérequis, bilans séparant connaissances, outils et méthode.
- Tableau de suivi des élèves et file de corrections ouvertes.
- Registre des 17 sources et consultation enseignant de leur extraction, localement ou depuis PostgreSQL.
- 8 règles pédagogiques reliées aux documents d’origine ; les références Word comprennent des identifiants de blocs.
- Tests d’intégration, dépendances verrouillées, configuration Render et workflow GitHub Actions.

## Ce qui n’est pas encore livré

Pas de dialogue avec un LLM dans cette version : l’aide pédagogique utilise des textes préparés et ne se présente pas comme une IA connectée. Pas encore de recherche vectorielle, de génération automatique de séances ni de correction automatique des réponses rédigées. Les autres chapitres sont indiqués comme « en préparation ».

Les 503 pages PDF et 921 blocs Word (dont 121 tableaux) du corpus ont été extraits. **Ce traitement n’équivaut pas à une validation scientifique, ni à la transformation de toutes les pages en activités.** L’OCR est en français ; les passages arabes, légendes, chiffres et tableaux scannés restent à vérifier. Voir [le rôle de chaque source](docs/SOURCE_USAGE.md) et [l’audit détaillé](docs/corpus-audit.json).

Les manuels originaux et le cache d’extraction sont séparés du dépôt. Les questions du pilote et les schémas sont des contenus préparés pour cette version ; le graphique utilise des données d’entraînement explicitement signalées. Aucun scan complet n’est intégré au code public.

## Démarrer localement

Python 3.12 recommandé. Depuis la racine du projet :

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.lock
.\.venv\Scripts\python -m app.cli create-user --username candy --role teacher
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Linux ou macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m app.cli create-user --username candy --role teacher
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Ouvrir http://127.0.0.1:8000. Le mot de passe enseignant est saisi interactivement, jamais stocké en clair dans le dépôt.

1. Se connecter comme enseignant.
2. Lire **Cadre pédagogique**, puis les séances, questions et critères dans **Contenus**.
3. Valider les questions d’un chapitre après vérification ; cela ouvre ce chapitre.
4. Créer un compte élève, terminer le diagnostic puis les trois séances et le bilan final.
5. Revenir dans **Mes élèves** pour corriger la réponse rédigée.

La validation de test effectuée pendant le développement n’est pas livrée avec la base. Le projet démarre avec un état de validation vierge.

## Corpus et référentiels

Le fichier `content/sources.json` décrit chaque source, sa fonction, son niveau et son empreinte SHA-256. Les référentiels IPSE Sciences Mathématiques et Sciences expérimentales sont des documents **de lycée** : ils structurent les acquis, les prérequis et les méthodes d’évaluation, mais ne sont pas utilisés comme contenu élève 2AC.

`content/pedagogy.json` traduit ces principes en règles du produit. `content/curriculum.json` définit objectifs, indicateurs et prérequis. `content/questions.json` contient les questions, les barèmes, les indices, les sources et la version. Toute modification d’une question, de sa séance, de ses sources ou du cadre pédagogique invalide sa publication précédente. Les tentatives conservent leur question et leur corrigé sous forme de snapshot.

### Utiliser le cache livré

Extraire `AlphaStudyFlex_corpus_v0.1.0.zip` **à la racine du projet** : il crée `data/processed/`. Ce dossier est ignoré par Git. L’écran Documents devient utilisable immédiatement en local.

### Refaire l’extraction à partir des 17 originaux

Installer Tesseract avec la langue française et LibreOffice pour le fichier `.doc`. Les exécutables `tesseract` et `soffice` doivent être dans le PATH. L’application web elle-même n’a pas besoin de ces outils.

```bash
python tools/ingest.py --source-dir "/chemin/vers/les/17-documents" --workers 4 --ocr-lang fra
python tools/audit_corpus.py
```

Le script vérifie les empreintes, reprend les pages déjà traitées et signale les fichiers absents, modifiés ou non extraits. Il conserve les tableaux Word et les coordonnées des blocs textuels des PDF natifs. Il ne reconstruit pas encore les tableaux des scans ni le lien exact entre chaque figure et chaque question.

## GitHub et déploiement gratuit

Consulter [GITHUB.md](docs/GITHUB.md) et [DEPLOY.md](docs/DEPLOY.md).

Architecture de cette itération : **FastAPI + interface HTML/CSS/JavaScript sans compilation + SQLite en local / PostgreSQL en hébergement**. Ce choix permet un seul service Render pour l’interface et l’API. Les règles pédagogiques sont séparées de l’interface pour permettre une évolution ultérieure.

Le service refuse de démarrer en mode hébergé sans `DATABASE_URL` et sans cookie sécurisé. Cela empêche une configuration Render qui perdrait les comptes en utilisant son disque éphémère.

## Vérifier

```bash
python -m pytest -q
python tools/check_content.py
node --check web/app.js
```

Les tests utilisent une base temporaire SQLite. Pour tester PostgreSQL, définir `TEST_DATABASE_URL` vers une **base de test dédiée** : les tests effacent leurs tables. GitHub Actions réalise les deux passages avec un service PostgreSQL isolé.

Les résultats réellement exécutés et les limites figurent dans [VALIDATION.md](docs/VALIDATION.md).

## Structure

```text
app/                 API, authentification, persistance et règles pédagogiques
web/                 Interface élève et enseignant
content/             Sources, cadre pédagogique, programme et questions versionnés
tools/               Extraction, synchronisation, audit et vérification du corpus
tests/               Parcours, rôles, barèmes, indices, sessions et publication
docs/                Architecture, usages des sources, GitHub et déploiement
data/                Données privées locales, ignorées par Git
render.yaml          Configuration du service Render
requirements.lock    Versions utilisées pour cette itération
```

Le périmètre de la v0.1 est une seule cohorte pilote. Il n’inclut pas encore plusieurs établissements, récupération de mot de passe, portail parent, paiements ou export des données élèves. Aucune mesure de gain d’apprentissage n’a été réalisée avec des élèves réels.
