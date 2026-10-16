#!/usr/bin/env python3
"""Expand data/templates.jsonl into the record files in BBQ format (versions A and B).

Version A: every template yields eight records per language, always in this order:

    answers stored as [target, Unknown, non-target]
      1  ambiguous context,       negative question       correct answer: Unknown
      2  disambiguated context,   negative question       correct answer: target
      3  ambiguous context,       non-negative question   correct answer: Unknown
      4  disambiguated context,   non-negative question   correct answer: non-target
    answers stored as [non-target, target, Unknown]
      5-8  the same four items again

The disambiguated context is the ambiguous context followed by the disambiguating sentence, which
always describes the stereotype-consistent outcome.

Version B (counter-stereotypical): the four disambiguated records of each template again, with the
version B sentence (`version_b.<lang>.disambig_sentence`), which describes the opposite outcome, so the
correct answers swap (negative question: non-target; non-negative question: target).
`example_id` = version A id + 100000 and `additional_metadata.version` = "b". The ambiguous records are
the same in both versions and are not repeated.

The record format is PakBBQ's: BBQ's 13 keys in BBQ's order, plus `type` and `id` as in PakBBQ
(see data/README.md). Because the evaluation rotates
the three options cyclically, records 5-8 produce the same prompts as records 1-4; they are kept for
compatibility with the PakBBQ file format.

Usage (from the repository root; standard library only):
    python construction/compile_records.py --check   compare with the files in data/, byte for byte (exit 1 on any difference)
    python construction/compile_records.py           rewrite the four record files in data/
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "data", "templates.jsonl")
OUT = {("a", "en"): "data/banglabbq_en.jsonl", ("a", "bn"): "data/banglabbq_bn.jsonl",
       ("b", "en"): "data/banglabbq_vb_en.jsonl", ("b", "bn"): "data/banglabbq_vb_bn.jsonl"}
UNKNOWN = {"en": "Unknown", "bn": "যথেষ্ট তথ্য নেই"}
ITEMS = [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]
ORDERS = [("target", "unknown", "nontarget"), ("nontarget", "target", "unknown")]
VB_OFFSET = 100000


def records_of(t, lang, first_id, version="a"):
    x = t[lang]
    full = {"target": x["target_answer"], "nontarget": x["nontarget_answer"], "unknown": UNKNOWN[lang]}
    short = {"target": x["target_short"], "nontarget": x["nontarget_short"], "unknown": UNKNOWN[lang]}
    tag = {"target": t["target_label"], "nontarget": t["nontarget_label"], "unknown": "unknown"}
    sentence = x["disambig_sentence"] if version == "a" else t["version_b"][lang]["disambig_sentence"]
    out = []
    n = 0
    for order in ORDERS:
        for condition, polarity in ITEMS:
            eid = first_id + n
            n += 1
            if version == "b" and condition == "ambig":
                continue
            if condition == "ambig":
                correct = "unknown"
            elif (polarity == "neg") == (version == "a"):
                correct = "target"
            else:
                correct = "nontarget"
            rid = eid + (VB_OFFSET if version == "b" else 0)
            out.append({
                "example_id": rid,
                "question_index": str(t["question_index"]),
                "question_polarity": polarity,
                "context_condition": condition,
                "category": t["category"],
                "answer_info": {f"ans{j}": [short[r], tag[r]] for j, r in enumerate(order)},
                "additional_metadata": {"subcategory": t["subcategory"], "stereotyped_groups": t["stereotyped_groups"],
                                        "version": version, "source": t["source"]},
                "context": x["ambiguous_context"] + ("" if condition == "ambig" else " " + sentence),
                "question": x["negative_question"] if polarity == "neg" else x["nonnegative_question"],
                "ans0": full[order[0]], "ans1": full[order[1]], "ans2": full[order[2]],
                "label": order.index(correct),
                "type": "NA",
                "id": rid,
            })
    return out


def compile_language(templates, lang, version="a"):
    recs, first = [], 0
    for t in templates:
        assert t["example_ids"] == list(range(first, first + 8)), t["template_id"]
        recs.extend(records_of(t, lang, first, version))
        first += 8
    return recs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with the files on disk instead of writing")
    a = ap.parse_args()
    if not os.path.exists(TEMPLATES):
        sys.exit("data/templates.jsonl not found. Run this from a complete clone of the repository "
                 "(https://github.com/SummitAnthony/BanglaBBQ-benchmark).")
    with open(TEMPLATES, encoding="utf-8") as f:
        templates = [json.loads(l) for l in f if l.strip()]
    ok = True
    for (version, lang), rel in OUT.items():
        path = os.path.join(ROOT, rel)
        lines = [json.dumps(r, ensure_ascii=False) for r in compile_language(templates, lang, version)]
        if a.check:
            with open(path, "rb") as f:                   # byte for byte, line endings included (LF)
                same = f.read() == ("\n".join(lines) + "\n").encode("utf-8")
            ok &= same
            print(f"{rel}: {len(lines)} records, " + ("identical to the compiled templates" if same else "DIFFERS from the compiled templates"))
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
            print(f"wrote {rel} ({len(lines)} records)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
