# evaluation/results_dt_tm/ — raw model outputs, BBQ templates adapted to Bangladesh

Raw outputs on the balanced evaluation sample of `bbq_dt_tm/` (BBQ's own templates sorted for Bangladesh:
DT = directly translated, TM = target modified). The sample is
`evaluation/dt_tm/banglabbq_dt_tm_sample_eng.jsonl` / `_bng.jsonl`: 3,256 records per language (1,880 DT,
1,376 TM; 1,628 ambiguous and 1,628 disambiguated), row-parallel between the languages. Same format as
`evaluation/results/` (`evaluation/README.md`, "Result files"). Every file is complete (each record under
all three option orders exactly once) and no call has an error.

| Category | Templates | Records per language |
|---|--:|--:|
| Age | 21 | 672 |
| Disability_status | 25 | 696 |
| Gender_identity | 43 | 544 |
| Physical_appearance | 22 | 672 |
| Religion | 5 | 80 |
| SES | 24 | 592 |
| **All** | **140** | **3,256** |

The full layer has 15,328 rows per language, most of them the same question with different names or groups
filled in. `evaluation/dt_tm/make_dt_tm_sample.py` keeps every template but only some of its 4-row blocks,
with equal numbers of blocks whose disambiguated answer is stereotype-consistent and inconsistent (seed
2026). It also skips 16 Gender_identity rows that pair two people of the same gender, as BBQ's own analysis
does. `evaluation/dt_tm/sample_map.csv` links every sample record to its source row.
`python evaluation/dt_tm/make_dt_tm_sample.py --check` rebuilds the sample from `bbq_dt_tm/` in memory and
compares it with the three shipped files without writing them. Unlike the
Bangladesh-specific templates, half of the disambiguated records here are counter-stereotypical, so
`s_dis` and `diff_dis` are defined.

**These `example_id`s start at 0 and overlap with the version A ids.** Score these files only with the
sample files as `--data-en` / `--data-bn`, never together with `evaluation/results/`.

## Runs

Only the two Qwen models were run on this sample. Counted from the files: dates are the first and last
`ts`; "Out-of-choice calls" are calls with `pred` = null.

| Model | Lang | Wording | File | Backend | Dates (`ts`) | Calls | Out-of-choice calls | API cost (USD) |
|---|---|--:|---|---|---|--:|--:|--:|
| Qwen3-4B | en | 1 | `Qwen_Qwen3-4B__en__p0_k3.jsonl` | local (Kaggle) | 2026-10-08 | 9,768 | 11 (0.11%) | – |
| Qwen3-4B | bn | 1 | `Qwen_Qwen3-4B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-08 | 9,768 | 3 (0.03%) | – |
| Qwen3-8B | en | 1 | `Qwen_Qwen3-8B__en__p0_k3.jsonl` | local (Kaggle) | 2026-10-07 | 9,768 | 0 | – |
| Qwen3-8B | bn | 1 | `Qwen_Qwen3-8B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-07 to 2026-10-08 | 9,768 | 0 | – |
| **All** | | | 4 files | | | **39,072** | **14** | – |

## Run settings

Kaggle notebook `evaluation/notebooks/banglabbq_kaggle_eval.ipynb` with `DATASET = "dt_tm"`: prompt wording
1 (`prompt_id` 0), three cyclic option orders, 16-bit weights, greedy decoding, at most 8 new tokens,
Qwen3 thinking disabled. The same settings as the Qwen wording 1 runs in `evaluation/results/`. The Bangla
Qwen3-8B run was made in several sessions and merged into one file.

## How these files are used

`reproduce.py` scores all four files for `evaluation/reports/dt_tm/` (paper Tables 6 and 10), without a keep
list (the BBQ-derived templates were not annotated, as in PakBBQ):

```
python evaluation/score_banglabbq.py "evaluation/results_dt_tm/*.jsonl" \
    --data-en evaluation/dt_tm/banglabbq_dt_tm_sample_eng.jsonl \
    --data-bn evaluation/dt_tm/banglabbq_dt_tm_sample_bng.jsonl --out evaluation/reports/dt_tm
```

For records of type DT/TM the scorer finds the target answer with BBQ's rule (the answer whose tag is in
`stereotyped_groups`), because BBQ's tags do not mark the non-target with `non`
(`evaluation/README.md`, "Roles of the answers").
