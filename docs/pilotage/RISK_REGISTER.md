# Registre des risques

| ID | Risque | Prob. | Impact | Mesure | Statut |
|---|---|---|---|---|---|
| R-01 | Programme officiel 2AC non fourni : graphe de compétences reconstruit depuis manuels/guides | élevée | moyen | Demander les orientations pédagogiques officielles collège ; marquer le graphe « dérivé des manuels » | ouvert |
| R-02 | Droits de reproduction des manuels commerciaux (APEF, Sochepress, Étincelle, L'Univers Plus, Almoufid) | élevée | élevé | Usage interne pour alignement ; contenus élèves originaux, sourcés par page, validés enseignant (H-6) | ouvert |
| R-03 | OCR imparfait sur pages scannées et schémas | élevée | moyen | Confiance OCR par page, revue humaine des pages à risque, pas de figure interprétée sans contrôle | ouvert |
| R-04 | Erreurs scientifiques dans les sources | moyenne | élevé | Relevé T-006, hiérarchie des sources, validation enseignant | ouvert |
| R-05 | Pas de clé API ni budget : multimodal non testable en réel | élevée | élevé | Intégration + mode dev signalé ; recette impossible sans services réels | ouvert |
| R-06 | Données de mineurs (Maroc loi 09-08 / CNDP ; RGPD si UE) | certaine | élevé | Minimisation, pas d'entraînement, validation juridique compétente avant pilote | ouvert |
| R-07 | Fuite entre écoles (DB, vecteurs, fichiers, cache, logs) | moyenne | critique | Isolation par tenant à tous les niveaux + tests d'accès croisés + seconde revue | ouvert |
| R-08 | Exposition des corrigés aux élèves / injection de prompt | moyenne | élevé | Séparation stockage corrigés, permissions côté outils, jeu de tests adversariaux | ouvert |
| R-09 | Divergence vision D22 (émotions, parents, coach) vs brief | certaine | moyen | DEC-004, Q7, Q8 | ouvert |
| R-10 | Manuels partiels : Étincelle (D17) = 14 pages (sommaire + ch.1 seulement) | certaine | faible | Noté dans le registre ; demander version complète si utile | ouvert |
| R-11 | Conteneur éphémère : outils et fichiers hors `/mnt/project-files` perdus | certaine | moyen | Tout état durable dans `alphastudyflex/`, dépôt Git dès Q5 | ouvert |
