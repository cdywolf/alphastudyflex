# Déployer le pilote gratuitement depuis GitHub

Configuration retenue pour la v0.1 : Render Free pour l’interface et l’API, Neon Free pour PostgreSQL. Les offres et limites ont été consultées le 1 octobre 2026 ; vérifier les écrans de souscription avant activation.

Références officielles :

- https://render.com/docs/free
- https://render.com/docs/blueprint-spec
- https://neon.com/pricing
- https://neon.com/faqs/free-plan-limits-and-quotas

Render Free se met en veille après 15 minutes sans trafic ; le premier accès suivant peut attendre environ une minute. Son disque est éphémère, donc aucune donnée élève ne doit y être conservée durablement. Render propose aussi une base gratuite qui expire au bout de 30 jours ; cette configuration utilise Neon à la place. Neon Free annonce notamment 0,5 Go par projet et un quota de calcul. Ces offres conviennent à un petit pilote, sous réserve de leurs limites ; elles ne garantissent pas un service permanent sans attente.

## 1. Préparer Neon

Créer un projet sur le plan Free. Copier sa chaîne PostgreSQL avec `sslmode=require` depuis la fonction de connexion. Choisir de préférence une région proche du service Render. Garder cette chaîne privée : elle contient les accès à la base.

Aucune carte ni formule payante n’est nécessaire au code. Ne pas activer volontairement un plan payant pour ces étapes. Si le fournisseur impose des conditions différentes, vérifier celles affichées dans le compte.

## 2. Déployer le dépôt

Pousser le code sur GitHub. Dans Render, créer un **Blueprint** depuis ce dépôt et sélectionner le fichier `render.yaml` à la racine.

- Le service doit afficher `plan: free`.
- Renseigner `DATABASE_URL` avec la connexion Neon.
- `ASF_SETUP_TOKEN` et `ASF_INVITE_CODE` sont générés par Render.
- `ASF_ENV=production` et `ASF_SECURE_COOKIE=1` sont définis dans le Blueprint.
- La commande de démarrage utilise le port fourni par Render.

Lancer le déploiement. Le service doit répondre sur `/api/health`. L’application initialise uniquement les tables manquantes ; elle n’efface pas les comptes lors d’un redéploiement.

## 3. Créer le compte enseignant

Dans les variables Render, consulter la valeur de `ASF_SETUP_TOKEN`. Ouvrir l’URL du site, cliquer **Première installation**, choisir son identifiant et un mot de passe, puis saisir ce code.

La route d’installation refuse de créer un second enseignant initial lorsque le premier existe. Après succès, supprimer `ASF_SETUP_TOKEN` des variables Render. Le code d’invitation élève, distinct, reste défini dans `ASF_INVITE_CODE`.

Se connecter, vérifier les 3 séances et les 19 questions, puis publier chaque question dans **Contenus**. Cette validation est conservée en PostgreSQL et invalidée automatiquement si le contenu correspondant change.

Partager l’URL et le code d’invitation uniquement avec les participants au pilote. Ils créent leur compte élève depuis l’écran de connexion.

## 4. Importer les extractions sans mettre les PDF dans Git

Extraire le pack corpus fourni dans le projet local pour obtenir `data/processed/`. Sur son ordinateur, définir temporairement la même `DATABASE_URL` Neon, puis lancer :

### PowerShell

```powershell
$env:DATABASE_URL = "CONNEXION_NEON_PRIVEE"
.\.venv\Scripts\python tools/sync_corpus.py --processed-dir data/processed
Remove-Item Env:DATABASE_URL
```

### Bash

```bash
read -r -s -p "Connexion Neon : " DATABASE_URL
export DATABASE_URL
.venv/bin/python tools/sync_corpus.py --processed-dir data/processed
unset DATABASE_URL
```

Cette opération importe 503 pages extraites et 2 documents Word structurés. Les comptes enseignants peuvent ensuite les consulter dans **Documents**, même après redémarrage du service Render. Aucun PDF brut ni donnée d’élève n’est transmis dans GitHub.

La v0.1 stocke le texte structuré en PostgreSQL. La bibliothèque distante d’images originales et l’index multimodal restent à ajouter dans une prochaine itération. Le premier parcours utilise des schémas pédagogiques inclus dans l’interface.

## 5. Déployer les itérations suivantes

Développer sur une branche, exécuter la CI, fusionner vers `main`, puis laisser Render déployer le nouveau commit. Dans les réglages du service, sélectionner le déploiement automatique après réussite des checks si cette option est disponible pour le dépôt.

Ne jamais exécuter les tests avec la connexion de production dans `TEST_DATABASE_URL`. Ne pas réinitialiser la base lors d’une mise à jour. Avant une future migration de schéma, sauvegarder la base et tester la migration sur une branche ou base séparée.

## Vérification après déploiement

- `/api/health` répond `status: ok`.
- Le premier compte enseignant peut se connecter et la page Documents affiche le corpus importé.
- Un élève invité termine une évaluation et retrouve son résultat après déconnexion.
- Après redéploiement, le compte et les résultats sont toujours présents.
- Une requête élève vers l’espace enseignant reçoit un refus.

L’archive ne contient aucun compte Render/Neon et aucun secret. Le déploiement sur un compte utilisateur n’a pas été effectué dans cette itération ; il nécessite la connexion GitHub et la configuration Neon dans Render.
