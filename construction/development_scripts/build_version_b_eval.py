#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Build the version B (counter-stereotypical) evaluation files from another author's version B data.

Version A disambiguates every template in the stereotyped direction, so on its own the BBQ
disambiguated bias score is +1 by construction and KoBBQ's diff_dis is undefined. Version B
(output/*_{eng,bng}_vb.jsonl, built by scripts/generate_all_version_b*.py) swaps in a
counter-stereotypical disambiguating sentence and flips the label. Its ambiguous rows are identical
to version A, so only its disambiguated rows need new model runs.

Each version B row is rebuilt from the CURRENT version A row (so later fixes to version A, e.g.
sources, carry over); only `context` and `label` come from the version B file. Version B rows get
example_id = version A example_id + 100000 and additional_metadata.version = "b".

Outputs (evaluation/version_b/):
  banglabbq_vb_dis_{eng,bng}.jsonl  version B disambiguated rows only (1,864 each): run models on these
  keep_vb.csv                       templates usable in version B (all minus EXCLUDE below)

Usage (repo root):  python evaluation/version_b/build_version_b_eval.py
Score version A + B together (score_banglabbq.py takes comma-separated data files):
  python evaluation/score_banglabbq.py "evaluation/results/*p0_k3.jsonl" "evaluation/results_vb/*.jsonl" \\
      --data-en output/banglabbq_eng_combined_v2.jsonl,evaluation/version_b/banglabbq_vb_dis_eng.jsonl \\
      --data-bn output/banglabbq_bng_combined.jsonl,evaluation/version_b/banglabbq_vb_dis_bng.jsonl \\
      --keep evaluation/version_b/keep_vb.csv --out evaluation/report_ab
"""
import copy, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OFFSET = 100000
A = {"eng": "output/banglabbq_eng_combined_v2.jsonl", "bng": "output/banglabbq_bng_combined.jsonl"}
CATS = ["marital", "age_politics", "educational", "region", "mental_health"]
# Templates whose version B item is not usable yet (content review, 2026-10-11): a question
# presupposes something that only fits the stereotyped person, or the answer is strained.
EXCLUDE = ["MAR-103", "MAR-308", "MAR-511", "MAR-609", "MAR-712", "REG-022", "REG-024",
           "REG-080", "REG-098", "REG-099", "MEN-311", "EDU-041"]


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def key(r):
    return (r["category"], str(r["question_index"]), r["question_polarity"], r["context_condition"],
            r["question"], r["ans0"], r["ans1"], r["ans2"])


def write(path, rows):
    with open(os.path.join(HERE, path), "w", encoding="utf-8", newline="\n") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def unknown_idx(r):
    return next(i for i in range(3) if r["answer_info"][f"ans{i}"][1].lower() == "unknown")


def main():
    for lang in ["eng", "bng"]:
        a_rows = load(A[lang])
        a_by_key = {}
        for r in a_rows:
            assert key(r) not in a_by_key, f"duplicate version A key {key(r)}"
            a_by_key[key(r)] = r
        b_rows = []
        for cat in CATS:
            for v in load(f"output/banglabbq_{cat}_{lang}_vb.jsonl"):
                if v["context_condition"] != "disambig":
                    continue
                a = a_by_key.get(key(v))
                if a is None:
                    sys.exit(f"{lang} {cat}: no version A row for version B example {v['example_id']}")
                assert v["label"] != a["label"], f"{lang} {a['example_id']}: label not flipped"
                assert v["label"] != unknown_idx(a), f"{lang} {a['example_id']}: version B label is Unknown"
                assert v["context"] != a["context"], f"{lang} {a['example_id']}: context unchanged"
                b = copy.deepcopy(a)
                b["context"], b["label"] = v["context"], v["label"]
                b["additional_metadata"]["version"] = "b"
                b["example_id"] = b["id"] = a["example_id"] + OFFSET
                b_rows.append(b)
        n_dis = sum(r["context_condition"] == "disambig" for r in a_rows)
        assert len(b_rows) == n_dis, f"{lang}: {len(b_rows)} version B rows for {n_dis} disambiguated rows"
        b_rows.sort(key=lambda r: r["example_id"])
        write(f"banglabbq_vb_dis_{lang}.jsonl", b_rows)
        print(f"{lang}: {len(b_rows)} version B disambiguated rows")

    with open(os.path.join(HERE, "..", "template_map.csv"), encoding="utf-8") as f:
        tids = [r["template_id"] for r in csv.DictReader(f)]
    missing = [t for t in EXCLUDE if t not in tids]
    assert not missing, f"EXCLUDE ids not in template_map.csv: {missing}"
    keep = [t for t in tids if t not in EXCLUDE]
    with open(os.path.join(HERE, "keep_vb.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("template_id\n" + "".join(t + "\n" for t in keep))
    print(f"keep_vb.csv: {len(keep)} templates ({len(EXCLUDE)} excluded)")


if __name__ == "__main__":
    main()
