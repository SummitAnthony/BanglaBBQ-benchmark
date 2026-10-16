"""Build and check the Bangla DT/TM rows for one or more categories.

Usage: python build_bangla.py <Category|all> [--samples N] [--write]

Run build_trace.py first (writes build/). Inputs, relative to this folder:
  packets/<Cat>.json        English templates + slot values (make_packets.py)
  bn/<Cat>.json             translation: {"templates": {key: {FIELD: bn}}, "fillers": {en: bn},
                            "filler_overrides": {key: {en: bn}}}   (overrides optional)
  bn/first_names.json       {en: bn} for the shared Bangladeshi first names
  build/eng/<Cat>.jsonl     English rows (identical to BanglaBBQ_ENG/)
  build/trace/<Cat>.trace.jsonl

Slot syntax in Bangla templates: {{NAME1}}, {{NAME2}}, {{WORD1}}, {{WORD2}} insert the filler as is;
{{NAME1:poss}} inserts the genitive (filler + "র" after a vowel, + "এর" after a consonant).

With --write, writes ../../BanglaBBQ_BN/<Cat>.jsonl. Exit status 1 if any hard check fails.
"""
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = HERE
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "BanglaBBQ_BN")
sys.path.insert(0, HERE)
from render import CATS, FIELDS, SLOTS, load, positions, template_key  # noqa: E402

# Register-symmetry heuristic from validate_bangla.py of the development repository, which is not part of
# this release; set BANGLABBQ_SCRIPTS to a folder that contains it to enable it. It is a soft check only,
# skipped when the module is not found.
sys.path.insert(0, os.environ.get("BANGLABBQ_SCRIPTS", HERE))
try:
    from validate_bangla import check_register_symmetry  # noqa: E402
except ImportError:
    def check_register_symmetry(rows):
        return []

UNKNOWN_BN = "যথেষ্ট তথ্য নেই"  # same wording as the NA Bangla file (evaluation/unknown_wording/report.md)
VOWEL_END = set("ািীুূৃেৈোৌঅআইঈউঊঋএঐওঔ")
SLOT_RE = re.compile(r"\{\{(NAME1|NAME2|WORD1|WORD2)(?::(poss))?\}\}")
LATIN_RE = re.compile(r"[A-Za-z]{2,}")
sys.stdout.reconfigure(encoding="utf-8")


def genitive(w):
    if w and w[-1] in "অআইঈউঊঋএঐওঔ":  # independent vowel letter: ভাই -> ভাইয়ের
        return w + "য়ের"
    return w + ("র" if w and w[-1] in VOWEL_END else "ের")


def fill(text, vals):
    def sub(m):
        v = vals.get(m.group(1))
        if v is None:
            return m.group(0)
        return genitive(v) if m.group(2) == "poss" else v
    return SLOT_RE.sub(sub, text)


