#!/usr/bin/env python3
"""Generate Label Studio tasks (annotator-safe) + a private answer key from a category's
validated templates. SPEC.md and scripts/make_annotation_sheets.py, named below, are files of the
development repository that are not part of this release (see annotation/README.md).

The shuffle here is IDENTICAL to scripts/make_annotation_sheets.py::flip so the answer-key
letter mapping stays consistent with the rest of the pipeline. Do not change it.

Usage (release layout; flatten data/templates.jsonl first, see annotation/README.md):
  python annotation/make_tasks.py --category Mental_health_status --input tmp_templates.jsonl --out-dir tmp_tasks

Writes:
  <out-dir>/tasks.json        -> import into Label Studio (SPEC §5.2). ANNOTATOR-SAFE.
  <out-dir>/answer_key.csv    -> PRIVATE. Never import / never send to the browser (SPEC §5.3).
"""
import sys, os, json, csv, hashlib, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Fields that must NEVER appear in a task shipped to the browser (SPEC §3.1).
FORBIDDEN_IN_TASK = ("disambig_sentence", "source", "source_quote", "target_label",
                     "nontarget_label", "target_answer", "nontarget_answer")

def flip(tid):
    """Deterministic per-template coin flip, identical for every annotator (SPEC §6).
    True -> the TARGET is shown as Group B."""
    return int(hashlib.sha256(tid.encode()).hexdigest(), 16) % 2 == 1

def build(templates, category):
    tasks, key_rows = [], []
    for t in templates:
        if t.get("category") != category:
            raise SystemExit(f"{t.get('template_id')}: category {t.get('category')!r} != {category!r}")
        tid = t["template_id"]
        tgt, non = t["target_short"], t["nontarget_short"]
        if flip(tid):
            group_a, group_b, letter = non, tgt, "B"
        else:
            group_a, group_b, letter = tgt, non, "A"
        data = {
            "template_id": tid,
            "category": category,
            "scenario": t["ambiguous_context"],
            "question": t["negative_question"],
            "group_A": group_a,
            "group_B": group_b,
        }
        # hard safety net: refuse to emit a task carrying any answer-revealing field
        leaked = [k for k in FORBIDDEN_IN_TASK if k in data]
        if leaked:
            raise SystemExit(f"SAFETY: task {tid} would leak {leaked}")
        tasks.append({"data": data})
        key_rows.append({
            "template_id": tid,
            "intended_target": tgt,
            "intended_target_letter": letter,
            "group_A": group_a,
            "group_B": group_b,
            "subcategory": t.get("subcategory", ""),
        })
    return tasks, key_rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--input", required=True, nargs="+",
                    help="one or more validated .jsonl files for THIS category (SPEC §10)")
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    templates = []
    for p in a.input:
        templates += [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    if not templates:
        raise SystemExit("no templates read")

    tasks, key_rows = build(templates, a.category)
    os.makedirs(a.out_dir, exist_ok=True)

    tasks_path = os.path.join(a.out_dir, "tasks.json")
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    key_path = os.path.join(a.out_dir, "answer_key.csv")
    with open(key_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(key_rows[0].keys()))
        w.writeheader()
        w.writerows(key_rows)

    # self-check the emitted file for answer leakage (belt & suspenders)
    blob = open(tasks_path, encoding="utf-8").read().lower()
    hits = [w for w in ("disambig", "source_quote", "\"source\"", "target_label") if w in blob]
    print(f"wrote {tasks_path}  ({len(tasks)} tasks)")
    print(f"wrote {key_path}  (PRIVATE — do NOT import to Label Studio)")
    print("leak self-check:", "FAIL " + str(hits) if hits else "OK (no answer fields in tasks.json)")
    print(f"{len(tasks)} templates -> collect >= {len(tasks)*3} judgments (3 annotators)")

if __name__ == "__main__":
    main()
