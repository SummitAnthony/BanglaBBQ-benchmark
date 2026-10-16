#!/usr/bin/env python3
"""Regenerate every evaluation report of the paper from the raw model outputs.

    python reproduce.py            rewrite evaluation/reports/<name>/ (from the repository root)
    python reproduce.py --check    write to a temporary folder and compare, file by file, with the
                                   reports in evaluation/reports/ (exit 1 if any file differs; the
                                   temporary folder is deleted if all files are identical, otherwise
                                   kept and its path printed)

Standard library only, no model calls, a few minutes. Writes
evaluation/reports/<name>/{report.md, scores_by_prompt.csv, scores_summary.csv}:

  final               main results (paper Tables 4 and 5): versions A and B, prompt wording 1, the 360
                      templates that passed human validation and have a usable version B item
                      (data/keep_final.csv)
  final_version_a     the same 360 templates, version A alone (paper Table 9, version A columns)
  final_version_b     the same 360 templates, version B alone (paper Table 9, version B columns)
  validated_a         version A, wording 1, the 372 validated templates (data/keep_validated.csv;
                      paper Table 7, "Valid." columns)
  rejected_a          version A, wording 1, the 94 templates that did not pass validation (paper
                      Table 7, "Rej." columns)
  wordings_validated  version A, all prompt wordings, the 372 validated templates (paper Table 8); the
                      failed Qwen3-8B English wording-3 run is excluded, as in the paper
  dt_tm               BBQ templates adapted to Bangladesh (bbq_dt_tm/), balanced evaluation sample
                      (paper Tables 6 and 10)

Each report scores the released result files listed below by name, so result files that you add to
evaluation/results*/ do not change the paper's reports. The reports shipped in evaluation/reports/ were
produced by this script; re-running it gives the same files byte for byte on any operating system (the
bootstrap uses a fixed seed, and all files are written with LF line endings). Prompt wordings are
numbered 0-2 in the files (`prompt_id`) and 1-3 in the paper.
"""
import argparse, filecmp, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SCORE = os.path.join("evaluation", "score_banglabbq.py")
A = {"en": "data/banglabbq_en.jsonl", "bn": "data/banglabbq_bn.jsonl"}
B = {"en": "data/banglabbq_vb_en.jsonl", "bn": "data/banglabbq_vb_bn.jsonl"}
DT = {"en": "evaluation/dt_tm/banglabbq_dt_tm_sample_eng.jsonl", "bn": "evaluation/dt_tm/banglabbq_dt_tm_sample_bng.jsonl"}

# the released result files (model__lang__tag.jsonl)
MODELS = ["Qwen_Qwen3-4B", "Qwen_Qwen3-8B", "google_gemini-2.5-flash", "openai_gpt-4.1-mini"]
P0 = [f"evaluation/results/{m}__{l}__p0_k3.jsonl" for m in MODELS for l in ("en", "bn")]
P12 = [f"evaluation/results/{m}__{l}__p12_k3.jsonl" for m in MODELS[1:] for l in ("en", "bn")]   # not Qwen3-4B
VB = [f"evaluation/results_vb/{m}__{l}__p0_k3.jsonl" for m in MODELS for l in ("en", "bn")]
DTTM = [f"evaluation/results_dt_tm/{m}__{l}__p0_k3.jsonl" for m in MODELS[:2] for l in ("en", "bn")]

# Qwen3-8B English with wording 3 (prompt_id 2) failed: 57% of the items on the 372 validated templates
# have no valid majority answer (45.8% of its calls on all 466 templates are out-of-choice). The paper
# excludes it (Table 8), and so does the prompt-wording report.
FAILED = ["Qwen/Qwen3-8B:en:2"]

# name: (result files, --data-en, --data-bn, --keep, extra scorer arguments)
RUNS = {
    "final": (P0 + VB, f"{A['en']},{B['en']}", f"{A['bn']},{B['bn']}", "data/keep_final.csv", []),
    "final_version_a": (P0, A["en"], A["bn"], "data/keep_final.csv", []),
    "final_version_b": (VB, B["en"], B["bn"], "data/keep_final.csv", []),
    "validated_a": (P0, A["en"], A["bn"], "data/keep_validated.csv", []),
    "rejected_a": (P0, A["en"], A["bn"], "data/keep_rejected.csv", []),
    "wordings_validated": (P0 + P12, A["en"], A["bn"], "data/keep_validated.csv",
                           [x for f in FAILED for x in ("--exclude", f)]),
    "dt_tm": (DTTM, DT["en"], DT["bn"], None, []),
}
FILES = ("report.md", "scores_by_prompt.csv", "scores_summary.csv")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with evaluation/reports/ instead of overwriting it")
    a = ap.parse_args()
    needed = sorted({p for files, en, bn, keep, extra in RUNS.values() for p in files + en.split(",") + bn.split(",") + [keep or A["en"]]})
    missing = [p for p in needed if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        sys.exit(f"{len(missing)} input files missing, e.g. {missing[0]}. Run this from a complete clone of the "
                 "repository (https://github.com/SummitAnthony/BanglaBBQ-benchmark).")
    out_root = tempfile.mkdtemp(prefix="banglabbq_reports_") if a.check else os.path.join(ROOT, "evaluation", "reports")
    differ = []
    for name, (files, en, bn, keep, extra) in RUNS.items():
        out = os.path.join(out_root, name)
        cmd = [sys.executable, SCORE, *files, "--data-en", en, "--data-bn", bn, "--out", out, *extra]
        if keep:
            cmd += ["--keep", keep]
        print(f"=== {name}", flush=True)
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:])
            sys.exit(f"{name} failed")
        print("\n".join(l.replace("·", "|") for l in r.stdout.splitlines() if l.startswith("Result files")))
        if a.check:
            for fn in FILES:
                shipped = os.path.join(ROOT, "evaluation", "reports", name, fn)
                same = os.path.exists(shipped) and filecmp.cmp(os.path.join(out, fn), shipped, shallow=False)
                print(f"  {name}/{fn}: {'identical' if same else 'DIFFERS'} (byte for byte)")
                if not same:
                    differ.append(f"{name}/{fn}")
    if a.check:
        if differ:
            print(f"{len(differ)} files differ: {', '.join(differ)}")
            print(f"(regenerated reports left in {out_root})")
            sys.exit(1)
        shutil.rmtree(out_root, ignore_errors=True)
        print("all report files identical to evaluation/reports/")
        sys.exit(0)
    print("all reports written to evaluation/reports/")


if __name__ == "__main__":
    main()
