"""Usage: python build_trace.py <BBQ templates dir> <build dir>

Mirror of build.sh that keeps the prepared templates and writes a per-block trace aligned with the final rows."""
import json, os, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)  # pipeline/
BBQ, OUT = sys.argv[1], sys.argv[2]
W = os.path.join(OUT, "_work")
shutil.rmtree(W, ignore_errors=True)
os.makedirs(f"{W}/split", exist_ok=True)
PY = sys.executable
def run(*a):
    subprocess.run([PY, *a], check=True, stdout=subprocess.DEVNULL)
GROUPS = ["Age,Disability_status", "Physical_appearance", "SES", "Gender_identity", "Religion"]
for T in ("DT", "TM", "TM_NAMES"):
    os.makedirs(f"{OUT}/tpl_{T}", exist_ok=True)
    run(f"{P}/prepare_templates.py", BBQ, f"{OUT}/tpl_{T}", T)
    for G in (GROUPS if T != "TM_NAMES" else ["SES"]):
        os.makedirs(f"{W}/raw_{T}_{G}", exist_ok=True)
        run(f"{HERE}/generate_bbq_trace.py", f"{OUT}/tpl_{T}", f"{W}/raw_{T}_{G}", G)
F = f"{P}/finalize.py"
run(F, f"{W}/raw_DT_Age,Disability_status", f"{W}/split", "DT")
run(F, f"{W}/raw_TM_Age,Disability_status", f"{W}/split", "TM", "Age=15,Disability_status=21")
for cat, start in [("Physical_appearance", 16), ("SES", 11), ("Gender_identity", 14), ("Religion", 5)]:
    run(F, f"{W}/raw_DT_{cat}", f"{W}/split", "DT", "", cat)
    run(F, f"{W}/raw_TM_{cat}", f"{W}/split", "TM", f"{cat}={start}", cat)
os.makedirs(f"{W}/fin_S8", exist_ok=True)
run(F, f"{W}/raw_TM_NAMES_SES", f"{W}/fin_S8", "TM", "SES=24", "SES")
run(f"{P}/append_tm.py", f"{W}/split/SES_TM_eng.jsonl", f"{W}/fin_S8/SES_TM_eng.jsonl")
os.makedirs(f"{OUT}/eng", exist_ok=True)
run(f"{P}/merge_categories.py", f"{W}/split", f"{OUT}/eng")
# trace, in final row order: DT blocks, TM blocks, then (SES) the S8 blocks
def grp(cat):
    return "Age,Disability_status" if cat in ("Age", "Disability_status") else cat
os.makedirs(f"{OUT}/trace", exist_ok=True)
for cat in ["Age", "Disability_status", "Physical_appearance", "SES", "Gender_identity", "Religion"]:
    tr = []
    for T in ("DT", "TM", "TM_NAMES"):
        p = f"{W}/raw_{T}_{grp(cat)}/{cat}.trace.jsonl"
        if os.path.exists(p):
            for l in open(p):
                d = json.loads(l); d["set"] = T; tr.append(d)
    with open(f"{OUT}/trace/{cat}.trace.jsonl", "w", encoding="utf-8") as f:
        for d in tr:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(cat, "blocks", len(tr))
