# evaluation/results/ — raw model outputs, version A

One JSONL file per model x language x set of wordings, one line per call. Format: `evaluation/README.md`,
section "Result files". The calls refer by `example_id` to `data/banglabbq_en.jsonl` and
`data/banglabbq_bn.jsonl` (3,728 records each, all 466 templates); templates are filtered only at scoring
time (`--keep`). Every file is complete: each record has each of its wordings under all three option
orders exactly once, and no call has an error.

File names: `p0` = wording 1 (`prompt_id` 0); `p12` = wordings 2 and 3 (`prompt_id` 1 and 2); `k3` = three
cyclic option orders.

## Runs

One row per model x language x wording. Counted from the files: dates are the first and last `ts`;
"Out-of-choice calls" are calls with `pred` = null (per call, before the majority vote); cost is the sum
of `usage.cost` as reported by OpenRouter (USD; local runs have none).

| Model | Lang | Wording | File | Backend | Dates (`ts`) | Calls | Out-of-choice calls | API cost (USD) |
|---|---|--:|---|---|---|--:|--:|--:|
| Qwen3-4B | en | 1 | `Qwen_Qwen3-4B__en__p0_k3.jsonl` | local (Colab) | 2026-09-29 | 11,184 | 2 (0.02%) | – |
| Qwen3-4B | bn | 1 | `Qwen_Qwen3-4B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-03 | 11,184 | 6 (0.05%) | – |
| Qwen3-8B | en | 1 | `Qwen_Qwen3-8B__en__p0_k3.jsonl` | local (Kaggle) | 2026-10-03 | 11,184 | 0 | – |
| Qwen3-8B | en | 2 | `Qwen_Qwen3-8B__en__p12_k3.jsonl` | API (OpenRouter) 8,819 + local (Kaggle) 2,365 | 2026-10-05 to 2026-10-10 | 11,184 | 4 (0.04%) | 0.15 |
| Qwen3-8B | en | 3 | `Qwen_Qwen3-8B__en__p12_k3.jsonl` | API (OpenRouter) 8,822 + local (Kaggle) 2,362 | 2026-10-05 to 2026-10-10 | 11,184 | **5,123 (45.81%)** | 0.15 |
| Qwen3-8B | bn | 1 | `Qwen_Qwen3-8B__bn__p0_k3.jsonl` | local (Kaggle) | 2026-10-03 to 2026-10-04 | 11,184 | 0 | – |
| Qwen3-8B | bn | 2 | `Qwen_Qwen3-8B__bn__p12_k3.jsonl` | API (OpenRouter) 9,222 + local (Kaggle) 1,962 | 2026-10-05 to 2026-10-10 | 11,184 | 0 | 0.61 |
| Qwen3-8B | bn | 3 | `Qwen_Qwen3-8B__bn__p12_k3.jsonl` | API (OpenRouter) 9,230 + local (Kaggle) 1,954 | 2026-10-05 to 2026-10-10 | 11,184 | 0 | 0.58 |
| GPT-4.1-mini | en | 1 | `openai_gpt-4.1-mini__en__p0_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.56 |
| GPT-4.1-mini | en | 2 | `openai_gpt-4.1-mini__en__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.56 |
| GPT-4.1-mini | en | 3 | `openai_gpt-4.1-mini__en__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 275 (2.46%) | 0.56 |
| GPT-4.1-mini | bn | 1 | `openai_gpt-4.1-mini__bn__p0_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.84 |
| GPT-4.1-mini | bn | 2 | `openai_gpt-4.1-mini__bn__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.84 |
| GPT-4.1-mini | bn | 3 | `openai_gpt-4.1-mini__bn__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.84 |
| Gemini 2.5 Flash | en | 1 | `google_gemini-2.5-flash__en__p0_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.41 |
| Gemini 2.5 Flash | en | 2 | `google_gemini-2.5-flash__en__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.42 |
| Gemini 2.5 Flash | en | 3 | `google_gemini-2.5-flash__en__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 3 (0.03%) | 0.42 |
| Gemini 2.5 Flash | bn | 1 | `google_gemini-2.5-flash__bn__p0_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 0 | 0.44 |
| Gemini 2.5 Flash | bn | 2 | `google_gemini-2.5-flash__bn__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 16 (0.14%) | 0.47 |
| Gemini 2.5 Flash | bn | 3 | `google_gemini-2.5-flash__bn__p12_k3.jsonl` | API (OpenRouter) | 2026-10-05 | 11,184 | 41 (0.37%) | 0.49 |
| **All** | | | 14 files | | | **223,680** | **5,470** | **8.34** |

An out-of-choice call is one reply that the parser could not map to an option. The "out-of-choice" column
of the reports is different: it is the share of records whose three option orders gave no majority answer.

## Run settings

| Model | Settings |
|---|---|
| Qwen3-4B | Notebooks in `evaluation/notebooks/` (English: Colab notebook, one T4; Bangla: Kaggle notebook, 2 x T4). 16-bit weights, greedy decoding, at most 8 new tokens, Qwen3 thinking disabled (`enable_thinking=False`). Wording 1 only. |
| Qwen3-8B, wording 1 | Kaggle notebook, settings as Qwen3-4B. The Bangla run was made in two sessions (records split in two halves) and merged. |
| Qwen3-8B, wordings 2 and 3 | Mostly OpenRouter (`qwen/qwen3-8b`, served by `Alibaba`, temperature 0, `--max-tokens 8`, seeds 1013-1015 and 2013-2015), finished in the Kaggle notebook. See below. |
| GPT-4.1-mini | OpenRouter `openai/gpt-4.1-mini`, temperature 0, `--max-tokens 16`, seed `13 + 1000 * prompt_id + perm`. Served by `OpenAI` (a few calls by `Azure`, see `provider`). |
| Gemini 2.5 Flash | OpenRouter `google/gemini-2.5-flash`, temperature 0, `--max-tokens 16`, `--reasoning-effort none` (thinking off; every call reports 0 reasoning tokens), seed as above. Served by `Google`. |

