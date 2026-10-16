#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Deterministic compiler: template objects (CLAUDE.md §3.1) -> 8-row BBQ/PakBBQ records (§3.2/§3.3).

Usage: python compile.py <input_templates.jsonl> <output_records.jsonl>
"""
import json, sys

UNKNOWN = ["Unknown", "unknown"]
UNKNOWN_STR = "Unknown"

REQUIRED = ["template_id","category","subcategory","target_group","nontarget_group",
            "target_label","nontarget_label","stereotyped_groups","target_answer",
            "nontarget_answer","target_short","nontarget_short","ambiguous_context",
            "disambig_sentence","negative_question","nonnegative_question","source"]

def expand(t, qindex, start_eid):
    """Return the 8 records for one template. §3.3 order/labels are hard-coded."""
    amb = t["ambiguous_context"]
    dis = (amb + " " + t["disambig_sentence"]).strip()
    T = [t["target_short"], t["target_label"]]
    N = [t["nontarget_short"], t["nontarget_label"]]
    U = UNKNOWN
    Ta, Na = t["target_answer"], t["nontarget_answer"]
    negq, nonq = t["negative_question"], t["nonnegative_question"]

    # answer_info per ordering
    ai_A = {"ans0": T, "ans1": U, "ans2": N}   # order A: T,U,N
    ai_B = {"ans0": N, "ans1": T, "ans2": U}   # order B: N,T,U
    # display strings per ordering
    sA = {"ans0": Ta, "ans1": UNKNOWN_STR, "ans2": Na}
    sB = {"ans0": Na, "ans1": Ta, "ans2": UNKNOWN_STR}

    meta = {"subcategory": t["subcategory"],
            "stereotyped_groups": t["stereotyped_groups"],
            "version": "a",
            "source": t["source"]}

    # (ctx_cond, polarity, ordering, context, question, label)
    plan = [
        ("ambig",   "neg",    "A", amb, negq, 1),  # U at pos1
        ("disambig","neg",    "A", dis, negq, 0),  # T at pos0
        ("ambig",   "nonneg", "A", amb, nonq, 1),  # U at pos1
        ("disambig","nonneg", "A", dis, nonq, 2),  # N at pos2
        ("ambig",   "neg",    "B", amb, negq, 2),  # U at pos2
        ("disambig","neg",    "B", dis, negq, 1),  # T at pos1
        ("ambig",   "nonneg", "B", amb, nonq, 2),  # U at pos2
        ("disambig","nonneg", "B", dis, nonq, 0),  # N at pos0
    ]
    recs = []
    for i, (cc, pol, order, ctx, q, label) in enumerate(plan):
        eid = start_eid + i
        ai = ai_A if order == "A" else ai_B
        s = sA if order == "A" else sB
        recs.append({
            "example_id": eid,
            "question_index": str(qindex),
            "question_polarity": pol,
            "context_condition": cc,
            "category": t["category"],
            "answer_info": {"ans0": ai["ans0"], "ans1": ai["ans1"], "ans2": ai["ans2"]},
            "additional_metadata": dict(meta),
            "context": ctx,
            "question": q,
            "ans0": s["ans0"], "ans1": s["ans1"], "ans2": s["ans2"],
            "label": label,
            "type": "NA",
            "id": eid,
        })
    return recs

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    templates = [json.loads(l) for l in open(inp, encoding="utf-8") if l.strip()]
    # validate schema presence
    for t in templates:
        missing = [k for k in REQUIRED if k not in t]
        if missing:
            raise SystemExit(f"Template {t.get('template_id','?')} missing fields: {missing}")
    all_recs = []
    eid = 0
    for qi, t in enumerate(templates, start=1):
        all_recs.extend(expand(t, qi, eid))
        eid += 8
    with open(outp, "w", encoding="utf-8") as f:
        for r in all_recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Compiled {len(templates)} templates -> {len(all_recs)} records -> {outp}")

if __name__ == "__main__":
    main()
