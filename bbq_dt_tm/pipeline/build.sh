#!/usr/bin/env bash
# Rebuild every BanglaBBQ DT/TM file from BBQ's templates.
# Usage: bash build.sh <path to BBQ's templates folder> <output folder>
# Writes <output folder>/<Category>.jsonl (PakBBQ layout: DT rows, then TM rows).
# BBQ: https://github.com/nyu-mll/BBQ (templates/ folder). Requires Python 3 with pandas.
set -euo pipefail
BBQ="$1"; OUT="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="$(mktemp -d)"
mkdir -p "$OUT" "$WORK/split"
for T in DT TM; do
  mkdir -p "$WORK/tpl_$T"; python3 "$HERE/prepare_templates.py" "$BBQ" "$WORK/tpl_$T" "$T" >/dev/null
  # categories are generated in the same groups as the delivered files (the random seed is shared within a group)
  for G in "Age,Disability_status" Physical_appearance SES Gender_identity Religion; do
    mkdir -p "$WORK/raw_${T}_${G}"; python3 "$HERE/generate_bbq.py" "$WORK/tpl_$T" "$WORK/raw_${T}_${G}" "$G" >/dev/null
  done
done
F="$HERE/finalize.py"
python3 "$F" "$WORK/raw_DT_Age,Disability_status" "$WORK/split" DT
python3 "$F" "$WORK/raw_TM_Age,Disability_status" "$WORK/split" TM Age=15,Disability_status=21
python3 "$F" "$WORK/raw_DT_Physical_appearance" "$WORK/split" DT "" Physical_appearance
python3 "$F" "$WORK/raw_TM_Physical_appearance" "$WORK/split" TM Physical_appearance=16 Physical_appearance
python3 "$F" "$WORK/raw_DT_SES" "$WORK/split" DT "" SES
python3 "$F" "$WORK/raw_TM_SES" "$WORK/split" TM SES=11 SES
python3 "$F" "$WORK/raw_DT_Gender_identity" "$WORK/split" DT "" Gender_identity
python3 "$F" "$WORK/raw_TM_Gender_identity" "$WORK/split" TM Gender_identity=14 Gender_identity
python3 "$F" "$WORK/raw_DT_Religion" "$WORK/split" DT "" Religion
python3 "$F" "$WORK/raw_TM_Religion" "$WORK/split" TM Religion=5 Religion
# SES 8 (first names) was built after the name list was agreed and appended as SES TM 24
mkdir -p "$WORK/tpl_S8" "$WORK/raw_S8" "$WORK/fin_S8"
python3 "$HERE/prepare_templates.py" "$BBQ" "$WORK/tpl_S8" TM_NAMES >/dev/null
python3 "$HERE/generate_bbq.py" "$WORK/tpl_S8" "$WORK/raw_S8" SES >/dev/null
python3 "$F" "$WORK/raw_S8" "$WORK/fin_S8" TM SES=24 SES >/dev/null
python3 "$HERE/append_tm.py" "$WORK/split/SES_TM_eng.jsonl" "$WORK/fin_S8/SES_TM_eng.jsonl"
python3 "$HERE/merge_categories.py" "$WORK/split" "$OUT"
rm -rf "$WORK"
