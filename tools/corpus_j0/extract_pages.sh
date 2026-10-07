#!/usr/bin/env bash
# Extraction page par page : texte natif (pdftotext) sinon OCR tesseract fra+ara à 200 dpi.
# Usage: extract_pages.sh <doc_id> <chemin_pdf> <dossier_sortie> [rev]   (rev = pages en ordre inverse, pour paralléliser un même document)
# Idempotent : une page déjà extraite (meta .json présent) est sautée.
set -u
DOC="$1"; PDF="$2"; OUT="$3/$DOC"; mkdir -p "$OUT"
N=$(pdfinfo "$PDF" | awk '/^Pages:/{print $2}')
TMP=$(mktemp -d)
ORDER=$(seq 1 "$N"); [ "${4:-}" = rev ] && ORDER=$(seq "$N" -1 1)
for p in $ORDER; do
  pp=$(printf "%03d" "$p")
  [ -f "$OUT/p$pp.json" ] && continue
  pdftotext -f "$p" -l "$p" -layout "$PDF" "$OUT/p$pp.txt" 2>/dev/null
  c=$(tr -d '[:space:]' < "$OUT/p$pp.txt" | wc -c)
  method=native; conf=null
  if [ "$c" -lt 100 ]; then
    pdftoppm -r 200 -f "$p" -l "$p" -png "$PDF" "$TMP/img" 2>/dev/null
    img=$(ls "$TMP"/img*.png | head -1)
    tesseract "$img" "$TMP/o" -l fra+ara txt tsv >/dev/null 2>&1
    cp "$TMP/o.txt" "$OUT/p$pp.txt"
    conf=$(awk -F'\t' 'NR>1 && $11>=0 && $12!="" {s+=$11;n++} END{if(n) printf "%.1f", s/n; else print "null"}' "$TMP/o.tsv")
    c=$(tr -d '[:space:]' < "$OUT/p$pp.txt" | wc -c)
    method=ocr_tesseract_fra+ara_200dpi
    rm -f "$TMP"/img*.png "$TMP"/o.*
  fi
  printf '{"doc_id":"%s","page":%d,"method":"%s","chars":%d,"ocr_mean_conf":%s}\n' "$DOC" "$p" "$method" "$c" "$conf" > "$OUT/p$pp.json"
done
rm -rf "$TMP"
echo "done $DOC $N"
