#!/usr/bin/env python3
# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Validator (CLAUDE.md §4.3). Merges seed + author files, checks schema/labels/
biased-direction/dedup, and verifies each source is live + its source_quote is
verbatim on the page (via source_tool's curl fetch). Writes validated.jsonl +
reports/validation_report.md.

Usage: python scripts/validate.py templates/existing_seed.jsonl templates/author_a.jsonl [more...]
"""
import sys, os, json, re
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

def structural(t):
    """Return (failures, warnings). failures disqualify; warnings are advisory."""
    f, w = [], []
    if "_parse_error" in t:
        return [f"JSON parse error: {t['_parse_error']}"], w
    for k in REQUIRED:
        if k not in t or (isinstance(t[k], str) and not t[k].strip()):
            f.append(f"missing/empty field: {k}")
    if f:
        return f, w
    if t["category"] != "Marital_status":
        f.append(f"category != Marital_status ({t['category']})")
    if t["nontarget_label"] != expected_nonlabel(t["target_label"]):
        f.append(f"label convention: nontarget_label '{t['nontarget_label']}' != expected '{expected_nonlabel(t['target_label'])}'")
    if t["target_group"] != t["target_short"] or t["nontarget_group"] != t["nontarget_short"]:
        f.append("target_group/short (or nontarget) mismatch")
    if not isinstance(t["stereotyped_groups"], list) or not t["stereotyped_groups"]:
        f.append("stereotyped_groups must be a non-empty list")
    # biased-direction: prefer full descriptor; else head noun; else WARN (semantic, not fatal)
    ds = t["disambig_sentence"].lower()
    head = t["target_short"].lower().split()[-1]
    if t["target_short"].lower() not in ds and head not in ds:
        w.append("biased-direction: target descriptor not literally in disambig_sentence (verify manually)")
    # questions are a proper distinct pair
    if t["negative_question"].strip() == t["nonnegative_question"].strip():
        f.append("negative_question == nonnegative_question")
    # answer leakage: a group descriptor should not appear in the questions
    for q in (t["negative_question"], t["nonnegative_question"]):
        if t["target_short"].lower() in q.lower() or t["nontarget_short"].lower() in q.lower():
            f.append(f"question leaks a group name: {q!r}")
            break
    # placeholder leakage
    blob = " ".join([t["ambiguous_context"], t["disambig_sentence"], t["negative_question"],
                     t["nonnegative_question"], t["target_answer"], t["nontarget_answer"]])
    if "{{" in blob or "TODO" in blob:
        f.append("placeholder/TODO leakage")
    return f, w

def dedup_flags(T):
    """Flag near-duplicate scenarios: same target_label+subcategory with overlapping context opening."""
    flags = {}
    seen = {}
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
        # exact ambiguous_context duplicate anywhere
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
    paths = sys.argv[1:]
    T = load_all(paths)
    dups = dedup_flags(T)
    # template_id uniqueness
    id_seen = {}
    id_dupe = {}
    for t in T:
        tid = t.get("template_id")
        if tid in id_seen:
            id_dupe[tid] = True
        else:
            id_seen[tid] = True

    src_cache = {}
    results = []
    for t in T:
        tid = t.get("template_id", f"{t['_file']}:{t['_line']}")
        sf, sw = structural(t)
        if tid in id_dupe:
            sf.append("duplicate template_id")
        # source check (only if structural fields present)
        src_status = "SKIPPED"
        if not any(x.startswith("missing/empty field: source") for x in sf) and "source" in t and "source_quote" in t:
            url = t["source"]
            if url not in src_cache:
                src_cache[url] = st.fetch(url)
            code, text = src_cache[url]
            if code != "200":
                src_status = f"DEAD/BLOCKED (HTTP {code})"
                sf.append(src_status)
            elif st.norm(t["source_quote"]).lower() not in text.lower():
                src_status = "QUOTE-NOT-VERBATIM"
                sf.append(src_status)
            else:
                src_status = "OK"
        dup = dups.get(tid)
        results.append((t, sf, sw, src_status, dup))

    passing = [t for (t, sf, sw, ss, dup) in results if not sf]
    # write outputs
    os.makedirs("reports", exist_ok=True)
    with open("templates/validated.jsonl", "w", encoding="utf-8") as f:
        for t in passing:
            o = {k: v for k, v in t.items() if not k.startswith("_")}
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    lines = []
    lines.append("# BanglaBBQ Marital_status — Validation Report\n")
    lines.append(f"- Templates examined: **{len(T)}**")
    lines.append(f"- **PASS: {len(passing)}**  |  FAIL: {len(T)-len(passing)}")
    from collections import Counter
    dom = Counter()
    for t in passing:
        try:
            dom[st.norm(t['source']).split('/')[2].replace('www.','')] += 1
        except Exception:
            pass
    lines.append(f"- Passing source domains: {dict(dom)}")
    lines.append(f"- Dedup flags: {len(dups)}\n")
    nwarn = sum(1 for r in results if r[2])
    lines.append(f"- Advisory warnings (non-blocking): {nwarn}\n")
    lines.append("## Per-template results\n")
    for (t, sf, sw, ss, dup) in sorted(results, key=lambda r: r[0].get("template_id","zzz")):
        tid = t.get("template_id", f"{t['_file']}:{t['_line']}")
        warn = f"  ⚠️ {'; '.join(sw)}" if sw else ""
        if not sf:
            note = f"  _(dedup: {dup})_" if dup else ""
            lines.append(f"- ✅ **{tid}** [{t.get('subcategory','?')} / {t.get('target_label','?')}] source={ss}{note}{warn}")
        else:
            lines.append(f"- ❌ **{tid}** — {'; '.join(sf)}" + (f"  _(dedup: {dup})_" if dup else "") + warn)
    open("reports/validation_report.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"Validated {len(T)} templates: {len(passing)} pass, {len(T)-len(passing)} fail.")
    print("-> templates/validated.jsonl, reports/validation_report.md")
    if dups:
        print(f"Dedup flags on: {list(dups)}")

if __name__ == "__main__":
    main()
