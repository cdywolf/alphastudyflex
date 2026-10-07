# Décisions

Format : ID — date — statut (proposée / validée Candy / remplacée) — décision — raison.

- **DEC-001** — 2026-10-07 — validée (brief Candy) — Périmètre actif SVT uniquement ; PC et maths en backlog futur sans travaux actifs.
- **DEC-002** — 2026-10-07 — proposée — Tant qu'aucun dépôt Git n'existe, la racine projet est
  `/mnt/project-files/alphastudyflex/` (persistante, partagée). Migration vers un dépôt privé dès accord (Q5).
- **DEC-003** — 2026-10-07 — proposée — Tranche verticale initiale : Unité 1, chapitre Volcanisme et sa relation
  avec la tectonique des plaques ; prérequis diagnostiqué : Tectonique des plaques.
  Raison : chapitre présent dans les 6 manuels/guides 2AC reçus, seul chapitre avec un exercice **corrigé**
  dédié (D02) plus deux séries non corrigées (D06, D10) ; fort potentiel multimodal (vidéo d'éruption, coupe
  de volcan à légender, mise en ordre d'étapes, manipulation simulée explosif/effusif décrite dans D11) ;
  prérequis clair et lui aussi bien documenté (D01, D05, D17 ch.1).
- **DEC-004** — 2026-10-07 — proposée — Pas de détection d'émotions, caméra ni biométrie, contrairement à D22.
  Raison : exigence du brief (§6) et données de mineurs. À confirmer Q7.
- **DEC-005** — 2026-10-07 — proposée — Équipe de construction : rôles tenus par Claude sous forme de revues
  structurées successives (**simulation organisationnelle**). Des sous-agents réels (outil Agent) sont utilisés
  uniquement pour la seconde revue indépendante des tâches sensibles, avec budget borné.
- **DEC-006** — 2026-10-07 — proposée — Extraction : texte natif `pdftotext` si ≥100 caractères utiles par page,
  sinon OCR tesseract fra+ara 200 dpi ; confiance OCR moyenne conservée par page.

## Réponses de Candy du 2026-10-07 10:52 UTC
- **DEC-007** — 2026-10-07 — validée Candy — Pilote : un établissement IPSE, **2 classes de 35 élèves** (70 élèves) de 2AC.
  Candy indique qu'un enseignant a déjà validé les contenus (= documents sources fournis). Les contenus **générés** par la
  plateforme (items, activités, corrigés rédigés) restent à faire valider par un enseignant (coordonnées à obtenir au J1).
- **DEC-008** — 2026-10-07 — validée Candy — Niveau 2AC parcours international option français confirmé (H-1 levée).
  Candy considère que les référentiels sont parmi les fichiers ; constat : D20/D21 sont des référentiels **lycée**.
  Décision de travail : le graphe de compétences 2AC est dérivé des guides D11/D12 et des manuels, marqué comme tel ;
  un référentiel collège reste bienvenu s'il existe (non bloquant).
- **DEC-009** — 2026-10-07 — validée Candy — Objectif du MVP : **démonstration convaincante pour investisseurs**, budget très limité,
  hébergement gratuit. Clé API Claude créée par Candy sur demande. Plafond de dépense : à fixer (demandé, voir T-012).
- **DEC-010** — 2026-10-07 — validée Candy — Dépôt GitHub privé sous le compte `cdywolf`. Aucun code POC existant : on part de zéro.
- **DEC-011** — 2026-10-07 — validée Candy — Langues : interface et contenus en français, glossaire arabe ; arabe/RTL complet reporté.
- **DEC-012** — 2026-10-07 — par défaut (non répondu, réversible) — Droits : manuels utilisés en interne pour alignement et références de page ;
  contenus élèves originaux. Pas de détection d'émotions (DEC-004). Rôles pilote : élève, enseignant, direction, admin ; parents/coach reportés.
- **DEC-013** — 2026-10-07 — proposée — Hébergement gratuit du MVP (conditions vérifiées le 2026-10-07, voir ARCHITECTURE.md §Hébergement) :
  API FastAPI sur Render (free web service) ; base PostgreSQL + pgvector + stockage fichiers sur Supabase (free) ; frontend statique
  sur Render static site. **Pas Vercel Hobby** : ses conditions le réservent à un usage personnel non commercial.
  Pas de Postgres gratuit Render (expire après 30 jours). Traitements lourds (OCR, extraction, génération audio) exécutés hors ligne
  et chargés dans la base, pas de worker gratuit disponible.
- **DEC-014** — 2026-10-07 — validée Candy (carte de décision) — Plafond API Claude phase démo : **25 $/mois**.
  À appliquer par : limite de dépense dans la console Anthropic (côté Candy) + quota applicatif par école dans le backend + arrêt contrôlé.
- **DEC-015** — 2026-10-07 — validée Candy (carte de décision) — On **continue sur le MVP existant** du dépôt (v0.1.1, FastAPI + PostgreSQL Neon + Render).
  Conséquence : DEC-013 ajustée, la base reste Neon (déjà intégrée) au lieu de Supabase ; stockage de médias à choisir quand nécessaire.
  Les documents de pilotage vont dans `docs/pilotage/` + `CLAUDE.md` à la racine du dépôt, sans écraser les docs existants.
