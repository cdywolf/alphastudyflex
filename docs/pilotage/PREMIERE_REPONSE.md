# AlphaStudyFlex — première réponse (2026-10-07)

## 1. Vision et hypothèses du premier pilote
AlphaStudyFlex est une plateforme SaaS vendue aux écoles. Elle apporte un accompagnement pédagogique traçable,
aligné sur le programme et piloté par l'enseignant. L'élève passe un diagnostic des acquis, reçoit un plan que
l'enseignant valide, suit des séances courtes et multimodales (lire, observer, légender, écouter, répondre à l'oral,
regarder une vidéo, envoyer une photo de son schéma), s'exerce avec des indices gradués puis est réévalué.
L'enseignant obtient un bilan sourcé qui distingue maîtrise démontrée, résultat assisté, incertain et non évalué.

Ce que les documents reçus établissent (lu, pas supposé) :
- Tous les manuels, guides et exercices portent sur la **2e année collégiale (2AC)**, programme marocain,
  **parcours international, option français**. Le cours de D18 donne aussi les termes en arabe.
- Le programme 2AC comporte deux unités : **géologie interne** (tectonique des plaques, séismes, volcanisme,
  roches magmatiques, déformations, chaînes de montagnes) et **reproduction et hérédité humaine**.
- Les deux référentiels IPSE (D20, D21) concernent le **lycée**, pas le collège.
- Les exercices reçus couvrent uniquement l'Unité 1. Deux fichiers seulement contiennent un corrigé (D01, D02).
- Ta présentation AlphaStudyFlex (D22) prévoit la détection des émotions ainsi que des rôles parents et coach.
  Ces éléments s'écartent du cadre actuel. Je les ai mis en hypothèse d'exclusion et je te pose la question (questions 7 et 8).

Hypothèses de travail réversibles (détail dans `docs/PROJECT_BRIEF.md`) : pilote dans un établissement IPSE,
classes 2AC parcours international, interface en français avec glossaire arabe, PWA mobile d'abord, rôles élève /
enseignant / direction / admin école / opérateur, aucune détection d'émotions.

