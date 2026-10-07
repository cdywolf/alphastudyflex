# État du projet

Dernière mise à jour : 2026-10-07 (session 1, fin de journée).

## Objectif et périmètre actuels
SVT 2AC parcours international option français (confirmé). Pilote IPSE, 2 classes × 35 élèves.
Code : dépôt privé `cdywolf/alphastudyflex`, on continue sur le MVP existant (DEC-015).
Tranche en cours : chapitre Volcanisme, version 0.2.0 sur la branche `claude/pilotage-et-volcanisme`.

## Fait (avec preuves)
- J0 corpus : inventaire de 22 fichiers, extraction page à page (natif + OCR fra+ara) → `corpus/pages/`, `DOCUMENT_REGISTER.md`, `DOCUMENT_COVERAGE.md` ; 6 écarts relevés (E-01 à E-06).
- Volcanisme pédagogie v0.1 : `pedagogy/volcanisme/competences.yaml` et `diagnostic_items.yaml` (non validés).
- Audit du MVP 0.1.1 → `AUDIT_MVP_0.1.1.md` (13 tests passants à la reprise).
- Code 0.2.0 (T-014) : serveur multi-chapitres, migration de schéma 2, chapitre Volcanisme (3 compétences, 3 séances, 20 questions en brouillon, schéma original de coupe de volcan), prérequis entre chapitres signalés.
  Tests : 19 passés sous SQLite et sous PostgreSQL 17 local ; `tools/check_content.py` OK ; essai navigateur du diagnostic Volcanisme sans erreur JS.

## Statuts
- 0.2.0 : **testé** localement. **Pas validé enseignant** (les 20 questions volcanisme sont des brouillons). **Pas déployé.**
- Tectonique : contenu inchangé octet pour octet, les validations déjà publiées restent valides.

## Bloquants / en attente de Candy
- Revue de la pull request 0.2.0, puis transmission des 20 questions à l'enseignant référent.
- Accord explicite avant tout déploiement (Render Free + Neon, T-013).
- Clé API Claude à demander au moment de brancher le tuteur (plafond 25 $/mois, DEC-014).

## Prochaines actions ordonnées
1. Driver la PR 0.2.0 jusqu'au vert (CI SQLite + PostgreSQL).
2. Médias manquants : carte des plaques, 2 vidéos d'éruption sous licence libre (audio/vidéo = exigence multimodale).
3. Multi-établissement / classes (isolation par établissement côté serveur).
4. Tuteur Claude côté serveur avec plafond de dépense et journal de coût.
5. Déploiement démo après accord de Candy.

## Opérations externes effectuées
- Push sur `cdywolf/alphastudyflex`, branche `claude/pilotage-et-volcanisme` (autorisé par Candy : dépôt fourni et connecté).
- Aucun déploiement, aucune dépense, aucun appel à l'API Claude.
