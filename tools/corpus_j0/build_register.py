"""Génère docs/DOCUMENT_REGISTER.md, docs/DOCUMENT_COVERAGE.md et corpus/coverage_pages.csv.

Entrées : tools/inventory_raw.tsv (empreintes/pages), tools/doc_ids.tsv, tools/doc_meta.tsv,
corpus/pages/<Dxx>/pNNN.json (statut d'extraction par page).
Usage : python3 tools/build_register.py
"""
import csv, json, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
today = datetime.date.today().isoformat()

def norm(p):
    return " ".join(p.split())

ids = {}
for line in open(os.path.join(T, "doc_ids.tsv"), encoding="utf-8"):
    i, p = line.rstrip("\n").split("\t")
    ids[norm(p)] = i
ids[norm("Referentiel Pedagogique IPSE/Version Préfinale Programme SVT,  SM envoyée le 5 Mars 2018 .docx")] = "D20"
ids[norm("Referentiel Pedagogique IPSE/Version préfinale Programme SVT, Sc Exp envoyée le 5 mars 2018.doc")] = "D21"

raw = {}
for line in open(os.path.join(T, "inventory_raw.tsv"), encoding="utf-8"):
    sha, size, pages, chars, low, prod, path = line.rstrip("\n").split("\t")
    rel = norm(path.removeprefix("svt/"))
    raw[ids[rel]] = dict(sha=sha, size=int(size), pages=pages, producer=prod.strip("; "), path=path)

meta = {r["id"]: r for r in csv.DictReader(open(os.path.join(T, "doc_meta.tsv"), encoding="utf-8"), delimiter="\t")}

def status(j):
    if j["method"].startswith("ocr"):
        conf = j["ocr_mean_conf"]
        if j["chars"] < 80:
            return "OCR quasi vide (image/illustration ?) – revue humaine"
        if conf is None or conf < 75:
            return "OCR confiance faible – revue humaine"
        return "OCR extrait – échantillonnage à faire"
    if j["chars"] < 100:
        return "texte natif quasi vide (image/illustration ?) – revue humaine"
    return "texte natif extrait"

rows, per_doc = [], {}
for d in sorted(meta):
    files = sorted(glob.glob(os.path.join(ROOT, "corpus", "pages", d, "*.json")))
    agg = per_doc.setdefault(d, {"pages_done": 0, "native": 0, "ocr": 0, "review": 0, "confs": []})
    for f in files:
        j = json.load(open(f, encoding="utf-8"))
        s = status(j)
        agg["pages_done"] += 1
        agg["ocr" if j["method"].startswith("ocr") else "native"] += 1
        if "revue" in s:
            agg["review"] += 1
        if j.get("ocr_mean_conf") is not None:
            agg["confs"].append(j["ocr_mean_conf"])
        rows.append([d, j["page"] if j["page"] is not None else "doc", j["method"], j["chars"],
                     j.get("ocr_mean_conf") if j.get("ocr_mean_conf") is not None else "",
                     s, "non analysé"])

with open(os.path.join(ROOT, "corpus", "coverage_pages.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["doc_id", "page", "methode_extraction", "caracteres", "confiance_ocr_moy",
                "statut_extraction", "statut_pedagogique"])
    w.writerows(rows)

