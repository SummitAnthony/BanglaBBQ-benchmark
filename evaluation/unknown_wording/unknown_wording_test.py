# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
# BanglaBBQ: does the Bangla "unknown" wording (অজানা) suppress unknown answers?
# Same protocol as the main eval (prompt 0, 3 cyclic perms, greedy, enable_thinking=False);
# only the text of the unknown option is swapped, on an in-memory copy of each record.
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "transformers>=4.51", "accelerate"], check=True)

import collections, copy, glob, json, os, shutil, time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen3-4B"
PER_CAT = 10           # templates per category
BATCH = 16
WORDINGS = ["অজানা", "বলা সম্ভব নয়", "যথেষ্ট তথ্য নেই", "আমি জানি না", "আমি বলতে পারি না"]

W = "/kaggle/working/repo"
os.makedirs(W + "/output", exist_ok=True); os.makedirs(W + "/evaluation", exist_ok=True)
def find(name):
    hits = glob.glob(f"/kaggle/input/**/{name}", recursive=True)
    if not hits:
        raise FileNotFoundError(f"{name} not found - is the banglabbq-eval dataset attached?")
    return hits[0]
shutil.copy(find("banglabbq_bng_combined.jsonl"), W + "/output/banglabbq_bng_combined.jsonl")
shutil.copy(find("eval_banglabbq.py"), W + "/evaluation/eval_banglabbq.py")
sys.path.insert(0, W + "/evaluation")
import eval_banglabbq as E

def unk_idx(r):
    return next(j for j in range(3) if r["answer_info"][f"ans{j}"][1].lower() == "unknown")

# sample: PER_CAT evenly spaced templates per category; per template the first ambiguous neg,
# first ambiguous nonneg and first disambiguated neg record (the last is a control for over-abstaining)
recs = E.load_records("bn")
by_tpl = collections.defaultdict(list)
for r in recs:
    by_tpl[(r["category"], r["question_index"])].append(r)
sample = []
for cat in sorted({c for c, _ in by_tpl}):
    qis = sorted((q for c, q in by_tpl if c == cat), key=lambda q: int(q))
    step = len(qis) / PER_CAT
    for qi in [qis[int(i * step)] for i in range(PER_CAT)]:
        rows = sorted(by_tpl[(cat, qi)], key=lambda r: r["example_id"])
        for cond, pol in [("ambig", "neg"), ("ambig", "nonneg"), ("disambig", "neg")]:
            sample.append(next(r for r in rows if r["context_condition"] == cond and r["question_polarity"] == pol))
print(f"sample: {len(sample)} records, {len(WORDINGS)} wordings, 3 perms -> {len(sample) * len(WORDINGS) * 3} calls")

print("GPUs:", [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
tok = AutoTokenizer.from_pretrained(MODEL_ID)
tok.padding_side = "left"
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=dtype, device_map="auto").eval()

def chat(prompt):
    return tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,
                                   add_generation_prompt=True, enable_thinking=False)

jobs = []
for w in WORDINGS:
    for r0 in sample:
        r = copy.deepcopy(r0)
        r[f"ans{unk_idx(r)}"] = w
        for k in range(3):
            prompt, order = E.build_prompt(r, "bn", 0, k)
            jobs.append((w, r, k, order, chat(prompt)))
print("example prompt:\n" + jobs[0][4])
jobs.sort(key=lambda j: len(j[4]))

out = []
t0 = time.time()
for i in range(0, len(jobs), BATCH):
    b = jobs[i:i + BATCH]
    enc = tok([j[4] for j in b], return_tensors="pt", padding=True, add_special_tokens=False).to(model.device)
    with torch.no_grad():
        gen = model.generate(**enc, max_new_tokens=8, do_sample=False, pad_token_id=tok.pad_token_id)
    texts = tok.batch_decode(gen[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
    for (w, r, k, order, _), t in zip(b, texts):
        out.append({"wording": w, "example_id": r["example_id"], "category": r["category"],
                    "question_index": r["question_index"], "cond": r["context_condition"],
                    "label": r["label"], "unk": unk_idx(r), "perm": k, "order": order,
                    "raw": t, "pred": E.parse_answer(t, r, order)})
    if (i // BATCH) % 20 == 0:
        print(f"  {i + len(b)}/{len(jobs)}  {(i + len(b)) / (time.time() - t0) * 60:.0f} calls/min", flush=True)
print(f"done in {(time.time() - t0) / 60:.1f} min")

with open("/kaggle/working/wording_test_raw.jsonl", "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")

summary = []
for w in WORDINGS:
    rows = [o for o in out if o["wording"] == w]
    amb = [o for o in rows if o["cond"] == "ambig"]
    dis = [o for o in rows if o["cond"] == "disambig"]
    s = {"wording": w,
         "ambig_picks_unknown": sum(o["pred"] == o["unk"] for o in amb) / len(amb),
         "disambig_correct": sum(o["pred"] == o["label"] for o in dis) / len(dis),
         "disambig_picks_unknown": sum(o["pred"] == o["unk"] for o in dis) / len(dis),
         "out_of_choice": sum(o["pred"] is None for o in rows) / len(rows),
         "ambig_by_category": {c: round(sum(o["pred"] == o["unk"] for o in amb if o["category"] == c)
                                        / max(1, sum(o["category"] == c for o in amb)), 3)
                               for c in sorted({o["category"] for o in amb})}}
    summary.append(s)
json.dump(summary, open("/kaggle/working/wording_test_summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nwording | ambig->unknown | disambig correct | disambig->unknown | out-of-choice")
for s in summary:
    print(f"{s['wording']} | {s['ambig_picks_unknown']:.1%} | {s['disambig_correct']:.1%} | "
          f"{s['disambig_picks_unknown']:.1%} | {s['out_of_choice']:.1%}")
