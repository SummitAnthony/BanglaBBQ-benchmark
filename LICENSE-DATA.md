# Data licence

The BanglaBBQ data is released under CC BY 4.0 and the code under MIT (`LICENSE`), with the exceptions
listed below.

## Summary

| Part of the release | Licence |
|---|---|
| Data: `data/`, `annotation/*.md` and `annotation/labeling_config.xml`, `evaluation/` result and report files, `bbq_dt_tm/` data files, except the model outputs below | CC BY 4.0 |
| Model outputs of GPT-4.1-mini and Gemini 2.5 Flash: `evaluation/results*/openai_gpt-4.1-mini__*.jsonl`, `evaluation/results*/google_gemini-2.5-flash__*.jsonl` | Not CC BY 4.0. Released for research use; users must also respect the providers' terms (see below) |
| Code: `*.py` scripts and notebooks, except the BBQ-derived scripts below | MIT (see `LICENSE`) |
| BBQ-derived scripts: `bbq_dt_tm/pipeline/generate_bbq.py`, `bbq_dt_tm/pipeline/utils.py`, `bbq_dt_tm/pipeline/bangla/generate_bbq_trace.py` | CC BY 4.0, as BBQ |
| `source_quote` text in the templates | Short quotations; owned by their publishers (see below) |

## BanglaBBQ data: CC BY 4.0

The BanglaBBQ data is released under the Creative Commons Attribution 4.0 International
licence (CC BY 4.0): <https://creativecommons.org/licenses/by/4.0/>

This is a short, human-readable summary. It is not the licence. The legal code at the link
above is the binding text.

You may:

- **Share:** copy and redistribute the data in any medium or format, for any purpose,
  including commercial use.
- **Adapt:** remix, transform and build on the data, for any purpose.

If you do, you must:

- **Give attribution:** cite the BanglaBBQ paper, link to the licence, and say whether you
  made changes. Do this in any reasonable way, but not in a way that suggests the authors
  endorse you or your use.
- **Add no further restrictions:** do not apply legal terms or technical measures that stop
  others from doing what the licence allows.

The data comes with no warranty.

Citation: Sumit Anthony Gomes, Yasin Rahman, Taeeba Tasnia and Faiza Nooren Suhita (2026). BanglaBBQ:
A Bias Benchmark for Question Answering in the Bangladeshi Context. Preprint.
<https://github.com/SummitAnthony/BanglaBBQ-benchmark>

## Model outputs of GPT-4.1-mini and Gemini 2.5 Flash

The replies of GPT-4.1-mini (OpenAI) and Gemini 2.5 Flash (Google) were obtained through OpenRouter.
Under the OpenAI Terms of Use (<https://openai.com/policies/terms-of-use/>) OpenAI assigns to the user
its rights in Output. Under the Gemini API Additional Terms of Service
(<https://ai.google.dev/gemini-api/terms>) Google does not claim ownership of generated content. These
outputs are released for research use. They are not covered by the CC BY 4.0 grant above, and users must
also respect those terms.

The outputs of Qwen3-4B and Qwen3-8B (open-weight models under the Apache 2.0 licence) are part of the
data and are released under CC BY 4.0.

## Attribution: `bbq_dt_tm/` is derived from BBQ

The files in `bbq_dt_tm/` are adapted from BBQ:

> Alicia Parrish, Angelica Chen, Nikita Nangia, Vishakh Padmakumar, Jason Phang, Jana Thompson,
> Phu Mon Htut, and Samuel R. Bowman. 2022. BBQ: A Hand-Built Bias Benchmark for Question
> Answering. In *Findings of the Association for Computational Linguistics: ACL 2022*.

- Source: <https://github.com/nyu-mll/BBQ>
- BBQ licence: CC BY 4.0, <https://creativecommons.org/licenses/by/4.0/>
- Cite Parrish et al. (2022) wherever these files are used.

What was changed (details in `bbq_dt_tm/README.md` and, per template, in
`bbq_dt_tm/sorting_logs/`):

1. **Sorted.** Each of the 343 templates in BBQ's 11 template files (nine categories and two
   intersectional ones) was sorted as DT (directly translated), TM (target-modified) or SR
   (removed) for Bangladesh, following the scheme of KoBBQ and PakBBQ. SR templates are not
   included. Six categories remain, with 76 DT and 64 TM templates.
2. **Target-modified.** In TM templates, American details (brands, places, institutions,
   names, jobs, customs) were replaced with Bangladeshi ones. Shared lists were changed: BBQ's
   US first names were replaced with 60 common Bangladeshi names, Muslim and Hindu, women and men,
   with both people in a pair sharing a religion (`bangladeshi_first_names.csv`), and U.S.-only
   entries were dropped from shared lists such as occupations and religions. Formatting errors, wrong answer keys and typos in BBQ's
   templates were fixed; each fix is listed in the sorting logs.
3. **Regenerated.** The rows were generated with BBQ's generation script, copied into
   `bbq_dt_tm/pipeline/generate_bbq.py` and `bbq_dt_tm/pipeline/utils.py` with the changes
   listed in `bbq_dt_tm/README.md`. These scripts remain under BBQ's CC BY 4.0 licence.
4. **Translated.** The templates and slot fillers were translated into Bangla by an LLM
   with the conventions of the newly authored part, and native Bangla speakers
   judged the translation acceptable (`bbq_dt_tm/BanglaBBQ_BN/`; method in
   `bbq_dt_tm/pipeline/bangla/README.md`).

These changes are the authors' own. Parrish et al. do not endorse them.

## Source quotations

Each of the 466 BanglaBBQ templates has a `source` (a URL) and a `source_quote` (a short
verbatim quotation from that page). The quotations come from public documents. They are
included only to show the evidence for each stereotype, and they remain the property of their
publishers. CC BY 4.0 does not apply to them. To reuse a quotation beyond that purpose, go to
the publisher at the given URL.

## Intended use (a request, not a licence term)

The data states real, harmful stereotypes about groups in Bangladesh. It is meant for
auditing and measuring social bias in language models. The authors ask that it not
be used to train or fine-tune models to reproduce these stereotypes. A low bias score on
BanglaBBQ is not proof that a system is unbiased.

This is a request about use. It is not a condition of the licence and does not change the
CC BY 4.0 terms above.
