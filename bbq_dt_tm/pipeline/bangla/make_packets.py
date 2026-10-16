"""Collect, per category, every distinct template (with its slots) and every slot filler that the
generator actually used, as the input for translation: packets/<Cat>.json.

Usage: python make_packets.py   (after build_trace.py has written build/)
"""
import collections
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import CATS, FIELDS, SLOTS, load, load_frames, template_key  # noqa: E402

B = f"{HERE}/build"
os.makedirs(f"{HERE}/packets", exist_ok=True)
nv = pd.read_csv(f"{B}/tpl_DT/vocabulary_proper_names.csv", na_filter=False)
first = set(nv[nv.First_last == "first_only"].Name)
names = set()
for cat in CATS:
    frames = load_frames(B, cat)
    rows = load(f"{B}/eng/{cat}.jsonl")
    trs = load(f"{B}/trace/{cat}.trace.jsonl")
    tpls = collections.OrderedDict()
    fill = collections.OrderedDict()
    for bi, tr in enumerate(trs):
        key = template_key(tr)
        fr = frames[(tr["set"], tr["frame"])]
        if key not in tpls:
            r = rows[4 * bi + 1]
            tpls[key] = {"key": key, "type": r["type"], "banglabbq_question_index": r["question_index"],
                         "bbq_Q_id": tr["Q_id"], "version": tr["version"],
                         "fields": {f: fr[f][0] for f in FIELDS}, "slot_values": {s: [] for s in SLOTS},
                         "example_row": {"context": r["context"], "question": r["question"],
                                         "answers": [r["ans0"], r["ans1"], r["ans2"]]}}
        sv = tpls[key]["slot_values"]
        for s, v in (("NAME1", tr["w1"]), ("NAME2", tr["w2"]), ("WORD1", tr["r1"]), ("WORD2", tr["r2"])):
            if v and v not in sv[s]:
                sv[s].append(v)
            if v:
                if v in first:
                    names.add(v)
                else:
                    fill.setdefault(v, set()).add(key)
    for t in tpls.values():
        t["slot_values"] = {k: v for k, v in t["slot_values"].items() if v}
    pk = {"category": cat, "templates": list(tpls.values()), "fillers": sorted(fill)}
    with open(f"{HERE}/packets/{cat}.json", "w", encoding="utf-8") as f:
        json.dump(pk, f, ensure_ascii=False, indent=1)
    print(cat, "templates", len(tpls), "fillers", len(fill))
with open(f"{HERE}/packets/first_names.json", "w") as f:
    json.dump(sorted(names), f, indent=0)
