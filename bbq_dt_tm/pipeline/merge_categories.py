"""Merge each category's DT and TM files into one PakBBQ-style file: DT rows, then TM rows,
example_id 0..n-1 through the file, additional_metadata reduced to PakBBQ's four keys.
`id` is set equal to example_id here; assign_ids.py gives the benchmark-wide id at the final merge.

Usage: python merge_categories.py <folder with <Cat>_DT_eng.jsonl / <Cat>_TM_eng.jsonl> <output folder>
"""
import glob, json, os, sys

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
META = ["subcategory", "stereotyped_groups", "version", "source"]
cats = sorted({os.path.basename(f).rsplit("_", 2)[0] for f in glob.glob(f"{SRC}/*_DT_eng.jsonl")})
for cat in cats:
    rows = []
    for t in ("DT", "TM"):
        p = f"{SRC}/{cat}_{t}_eng.jsonl"
        if os.path.exists(p):
            rows += [json.loads(l) for l in open(p)]
    with open(f"{OUT}/{cat}.jsonl", "w") as f:
        for i, r in enumerate(rows):
            r["example_id"] = r["id"] = i
            r["additional_metadata"] = {k: r["additional_metadata"][k] for k in META}
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{cat}.jsonl: {len(rows)} rows")
