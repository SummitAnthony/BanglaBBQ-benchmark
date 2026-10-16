#!/usr/bin/env python3
"""Build evaluation/notebooks/banglabbq_kaggle_upload.zip: the data files and evaluation code the
Kaggle notebook looks for (it finds them by file name anywhere under /kaggle/input).

Usage (from the repo root):  python evaluation/notebooks/make_kaggle_upload.py
"""
import os, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FILES = [
    "data/banglabbq_en.jsonl",               # NA categories (DATASET = "na")
    "data/banglabbq_bn.jsonl",
    "evaluation/dt_tm/banglabbq_dt_tm_sample_eng.jsonl",    # BBQ DT/TM sample (DATASET = "dt_tm")
    "evaluation/dt_tm/banglabbq_dt_tm_sample_bng.jsonl",
    "data/banglabbq_vb_en.jsonl",       # version B disambiguated rows (DATASET = "vb")
    "data/banglabbq_vb_bn.jsonl",
    "evaluation/eval_banglabbq.py",
    "evaluation/score_banglabbq.py",
    "data/template_map.csv",
]

out = os.path.join(HERE, "banglabbq_kaggle_upload.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in FILES:
        z.write(os.path.join(ROOT, p), os.path.basename(p))
print(f"wrote {out} ({os.path.getsize(out) / 1e6:.1f} MB): " + ", ".join(os.path.basename(p) for p in FILES))
