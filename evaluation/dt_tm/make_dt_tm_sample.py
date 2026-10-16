#!/usr/bin/env python3
"""Build the balanced evaluation sample of the BBQ DT/TM layer (bbq_dt_tm/), English + Bangla.

The full DT/TM files have 15,328 rows, most of them the same question with different people
filled in (8 to 408 rows per template). Evaluating all of them would take ~4x the GPU time of
the NA pilot, and the templates with the most rows (SES, Gender_identity) would dominate the
scores. This script keeps every template but only a few of its 4-row blocks:

  * per template (category + question_index), take n blocks whose disambiguated answer is
    stereotype-consistent and n that are inconsistent, n = min(2 x number of versions,
    available of each), picked round-robin across versions, seeded -> ~16 rows per version;
  * blocks are kept whole (ambig/neg, disambig/neg, ambig/nonneg, disambig/nonneg), and
    exact duplicate blocks are skipped;
  * blocks where the stereotyped group matches neither or both people are skipped, as in BBQ's
    own analysis: 16 Gender_identity rows that pair two people of the same gender (a man and a
    boy, a girl and a woman), where the gender stereotype cannot apply;
  * the Bangla sample holds the same rows as the English one (BanglaBBQ_BN is row-parallel).

Rows keep every field; example_id and id are renumbered 0..n-1 across the sample (the source
files restart at 0 per category). sample_map.csv links each sample row to its source row.

Usage (from the repo root):
    python evaluation/dt_tm/make_dt_tm_sample.py           rewrite the three files in evaluation/dt_tm/
    python evaluation/dt_tm/make_dt_tm_sample.py --check   build them in memory and compare them with the
                                                           shipped files, without writing (exit 1 if any differs)
"""
import argparse, csv, io, json, os, random, sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = {"en": os.path.join(ROOT, "bbq_dt_tm", "BanglaBBQ_ENG"), "bn": os.path.join(ROOT, "bbq_dt_tm", "BanglaBBQ_BN")}
OUT = {"en": os.path.join(HERE, "banglabbq_dt_tm_sample_eng.jsonl"),
       "bn": os.path.join(HERE, "banglabbq_dt_tm_sample_bng.jsonl")}
CATS = ["Age", "Disability_status", "Gender_identity", "Physical_appearance", "Religion", "SES"]
SEED = 2026
PER_VERSION = 2   # consistent blocks (and as many inconsistent ones) per template version