## 2. Mes capacités réelles dans cet environnement
| Capacité | Réalité aujourd'hui |
|---|---|
| Fichiers | Je lis et j'écris dans le dossier partagé du projet (persistant). Tes 22 fichiers SVT y sont déjà, je les ai lus. |
| Code et exécution | Je code et j'exécute dans un conteneur cloud **éphémère** : Python 3.13, Node 22, PostgreSQL 16, Docker, ffmpeg, LibreOffice, Chromium/Playwright. J'ai installé l'OCR tesseract français + arabe. |
| Tests | Je peux exécuter des tests unitaires, d'intégration et de navigateur, et en fournir les sorties. |
| Agents | Je peux lancer de vrais sous-agents en parallèle, mais cela coûte cher. Par défaut, je tiens les rôles de l'équipe sous forme de revues successives : c'est une **simulation organisationnelle**. Les vrais sous-agents seront réservés aux secondes revues des tâches sensibles. |
| Web | Je peux faire des recherches et lire des pages, par exemple la documentation officielle de l'API Claude ou de la CNDP. |
| Git | Aucun dépôt n'est connecté au projet. Je peux créer un dépôt et y pousser le code une fois GitHub connecté **et avec ton accord**. |
| Déploiement | Je n'ai aucun compte d'hébergement. Je peux publier des pages de démonstration privées (prototypes d'interface statiques). Un backend en ligne nécessite un hébergeur et un budget que tu valides. |
| API Claude / STT / TTS | Je n'ai **pas de clé**. L'intégration sera codée avec un mode de développement clairement signalé. Les tests réels demandent ta clé et un plafond de dépense. |
| Hors de portée | Contacter des écoles, valider juridiquement, remplacer la validation par un enseignant. |

## 3. Questions prioritaires (8)
**Bloquantes** : sans réponse, une partie du produit ou du budget ne peut pas avancer.
1. **École pilote et enseignant référent.** Le premier pilote se fait-il dans un établissement IPSE ? Combien de
   classes et d'élèves de 2AC ? Un enseignant de SVT peut-il valider les contenus (environ 1 à 2 h par chapitre) ?
2. **Programme.** Tu confirmes la 2AC, parcours international option français ? As-tu le programme officiel du
   collège (orientations pédagogiques) ou un référentiel IPSE pour le collège ? Quel manuel l'école utilise-t-elle ?
3. **Droits.** Les manuels APEF, Compétence, Étincelle, les guides et le polycopié de Pr. Naciri : as-tu le droit
   de les exploiter dans la plateforme ? Ma proposition par défaut : je les utilise en interne pour l'alignement et
   les références de page, et les élèves reçoivent des contenus originaux validés par l'enseignant.
4. **Budget et API.** Quel plafond mensuel acceptes-tu pour le développement (API Claude, transcription et synthèse
   vocale, hébergement) ? Vas-tu créer une clé API Anthropic à ton nom ? Préfères-tu un hébergement au Maroc ou dans l'UE ?
5. **Accès technique.** Puis-je créer un dépôt GitHub privé (en connectant GitHub au projet) pour y migrer les
   fichiers ? Existe-t-il du code du POC web mentionné dans D22 ?

**Hypothèses réversibles** : j'avance avec le choix indiqué si tu ne réponds pas.
6. **Langues.** Interface et contenus en français, avec glossaire arabe. Arabe/RTL complet plus tard. D'accord ?
7. **Émotions.** J'abandonne la détection d'émotions de D22 : pas de caméra ni de biométrie. Seules la confiance
   déclarée par l'élève et les observations de l'enseignant sont utilisées. D'accord ?
8. **Rôles.** Le pilote couvre élève, enseignant, direction et administrateur. Parents et coach sont reportés. D'accord ?

## 4. Feuille de route par jalons
Détail complet, avec responsables, dépendances et critères : `docs/BACKLOG.md`. Aucune durée n'est annoncée avant analyse.

| Jalon | Livrable utilisable | Critère d'acceptation |
|---|---|---|
| J0 Cadrage & corpus *(en cours)* | Registre, extraction page à page, couverture, écarts | Toutes les pages ont un statut ; questions bloquantes répondues |
| J1 Modèle pédagogique Volcanisme | Graphe de compétences, items de diagnostic, activités, critères de correction sourcés | Revue par un enseignant SVT consignée |
| J2 Socle technique | Multi-écoles, rôles, import de documents, CI | Tests verts, y compris les accès croisés entre écoles |
| J3 Tranche verticale | Parcours complet sur Volcanisme, de l'import au bilan enseignant | Scénario de recette avec services réels, mobile, connexion faible |
| J4 Ta revue | Démo, guide de lancement, scénarios élève/enseignant | Tes retours corrigés |
| J5 Couverture SVT 2AC | Unité 1, puis Unité 2 | Revue enseignant par chapitre |
| J6 Préparation pilote | Sécurité, restauration testée, coûts suivis, onboarding, données | Check-list « pilote prêt » |
| J7 Pilote → J8 Commercialisation | Mesures, offre, contrats | Protocole respecté ; validation juridique |

## 5. Mémoire et backlog créés
Ils sont dans `/mnt/project-files/alphastudyflex/` puisqu'aucun dépôt n'existe encore : `CLAUDE.md`, ainsi que
`docs/` (brief, exigences REQ-001 à 032, décisions, registre, couverture, pédagogie, agents, sécurité, tests,
pilote, risques, backlog, état, reprise, journal). Ce dossier persiste entre les sessions, mais ce n'est pas un
dépôt versionné. Je te conseille d'en télécharger une copie tant qu'il n'y a pas de dépôt.

## 6. Inventaire et analyse
Voir `docs/DOCUMENT_REGISTER.md` (22 fichiers : empreinte, pages, rôle, niveau, droits, organisation par
chapitre, pièces attendues) et `docs/DOCUMENT_COVERAGE.md` (statut page par page, écarts relevés).
Points saillants :
- 7 fichiers sont des **scans sans texte**, dont les manuels APEF et Compétence. Je les ai passés à l'OCR, soit
  530 pages extraites sur 530. Le score de confiance moyen de l'OCR va de 85 à 94 sur 100 selon le document ; ce
  n'est pas un taux d'exactitude. 24 pages sont marquées pour une revue humaine, et un échantillonnage reste à faire.
- Étincelle (D17) n'est qu'un extrait de 14 pages : le sommaire et le chapitre 1.
- 3 erreurs probables dans les sources sont à faire valider (E-01 à E-03). Exemple : le guide Almoufid donne une
  lave visqueuse « à environ 350 °C ». Ces passages ne seront jamais utilisés comme vérité canonique.

## 7. Prochain incrément
**Tranche Volcanisme** (Unité 1), avec la tectonique des plaques comme prérequis diagnostiqué (DEC-003). Ce chapitre
est présent dans toutes les sources 2AC. C'est le seul qui dispose d'un exercice corrigé dédié (D02) et de deux
séries supplémentaires (D06, D10), et il se prête bien au multimodal : vidéo d'éruption, coupe de volcan à
légender, étapes à remettre en ordre, simulation explosif/effusif.
Travaux lancés qui ne dépendent pas de tes réponses : carte d'alignement des sources du chapitre (T-005), relevé des
erreurs (T-006), puis graphe de compétences et items de diagnostic (T-007, T-008), qui resteront marqués « non validés ».
