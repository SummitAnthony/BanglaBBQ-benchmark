# construction/development_scripts/

Scripts used while the benchmark was built and extended with version B, with a unit test. They are copied
as they were and kept for provenance, so that the English construction steps and the version B build can be
read in the code that ran them. The development scripts of the Bangla translation pipeline are not part of
this release; how the Bangla was produced and checked is described in `construction/README.md`, "Bangla",
and the results of the automatic checks are in `construction/reports/*/bangla_validation.md`.

- They were written for the layout of the development repository (`templates/`, `output/`, `scripts/`,
  `reports/`, per-category folders), which is not part of this release. Paths inside them point there, and
  most of them will not run here without changes. Each script starts with a note saying so.
- They are **not needed to use the benchmark**. The released data are rebuilt and checked with
  `construction/compile_records.py` and `construction/check_data.py`; sources are re-checked with
  `construction/source_tool.py` (see `construction/README.md`).
- The BBQ-derived part of the release, `bbq_dt_tm/`, has its own pipeline and does not use these scripts.
- Docstrings cite sections such as `CLAUDE.md §3.3` or `§9`; these are the sections of
  `construction/drafting_instructions.md`, which was the development repository's `CLAUDE.md` at the time.

## Scripts

Location in the development repository: `scripts/`, except where noted.

| File | Step | Role during construction |
|---|---|---|
| `validate.py` | English: source + schema validation | Validator for Marital_status (`drafting_instructions.md` §4.3). Merges the author files; checks fields, the `X` / `non<X>` labels, the direction of the disambiguating sentence, the question pair, group names inside a question, placeholders, duplicate ids and near-duplicates; re-fetches every source through `source_tool.py` and checks the quote. Writes the validated template file and `validation_report.md`. |
| `validate_category.py` | English: source + schema validation | The same checks for any category (`--category`). |
| `stats.py` | English: statistics | The statistician (§4.4). `templates` mode: counts per target group, subcategory and source domain; `records` mode: the invariants of a compiled file (labels 2 : 3 : 3, ambiguous / disambiguated and negative / non-negative 50/50, 8 records per template). Source of the `stats_report.md` files. |
| `compile.py` | English: compilation | Expands template objects into the eight BBQ/PakBBQ records per template (§3.3). Replaced by `construction/compile_records.py`, which produces the same expansion from `data/templates.jsonl`. |
| `gen_age_politics.py` | English: Age_political_perception | Contains the 100 Age_political_perception templates, each with its source URL and verbatim quote, and writes them and their 800 English records. |
| `build_combined_v2.py` | Combine | Concatenates the five per-category files into one English and one Bangla file and renumbers `example_id` / `id` from 0. These combined files became `data/banglabbq_en.jsonl` and `data/banglabbq_bn.jsonl`. |
| `generate_all_version_b.py` | Version B, English | Builds per-category English version B files from the authors' version B sentences: replaces the disambiguating sentence, swaps the correct answer of the disambiguated records, keeps the ambiguous records, and restarts `example_id` at 0 in each file. |
| `generate_all_version_b_bangla.py` | Version B, Bangla | The same for the Bangla files. |
| `build_version_b_eval.py` | Version B, evaluation files | Development location: `evaluation/version_b/`. Rebuilds every version B record from the current version A record (only `context` and `label` come from the version B files), keeps the disambiguated records only, sets `example_id` = version A id + 100000 and `version` = `"b"`, and writes the list of usable templates (`keep_vb.csv`) without the 12 templates excluded after the content review. Its output became `data/banglabbq_vb_{en,bn}.jsonl` and `data/keep_vb.csv`. |
| `import_closed_src_vb.py` | Version B, model outputs | Development location: `evaluation/version_b/`. The GPT-4.1-mini and Gemini 2.5 Flash version B runs were made on the per-category version B files, whose ids restart at 0; this script maps each call to the version B id above and keeps the disambiguated records only. |

## Tests

Location in the development repository: `scripts/tests/`. It needs `pytest`. Run from this folder with
`python -m pytest tests -q` (one test, which passes in this layout).

| File | Tests |
|---|---|
| `tests/test_build_combined_v2.py` | Concatenation and renumbering in `build_combined_v2.py`. |
| `tests/fixtures/combined/cat_a.jsonl` | Small record file used by the combine test. |
| `tests/fixtures/combined/cat_b.jsonl` | Second small record file used by the combine test. |
