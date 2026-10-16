# evaluation/results_vb/ — raw model outputs, version B

Raw outputs on the version B (counter-stereotypical) disambiguated records, `data/banglabbq_vb_en.jsonl`
and `data/banglabbq_vb_bn.jsonl`: 1,864 records per language, 4 per template, for all 466 templates.
`example_id` = version A id + 100000 (ids 100001-103727 here). The ambiguous records of version B are the
same as in version A and were not run again; they are scored from `evaluation/results/`. Same format as
`evaluation/results/` (`evaluation/README.md`, "Result files"). Every file is complete (each record under
all three option orders exactly once) and no call has an error.

All runs use wording 1 only (`prompt_id` 0, file suffix `p0_k3`).

## Runs

Counted from the files: dates are the first and last `ts`; "Out-of-choice calls" are calls with `pred` =
null; cost is the sum of `usage.cost` as reported by OpenRouter (USD).

| Model | Lang | Wording | File | Backend | Dates (`ts`) | Calls | Out-of-choice calls | API cost (USD) |
|---|---|--:|---|---|---|--:|--:|--:|
| Qwen3-4B | en | 1 | `Qwen_Qwen3-4B__en__p0_k3.jsonl` | local (Kaggle) | 2026-10-11 | 5,592 | 2 (0.04%) | – |
| Qwen3-4B | bn | 1 | `Qwen_Qwen3-4B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-11 | 5,592 | 0 | – |
| Qwen3-8B | en | 1 | `Qwen_Qwen3-8B__en__p0_k3.jsonl` | local (Kaggle) | 2026-10-11 | 5,592 | 0 | – |
| Qwen3-8B | bn | 1 | `Qwen_Qwen3-8B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-11 | 5,592 | 0 | – |
| GPT-4.1-mini | en | 1 | `openai_gpt-4.1-mini__en__p0_k3.jsonl` | API (OpenRouter) | 2026-10-08 | 5,592 | 0 | 0.33 |
| GPT-4.1-mini | bn | 1 | `openai_gpt-4.1-mini__bn__p0_k3.jsonl` | API (OpenRouter) | 2026-10-08 | 5,592 | 0 | 0.50 |
| Gemini 2.5 Flash | en | 1 | `google_gemini-2.5-flash__en__p0_k3.jsonl` | API (OpenRouter) | 2026-10-08 | 5,592 | 0 | 0.24 |
| Gemini 2.5 Flash | bn | 1 | `google_gemini-2.5-flash__bn__p0_k3.jsonl` | API (OpenRouter) | 2026-10-08 | 5,592 | 0 | 0.26 |
| **All** | | | 8 files | | | **44,736** | **2** | **1.33** |

## Run settings

The same settings as the wording 1 runs in `evaluation/results/`:

| Model | Settings |
|---|---|
| Qwen3-4B, Qwen3-8B | Kaggle notebook (`evaluation/notebooks/banglabbq_kaggle_eval.ipynb`, `DATASET = "vb"`), 16-bit weights, greedy decoding, at most 8 new tokens, thinking disabled |
| GPT-4.1-mini | OpenRouter `openai/gpt-4.1-mini`, temperature 0, `--max-tokens 16`, seeds 13-15 (one per option order) |
| Gemini 2.5 Flash | OpenRouter `google/gemini-2.5-flash`, temperature 0, `--max-tokens 16`, `--reasoning-effort none` (every call reports 0 reasoning tokens), seeds 13-15 |

No API reply was cut at `--max-tokens` (`finish` = `stop` for every call).

**Provenance of the API runs.** GPT-4.1-mini and Gemini 2.5 Flash were run by one of the authors with
`evaluation/eval_banglabbq.py` on per-category version B files whose ids started at 0 in each file. The
calls were then mapped to the version B ids used here (matched on category, template, polarity, context
condition, question and answer texts), and only the disambiguated records were kept. The script that did
this is kept for provenance: `construction/development_scripts/import_closed_src_vb.py` (written for the
development layout). Re-parsing every `raw` reply against the released version B files gives the stored
`pred`.

## How these files are used

Version B is scored together with version A: both files of a model and language are passed to the scorer,
and the data files are given comma-separated, as in `reproduce.py` (`reports/final`):

```
python evaluation/score_banglabbq.py "evaluation/results/*p0_k3.jsonl" "evaluation/results_vb/*.jsonl" \
    --data-en data/banglabbq_en.jsonl,data/banglabbq_vb_en.jsonl \
    --data-bn data/banglabbq_bn.jsonl,data/banglabbq_vb_bn.jsonl \
    --keep data/keep_final.csv --out evaluation/reports/final
```

`--keep data/keep_final.csv` (360 templates) restricts scoring to templates that passed human validation
and have a usable version B item. Twelve templates whose question presupposes something that fits only the
stereotyped person, or whose counter-stereotypical answer is strained, are not usable in version B
(`data/keep_vb.csv` lists the other 454). Their calls are in these files but none of the paper's reports
scores them.

Version B alone (paper Table 9, version B columns) is `reports/final_version_b`: these files scored against
`data/banglabbq_vb_{en,bn}.jsonl` with `--keep data/keep_final.csv`.
