#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Import the GPT-4.1-mini / Gemini 2.5 Flash version B API runs made by one of the authors
(kaggle_eval/results/*__vb_p0_k3.jsonl in the development repository) into evaluation/results_vb/.

Those runs used evaluation/eval_banglabbq.py (prompt wording 0, 3 cyclic option orders) on the
per-category version B files, whose example_ids restart at 0 in each file. This script maps every
call to the version B id used by build_version_b_eval.py (version A example_id + 100000) and keeps
only disambiguated rows (the ambiguous rows are identical to version A, already scored there).

Usage (repo root):
  python evaluation/version_b/import_closed_src_vb.py <dir with the 20 *__vb_p0_k3.jsonl files>
"""
import glob, json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OFFSET = 100000
A = {"en": "output/banglabbq_eng_combined_v2.jsonl", "bn": "output/banglabbq_bng_combined.jsonl"}
VB = {"en": "output/banglabbq_{}_eng_vb.jsonl", "bn": "output/banglabbq_{}_bng_vb.jsonl"}
CATS = ["marital", "age_politics", "educational", "region", "mental_health"]


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def key(r):
    return (r["category"], str(r["question_index"]), r["question_polarity"], r["context_condition"],
            r["question"], r["ans0"], r["ans1"], r["ans2"])


def main(src):
    out_dir = os.path.join(ROOT, "evaluation", "results_vb")
    os.makedirs(out_dir, exist_ok=True)
    merged = defaultdict(list)
    for lang in ["en", "bn"]:
        a_id = {key(r): r["example_id"] for r in load(A[lang])}
        for cat in CATS:
            vb = {r["example_id"]: r for r in load(VB[lang].format(cat))}
            for path in glob.glob(os.path.join(src, f"*__{lang}__{cat}__vb_p0_k3.jsonl")):
                model = os.path.basename(path).split("__")[0]
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        j = json.loads(line)
                        v = vb[j["example_id"]]
                        if v["context_condition"] != "disambig":
                            continue
                        j["example_id"] = a_id[key(v)] + OFFSET
                        merged[(model, lang)].append(j)
    for (model, lang), rows in sorted(merged.items()):
        rows.sort(key=lambda j: (j["example_id"], j["perm"]))
        keys = {(j["example_id"], j["prompt_id"], j["perm"]) for j in rows}
        assert len(keys) == len(rows), f"{model} {lang}: duplicate calls"
        out = os.path.join(out_dir, f"{model}__{lang}__p0_k3.jsonl")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(json.dumps(j, ensure_ascii=False) + "\n" for j in rows)
        print(f"{os.path.relpath(out, ROOT)}: {len(rows)} calls, "
              f"{len({j['example_id'] for j in rows})} records, errors {sum(1 for j in rows if j.get('error'))}")


if __name__ == "__main__":
    main(sys.argv[1])
