#!/usr/bin/env python3
"""Consistency checks on the released files. Standard library only; run from the repository root:

    python construction/check_data.py            all checks
    python construction/check_data.py --quick    skip the model-output files (the slowest check)

Checks
  templates   data/templates.jsonl: 466 templates, counts per category, required fields, distinct ids,
              distinct questions, no duplicated context, version B sentence differs from version A
  records     the four record files in data/ are exactly the compiled templates (compile_records.py) and
              have the BBQ invariants (8 records per template, ambiguous -> Unknown, labels 2:3:3,
              English and Bangla aligned; version B answers are the opposite group of version A)
  validation  data/validated_templates.csv, the keep lists and the validation block of the templates agree;
              data/validated/ holds exactly the validated templates
  privacy     no e-mail address and no local file path in any text file of the release; no annotator-level
              field (annotator, completed_by, lead_time, notes, created_at, ...) as a key or column of any
              JSON, JSONL or CSV file
  results     every model-output file covers its data file completely (each record x 3 option orders, once);
              every call's `order` is the cyclic rotation of its `perm`, its `category` and `question_index`
              match the record, and re-parsing `raw` with eval_banglabbq.parse_answer gives the stored `pred`

The script exits with status 1 if any check fails.
"""
import argparse, csv, glob, json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_records  # noqa: E402

EXPECTED = {"Marital_status": 100, "Educational_background": 95, "Regional_origin": 100,
            "Mental_health_status": 71, "Age_political_perception": 100}
TEXT = ["ambiguous_context", "disambig_sentence", "negative_question", "nonnegative_question",
        "target_answer", "nontarget_answer", "target_short", "nontarget_short"]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+")
LOCAL_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:(?:\\\\|\\|/)(?=[A-Z0-9_])|/(?:home|Users)/[A-Za-z]")
ANNOTATOR_FIELDS = {"annotator", "annotator_id", "completed_by", "pseudonym", "lead_time", "lead_time_s", "notes",
                    "created_at", "updated_at", "annotation_id", "first_assumed_group", "seq"}
TEXT_EXT = (".md", ".py", ".txt", ".csv", ".xml", ".ipynb", ".json", ".jsonl", ".sh")
FAILED = []


def report(name, problems):
    print(f"[{'FAIL' if problems else 'ok':4}] {name}")
    for p in list(problems)[:15]:
        print("        ", p)
    if problems:
        FAILED.append(name)


