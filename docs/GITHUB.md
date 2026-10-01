# Versionner et pousser chaque itération

L’archive contient le code et un dépôt Git local avec le commit de la première itération. Aucun remote ni identifiant GitHub n’est configuré.

## Premier envoi

1. Créer sur GitHub un dépôt vide nommé `alphastudyflex`, sans README généré.
2. Extraire l’archive, ouvrir un terminal dans le dossier `alphastudyflex`.
3. Vérifier le contenu, puis ajouter son remote :

```bash
git status
git remote add origin https://github.com/cdywolf/alphastudyflex.git
git push -u origin main
git push origin v0.1.0
```

Adapter l’URL si le dépôt porte un autre nom. L’authentification s’effectue avec le gestionnaire Git installé ou GitHub CLI ; aucun jeton ne doit figurer dans l’URL ou dans un fichier du dépôt.

Si l’outil d’extraction a omis le dossier `.git`, initialiser une seule fois :

```bash
git init -b main
git add .
git commit -m "feat: initial SVT learning pilot"
git tag v0.1.0
```

## Itérations suivantes

Garder le même dossier et le même dépôt. Ne pas recréer Git ni écraser `.git` avec une nouvelle archive.

```bash
git pull --ff-only
git switch -c iteration-02
# Appliquer les modifications de l’itération.
python -m pytest -q
python tools/check_content.py
git diff --stat
git status
git add app web content tools tests docs README.md CHANGELOG.md pyproject.toml requirements.lock render.yaml .github
git commit -m "feat: describe the second iteration"
git push -u origin iteration-02
```

Créer une pull request vers `main`. Après réussite de la CI et revue, fusionner. Render peut être configuré pour déployer la branche `main` après réussite des vérifications.

## Ce qui reste hors Git

Le fichier `.gitignore` exclut les PDF et Word originaux, `data/`, les bases SQLite, `.env`, les caches et les environnements Python. Le cache d’extraction du corpus se synchronise vers la base distante au moyen du script dédié ; il ne doit pas être ajouté de force au dépôt.

Les configurations pédagogiques et les questions préparées pour le produit sont versionnées. Le corpus source reste séparé. Les règles de réutilisation des illustrations devront être clarifiées avant une diffusion publique de reproductions de manuels.

## Revenir à une version

Les changements de code peuvent être consultés avec `git log` et les versions identifiées par des tags. Ne pas supprimer la base pour revenir à un ancien code. Les futures évolutions du schéma devront ajouter une migration numérotée ; le schéma initial est la version 1.