def build(cat, samples, write):
    pk = json.load(open(f"{S}/packets/{cat}.json", encoding="utf-8"))
    bn = json.load(open(f"{S}/bn/{cat}.json", encoding="utf-8"))
    names = json.load(open(f"{S}/bn/first_names.json", encoding="utf-8"))
    eng = load(f"{S}/build/eng/{cat}.jsonl")
    trs = load(f"{S}/build/trace/{cat}.trace.jsonl")
    hard, soft = [], []
    tb, fb, ov = bn.get("templates", {}), bn.get("fillers", {}), bn.get("filler_overrides", {})

    # template-level checks
    for t in pk["templates"]:
        k = t["key"]
        if k not in tb:
            hard.append(f"{k}: template missing")
            continue
        for f in FIELDS:
            b = tb[k].get(f)
            if not isinstance(b, str) or (not b.strip() and t["fields"][f].strip()):
                hard.append(f"{k}: field {f} missing/empty")
                continue
            need = set(re.findall(r"\{\{(NAME1|NAME2|WORD1|WORD2)\}\}", t["fields"][f]))
            have = {m.group(1) for m in SLOT_RE.finditer(b)}
            if need - have:
                hard.append(f"{k}: {f} lost slot(s) {sorted(need - have)}")
            if have - need and f not in ("Ambiguous_Context", "Disambiguating_Context"):
                soft.append(f"{k}: {f} has extra slot(s) {sorted(have - need)}")
            stray = re.sub(SLOT_RE, "", b)
            if "{" in stray or "}" in stray:
                hard.append(f"{k}: {f} malformed slot: {b}")
    for f in pk["fillers"]:
        if f not in fb and not all(f in ov.get(k, {}) for k in
                                   [t["key"] for t in pk["templates"]
                                    if any(f in v for v in t["slot_values"].values())]):
            hard.append(f"filler missing: {f!r}")
    if hard:
        return hard, soft, []

    def fbn(key, en):
        if en in ov.get(key, {}):
            return ov[key][en]
        if en in fb:
            return fb[en]
        return names[en]

    out = []
    by_key_rows = {}
    for bi, tr in enumerate(trs):
        block = eng[4 * bi: 4 * bi + 4]
        key = template_key(tr)
        vals = {"NAME1": fbn(key, tr["w1"]).strip(), "NAME2": fbn(key, tr["w2"]).strip()}
        if tr["r1"]:
            vals["WORD1"] = fbn(key, tr["r1"]).strip()
        if tr["r2"]:
            vals["WORD2"] = fbn(key, tr["r2"]).strip()
        t = {f: re.sub(r"\s+", " ", fill(tb[key][f], vals)).strip() for f in FIELDS}
        amb = t["Ambiguous_Context"]
        dis = f"{amb} {t['Disambiguating_Context']}".strip()
        text_for = {"neg": t["Answer_negative"], "nonneg": t["Answer_non_negative"], "unknown": UNKNOWN_BN}
        pos = positions(block)
        short_map = {tr["w1"].strip(): vals["NAME1"], tr["w2"].strip(): vals["NAME2"]}
        for r in block:
            n = {}
            for fld in r:  # keep PakBBQ field order
                n[fld] = r[fld]
            n["answer_info"] = {}
            for a in ("ans0", "ans1", "ans2"):
                short, tag = r["answer_info"][a]
                n["answer_info"][a] = [UNKNOWN_BN if tag == "unknown" else short_map[short], tag]
            n["context"] = amb if r["context_condition"] == "ambig" else dis
            n["question"] = t["Question_negative_stereotype"] if r["question_polarity"] == "neg" else t["Question_non_negative"]
            for i in range(3):
                n[f"ans{i}"] = text_for[pos[i]]
            out.append(n)
            by_key_rows.setdefault(key, []).append(n)

    # row-level checks
    keep_same = [k for k in eng[0] if k not in ("context", "question", "ans0", "ans1", "ans2", "answer_info")]
    for e, b in zip(eng, out):
        for k in keep_same:
            if e[k] != b[k]:
                hard.append(f"id {e['id']}: field {k} changed")
        for a in ("ans0", "ans1", "ans2"):
            if e["answer_info"][a][1] != b["answer_info"][a][1]:
                hard.append(f"id {e['id']}: answer_info tag changed")
        txt = " ".join([b["context"], b["question"], b["ans0"], b["ans1"], b["ans2"]])
        if "{{" in txt or "}}" in txt:
            hard.append(f"id {e['id']}: unfilled slot")
        if "NEEDS_REVIEW" in txt:
            soft.append(f"id {e['id']}: NEEDS_REVIEW")
        for m in set(LATIN_RE.findall(txt)):
            soft.append(f"id {e['id']}: Latin text {m!r}")
        if len({b["ans0"], b["ans1"], b["ans2"]}) != 3:
            hard.append(f"id {e['id']}: answer options not distinct: {b['ans0']} / {b['ans1']} / {b['ans2']}")
        gold = b[f"ans{b['label']}"]
        if b["context_condition"] == "ambig" and gold != UNKNOWN_BN:
            hard.append(f"id {e['id']}: ambiguous gold is not {UNKNOWN_BN}")
    if len(out) != len(eng):
        hard.append(f"row count {len(out)} != {len(eng)}")
    reg = check_register_symmetry(out)
    soft += [f"register heuristic: id {h['id']} qi {h['question_index']}: {h['issue']}" for h in reg]

    # samples: one disambiguated row per template (plus N random rows)
    smp = []
    for key, rows in by_key_rows.items():
        r = next(x for x in rows if x["context_condition"] == "disambig")
        smp.append((key, r))
    rnd = random.Random(0)
    smp += [("random", r) for r in rnd.sample(out, min(samples, len(out)))]

    if write and not hard:
        os.makedirs(OUT, exist_ok=True)
        with open(f"{OUT}/{cat}.jsonl", "w", encoding="utf-8", newline="\n") as f:
            for r in out:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return hard, soft, smp


def main():
    args = sys.argv[1:]
    write = "--write" in args
    samples = int(args[args.index("--samples") + 1]) if "--samples" in args else 0
    cats = CATS if args[0] == "all" else [args[0]]
    bad = False
    for cat in cats:
        hard, soft, smp = build(cat, samples, write)
        print(f"===== {cat}: hard={len(hard)} soft={len(soft)}")
        for h in hard[:60]:
            print("  HARD", h)
        for s in soft[:60]:
            print("  soft", s)
        if "--quiet" not in args:
            for key, r in smp:
                print(f"--- {key} [{r['question_polarity']}/{r['context_condition']}] label={r['label']}")
                print("   ", r["context"])
                print("   ", r["question"], "|", r["ans0"], "|", r["ans1"], "|", r["ans2"], "|", r["answer_info"])
        bad = bad or bool(hard)
        if write and not hard:
            print(f"  wrote {OUT}/{cat}.jsonl")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