def jl(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def rcsv(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def check_templates(T):
    p = []
    c = Counter(t["category"] for t in T)
    if dict(c) != EXPECTED:
        p.append(f"templates per category {dict(c)} != {EXPECTED}")
    if len({t["template_id"] for t in T}) != len(T):
        p.append("duplicate template_id")
    for t in T:
        for k in ("template_id", "category", "subcategory", "question_index", "example_ids", "target_label",
                  "nontarget_label", "stereotyped_groups", "source", "source_quote", "en", "bn", "version_b", "validation"):
            if k not in t or t[k] in ("", None, []):
                p.append(f"{t.get('template_id')}: missing {k}")
        for lang in ("en", "bn"):
            for k in TEXT:
                if not t[lang].get(k, "").strip():
                    p.append(f"{t['template_id']} {lang}: empty {k}")
            if t[lang]["negative_question"] == t[lang]["nonnegative_question"]:
                p.append(f"{t['template_id']} {lang}: identical questions")
            if t["version_b"][lang]["disambig_sentence"] == t[lang]["disambig_sentence"]:
                p.append(f"{t['template_id']} {lang}: version B sentence equals version A")
        if not t["source"].startswith("http"):
            p.append(f"{t['template_id']}: source is not a URL")
    for lang in ("en", "bn"):
        ctx = Counter(t[lang]["ambiguous_context"] for t in T)
        p += [f"{lang}: duplicated ambiguous context: {k[:60]}" for k, v in ctx.items() if v > 1]
    report("templates", p)


def check_records(T):
    p = []
    for (version, lang), rel in compile_records.OUT.items():
        disk = jl(rel)
        comp = compile_records.compile_language(T, lang, version)
        if disk != comp:
            bad = next((i for i, (a, b) in enumerate(zip(disk, comp)) if a != b), min(len(disk), len(comp)))
            p.append(f"{rel}: differs from the compiled templates (first at row {bad}; {len(disk)} vs {len(comp)} rows)")
            continue
        per = defaultdict(list)
        for r in disk:
            per[(r["category"], r["question_index"])].append(r)
        n = 8 if version == "a" else 4
        for k, rs in per.items():
            if len(rs) != n:
                p.append(f"{rel} {k}: {len(rs)} records")
            unk = [r for r in rs if r["context_condition"] == "ambig"]
            if any(r["answer_info"][f"ans{r['label']}"][1] != "unknown" for r in unk):
                p.append(f"{rel} {k}: ambiguous record not answered Unknown")
            if version == "a" and sorted(Counter(r["label"] for r in rs).values()) != [2, 3, 3]:
                p.append(f"{rel} {k}: label counts {Counter(r['label'] for r in rs)}")
    a = {r["example_id"]: r for r in jl("data/banglabbq_en.jsonl")}
    for r in jl("data/banglabbq_vb_en.jsonl"):
        x = a[r["example_id"] - compile_records.VB_OFFSET]
        tags = lambda rec: rec["answer_info"][f"ans{rec['label']}"][1]
        if tags(r) == tags(x) or tags(r) == "unknown":
            p.append(f"version B {r['example_id']}: correct answer is not the opposite group of version A")
    en, bn = jl("data/banglabbq_en.jsonl"), jl("data/banglabbq_bn.jsonl")
    for x, y in zip(en, bn):
        if (x["example_id"], x["label"], x["question_polarity"], x["context_condition"]) != \
           (y["example_id"], y["label"], y["question_polarity"], y["context_condition"]):
            p.append(f"English and Bangla records not aligned at {x['example_id']}")
            break
    report("records (versions A and B)", p)


def check_validation(T):
    p = []
    rows = {r["template_id"]: r for r in rcsv("data/validated_templates.csv")}
    if len(rows) != len(T):
        p.append(f"validated_templates.csv has {len(rows)} rows")
    for t in T:
        r, v = rows[t["template_id"]], t["validation"]
        if int(r["validated"]) != v["validated"] or int(r["version_b_usable"]) != t["version_b"]["usable"]:
            p.append(f"{t['template_id']}: csv and templates.jsonl disagree")
        for lang in ("en", "bn"):
            tv, nv, cv = v[lang]["votes_target_nontarget_cant_tell"]
            if [int(r[f"{lang}_target"]), int(r[f"{lang}_nontarget"]), int(r[f"{lang}_cant_tell"])] != [tv, nv, cv]:
                p.append(f"{t['template_id']} {lang}: vote counts disagree")
    lists = {"data/keep_validated.csv": lambda r: r["validated"] == "1",
             "data/keep_rejected.csv": lambda r: r["validated"] == "0",
             "data/keep_vb.csv": lambda r: r["version_b_usable"] == "1",
             "data/keep_final.csv": lambda r: r["in_final_set"] == "1"}
    for rel, f in lists.items():
        ids = sorted(r["template_id"] for r in rcsv(rel))
        if ids != sorted(k for k, r in rows.items() if f(r)):
            p.append(f"{rel} disagrees with validated_templates.csv")
    tmap = {(r["category"], r["question_index"]): r["template_id"] for r in rcsv("data/template_map.csv")}
    for rel, full, col in (("data/validated/banglabbq_en.jsonl", "data/banglabbq_en.jsonl", "validated"),
                           ("data/validated/banglabbq_bn.jsonl", "data/banglabbq_bn.jsonl", "validated"),
                           ("data/validated/banglabbq_vb_en.jsonl", "data/banglabbq_vb_en.jsonl", "in_final_set"),
                           ("data/validated/banglabbq_vb_bn.jsonl", "data/banglabbq_vb_bn.jsonl", "in_final_set")):
        exp = [r for r in jl(full) if rows[tmap[(r["category"], r["question_index"])]][col] == "1"]
        if jl(rel) != exp:
            p.append(f"{rel} is not the {col} subset of {full}")
    report("validation outcome", p)


def check_privacy():
    p = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in files:
            if not fn.endswith(TEXT_EXT):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, ROOT)
            with open(fp, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if "@" in line and EMAIL.search(line):
                        p.append(f"{rel}:{i}: e-mail address")
                    if LOCAL_PATH.search(line):
                        p.append(f"{rel}:{i}: local file path")
                    if fn.endswith(".jsonl") and i == 1:          # every row of a file has the same keys
                        bad = ANNOTATOR_FIELDS & set(json.loads(line))
                        if bad:
                            p.append(f"{rel}: annotator-level field {sorted(bad)}")
            if fn.endswith(".csv"):
                with open(fp, encoding="utf-8-sig") as f:
                    bad = ANNOTATOR_FIELDS & {c.strip().lower() for c in next(csv.reader(f), [])}
                if bad:
                    p.append(f"{rel}: annotator-level column {sorted(bad)}")
    report("privacy", p)


def check_results():
    sys.path.insert(0, os.path.join(ROOT, "evaluation"))
    import eval_banglabbq as E
    p = []
    data = {"results": {"en": "data/banglabbq_en.jsonl", "bn": "data/banglabbq_bn.jsonl"},
            "results_vb": {"en": "data/banglabbq_vb_en.jsonl", "bn": "data/banglabbq_vb_bn.jsonl"},
            "results_dt_tm": {"en": "evaluation/dt_tm/banglabbq_dt_tm_sample_eng.jsonl",
                              "bn": "evaluation/dt_tm/banglabbq_dt_tm_sample_bng.jsonl"}}
    recs = {d: {lang: {r["example_id"]: r for r in jl(rel)} for lang, rel in m.items()} for d, m in data.items()}
    ids = {d: {lang: set(m) for lang, m in x.items()} for d, x in recs.items()}
    n_files = n_calls = 0
    for d in data:
        for fp in sorted(glob.glob(os.path.join(ROOT, "evaluation", d, "*.jsonl"))):
            n_files += 1
            runs = defaultdict(Counter)
            wrong = Counter()
            for line in open(fp, encoding="utf-8"):
                j = json.loads(line)
                n_calls += 1
                runs[(j["model"], j["lang"], j["prompt_id"])][(j["example_id"], j["perm"])] += 1
                rec = recs[d][j["lang"]].get(j["example_id"])
                if rec is None:
                    wrong["example_id not in the data file"] += 1
                    continue
                if j["order"] != E.rotation(j["perm"]):
                    wrong["order is not the rotation of perm"] += 1
                if (j["category"], str(j["question_index"])) != (rec["category"], str(rec["question_index"])):
                    wrong["category/question_index differ from the record"] += 1
                if E.parse_answer(j["raw"], rec, j["order"]) != j["pred"]:
                    wrong["re-parsing raw does not give pred"] += 1
            p += [f"{d}/{os.path.basename(fp)}: {n} calls: {k}" for k, n in wrong.items()]
            for (m, lang, pid), c in runs.items():
                exp = {(e, k) for e in ids[d][lang] for k in range(3)}
                if set(c) != exp or any(v != 1 for v in c.values()):
                    p.append(f"{d}/{os.path.basename(fp)} {m} {lang} p{pid}: {len(c)} of {len(exp)} (record, order) pairs, "
                             f"{sum(v > 1 for v in c.values())} duplicated")
    report(f"model outputs ({n_files} files, {n_calls:,} calls; raw answers re-parsed)", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(os.path.join(ROOT, "data", "templates.jsonl")):
        sys.exit("data/templates.jsonl not found. Run this from a complete clone of the repository "
                 "(https://github.com/SummitAnthony/BanglaBBQ-benchmark).")
    T = jl("data/templates.jsonl")
    check_templates(T)
    check_records(T)
    check_validation(T)
    check_privacy()
    if not a.quick:
        check_results()
    print("\nall checks passed" if not FAILED else f"\nFAILED: {', '.join(FAILED)}")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
