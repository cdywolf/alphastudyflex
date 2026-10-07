# Plan de tests et d'évaluation — v0

Statut : **proposé**. Aucun test produit exécuté à ce jour (aucun code produit).

- Tests auto : unitaires (calculs de résultats, règles de diagnostic), intégration, E2E du scénario §12,
  autorisations et accès croisés entre écoles, imports, accessibilité, charge, restauration.
- Évaluation IA : jeu annoté et validé par enseignants (questions simples, erreurs fréquentes, schémas, contradictions,
  absence de réponse, demandes de corrigé, injections, hors périmètre). Mesures : retrieval, fidélité, validité des citations,
  correction pédagogique, niveau de langue, abstention, latence, coût. Juge LLM calibré sur revue humaine.
- Multimodal : erreurs de transcription, schémas mal lus, décalage audio/image, passages vidéo manqués.
- Contrôles déjà réalisés : extraction page à page avec statut (voir DOCUMENT_COVERAGE.md).
