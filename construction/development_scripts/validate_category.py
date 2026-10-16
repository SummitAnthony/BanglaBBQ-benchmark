#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Category-parametrized validator — a generalization of validate.py (CLAUDE.md §4.3)
that works for ANY BanglaBBQ category instead of hard-coding Marital_status.

Same checks: schema completeness (18 fields), X/non<X> label convention, biased-direction,
distinct neg/nonneg pair, no group-name leakage, no placeholder/TODO, dedup, template_id
uniqueness, and live-source + verbatim source_quote (via source_tool's curl fetch).

Usage:
  python scripts/validate_category.py --category Mental_health_status \
      --out mental_health/templates/validated.jsonl \
      --report reports/mental_health_validation_report.md \
      mental_health/templates/author_*.jsonl
"""
import sys, os, json, re, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import source_tool as st

REQUIRED = ["template_id","category","subcategory","target_group","nontarget_group",
            "target_label","nontarget_label","stereotyped_groups","target_answer",
            "nontarget_answer","target_short","nontarget_short","ambiguous_context",
            "disambig_sentence","negative_question","nonnegative_question","source","source_quote"]

def load_all(paths):
    T = []
    for p in paths:
        if not os.path.exists(p):
            continue
        for i, l in enumerate(open(p, encoding="utf-8")):
            l = l.strip()
            if not l:
                continue
            try:
                obj = json.loads(l)
                obj["_file"] = os.path.basename(p)
                obj["_line"] = i + 1
                T.append(obj)
            except Exception as e:
                T.append({"_file": os.path.basename(p), "_line": i+1, "_parse_error": str(e)})
    return T

def expected_nonlabel(tl):
    return "non" + tl[:1].upper() + tl[1:]

def structural(t, category):
    f, w = [], []
    if "_parse_error" in t:
        return [f"JSON parse error: {t['_parse_error']}"], w
    for k in REQUIRED:
        if k not in t or (isinstance(t[k], str) and not t[k].strip()):
            f.append(f"missing/empty field: {k}")
    if f:
        return f, w
    if t["category"] != category:
        f.append(f"category != {category} ({t['category']})")
    if t["nontarget_label"] != expected_nonlabel(t["target_label"]):
        f.append(f"label convention: nontarget_label '{t['nontarget_label']}' != expected '{expected_nonlabel(t['target_label'])}'")
    if t["target_group"] != t["target_short"] or t["nontarget_group"] != t["nontarget_short"]:
        f.append("target_group/short (or nontarget) mismatch")
    if not isinstance(t["stereotyped_groups"], list) or not t["stereotyped_groups"]:
        f.append("stereotyped_groups must be a non-empty list")
    ds = t["disambig_sentence"].lower()
    head = t["target_short"].lower().split()[-1]
    if t["target_short"].lower() not in ds and head not in ds:
        w.append("biased-direction: target descriptor not literally in disambig_sentence (verify manually)")
    if t["negative_question"].strip() == t["nonnegative_question"].strip():
        f.append("negative_question == nonnegative_question")
    for q in (t["negative_question"], t["nonnegative_question"]):
        if t["target_short"].lower() in q.lower() or t["nontarget_short"].lower() in q.lower():
            f.append(f"question leaks a group name: {q!r}")
            break
    blob = " ".join([t["ambiguous_context"], t["disambig_sentence"], t["negative_question"],
                     t["nonnegative_question"], t["target_answer"], t["nontarget_answer"]])
    if "{{" in blob or "TODO" in blob:
        f.append("placeholder/TODO leakage")
    return f, w

def dedup_flags(T):
    flags, seen = {}, {}
    for t in T:
        if "_parse_error" in t:
            continue
        key = (t.get("target_label"), t.get("subcategory"))
        opening = " ".join(re.sub(r"[^a-z ]", "", t.get("ambiguous_context","").lower()).split()[:8])
        sig = (key, opening)
        if sig in seen:
            flags[t["template_id"]] = f"near-duplicate of {seen[sig]} (same target/subcat + same opening)"
        else:
            seen[sig] = t["template_id"]
    ctxs = {}
    for t in T:
        if "_parse_error" in t: continue
        c = t.get("ambiguous_context","").strip()
        if c in ctxs:
            flags[t["template_id"]] = f"identical ambiguous_context to {ctxs[c]}"
        else:
            ctxs[c] = t["template_id"]
    return flags

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("inputs", nargs="+")
    a = ap.parse_args()

    T = load_all(a.inputs)
    dups = dedup_flags(T)
    id_seen, id_dupe = {}, {}
    for t in T:
        tid = t.get("template_id")
        if tid in id_seen: id_dupe[tid] = True
        else: id_seen[tid] = True

    src_cache, results = {}, []
    for t in T:
        tid = t.get("template_id", f"{t.get('_file','?')}:{t.get('_line','?')}")
        sf, sw = structural(t, a.category)
        if tid in id_dupe:
            sf.append("duplicate template_id")
        src_status = "SKIPPED"
        if not any(x.startswith("missing/empty field: source") for x in sf) and "source" in t and "source_quote" in t:
            url = t["source"]
            if url not in src_cache:
                src_cache[url] = st.fetch(url)
            code, text = src_cache[url]
            if code != "200":
                src_status = f"DEAD/BLOCKED (HTTP {code})"; sf.append(src_status)
            elif st.norm(t["source_quote"]).lower() not in text.lower():
                src_status = "QUOTE-NOT-VERBATIM"; sf.append(src_status)
            else:
                src_status = "OK"
        results.append((t, sf, sw, src_status, dups.get(tid)))

    passing = [t for (t, sf, sw, ss, dup) in results if not sf]
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for t in passing:
            o = {k: v for k, v in t.items() if not k.startswith("_")}
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    from collections import Counter
    dom = Counter()
    for t in passing:
        try: dom[st.norm(t['source']).split('/')[2].replace('www.','')] += 1
        except Exception: pass
    lines = [f"# BanglaBBQ {a.category} — Validation Report\n",
             f"- Templates examined: **{len(T)}**",
             f"- **PASS: {len(passing)}**  |  FAIL: {len(T)-len(passing)}",
             f"- Passing source domains: {dict(dom)}",
             f"- Dedup flags: {len(dups)}\n",
             f"- Advisory warnings (non-blocking): {sum(1 for r in results if r[2])}\n",
             "## Per-template results\n"]
    for (t, sf, sw, ss, dup) in sorted(results, key=lambda r: r[0].get("template_id","zzz")):
        tid = t.get("template_id", f"{t.get('_file','?')}:{t.get('_line','?')}")
        warn = f"  ⚠️ {'; '.join(sw)}" if sw else ""
        if not sf:
            note = f"  _(dedup: {dup})_" if dup else ""
            lines.append(f"- ✅ **{tid}** [{t.get('subcategory','?')} / {t.get('target_label','?')}] source={ss}{note}{warn}")
        else:
            lines.append(f"- ❌ **{tid}** — {'; '.join(sf)}" + (f"  _(dedup: {dup})_" if dup else "") + warn)
    os.makedirs(os.path.dirname(a.report) or ".", exist_ok=True)
    open(a.report, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"[{a.category}] Validated {len(T)}: {len(passing)} pass, {len(T)-len(passing)} fail.")
    print(f"-> {a.out}, {a.report}")
    if dups: print(f"Dedup flags on: {list(dups)}")

if __name__ == "__main__":
    main()
