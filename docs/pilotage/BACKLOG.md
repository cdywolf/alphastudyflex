# Backlog et feuille de route

Cycle obligatoire par tâche : planifier → préconditions → réaliser → tester → revue → corriger → clôturer avec preuves.
Statuts : `à faire` · `en cours` · `bloqué` · `implémenté` · `testé` · `validé enseignant` · `déployé` · `terminé (preuve)`.
Responsables = rôles (tenus par Claude en simulation organisationnelle, DEC-005) ; « Candy » / « Enseignant » = humains.
Aucune durée n'est annoncée avant analyse.

## Jalons

| Jalon | Livrables | Responsable | Dépend de | Critères d'acceptation |
|---|---|---|---|---|
| **J0 Cadrage & corpus** | Brief, questions, registre documentaire, extraction page à page, matrice de couverture, hiérarchie des sources, mémoire projet | Orchestrateur, Resp. documentaire | Documents reçus | 100 % des fichiers et pages ont un statut ; écarts et lacunes listés ; Candy a répondu aux questions bloquantes |
| **J1 Modèle pédagogique – tranche Volcanisme** | Graphe compétences/prérequis/erreurs fréquentes, items de diagnostic, activités multimodales, critères de correction, alignement sources (Dxx p.) | Expert pédagogique, Expert mesure | J0, Q2 | Chaque item relié à une compétence et à une source ; revue par un enseignant SVT réel consignée |
| **J2 Socle technique** | Monolithe modulaire, multi-tenant, auth, rôles, import de documents, stockage objet, worker, CI | Architecte, Backend, Sécurité | Q4, Q5 (dépôt) | Tests auto verts, dont accès croisés entre écoles ; secrets hors code |
| **J3 Tranche verticale démontrable** | Parcours import→diagnostic→plan→séance multimodale→exercice→feedback→réévaluation→bilan enseignant, sur le chapitre Volcanisme | Toute l'équipe | J1, J2, budget API (Q4) | Scénario §12 exécuté avec services réels (LLM, STT, TTS), sur mobile et connexion limitée, preuves jointes |
| **J4 Revue Candy** | Démo, guide de lancement, scénarios élève/enseignant, limites | Orchestrateur | J3 | Retours de Candy consignés et corrigés |
| **J5 Couverture SVT 2AC** | Unité 1 complète, puis Unité 2 | Pédagogie, Documentaire | J4 | Matrice de couverture à jour, revue enseignant par chapitre |
| **J6 Préparation pilote** | Sécurité, sauvegarde + restauration testée, suivi coûts, onboarding, accord données, CNDP à faire valider | Sécurité, DevOps, Onboarding | J5 partiel | Check-list « pilote prêt » du brief §14 |
| **J7 Pilote école** | Classes, formation, support, mesures | PM, Mesure éducative | J6, école | Indicateurs collectés selon protocole |
| **J8 Commercialisation** | Offre, contrats, facturation, support | PM B2B, Commercial | J7 | Préparation contractuelle vérifiée par un juriste |

## Tâches actives

| ID | Tâche | Resp. | Entrées | Dépend | Résultat attendu | Risques | Acceptation | Statut |
|---|---|---|---|---|---|---|---|---|
| T-001 | Inventaire des fichiers (empreinte, pages, type, langue) | Documentaire | `svt/` | — | `DOCUMENT_REGISTER.md` | fichiers manquants | 22/22 fichiers enregistrés | terminé (registre) |
| T-002 | Extraction page à page (natif + OCR) | Documentaire | T-001 | — | `corpus/pages/` | OCR faible sur schémas | chaque page a un `.json` de statut | terminé (530/530 pages + 2 docs Word) |
| T-003 | Matrice de couverture J0 | Documentaire | T-002 | T-002 | `DOCUMENT_COVERAGE.md` | — | toutes les pages ont un statut | en cours |
| T-004 | Questions prioritaires à Candy (Q1-Q5 bloquantes, Q6-Q8 réversibles, voir PREMIERE_REPONSE.md) | Orchestrateur | brief | — | 8 questions | — | réponses consignées dans DECISIONS | en attente Candy |
| T-005 | Carte d'alignement des sources pour Volcanisme (pages par document) | Pédagogie | T-002 | T-002 | `pedagogy/volcanisme/sources.md` | découpages différents selon éditeurs | chaque document 2AC localisé ou « absent » | en cours (D15 à borner) |
| T-006 | Relevé des erreurs/contradictions probables dans les sources | Pédagogie, QA | T-005 | T-005 | liste dans `DOCUMENT_COVERAGE.md` | — | chaque point cité avec page | en cours (2 relevés) |
| T-007 | Graphe de compétences Volcanisme + prérequis | Pédagogie | T-005 | Q2 | `pedagogy/volcanisme/competences.yaml` | programme officiel 2AC absent | relié aux sources ; revue enseignant | implémenté v0.1 (`pedagogy/volcanisme/competences.yaml`), non validé enseignant |
| T-008 | Items de diagnostic + barème + erreurs fréquentes | Mesure éducative | T-007 | T-007 | banque d'items sourcée | items non standardisés | marqués « non standardisé » ; revue enseignant | implémenté v0.1 (13 items, `pedagogy/volcanisme/diagnostic_items.yaml`), non validé ; 4 médias à produire |
| T-009 | Proposition d'architecture comparée | Architecte | brief | — | `ARCHITECTURE.md` v1 | — | options comparées, décision Candy | proposé |
| T-010 | Vérification doc officielle API Claude (modalités, tarifs, données) | IA/RAG | — | — | note datée dans `ARCHITECTURE.md` | évolution tarifs | sources officielles citées | partiel (tarifs notés ; modalités audio/vidéo à vérifier au J2) |
| T-011 | Créer dépôt privé `cdywolf/alphastudyflex` et migrer | DevOps | DEC-010 | Candy : connecter GitHub + créer le dépôt vide | dépôt + CI | — | dépôt attaché à la session | terminé (dépôt existant connecté le 2026-10-07 ; MVP 0.1.1 repris, DEC-015) |
| T-012 | Fixer le plafond de dépense API pour la phase démo | Candy | DEC-009 | — | montant en $/mois dans DECISIONS | — | décision consignée | terminé (DEC-014 : 25 $/mois) |
| T-013 | Hébergement gratuit (Render + Neon, DEC-015) : comptes, projets | Candy + DevOps | DEC-013, DEC-015 | accord de Candy pour déployer | URL de démo | veille des offres gratuites | démo accessible | à faire |
| T-014 | Chapitre Volcanisme dans le code (0.2.0) : serveur multi-chapitres, 3 séances, 20 questions, schéma original | Dév. + Concepteur pédagogique | T-008, DEC-015 | dépôt connecté | branche `claude/pilotage-et-volcanisme` + pull request | 19 tests SQLite et PostgreSQL, `check_content.py`, essai navigateur | revue de code, puis validation enseignant des 20 questions | testé (pas validé enseignant, pas déployé) |

## Backlog futur (aucun travail actif)
- F-001 Extension physique-chimie (sources, critères, validations propres) — après décision Candy.
- F-002 Extension mathématiques — idem.
- F-003 Interface arabe / RTL complète.
- F-004 Espace parents ; rôle coach pédagogique.
- F-005 SSO / LMS / exports avancés, selon écoles identifiées.
- F-006 Modèles de suivi de maîtrise (BKT/IRT) si volume et qualité des données le permettent.
- F-007 Autres niveaux collège (1AC, 3AC) et lycée (référentiels IPSE D20/D21 déjà reçus).