# Registre
out = [f"# Registre documentaire SVT\n",
       f"Généré par `tools/build_register.py` le {today}. Sources : `/mnt/project-files/svt/` (lecture seule).",
       "Version d'un fichier = 16 premiers caractères de son SHA-256. Droits : rien n'est présumé autorisé à la redistribution.\n",
       "| ID | Fichier | Type | Rôle pédagogique | Langue | Niveau | Éditeur / origine | Droits connus | Pages | Taille | Version (sha256) | Contenu | Notes |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for d in sorted(meta):
    m, r = meta[d], raw[d]
    out.append(f"| {d} | `{r['path']}` | {m['type']} | {m['role']} | {m['langue']} | {m['niveau']} | {m['editeur_origine']} | "
               f"{m['droits']} | {r['pages']} | {r['size']/1e6:.1f} Mo | `{r['sha']}` | {m['contenu']} | {m['notes']} |")
out += ["", "## Organisation par niveau, programme et chapitre (SVT 2AC)", "",
        "Colonnes = sources ; ✓ = chapitre présent (d'après sommaires lus) ; partiel = extrait ; — = absent.", "",
        "| Unité / chapitre | D13-14 APEF | D15-16 Compétence | D17 Étincelle | D18 Naciri | D11 guide Almoufid | D12 guide Univers+ | Exercices |",
        "|---|---|---|---|---|---|---|---|",
        "| U1 Tectonique des plaques / dérive | ✓ | à vérifier (OCR) | ✓ | ✓ | ✓ | ✓ | D01, D05 |",
        "| U1 Séismes | ✓ | à vérifier | sommaire seul | ✓ | ✓ | ✓ | D01, D07, D09 |",
        "| U1 Volcanisme | ✓ | à vérifier | sommaire seul | ✓ | ✓ | ✓ (avec roches) | **D02 (corrigé)**, D06, D10 |",
        "| U1 Roches magmatiques | ✓ | à vérifier | sommaire seul | partiel | ✓ | ✓ (avec volcanisme) | D01, D08 |",
        "| U1 Déformations tectoniques | ✓ | à vérifier | sommaire seul | ✓ | ✓ | ✓ (avec chaînes) | D04 |",
        "| U1 Chaînes de montagnes | ✓ | à vérifier | sommaire seul | ✓ | ✓ | ✓ | D03 |",
        "| U2 Reproduction sexuée animale | ✓ | à vérifier | sommaire seul | — | ✓ | ✓ | — |",
        "| U2 Reproduction végétale | ✓ | à vérifier | sommaire seul | — | ✓ | ✓ | — |",
        "| U2 Reproduction humaine | ✓ | à vérifier | sommaire seul | — | ✓ | ✓ | — |",
        "| U2 Hérédité humaine | ✓ | à vérifier | sommaire seul | — | ✓ | ✓ | — |",
        "", "## Documents encore attendus (SVT) et travaux dépendants", "",
        "| Pièce attendue | Pourquoi | Travaux bloqués ou fragilisés |",
        "|---|---|---|",
        "| Programme / orientations pédagogiques officiels SVT collège (MEN), ou référentiel IPSE collège s'il existe | D20/D21 couvrent le lycée seulement | Graphe de compétences « officiel » (T-007), alignement curriculaire |",
        "| Confirmation du manuel de référence de l'école pilote | 4 manuels différents reçus | Hiérarchie des sources, citations élèves |",
        "| Étincelle complet (D17 = 14 p. sur ~160) | Seul le ch.1 est présent | Couverture U1 ch.2-6 et U2 dans cette collection |",
        "| Corrigés des exercices D03-D10 (ou accord pour corrigés rédigés par nous puis validés) | Sans corrigé de référence | Critères de correction, jeu d'évaluation IA |",
        "| Exercices Unité 2 | Aucun reçu | Diagnostic et activités U2 (J5) |",
        "| Évaluations réelles anonymisées (contrôles, grilles, copies) si l'école l'autorise | Calibrer barèmes et erreurs fréquentes | T-008, évaluation IA |",
        "| Médias autorisés : vidéos, audio, images libres de droits ou de l'école | Exigence multimodale | Activités vidéo/audio de la tranche Volcanisme |",
        "| Statut des droits des manuels et du polycopié | Redistribution aux écoles non présumée | Publication de contenus dérivés aux élèves |",
        ""]
open(os.path.join(ROOT, "docs", "DOCUMENT_REGISTER.md"), "w", encoding="utf-8").write("\n".join(out))

# Couverture
cov = [f"# Matrice de couverture documentaire\n",
       f"Généré le {today} par `tools/build_register.py`. Détail page par page : `corpus/coverage_pages.csv`.",
       "Chaîne : document → pages → extraction → contrôle qualité → compétences → ressources/évaluations → statut.",
       "Un décompte de pages ne prouve pas une extraction parfaite : les pages « revue humaine » et un échantillon des autres doivent être vérifiés.\n",
       "| ID | Pages attendues | Pages traitées (au moment de la génération) | Texte natif | OCR | Conf. OCR moy. | Pages à revoir | Contrôle qualité | Exploitation pédagogique |",
       "|---|---|---|---|---|---|---|---|---|"]
for d in sorted(meta):
    a, r = per_doc[d], raw[d]
    conf = f"{sum(a['confs'])/len(a['confs']):.0f}" if a["confs"] else "—"
    exp = "doc entier" if r["pages"] == "-" else r["pages"]
    cov.append(f"| {d} | {exp} | {a['pages_done']} | {a['native']} | {a['ocr']} | {conf} | {a['review']} | non échantillonné | non analysé |")
cov += ["", "## Erreurs, contradictions et écarts relevés (T-006, à faire valider par un enseignant)", "",
        "| Réf. | Source | Constat | Statut |", "|---|---|---|---|",
        "| E-01 | D11 guide Almoufid, ch.3 séquence 1, tâche 1 (PDF p.42) | Lave visqueuse du Saint Helens annoncée à « à peu près 350 °C ». D12 p036 attribue ces 350 °C à la nuée ardente, pas à la lave : confusion probable lave / nuée ardente. Le même « 350 °C » est donné pour les eaux hydrothermales en PDF p.44 (cohérent). | à valider |",
        "| E-02 | D11, ch.3 (PDF p.42-44) | « volcans explosives et intrusives », « basalte andésitique » : terminologie incohérente (intrusif ≠ effusif ; andésite ≠ basalte). | à valider |",
        "| E-03 | D18 Naciri, ch.4 « Formation des chaînes de montagnes » (PDF p.25-26) | Deux sections titrées « Formation de chaîne de subduction » ; la seconde traite de l'Himalaya, chaîne de **collision** (le texte le dit ensuite). Titre erroné. | à valider |",
        "| E-04 | D18 | Nombreuses fautes de frappe (« blog » pour bloc, « océane ») : non canonique pour citations élèves. | constaté |",
        "| E-05 | Découpage | Volcanisme et roches magmatiques : chapitres séparés (D11, D13, D17) ou fusionnés (D12). Le graphe de compétences doit être indépendant du découpage éditeur. | constaté |",
        "| E-06 | D20/D21 | Référentiels lycée, hors niveau 2AC. | constaté |",
        ""]
open(os.path.join(ROOT, "docs", "DOCUMENT_COVERAGE.md"), "w", encoding="utf-8").write("\n".join(cov))
print("ok", len(rows), "lignes de couverture")
