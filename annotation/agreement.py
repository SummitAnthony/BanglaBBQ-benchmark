#!/usr/bin/env python3
"""Recompute the agreement statistics of annotation/agreement.md from the released vote counts.

    python annotation/agreement.py           print the table
    python annotation/agreement.py --check   also compare it with annotation/agreement.md (exit 1 on a difference)

Standard library only; run from the repository root. Input: data/validated_templates.csv (per template and
language, the number of annotators who chose the intended target, the other group and "Can't tell").
The letter coding needs annotation/make_tasks.py (flip(): which letter showed the target).

Statistics per project (category x language):
  AC1 target  Gwet's multi-rater AC1 over three categories coded relative to the template:
              intended target / other group / Can't tell; 95% percentile bootstrap interval over
              templates (2,000 resamples, seed 0)
  AC1 raw     the same coefficient over the three options as displayed: A / B / Can't tell
  Fleiss      Fleiss' kappa over the target / other / Can't tell coding, computed over the templates
              that have the full number of answers (Age_political_perception, Bangla: the 99 templates
              with three answers; APO-067 has two)
  Unanimous   templates on which all answers agree;  % target  share of answers naming the intended target

The point estimates and the bootstrap intervals equal those in agreement.md and in Table 1 of the paper.
The bootstrap draws the templates of each project in template_id order, which reproduces the intervals of
the development script exactly (that script drew them in the order of the annotation exports).
"""
import argparse, csv, os, random, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "annotation"))
from make_tasks import flip  # noqa: E402  (make_tasks also sets stdout to UTF-8)

CATS = ["Marital_status", "Age_political_perception", "Regional_origin", "Educational_background", "Mental_health_status"]  # order of paper Table 1
JUDGED = ["target", "nontarget", "cant_tell"]
BOOT = 2000


def gwet_ac1(units, cats):
    units = [u for u in units if len(u) >= 2]
    pa = sum(sum(v * (v - 1) for v in Counter(u).values()) / (len(u) * (len(u) - 1)) for u in units) / len(units)
    pi = {k: sum(u.count(k) / len(u) for u in units) / len(units) for k in cats}
    pe = sum(p * (1 - p) for p in pi.values()) / (len(cats) - 1)
    return (pa - pe) / (1 - pe)


def fleiss_kappa(units, cats):
    n, N = len(units[0]), len(units)
    pj = [sum(u.count(c) for u in units) / (N * n) for c in cats]
    pbar = sum((sum(u.count(c) ** 2 for c in cats) - n) / (n * (n - 1)) for u in units) / N
    pe = sum(p * p for p in pj)
    return 1.0 if pe == 1 else (pbar - pe) / (1 - pe)


def boot_ci(units, cats, seed=0):
    rng = random.Random(seed)
    vals = sorted(gwet_ac1([rng.choice(units) for _ in units], cats) for _ in range(BOOT))
    return vals[int(0.025 * BOOT)], vals[int(0.975 * BOOT) - 1]


def projects():
    with open(os.path.join(ROOT, "data", "validated_templates.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for cat in CATS:
        for lang, tag in (("en", "EN"), ("bn", "BN")):
            judged, raw = [], []
            for r in sorted((r for r in rows if r["category"] == cat), key=lambda r: r["template_id"]):
                u = (["target"] * int(r[f"{lang}_target"]) + ["nontarget"] * int(r[f"{lang}_nontarget"])
                     + ["cant_tell"] * int(r[f"{lang}_cant_tell"]))
                tl, nl = ("B", "A") if flip(r["template_id"]) else ("A", "B")
                judged.append(u)
                raw.append([{"target": tl, "nontarget": nl, "cant_tell": "CT"}[x] for x in u])
            sizes = Counter(len(u) for u in judged)
            nmax = max(sizes)
            lo, hi = boot_ci([u for u in judged if len(u) >= 2], JUDGED)
            out.append({
                "project": f"{cat} ({tag})", "templates": len(judged),
                "per_template": ", ".join(f"{k}×{v}" for k, v in sorted(sizes.items(), reverse=True)),
                "ac1": gwet_ac1(judged, JUDGED), "lo": lo, "hi": hi, "raw": gwet_ac1(raw, ["A", "B", "CT"]),
                "fleiss": fleiss_kappa([u for u in judged if len(u) == nmax], JUDGED),
                "unanimous": sum(len(set(u)) == 1 for u in judged if len(u) >= 2),
                "target": sum(u.count("target") for u in judged) / sum(len(u) for u in judged)})
    return out


def check(out):
    """Compare with the table in annotation/agreement.md; every value, intervals included, must agree to 3 decimals."""
    with open(os.path.join(ROOT, "annotation", "agreement.md"), encoding="utf-8") as f:
        md = f.read()
    rx = re.compile(r"^\| (.+?) \| (\d+) \| \d+ \| (.+?) \| \*\*([\d.]+)\*\* \[([\d.]+), ([\d.]+)\] \| ([\d.]+) \| "
                    r"([\d.]+) \| (\d+) \| ([\d.]+)% \|$", re.M)
    pub = {m.group(1): m.groups() for m in rx.finditer(md)}
    bad = []
    for p in out:
        g = pub.get(p["project"])
        if not g:
            bad.append(f"{p['project']}: not in agreement.md")
            continue
        mine = (p["project"], str(p["templates"]), p["per_template"], f"{p['ac1']:.3f}", f"{p['raw']:.3f}",
                f"{p['fleiss']:.3f}", str(p["unanimous"]), f"{100 * p['target']:.1f}")
        theirs = (g[0], g[1], g[2], g[3], g[6], g[7], g[8], g[9])
        if mine != theirs:
            bad.append(f"{p['project']}: {mine} != {theirs}")
        if f"{p['lo']:.3f}" != g[4] or f"{p['hi']:.3f}" != g[5]:
            bad.append(f"{p['project']}: interval [{p['lo']:.3f}, {p['hi']:.3f}] vs [{g[4]}, {g[5]}]")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with annotation/agreement.md")
    a = ap.parse_args()
    if not os.path.exists(os.path.join(ROOT, "data", "validated_templates.csv")):
        sys.exit("data/validated_templates.csv not found. Run this from a complete clone of the repository "
                 "(https://github.com/SummitAnthony/BanglaBBQ-benchmark).")
    out = projects()
    print("| Project | Templates | Ratings/template | AC1 target [95% CI] | AC1 raw A/B/CT | Fleiss' kappa | Unanimous | % target |")
    print("|---|--:|---|--:|--:|--:|--:|--:|")
    for p in out:
        print(f"| {p['project']} | {p['templates']} | {p['per_template']} | {p['ac1']:.3f} [{p['lo']:.3f}, {p['hi']:.3f}] | "
              f"{p['raw']:.3f} | {p['fleiss']:.3f} | {p['unanimous']} | {100 * p['target']:.1f}% |")
    if a.check:
        bad = check(out)
        for b in bad:
            print("DIFFERS:", b)
        print("agreement.md: " + ("all values reproduced" if not bad else f"{len(bad)} differences"))
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
