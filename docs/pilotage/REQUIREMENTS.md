# Exigences (v0, extraites du brief de Candy du 2026-10-07)

Statut de chaque exigence : proposé → implémenté → testé → validé enseignant → déployé.
Colonnes Spéc / Impl / Test à remplir au fil des jalons. Phase : P = pilote, C = lancement commercial, E = évolution.

| ID | Exigence | Phase | Spéc | Impl | Test | Statut |
|---|---|---|---|---|---|---|
| REQ-001 | Multimodal de bout en bout : texte, image, audio, vidéo dans ingestion, recherche, activités, interactions, restitutions | P | brief §4,§5,§8 | — | — | proposé |
| REQ-002 | Provenance de chaque unité : fichier, version (empreinte), page, section, coordonnées si utile | P | §4 | extract_pages.sh (page) | — | partiel |
| REQ-003 | Distinguer texte extrait / description générée / interprétation / contenu créé | P | §4 | — | — | proposé |
| REQ-004 | Matrice de couverture : tous fichiers et pages ont un statut | P | §4 | DOCUMENT_COVERAGE.md | — | en cours |
| REQ-005 | Graphe compétences / prérequis / erreurs fréquentes ; chaque activité reliée à programme, compétence, difficulté, source | P | §5 | — | — | proposé |
| REQ-006 | Parcours : classe → diagnostic → plan proposé → validation enseignant → séances → exercices/feedback → réévaluation → bilan | P | §5 | — | — | proposé |
| REQ-007 | Tuteur à indices gradués, ne donne pas la réponse d'emblée | P | §5 | — | — | proposé |
| REQ-008 | Bilans : maîtrise démontrée / résultat assisté / incertain / non évalué | P | §5 | — | — | proposé |
| REQ-009 | Photo/schéma : confirmer ce qui est reconnu avant correction incertaine | P | §5 | — | — | proposé |
| REQ-010 | Oral évalué sur l'objectif disciplinaire, pas l'accent ni le micro ; micro/caméra facultatifs ; pas d'autoplay | P | §5,§9 | — | — | proposé |
| REQ-011 | Alternative accessible à tout objectif essentiel (transcription, sous-titres, description, clavier, écrit) | P | §5 | — | — | proposé |
| REQ-012 | Diagnostic pédagogique uniquement : ni QI, ni trouble, ni styles d'apprentissage, ni émotions | P | §6 | — | — | proposé |
| REQ-013 | Pour chaque dimension : observé, tâches, barème, preuves, confiance, manques, limites, date de réévaluation | P | §6 | — | — | proposé |
| REQ-014 | Agents produit : entrées/sorties typées, outils autorisés, périmètre, prompts versionnés, budgets, arrêt, validation humaine | P | §7 | — | — | proposé |
| REQ-015 | Permissions appliquées côté serveur et par les outils, jamais seulement par le prompt | P | §7 | — | — | proposé |
| REQ-016 | États de contenu : brouillon, contrôle auto, à vérifier, validé, publié, retiré ; corrigés séparés | P | §7 | — | — | proposé |
| REQ-017 | Réponses citant des sources récupérées et accessibles à l'utilisateur ; abstention si source absente | P | §8 | — | — | proposé |
| REQ-018 | Appels IA via backend, clé en configuration sécurisée, plafond de coût, quotas par école | P | §8 | — | — | proposé |
| REQ-019 | Isolation multi-tenant : DB, vecteurs, fichiers, caches, tâches, logs, exports, sauvegardes, outils IA ; tests d'accès croisés | P | §9 | — | — | proposé |
| REQ-020 | Matrice de permissions par rôle ; accès support limité et audité | P | §9 | — | — | proposé |
| REQ-021 | Expérience élève agréable : missions, progrès démontrés, pas de classement public ni de pression ; ludification désactivable | P | §9 | — | — | proposé |
| REQ-022 | Mobile, connexion faible, réduction des animations, contrastes, lecteurs d'écran | P | §9 | — | — | proposé |
| REQ-023 | MFA rôles privilégiés, chiffrement, limitation d'abus, journalisation sans données personnelles | P | §10 | — | — | proposé |
| REQ-024 | Pas d'entraînement sur données élèves ; suppression couvrant dérivés, index, caches ; politique de sauvegardes | P | §10 | — | — | proposé |
| REQ-025 | Panne IA n'empêche pas l'accès aux cours publiés | P | §11 | — | — | proposé |
| REQ-026 | Sauvegarde + restauration testée ; RPO/RTO définis | P | §11 | — | — | proposé |
| REQ-027 | Suivi des coûts par élève, école, import, séance | P | §11 | — | — | proposé |
| REQ-028 | Scénario de recette minimal §12 (créer école → … → exporter) | P | §12 | — | — | proposé |
| REQ-029 | Recette multimodale réelle avec services externes réels (pas de simulation) | P | §12 | — | — | proposé |
| REQ-030 | Jeu de démonstration séparé des données réelles | P | §12 | — | — | proposé |
| REQ-031 | Abonnements, facturation, impayés, résiliation, portabilité | C | §12 | — | — | proposé |
| REQ-032 | Ajout de disciplines, niveaux, langues, écoles sans refonte | E (conçu dès P) | intro | — | — | proposé |
