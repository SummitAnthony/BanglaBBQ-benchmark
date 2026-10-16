# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""Step 6: refresh the combined English file (scripts/build_combined.py's SOURCES was
missing Mental_health_status) and build the analogous combined Bangla file, once all
five per-category Bangla files exist. Writes new files only -- never overwrites
output/banglabbq_eng_combined.jsonl in place.
"""
import json

ENG_SOURCES = [
    "output/banglabbq_marital_eng.jsonl",
    "output/banglabbq_age_politics_eng.jsonl",
    "educational_background/output/banglabbq_educational_eng.jsonl",
    "regional bias outputs/banglabbq_region_eng.jsonl",
    "output/banglabbq_mental_health_eng.jsonl",
]
BNG_SOURCES = [
    "output/banglabbq_marital_bng_v2.jsonl",
    "output/banglabbq_age_politics_bng_v2.jsonl",
    "output/banglabbq_educational_bng_v2.jsonl",
    "output/banglabbq_region_bng_v2.jsonl",
    "output/banglabbq_mental_health_bng_v2.jsonl",
]
ENG_OUT = "output/banglabbq_eng_combined_v2.jsonl"
BNG_OUT = "output/banglabbq_bng_combined.jsonl"


def build_combined(sources, out_path):
    rows, gid = [], 0
    for path in sources:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                r["example_id"] = gid
                r["id"] = gid
                gid += 1
                rows.append(r)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def main():
    n_eng = build_combined(ENG_SOURCES, ENG_OUT)
    print(f"wrote {n_eng} records -> {ENG_OUT}")
    n_bng = build_combined(BNG_SOURCES, BNG_OUT)
    print(f"wrote {n_bng} records -> {BNG_OUT}")


if __name__ == "__main__":
    main()
