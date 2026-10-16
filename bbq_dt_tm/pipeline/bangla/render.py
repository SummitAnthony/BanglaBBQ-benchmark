"""Render BanglaBBQ DT/TM rows from (template, slot fillers) using the generator trace.

The English rows are the structural source of truth: every field except context, question,
ans0-2 and answer_info[*][0] is copied unchanged from the English row. Only the text is rendered
from the (translated) template and fillers.
"""
import json
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import do_slotting  # noqa: E402

FIELDS = ["Ambiguous_Context", "Disambiguating_Context", "Question_negative_stereotype",
          "Question_non_negative", "Answer_negative", "Answer_non_negative"]
SLOTS = ["NAME1", "NAME2", "WORD1", "WORD2"]
CATS = ["Age", "Disability_status", "Gender_identity", "Physical_appearance", "Religion", "SES"]


def load_frames(build, cat):
    out = {}
    for s in ("DT", "TM", "TM_NAMES"):
        p = f"{build}/tpl_{s}/new_templates - {cat}.csv"
        if not os.path.exists(p):
            continue
        df = pd.read_csv(p, na_filter=False)
        df = df[df.Ambiguous_Context != ""].reset_index()
        for i in range(len(df)):
            out[(s, i)] = df.iloc[[i]].reset_index(drop=True)
    return out


def template_key(tr):
    return f"{tr['set']}|{tr['Q_id']}|{tr['version']}|{tr['frame']}"


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def positions(block):
    """Which answer (neg / nonneg / unknown) sits in ans0..ans2, read from the English labels."""
    a_neg, d_neg, a_non, d_non = block
    pos = {a_neg["label"]: "unknown", d_neg["label"]: "neg", d_non["label"]: "nonneg"}
    assert len(pos) == 3 and a_non["label"] == a_neg["label"]
    return [pos[k] for k in range(3)]


def english_render(frame, tr, block):
    """Reproduce the generator's text for one block (used to prove the renderer is faithful)."""
    cols = frame.columns
    lex = frame.Lexical_diversity[0]
    row = do_slotting(frame, cols, tr["w1"], None, tr["w2"], None, lex, tr["r1"], tr["r2"])
    amb = row.Ambiguous_Context[0]
    dis = "%s %s" % (amb.strip(), row.Disambiguating_Context[0])
    dis = re.sub(r"([.!?] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), dis.strip())
    amb = re.sub(r"([.!?] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), amb.strip())
    return amb, dis, row.Question_negative_stereotype[0].strip(), row.Question_non_negative[0].strip(), \
        row.Answer_negative[0], row.Answer_non_negative[0]


def fill(text, vals):
    for s in SLOTS:
        if vals.get(s) is not None:
            text = text.replace("{{%s}}" % s, vals[s])
    return text


def bangla_rows(block, tr, tpl_bn, fill_bn, unknown_bn):
    """tpl_bn: dict FIELD -> Bangla template text. fill_bn: function(english filler) -> Bangla filler."""
    vals = {"NAME1": fill_bn(tr["w1"]), "NAME2": fill_bn(tr["w2"])}
    if tr["r1"]:
        vals["WORD1"] = fill_bn(tr["r1"])
    if tr["r2"]:
        vals["WORD2"] = fill_bn(tr["r2"])
    t = {k: re.sub(r"\s+", " ", fill(v, vals)).strip() for k, v in tpl_bn.items()}
    amb = t["Ambiguous_Context"]
    dis = f"{amb} {t['Disambiguating_Context']}".strip()
    text_for = {"neg": t["Answer_negative"], "nonneg": t["Answer_non_negative"], "unknown": unknown_bn}
    pos = positions(block)
    short_map = {tr["w1"].strip(): vals["NAME1"].strip(), tr["w2"].strip(): vals["NAME2"].strip()}
    out = []
    for r in block:
        n = dict(r)
        n["answer_info"] = {}
        for k in ("ans0", "ans1", "ans2"):
            short, tag = r["answer_info"][k]
            if tag == "unknown":
                n["answer_info"][k] = [unknown_bn, tag]
            else:
                n["answer_info"][k] = [short_map[short], tag]
        n["context"] = amb if r["context_condition"] == "ambig" else dis
        n["question"] = t["Question_negative_stereotype"] if r["question_polarity"] == "neg" else t["Question_non_negative"]
        for k in range(3):
            n[f"ans{k}"] = text_for[pos[k]]
        out.append(n)
    return out