def bbq_target(rec):
    """Answer index of the stereotyped person, by BBQ's rule: the answer tag (woman/girl -> F,
    man/boy -> M) appears in stereotyped_groups, compared without case and spaces."""
    st = {s.lower().replace(" ", "") for s in rec["additional_metadata"]["stereotyped_groups"]}
    hits = []
    for j in range(3):
        tag = rec["answer_info"][f"ans{j}"][1]
        if tag.lower() == "unknown":
            continue
        g = {"woman": "f", "girl": "f", "man": "m", "boy": "m"}.get(tag.lower(), tag.lower().replace(" ", ""))
        if g in st:
            hits.append(j)
    return hits[0] if len(hits) == 1 else None


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def rel(p):
    """Path relative to the repository root, for printing."""
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="build the sample in memory and compare it with the shipped files, without writing them")
    a = ap.parse_args()
    rnd = random.Random(SEED)
    picked = []                                    # (category, first row index of block)
    skipped = 0
    stats = []
    for cat in CATS:
        en = load(os.path.join(SRC["en"], f"{cat}.jsonl"))
        bn = load(os.path.join(SRC["bn"], f"{cat}.jsonl"))
        assert len(en) == len(bn) and len(en) % 4 == 0
        # blocks per template, by version and direction, skipping exact duplicates
        blocks = defaultdict(lambda: defaultdict(lambda: {True: [], False: []}))
        seen = set()
        for b in range(0, len(en), 4):
            blk = en[b:b + 4]
            assert [(r["context_condition"], r["question_polarity"]) for r in blk] == \
                [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]
            if bbq_target(blk[1]) is None:
                skipped += 4
                continue
            key = json.dumps([[r["context"], r["question"], r["ans0"], r["ans1"], r["ans2"]] for r in blk])
            if key in seen:
                continue
            seen.add(key)
            consistent = blk[1]["label"] == bbq_target(blk[1])      # disambig/neg answer is the target
            blocks[blk[0]["question_index"]][blk[0]["additional_metadata"]["version"]][consistent].append(b)
        for qi in sorted(blocks, key=int):
            vers = blocks[qi]
            for v in vers.values():
                for d in (True, False):
                    rnd.shuffle(v[d])
            n = min(PER_VERSION * len(vers), sum(len(v[True]) for v in vers.values()),
                    sum(len(v[False]) for v in vers.values()))
            chosen = []
            for d in (True, False):
                queues = [list(vers[k][d]) for k in sorted(vers)]
                got = []
                while len(got) < n:                                   # round-robin across versions
                    for q in queues:
                        if q and len(got) < n:
                            got.append(q.pop(0))
                chosen += got
            picked += [(cat, b) for b in sorted(chosen)]
            stats.append((cat, qi, len(vers), n))
    # write both languages from the same picks
    rows_by, texts = {}, {}
    for lang in ("en", "bn"):
        src = {cat: load(os.path.join(SRC[lang], f"{cat}.jsonl")) for cat in CATS}
        out, mp = [], []
        for cat, b in picked:
            for r in src[cat][b:b + 4]:
                r = dict(r)
                mp.append((len(out), cat, r["example_id"]))
                r["example_id"] = r["id"] = len(out)
                out.append(r)
        texts[OUT[lang]] = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out)
        rows_by[lang] = (out, mp)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["example_id", "category", "source_example_id"])
    w.writerows(rows_by["en"][1])
    texts[os.path.join(HERE, "sample_map.csv")] = buf.getvalue()
    if not a.check:
        for p, text in texts.items():
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(text)

    # checks
    en, bn = rows_by["en"][0], rows_by["bn"][0]
    struct = ["question_index", "question_polarity", "context_condition", "category", "label", "type",
              "additional_metadata"]
    assert all(all(a[k] == b[k] for k in struct) for a, b in zip(en, bn)), "English/Bangla samples not parallel"
    bal = defaultdict(Counter)
    for r in en:
        if r["context_condition"] == "disambig":
            t = bbq_target(r)
            bal[(r["category"], r["question_index"])][(r["question_polarity"] == "neg") == (r["label"] == t)] += 1
    unbalanced = {k: dict(v) for k, v in bal.items() if v[True] != v[False]}
    small = [s for s in stats if s[3] < PER_VERSION * s[2]]
    print(f"skipped {skipped} rows whose stereotyped group matches neither or both people")
    print(f"sample: {len(en)} rows ({len(picked)} blocks) from {len(stats)} templates -> {rel(OUT['en'])}, "
          f"{rel(OUT['bn'])}" + (" (not written: --check)" if a.check else ""))
    for cat in CATS:
        print(f"  {cat:20} rows {sum(r['category'] == cat for r in en):5}  templates {sum(s[0] == cat for s in stats)}")
    print("templates with unequal consistent/inconsistent rows:", unbalanced or "none")
    print("templates with fewer blocks than the target (all their unique blocks of one direction used):",
          [f"{c} {q}" for c, q, _, _ in small] or "none")
    if a.check:
        differ = []
        for p, text in texts.items():
            try:
                with open(p, encoding="utf-8", newline="") as f:
                    same = f.read() == text
            except FileNotFoundError:
                same = False
            print(f"  {rel(p)}: {'identical to the shipped file' if same else 'DIFFERS from the shipped file'}")
            if not same:
                differ.append(rel(p))
        sys.exit(1 if differ else 0)


if __name__ == "__main__":
    main()
