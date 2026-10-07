# Agents exécutés dans le produit — v0

Statut : **proposé**. Distinct de l'équipe qui construit le logiciel (voir DEC-005).
Principe : workflow contrôlé ; code déterministe quand c'est suffisant ; LLM seulement là où il apporte de la valeur.

| Fonction | Forme proposée | Déclencheur | Validation humaine |
|---|---|---|---|
| Préparation documentaire | Pipeline déterministe + vision/OCR | import | contrôle enseignant des pages à risque |
| Alignement curriculaire | LLM structuré + règles | après extraction | enseignant |
| Conception d'activités | LLM structuré, sources imposées | demande enseignant | obligatoire avant publication |
| Diagnostic | Règles explicites auditables | entrée en classe | enseignant peut contester |
| Planification | Règles + LLM pour la formulation | après diagnostic | validation enseignant |
| Tutorat | LLM borné (indices gradués, RAG filtré) | séance élève | supervision a posteriori |
| Correction | Barème + LLM calibré sur revue humaine | soumission | échantillonnage enseignant |
| Contrôle des sources | Vérification citation ↔ segment récupéré | chaque réponse | — |
| Suivi de progression / synthèse enseignant | Calcul déterministe + rédaction LLM sourcée | périodique | enseignant |

Contrat commun à détailler au J2 : entrées/sorties typées (Pydantic), outils autorisés, périmètre école/classe/élève
imposé par le serveur, prompt versionné, budget tokens et temps, conditions d'arrêt, reprise, journal de trace.
