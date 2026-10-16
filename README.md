# BanglaBBQ

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23415895.svg)](https://doi.org/10.5281/zenodo.23415895)

BanglaBBQ is a bias benchmark for question answering in the Bangladeshi context, in parallel English and
Bangla, in the format of BBQ (Parrish et al., 2022) and its KoBBQ and PakBBQ adaptations. It has two parts:

- **466 newly authored templates** in five Bangladesh-specific categories: marital status, age and political
  perception, regional origin, educational background, and mental-health status. The authors built the
  templates with the help of LLM assistants, after studying BBQ, KoBBQ and PakBBQ, reading newspapers and
  articles, and consulting anthropology professors; the Age_political_perception templates were written by
  one author and reviewed by another. Each template is based on a passage of a public document about
  Bangladesh, cites that source and quotes the passage verbatim, and the authors reviewed and approved every
  template. Each template gives 8 records per
  language (3,728 per language), and a counter-stereotypical version B adds 4 more per template (1,864 per
  language). Native Bangladeshi annotators validated the templates: 372 passed, and the 360 of them with a
  usable version B item form the main evaluation set (2,880 version A and 1,440 version B records per
  language).
- **140 BBQ templates adapted to Bangladesh** (`bbq_dt_tm/`): BBQ's own templates sorted into directly
  translated (76), target-modified (64) and removed, in six categories, giving 15,328 records per language.

This repository holds the data, the aggregate validation outcome, the raw outputs of four models (Qwen3-4B,
Qwen3-8B, GPT-4.1-mini and Gemini 2.5 Flash) and the code behind the paper *BanglaBBQ: A Bias Benchmark for
Question Answering in the Bangladeshi Context* by Sumit Anthony Gomes, Taeeba Tasnia, Yasin Rahman and Faiza
Nooren Suhita (BRAC University, Dhaka).

> **Content warning and intended use.** The data states harmful stereotypes about real groups in Bangladesh,
> for example divorced and widowed people, people with mental illness, Indigenous/Adivasi people, Biharis,
> Rohingya refugees, people from particular districts, people with particular kinds of education, and young
> and older people's political attitudes. It exists only to audit language models.
> Do not use it to train or fine-tune models to reproduce these stereotypes. A low bias score on it is not
> proof that a system is unbiased.

## Getting the files

```
git clone https://github.com/SummitAnthony/BanglaBBQ-benchmark.git
cd BanglaBBQ-benchmark
```

Run every command below from the repository root (`BanglaBBQ-benchmark/`).

## At a glance

From `annotation/agreement.md` (paper Tables 1 and 2), in the paper's order. *Validated*: passed human
validation (the paper's "Retained"). *Final set*: validated and with a usable version B item
(`data/keep_final.csv`; the paper's "Eval."). *Records*: test instances per language in the final set, 8 in
version A and 4 in version B per template. AC1: Gwet's multi-rater AC1 over three categories coded relative
to the template (intended target, other group, Can't tell).

| Category | Templates | Validated | Final set | Records | AC1 (English) | AC1 (Bangla) |
|---|--:|--:|--:|--:|--:|--:|
| Marital_status | 100 | 80 | 75 | 900 | 0.654 | 0.821 |
| Age_political_perception | 100 | 62 | 62 | 744 | 0.563 | 0.617 |
| Regional_origin | 100 | 85 | 80 | 960 | 0.658 | 0.678 |
| Educational_background | 95 | 77 | 76 | 912 | 0.667 | 0.716 |
| Mental_health_status | 71 | 68 | 67 | 804 | 0.798 | 0.880 |
| **All** | **466** | **372** | **360** | **4,320** | | |

Five further Educational_background templates (EDU-081, EDU-092, EDU-093, EDU-094, EDU-098) were dropped
before annotation because their quotes did not support the encoded stereotype (`construction/README.md`).

## Headline results

From `evaluation/reports/final/report.md` (Overall), in the layout and order of paper Table 4: versions A
and B, prompt wording 1 (`prompt_id` 0), the 360 templates of the final set, three cyclic option orders
combined by majority vote. Brackets are 95% bootstrap intervals over templates (1,000 resamples). Bias
scores: positive = stereotype-aligned. `s_dis` and `diff_dis` are computed over versions A and B together.

| model | lang | acc_amb | acc_dis | s_amb | diff_amb | s_dis | diff_dis | OOS | consistency |
|---|---|---|---|---|---|---|---|--:|--:|
| Qwen/Qwen3-4B | en | 0.169 [0.14,0.20] | 0.992 | +0.425 [0.36,0.49] | +0.407 | +0.012 | +0.012 [0.00,0.02] | 1.2% | 0.862 |
| Qwen/Qwen3-4B | bn | 0.069 [0.05,0.09] | 0.963 | +0.336 [0.27,0.40] | +0.328 | +0.042 | +0.042 [0.03,0.06] | 0.7% | 0.825 |
| Qwen/Qwen3-8B | en | 0.461 [0.42,0.51] | 0.999 | +0.293 [0.24,0.35] | +0.278 | +0.001 | +0.001 [0.00,0.00] | 0.9% | 0.866 |
| Qwen/Qwen3-8B | bn | 0.554 [0.51,0.60] | 0.988 | +0.210 [0.16,0.26] | +0.176 | +0.013 | +0.017 [0.01,0.03] | 2.6% | 0.839 |
| openai/gpt-4.1-mini | en | 0.372 [0.33,0.41] | 0.999 | +0.475 [0.42,0.52] | +0.469 | +0.002 | +0.003 [0.00,0.01] | 0.3% | 0.910 |
| openai/gpt-4.1-mini | bn | 0.384 [0.35,0.43] | 0.993 | +0.399 [0.34,0.45] | +0.396 | +0.002 | +0.002 [-0.00,0.01] | 0.2% | 0.897 |
| google/gemini-2.5-flash | en | 0.798 [0.76,0.83] | 0.999 | +0.146 [0.11,0.18] | +0.142 | 0.000 | -0.001 [-0.00,0.00] | 0.2% | 0.940 |
| google/gemini-2.5-flash | bn | 0.690 [0.65,0.73] | 0.998 | +0.218 [0.17,0.26] | +0.209 | +0.001 | +0.001 [0.00,0.00] | 0.4% | 0.916 |

`acc_amb`: share of ambiguous items answered Unknown (the correct answer). `acc_dis`: accuracy on
disambiguated items, versions A and B pooled. `s_amb`: BBQ bias score in ambiguous contexts. `diff_amb`:
KoBBQ diff-bias in ambiguous contexts. `s_dis`: BBQ bias score in disambiguated contexts. `diff_dis`:
accuracy on stereotype-consistent (version A) minus counter-stereotypical (version B) disambiguated items.
OOS: share of items without a valid majority answer (the report's `out-of-choice` column). `consistency`:
share of items answered identically in all three option orders. Definitions are in `evaluation/README.md`
and `evaluation/score_banglabbq.py`. The report gives intervals for every column, and a table per category
(paper Table 5).

**Plain reading.** When the context states who did what, the four models answer 96-100% of the
disambiguated items correctly, pooled over both directions (`acc_dis`). Per direction (paper Table 9,
`evaluation/reports/final_version_a/` and `final_version_b/`) the range is 94-100%: on version A (evidence
supports the stereotype) at least 98.3% for every model and language; on version B (evidence contradicts it)
94.2% for Qwen3-4B in Bangla and at least 97.9% otherwise; `diff_dis` is at most 0.042. When the context
does not say, the models choose Unknown between 7% (Qwen3-4B, Bangla) and 80% (Gemini 2.5 Flash, English)
of the time. The answers that are not Unknown lean towards the stereotype for every model and language
(`s_amb` +0.146 to +0.475, every interval above zero). The `s_amb` point estimate is higher on the templates
that passed human validation than on the rejected ones for every model and language (paper Table 7;
`evaluation/reports/validated_a/` vs `evaluation/reports/rejected_a/`), and it stays higher under the two
alternative keep rules (`annotation/README.md`, "Other rules"). Under the released rule the 95% intervals of
the two sets are disjoint except for Qwen3-4B in Bangla; under the alternative rules they overlap for two or
three of the eight model-language pairs. On the BBQ templates adapted to Bangladesh (`bbq_dt_tm/`, Qwen
models only, a balanced sample; paper Tables 6 and 10, `evaluation/reports/dt_tm/`) both models choose
Unknown more often than on the Bangladesh-specific templates, are less accurate when the context contradicts
the stereotype than when it confirms it (`diff_dis` +0.039 to +0.063), and are more biased in Bangla than in
English. Results change with the prompt wording (paper Table 8, `evaluation/reports/wordings_validated/`):
the size of the bias changes, its direction does not. Qwen3-8B English with wording 3 (`prompt_id` 2)
failed: 57% of its items on the 372 validated templates have no valid majority answer (45.8% of its calls on
all 466 templates are out-of-choice). It is excluded from the prompt-wording report, as in the paper.

## Paper tables in this release

| Paper | Release file | Regenerate or check with |
|---|---|---|
| Table 1 (human annotation) | `annotation/agreement.md`, `data/validated_templates.csv` | `python annotation/agreement.py --check` |
| Table 2 (newly authored templates) | `data/README.md` ("Counts per category"), `data/keep_*.csv` | `python construction/check_data.py` |
| Table 3 (adapted BBQ templates) | `bbq_dt_tm/README.md`, `bbq_dt_tm/sorting_logs/` | `bbq_dt_tm/pipeline/build.sh` |
| Tables 4 and 5 (main results, by category) | `evaluation/reports/final/` | `python reproduce.py` |
| Tables 6 and 10 (adapted BBQ templates) | `evaluation/reports/dt_tm/` | `python reproduce.py` |
| Table 7 (validated vs rejected) | `evaluation/reports/validated_a/`, `evaluation/reports/rejected_a/` | `python reproduce.py` |
| Table 8 (prompt wordings) | `evaluation/reports/wordings_validated/scores_by_prompt.csv` | `python reproduce.py` |
| Table 9 (version A vs version B) | `evaluation/reports/final_version_a/`, `evaluation/reports/final_version_b/` (`diff_dis` from `final/`) | `python reproduce.py` |

## Three things to know

1. **Version A disambiguation is always stereotype-consistent; version B adds the opposite.** In version A the
   disambiguating sentence always describes the stereotype-consistent outcome, so version A alone cannot tell
   comprehension from bias in disambiguated contexts. For every template the authors wrote a version B
   sentence with the opposite outcome (`data/banglabbq_vb_{en,bn}.jsonl`, `example_id` = version A id + 100000,
   correct answers swapped; the ambiguous records are shared with version A). For 12 templates the question
   presupposes something that fits only the stereotyped person, or the counter-stereotypical answer is
   strained; they are left out of version B scoring (`data/keep_vb.csv`, 454 templates). Version B sentences
   are on average 2.9 words longer than the version A sentences in English (2.2 in Bangla) and more often
   state a reason for the outcome (DATASHEET sections 3.3 and 5.5), so versions A and B are not minimal pairs.
2. **The Bangla is an LLM-assisted translation guided by a native-Bangla-speaking author, and native Bangla
   speakers judged it acceptable.** A native-Bangla-speaking author set the terminology, register and wording
   choices, and the Bangla of all five categories and of the version B sentences was produced by LLM-assisted
   translation following them (`construction/README.md`, "Bangla"); several native Bangla speakers then
   judged its quality and found it acceptable. All Bangla was also checked automatically (Latin script,
   register symmetry and others, `construction/reports/*/bangla_validation.md`); in Educational_background the
   register check flagged 13 templates, whose Bangla disambiguating sentences were rewritten. The Bangla
   annotators were asked to report translation problems and reported none. The Bangla Unknown option is
   "যথেষ্ট তথ্য নেই" ("not enough information"), chosen after a wording pilot
   (`evaluation/unknown_wording/report.md`). The Bangla of the BBQ-derived `bbq_dt_tm/` was translated by an
   LLM with the same conventions, and native Bangla speakers judged it acceptable.
3. **Templates were built by the authors from verified sources, with LLM assistance, and judged by native
   annotators.** For each category the authors fixed the target groups and the areas of life to cover, and
   built the templates with the help of LLM assistants, each from a passage of a public document about
   Bangladesh; the authors reviewed and approved every template, and each template's records were
   unit-tested before being added. The instructions given to the assistants are in
   `construction/drafting_instructions.md` (see `construction/README.md`). The 100 Age_political_perception
   templates were written by one author and reviewed by another, as literals in one script
   (`construction/development_scripts/gen_age_politics.py`), which writes them and their records; they share
   11 quotes that document the political context rather than each age stereotype (47 mention no age group;
   `DATASHEET.md`, section 3.1). Every source URL and verbatim quote was
   verified against the source page, and templates whose source could not be verified were re-grounded or
   dropped. In the last validation run before release the source page of three Marital_status templates
   (MAR-411, MAR-413, MAR-414) refused the automated fetch, so their quotes were checked by hand, and a
   re-check on 2026-10-12 could not fetch the pages of 25 templates (`construction/README.md`, "Sources that
   refuse automated checks"). Three annotators per category and language then judged which group each
   scenario's question points to, as most people in Bangladesh would perceive it, without seeing the
   disambiguating sentence, the source or the intended answer. The English judgments decide which templates
   are validated, for every category; they come from three annotators, the same three for all five
   categories. The Bangla judgments, from a separate group of annotators, are reported to describe the
   Bangla annotation. `data/validated_templates.csv` gives the vote counts per
   template; annotator-level answers are not released. Protocol and disclosures: `annotation/README.md`.

## Layout

```
data/            templates, records (versions A and B, English and Bangla), validated subset,
                 keep lists, per-template vote counts                         -> data/README.md
annotation/      annotator guide, Label Studio interface, task builder, agreement statistics and
                 the script that recomputes them                              -> annotation/README.md
construction/    how the data was built: drafting instructions, source verification, compiler
                 from templates to records, consistency checks, development scripts
                                                                              -> construction/README.md
evaluation/      model runner, scorer, notebooks for local models, raw model outputs, reports
                                                                              -> evaluation/README.md
bbq_dt_tm/       BBQ's own templates sorted for Bangladesh (DT / TM / SR), 6 categories, English
                 and Bangla, with their rebuild pipeline; not human-annotated -> bbq_dt_tm/README.md
reproduce.py     regenerates every report in evaluation/reports/ from the raw model outputs
DATASHEET.md     datasheet for the dataset
```

## Quick start

Python 3.9 or later. The core scripts use the standard library only; the notebooks in `evaluation/notebooks/`
need `torch` and `transformers`. Run everything from the repository root (`BanglaBBQ-benchmark/`).

```
# 1. check the data (and that the records are exactly the compiled templates)
python construction/check_data.py
python construction/compile_records.py --check

# 2. evaluate a model through the OpenRouter API (key read from the environment, never stored);
#    write your runs to runs/, not to evaluation/results*/, which hold the paper's runs
export OPENROUTER_API_KEY=...
python evaluation/eval_banglabbq.py run --model <model-id> --lang en --out runs/<name>__en__p0_k3.jsonl --estimate   # cost, no calls
python evaluation/eval_banglabbq.py run --model <model-id> --lang en --out runs/<name>__en__p0_k3.jsonl
python evaluation/eval_banglabbq.py run --model <model-id> --lang bn --out runs/<name>__bn__p0_k3.jsonl
#    version B (disambiguated records only)
python evaluation/eval_banglabbq.py run --model <model-id> --lang en --data data/banglabbq_vb_en.jsonl --out runs_vb/<name>__en__p0_k3.jsonl
python evaluation/eval_banglabbq.py run --model <model-id> --lang bn --data data/banglabbq_vb_bn.jsonl --out runs_vb/<name>__bn__p0_k3.jsonl

# 3. score (versions A + B on the final set, as in the paper)
python evaluation/score_banglabbq.py "runs/<name>__*.jsonl" "runs_vb/<name>__*.jsonl" \
    --data-en data/banglabbq_en.jsonl,data/banglabbq_vb_en.jsonl \
    --data-bn data/banglabbq_bn.jsonl,data/banglabbq_vb_bn.jsonl \
    --keep data/keep_final.csv --out runs/report

# 4. reproduce every report of the paper from the released outputs (a few minutes)
python reproduce.py --check     # regenerate in a temporary folder and compare byte for byte
python reproduce.py             # regenerate evaluation/reports/ in place
```

The paper's settings for the closed models are temperature 0 (the runner's default) and, for Gemini 2.5
Flash, `--reasoning-effort none` (thinking off); `evaluation/README.md` lists the settings of every model.
The runner resumes from its output file: with `--out` pointing at a new file it starts from scratch, and the
same command repeated skips the calls already made. Without `--out` it writes to
`evaluation/results/<model>__<lang>__p0_k3.jsonl`, the folder of the paper's runs; for a paper model that
file is already complete, so no call is made. `reproduce.py` scores only the released result files, listed
by name, so runs added anywhere do not change its reports.

The main set is scored from the full data files with `--keep data/keep_final.csv`, as above. `data/validated/`
holds convenience copies of the record files restricted to the 372 validated templates (version A) and to the
360 templates of the final set (version B); scoring a run on these without `--keep` mixes 372 version A and 360
version B templates, so pass `--keep data/keep_final.csv` for the main set in any case. Pass them with `--data`
(runner) or `--data-en` / `--data-bn` (scorer). Local models (Qwen3-4B and Qwen3-8B in the paper) are run with
the notebooks in `evaluation/notebooks/` (Hugging Face Transformers, greedy decoding, thinking mode off), which
write the same result format. The exception is Qwen3-8B with prompt wordings 2 and 3 (paper Table 8): 78% of
the calls scored in Table 8 (80.7% of all calls) went through OpenRouter (`qwen/qwen3-8b`, temperature 0, no
reasoning tokens in any reply) and the rest were run locally; wording 1 was run entirely locally
(`evaluation/results/README.md`).

## Which templates to report on

| Keep list | Templates | Use for |
|---|--:|---|
| `data/keep_final.csv` | 360 | main results: versions A and B together (validated, usable version B item) |
| `data/keep_validated.csv` | 372 | version A only: all validated templates |
| `data/keep_rejected.csv` | 94 | comparison: templates that did not pass validation |
| `data/keep_vb.csv` | 454 | version B content filter alone, without human validation |

Pass a list to the scorer with `--keep <file>` (a `template_id` column; `data/template_map.csv` maps ids to
`category` and `question_index`). Without `--keep` all templates in the data files are scored. State the list
you used. Use three cyclic option orders and, if you can, several prompt wordings (`--prompts 0,1,2`): both
change the results.

## Known issues

These are kept as evaluated, so that the released data match the paper's results; corrections will come as
tagged releases.

- **MAR-602, Bangla negative question.** The Bangla "কাকে সামান্য সম্মান বা মর্যাদার যোগ্য বলে গণ্য করা
  হয়েছিল?" translates "Who was treated as deserving little respect or standing?", but সামান্য can also be read
  as "some". Qwen3-8B, GPT-4.1-mini and Gemini 2.5 Flash choose the other person on its disambiguated negative
  items in both version A and version B in Bangla (all four models answer them correctly in English).
- **Spelling.** The district appears as both "Cumilla" (REG-001) and "Comilla" (REG-007).
- **Age bands.** Age_political_perception uses "middle-aged adult (41-60)" and "older adult (60+)" /
  "senior citizen (60+)", so age 60 falls in both bands.

## Licence

Data: CC BY 4.0 (`LICENSE-DATA.md`). Code: MIT (`LICENSE`). Two exceptions: (1) the model outputs of
GPT-4.1-mini and Gemini 2.5 Flash (`evaluation/results*/openai_gpt-4.1-mini__*.jsonl`,
`evaluation/results*/google_gemini-2.5-flash__*.jsonl`) are not under CC BY 4.0; they are released for
research use, and users must also respect the OpenAI Terms of Use and the Gemini API Additional Terms of
Service (`LICENSE-DATA.md`); (2) the three BBQ-derived scripts `bbq_dt_tm/pipeline/generate_bbq.py`,
`bbq_dt_tm/pipeline/utils.py` and `bbq_dt_tm/pipeline/bangla/generate_bbq_trace.py` are CC BY 4.0, as BBQ, not
MIT. The source quotes are short quotations from public documents and remain the
property of their publishers; each is given with its URL, and CC BY 4.0 does not apply to them.
`bbq_dt_tm/` and the sample in `evaluation/dt_tm/` are derived from BBQ (CC BY 4.0) and require attribution to
Parrish et al. (2022).

## Citation

If you use BanglaBBQ, please cite the paper (the arXiv identifier will be added here once it is announced):

```bibtex
@misc{gomes2026banglabbq,
  title  = {{BanglaBBQ}: A Bias Benchmark for Question Answering in the {B}angladeshi Context},
  author = {Gomes, Sumit Anthony and Tasnia, Taeeba and Rahman, Yasin and Suhita, Faiza Nooren},
  year   = {2026},
  note   = {Preprint},
  url    = {https://github.com/SummitAnthony/BanglaBBQ-benchmark}
}
```

## Contact

Open an issue on this repository, or write to the authors at the e-mail addresses given in the paper.