All runs: zero-shot, one user message, no system message, three cyclic option orders.

## Notes

**Qwen3-8B, wordings 2 and 3, two backends.** These runs were started through OpenRouter. The last
OpenRouter call in the files is from 2026-10-05 (`ts` up to 2026-10-05T21:31 in both languages); the
remaining calls were run locally with the Kaggle notebook on 2026-10-10 (`PROMPTS = [1, 2]`). The local
run covered a slice of the records (English from record 2141, Bangla from record 2229, to the last record,
3727) and filled only the calls missing from the file: 795 English and 660 Bangla records have calls run
locally (English: 784 local only, mostly records 2947-3727; Bangla: 648 local only, mostly records 3083-3727), and the rest of those ranges came from OpenRouter. 11 English and 12 Bangla records have option
orders from both backends. By call: English 17,641 OpenRouter and 4,727 local, Bangla 18,452 OpenRouter
and 3,916 local, over both wordings. The OpenRouter rows
were relabelled `model = "Qwen/Qwen3-8B"` so that the scorer groups them with the notebook rows; `provider`
still shows the backend of every call (`Alibaba` or `kaggle-transformers`). In a development check on the
first 200 records of wording 1 (three option orders, 600 calls per language), the OpenRouter model and the
Kaggle run chose the same answer in 596 of 600 calls in English and in Bangla; the outputs of that check
are not part of the release. The numeric precision of the OpenRouter deployment is not known. The
OpenRouter id `qwen/qwen3-8b` has since been withdrawn (2026-10-09) and can no longer be called; rerun
these wordings with the Kaggle notebook.

**Qwen3-8B, English, wording 3: failed run, excluded.** On the 372 validated templates, 1,686 of the 2,976
records (57%) have no valid majority answer over their three option orders; the paper excludes this run
(Table 8), and so does `reports/wordings_validated/`. Per call, 5,123 of 11,184 calls (45.8%, all 466
templates) begin an explanation
instead of giving a letter (for example `The passage states that the landlord **turned`, cut at 8 tokens;
4,673 of the 5,123 begin with "The passage states"), so many records have no majority answer. Other
replies start with an option letter and then explain (for example `A\n\nThe passage does not ...`). Counted
with the rule "the reply begins with A, B or C, the next character is not a letter or digit, and some
non-space text follows" (Python: `re.match(r"[ABC](?![A-Za-z0-9])\W*\S", raw)`), there are 3,035 such calls
(A 2,812, B 146, C 77; OpenRouter 2,380, Kaggle 655). 3,019 of them are parsed to their first letter; 16
are out-of-choice because their first 40 characters contain a second standalone capital (`... that the B`,
cut at 8 tokens). Out-of-choice calls occur with both backends (OpenRouter 3,784 of 8,822 calls;
Kaggle 1,339 of 2,362). `reproduce.py` leaves the run out of `reports/wordings_validated/` with the
scorer's `--exclude Qwen/Qwen3-8B:en:2`; the calls stay in the file, so the run can still be scored on its
own. The Bangla run with the same wording has no out-of-choice call.

**Replies cut at `--max-tokens`.** Some API replies have `finish` = `length`: Qwen3-8B (English 9,733,
Bangla 8,063 calls, with `--max-tokens 8`), Gemini 2.5 Flash Bangla wordings 2-3 (1,435), GPT-4.1-mini
English wordings 2-3 (271), Gemini 2.5 Flash English wordings 2-3 (3). A letter at the start of a cut reply
is still parsed; cut replies that do not start with a letter are among the out-of-choice calls above.

## Runs not released

* **Qwen3-4B, wordings 2 and 3.** Run with the Kaggle notebook, excluded from all analyses, and not
  released. The English run was complete: 2,386 (wording 2) and 6,978 (wording 3) of 11,184 calls each
  were out-of-choice (explanations instead of a letter), that is 21% and 62% of the English calls. The
  Bangla run was incomplete: only records 0-1863 were run before the free GPU quota ran out (wording 2:
  1,790 of 5,592 calls out-of-choice). Qwen3-4B is therefore reported on wording 1 only (paper Table 8).
* **Bangla-specific models.** TituLLM-3B (`hishab/titulm-llama-3.2-3b-v2.0`) and TigerLLM-9B
  (`md-nishat-008/TigerLLM-9B-it`) were tried on 200 records. TituLLM never
  answered with a letter (100% out-of-choice in English); TigerLLM answered with letters in English but
  began an explanation instead of a letter in Bangla (100% out-of-choice). Neither was run further.

## How these files are used

`reproduce.py` scores the `*p0_k3.jsonl` files (wording 1) for `reports/final` (together with
`results_vb/`), `reports/final_version_a`, `reports/validated_a` and `reports/rejected_a`, and all 14 files,
without the failed Qwen3-8B English wording-3 run, for `reports/wordings_validated`. See
`evaluation/reports/README.md`.
