"""Turn generator output into PakBBQ-structured BanglaBBQ files and validate them.

Usage: python finalize.py <raw dir> <out dir> <DT|TM> <start index per category as Cat=N,...>
"""
import collections
import json
import re
import sys

RAW, OUT, TYPE = sys.argv[1], sys.argv[2], sys.argv[3]
START = dict(kv.split("=") for kv in sys.argv[4].split(",")) if len(sys.argv) > 4 and sys.argv[4] else {}
CATS = sys.argv[5].split(",") if len(sys.argv) > 5 else ["Age", "Disability_status"]
ORDER = ["example_id", "question_index", "question_polarity", "context_condition", "category",
         "answer_info", "additional_metadata", "context", "question", "ans0", "ans1", "ans2",
         "label", "type", "id"]
DROPPED = ["high schooler", "middle schooler", "middle school student", "college freshman",
           "college sophomore", "high school freshman", "high school junior", "bartender", "tattoos",
           "autistic girlfriend", "autistic boyfriend", "jock", "Midwest", "redhead", "blonde hair",
           "record collection", "monther", "blue eyes", "green eyes", "blonde", "red head", "nose piercing",
           "the Y ", "boyfriend", "girlfriend", "already already", "hers, on who was", "line cook", "parking attendant", "optometrist",
           "junior high", "Jeopardy", "welfare", "public assistance", "one percenter", "honors society",
           "forest preserve", "bake sale", "brownies", "daycare", "cocaine", "heroine", "third language",
           "upper level", "The on ", "Yelp", "bartender", "out of state", "adopt children", "middle school",
           "college counselor", "dating for six", " bar.", " club."]

for cat in CATS:
    rows = [json.loads(l) for l in open(f"{RAW}/{cat}.jsonl")]
    bbq_ids = sorted({int(r["question_index"]) for r in rows})
    start = int(START.get(cat, 1))
    new_id = {q: str(start + i) for i, q in enumerate(bbq_ids)}
    out = []
    for i, r in enumerate(rows):
        # capitalise a sentence that starts with a filled-in slot (BBQ: "{{NAME1}} parents rarely ...")
        r["context"] = re.sub(r"([.!?] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), r["context"])
        md = r["additional_metadata"]
        md["bbq_question_index"] = str(r["question_index"])
        r["question_index"] = new_id[int(r["question_index"])]
        r["example_id"] = i
        r["type"] = TYPE
        r["id"] = i
        out.append({k: r[k] for k in ORDER})

    # ---------- validation ----------
    errs = []
    per = collections.defaultdict(lambda: collections.Counter())
    versions = collections.defaultdict(set)
    labels = collections.Counter()
    for r in out:
        q = r["additional_metadata"]["bbq_question_index"]
        versions[q].add(r["additional_metadata"]["version"])
        labels[r["label"]] += 1
        text = " ".join([r["context"], r["question"], r["ans0"], r["ans1"], r["ans2"]])
        if "{{" in text or "{[" in text or "}}" in text:
            errs.append(("unfilled slot", r["id"]))
        for w in (DROPPED if cat != "Physical_appearance" else [d for d in DROPPED if d not in ("tattoos",)]):
            if w.lower() in text.lower():
                errs.append(("dropped entry present", w, r["id"]))
        tags = [r["answer_info"][f"ans{k}"] for k in range(3)]
        if any(t[0] == "" or t[1] == "" for t in tags):
            errs.append(("empty answer_info", r["id"]))
        people = [t for t in tags if t[1] != "unknown"]
        if len(people) == 2 and people[0][1] == people[1][1]:
            errs.append(("both people share one tag", r["id"]))
        if sum(t[1] == "unknown" for t in tags) != 1:
            errs.append(("unknown count", r["id"]))
        gold = r["answer_info"][f"ans{r['label']}"][1]
        if r["context_condition"] == "ambig":
            if gold != "unknown":
                errs.append(("ambig gold not unknown", r["id"]))
        else:
            if gold == "unknown":
                errs.append(("disambig gold unknown", r["id"]))
            st = [s.lower().replace(" ", "") for s in r["additional_metadata"]["stereotyped_groups"]]
            g = {"woman": "f", "girl": "f", "man": "m", "boy": "m"}.get(gold.lower(), gold.lower().replace(" ", ""))
            is_target = g in st
            consistent = (r["question_polarity"] == "neg") == is_target
            per[q]["consistent" if consistent else "inconsistent"] += 1
    unbalanced = {q: dict(c) for q, c in per.items() if c["consistent"] != c["inconsistent"]}
    missing_v = {q: sorted(v) for q, v in versions.items() if len(v) < 2}
    with open(f"{OUT}/{cat}_{TYPE}_eng.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{cat}_{TYPE}_eng.jsonl: {len(out)} rows, {len(bbq_ids)} templates, "
          f"question_index {start}..{start + len(bbq_ids) - 1}, labels {dict(sorted(labels.items()))}")
    print("   errors:", errs[:5], "| unbalanced directions:", unbalanced, "| single-version templates:", missing_v)
    tot = collections.Counter()
    for c in per.values():
        tot.update(c)
    print("   disambiguated rows:", dict(tot))
