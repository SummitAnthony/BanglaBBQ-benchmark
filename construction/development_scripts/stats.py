#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Statistician: summarize a template file and/or a compiled record file.

Usage:
  python stats.py templates <templates.jsonl>          # pre-compile summary
  python stats.py records   <records.jsonl>            # post-compile invariant check
"""
import json, sys
from collections import Counter
from urllib.parse import urlparse
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

def domain(u):
    try:
        return urlparse(u).netloc.replace("www.", "")
    except Exception:
        return "?"

def templates_report(path):
    T = load(path)
    print(f"# Template summary — {path}\n")
    print(f"- Template count: **{len(T)}**  (cap 100)  -> projected records: **{len(T)*8}**")
    tid = Counter(t["template_id"] for t in T)
    dups = [k for k,v in tid.items() if v>1]
    print(f"- Duplicate template_id: {dups if dups else 'none'}")
    print("\n## Per target group (stereotyped_groups)")
    grp = Counter(tuple(t["stereotyped_groups"]) for t in T)
    for k,v in grp.most_common():
        print(f"  - {', '.join(k):<45} {v}")
    print("\n## Per subcategory")
    for k,v in Counter(t["subcategory"] for t in T).most_common():
        print(f"  - {k:<30} {v}")
    print("\n## Per target_label")
    for k,v in Counter(t["target_label"] for t in T).most_common():
        print(f"  - {k:<20} {v}")
    print("\n## Per source domain (over-concentration flag if one dominates)")
    dc = Counter(domain(t["source"]) for t in T)
    tot = sum(dc.values())
    for k,v in dc.most_common():
        flag = "  <-- OVER 40%" if v/tot > 0.40 else ""
        print(f"  - {k:<35} {v}  ({v/tot*100:.0f}%){flag}")
    # duplicate scenario heuristic: same target_label + subcategory
    print("\n## Scenario density (target_label × subcategory)")
    for k,v in Counter((t["target_label"], t["subcategory"]) for t in T).most_common():
        print(f"  - {k[0]:<14} / {k[1]:<24} {v}")

def records_report(path):
    R = load(path)
    print(f"# Compiled-record invariant check — {path}\n")
    print(f"- Total records: **{len(R)}**")
    # label ratio
    lc = Counter(r["label"] for r in R)
    print(f"- label distribution: {dict(sorted(lc.items()))}  (expect ratio 2:3:3)")
    if len(R) % 8 == 0:
        u = len(R)//8
        print(f"  expected for {u} templates: {{0:{2*u}, 1:{3*u}, 2:{3*u}}}")
    # ambig vs disambig
    cc = Counter(r["context_condition"] for r in R)
    print(f"- context_condition: {dict(cc)}  (expect 50/50)")
    pol = Counter(r["question_polarity"] for r in R)
    print(f"- question_polarity: {dict(pol)}  (expect 50/50)")
    # per question_index = 8 rows
    qi = Counter(r["question_index"] for r in R)
    bad = {k:v for k,v in qi.items() if v!=8}
    print(f"- question_index groups: {len(qi)}; any != 8 rows: {bad if bad else 'none'}")
    # ambiguous rows always Unknown
    bad_amb = [r["example_id"] for r in R if r["context_condition"]=="ambig"
               and r["answer_info"][f"ans{r['label']}"][1] != "unknown"]
    print(f"- ambiguous rows whose correct answer is NOT Unknown: {bad_amb if bad_amb else 'none'}")
    # disambig rows never Unknown
    bad_dis = [r["example_id"] for r in R if r["context_condition"]=="disambig"
               and r["answer_info"][f"ans{r['label']}"][1] == "unknown"]
    print(f"- disambig rows whose correct answer IS Unknown: {bad_dis if bad_dis else 'none'}")
    # per-template label multiset must be {0:2,1:3,2:3}
    per = {}
    for r in R:
        per.setdefault(r["question_index"], Counter())[r["label"]] += 1
    bad_blocks = {k:dict(v) for k,v in per.items() if dict(v)!={0:2,1:3,2:3}}
    print(f"- per-template label multiset != {{0:2,1:3,2:3}}: {bad_blocks if bad_blocks else 'none'}")
    # duplicate example_id / id
    eids = [r["example_id"] for r in R]
    ids = [r["id"] for r in R]
    print(f"- duplicate example_id: {[k for k,v in Counter(eids).items() if v>1] or 'none'}")
    print(f"- example_id contiguous 0..N-1: {eids==list(range(len(R)))}")
    print(f"- id == example_id for all rows: {all(r['id']==r['example_id'] for r in R)}")
    # metadata keys
    okmeta = all(set(r["additional_metadata"].keys())=={"subcategory","stereotyped_groups","version","source"} for r in R)
    print(f"- additional_metadata has exactly 4 keys everywhere: {okmeta}")
    verdict = not (bad or bad_blocks or bad_amb or bad_dis) and eids==list(range(len(R)))
    print(f"\n## Verdict: {'PASS — all invariants hold' if verdict else 'FAIL — see flags above'}")

if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    (templates_report if mode=="templates" else records_report)(path)
