"""Give every row a benchmark-wide `id`, as PakBBQ does: one running number across all category
files in alphabetical order of file name, while example_id keeps counting within each file.
Run once, on the final English folder (NA + DT + TM categories). The Bangla folder must use the
same ids, so run it on both folders with the same file set.

Usage: python assign_ids.py <folder with one <Category>.jsonl per category>
"""
import glob, json, os, sys

n = 0
for path in sorted(glob.glob(os.path.join(sys.argv[1], "*.jsonl"))):
    rows = [json.loads(l) for l in open(path)]
    for r in rows:
        r["id"] = n
        n += 1
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{os.path.basename(path)}: id {rows[0]['id']}..{rows[-1]['id']}")
