"""Append a separately built TM block (e.g. SES 8, built after the name list) to an existing TM file,
continuing example_id and id. Usage: python append_tm.py <existing TM file> <block file>"""
import json, sys
base = [json.loads(l) for l in open(sys.argv[1])]
extra = [json.loads(l) for l in open(sys.argv[2])]
n = len(base)
for i, r in enumerate(extra):
    r["example_id"] = r["id"] = n + i
with open(sys.argv[1], "w") as f:
    for r in base + extra:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{sys.argv[1]}: {len(base)} + {len(extra)} rows")
