# evaluation/reports/ — the paper's evaluation reports

Every folder here was written by `python reproduce.py` from the raw outputs in `evaluation/results/`,
`evaluation/results_vb/` and `evaluation/results_dt_tm/`. No report contains a number that cannot be
regenerated from those files. Prompt wordings are `prompt_id` 0-2 in the files and wordings 1-3 in the
paper. The result files of each report are listed by name in `RUNS` in `reproduce.py`; the patterns below
describe them.

| Folder | Content | Result files scored | Data files | Keep list | Templates | Paper |
|---|---|---|---|---|--:|---|
| `final/` | **Main results.** Versions A and B together, wording 1 | `results/*p0_k3.jsonl` + `results_vb/*.jsonl` (16) | `data/banglabbq_{en,bn}.jsonl` + `data/banglabbq_vb_{en,bn}.jsonl` | `data/keep_final.csv` | 360 | Tables 4 and 5 |
| `final_version_a/` | The same templates, version A alone, wording 1 | `results/*p0_k3.jsonl` (8) | `data/banglabbq_{en,bn}.jsonl` | `data/keep_final.csv` | 360 | Table 9, version A |
| `final_version_b/` | The same templates, version B alone, wording 1 | `results_vb/*.jsonl` (8) | `data/banglabbq_vb_{en,bn}.jsonl` | `data/keep_final.csv` | 360 | Table 9, version B |
| `validated_a/` | Version A, wording 1, templates that passed human validation | `results/*p0_k3.jsonl` (8) | `data/banglabbq_{en,bn}.jsonl` | `data/keep_validated.csv` | 372 | Table 7, "Valid." |
| `rejected_a/` | Version A, wording 1, templates that did not pass validation | `results/*p0_k3.jsonl` (8) | `data/banglabbq_{en,bn}.jsonl` | `data/keep_rejected.csv` | 94 | Table 7, "Rej." |
| `wordings_validated/` | Version A, all prompt wordings, validated templates; the failed Qwen3-8B English wording-3 run is excluded | `results/*_k3.jsonl` (14) | `data/banglabbq_{en,bn}.jsonl` | `data/keep_validated.csv` | 372 | Table 8 (`scores_by_prompt.csv`) |
| `dt_tm/` | BBQ templates adapted to Bangladesh, balanced sample, wording 1, Qwen models only | `results_dt_tm/*.jsonl` (4) | `evaluation/dt_tm/banglabbq_dt_tm_sample_{eng,bng}.jsonl` | none (not annotated) | 140 | Tables 6 and 10 |

Each folder holds three files (column definitions: `evaluation/README.md`, "Output files"):

* `report.md`: overall table per model and language, then a table per category. With one wording the
  values have 95% bootstrap intervals over templates (1,000 resamples, fixed seed); with several wordings
  they are means ± sample standard deviation over the wordings.
* `scores_by_prompt.csv`: every metric per model x language x wording x group (`ALL` or a category), with
  the bootstrap interval for `ALL`.
* `scores_summary.csv`: mean and standard deviation over wordings per model x language x group.

## Reading the reports

* **`final/`** is the evaluation set of the paper: 360 templates that passed human validation and have a
  usable version B item. Its ambiguous items come from version A; its disambiguated items are the 4
  version A and the 4 version B records of each template. `acc_dis` therefore pools both directions, and
  `diff_dis` = accuracy on version A (stereotype-consistent) minus accuracy on version B
  (counter-stereotypical) disambiguated items. Per direction, version A accuracy is 0.983 to 1.000 and
  version B accuracy 0.942 (Qwen3-4B, Bangla) to 0.999 (`final_version_a/` and `final_version_b/`). Version B
  sentences are longer than version A sentences and more often state a reason (`DATASHEET.md`, section
  3.3), so the two directions are not matched in wording.
* **`final_version_a/` and `final_version_b/`** score the 360 templates of `final/` on one version each, so
  together they give paper Table 9: `acc_dis` and `s_dis` per version (`diff_dis` is in `final/`). In
  `final_version_a/` every disambiguated context is stereotype-consistent, so `s_dis` is close to +1 by
  construction and `diff_dis` is undefined; `final_version_b/` holds disambiguated records only, so its
  ambiguous-context columns are empty (`—`) and `s_dis` is close to -1 for a model that follows the
  evidence.
* **`validated_a/` and `rejected_a/`** compare the 372 validated templates with the 94 that did not pass.
  They use version A only, so `diff_dis` is undefined (`—`) and `s_dis` is close to +1 by construction
  (the report says so in a note). Compare the ambiguous-context scores: `s_amb` is higher on the validated
  templates for every model and language; the two 95% intervals are disjoint except for Qwen3-4B in Bangla (0.329 [0.26, 0.40] vs 0.197 [0.07, 0.32]).
  Under the two alternative keep rules of `annotation/README.md` ("Other rules") the point estimates keep the
  same order, but the intervals overlap for two or three of the eight model-language pairs (table there).
* **`wordings_validated/`** shows how much the results depend on the prompt wording; paper Table 8 is its
  `s_amb` per `prompt_id` (group `ALL`) in `scores_by_prompt.csv`. Qwen3-4B has wording 1 only, so its rows
  have intervals instead of a standard deviation. The Qwen3-8B English run with wording 3 failed (57% of its
  items without a valid majority answer; 45.8% of its calls out-of-choice, `evaluation/results/README.md`)
  and is excluded, as in the paper: `reproduce.py` passes `--exclude Qwen/Qwen3-8B:en:2`, and the report
  names the excluded run. Its Qwen3-8B English mean ± sd is over wordings 1 and 2.
* **`dt_tm/`** uses the same metrics on BBQ's own templates sorted for Bangladesh. Half of its
  disambiguated records are counter-stereotypical, so `s_dis` and `diff_dis` are defined. The records
  differ from the Bangladesh-specific templates in category, template style and number, so compare the
  two sets descriptively. The Bangla `dt_tm` text is an LLM translation made with the
  conventions of the newly authored part and judged acceptable by native Bangla speakers
  (`bbq_dt_tm/pipeline/bangla/README.md`).

## Regenerating

```
python reproduce.py --check     # regenerate in a temporary folder and compare file by file
python reproduce.py             # overwrite the seven folders
```

Standard library only, no model calls, a few minutes. The output is identical byte for byte to the released
files on any operating system (LF line endings). `reproduce.py` scores only the released result files, listed
by name, so result files you add do not change the reports. To score your own runs, call
`evaluation/score_banglabbq.py` with your own `--out` folder; the command behind each report is in `RUNS` in
`reproduce.py`, for example:

```
python evaluation/score_banglabbq.py "evaluation/results/*p0_k3.jsonl" \
    --data-en data/banglabbq_en.jsonl --data-bn data/banglabbq_bn.jsonl \
    --keep data/keep_validated.csv --out evaluation/reports/validated_a
```
