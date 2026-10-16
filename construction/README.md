# construction/

How the benchmark was built, and the tools to check it.

| File | What it is |
|---|---|
| `drafting_instructions.md` | The instructions given to the LLM assistants with whose help the authors built the templates (paper §3.2), reproduced from the development repository (see the note at its top). Written for the first category (Marital_status); Educational_background, Regional_origin and Mental_health_status used the same schema, roles and checks with other target groups. The Age_political_perception templates were written into a script instead (below). It defines the template schema (§3), the eight-record expansion (§3.3), the roles (§4), the workflow with an approval step before compilation (§5), the source rules (§6) and the per-record assertions (§9). Its §1 plan for the Bangla (Google Translate + human post-edit) was not followed ([Bangla](#bangla)). |
| `source_tool.py` | Fetches a source URL and checks that a passage occurs verbatim on the page (HTML or PDF). The check every template had to pass. |
| `compile_records.py` | Expands `data/templates.jsonl` into the four record files in `data/` (versions A and B, English and Bangla). `--check` verifies that the released files are exactly this expansion. |
| `check_data.py` | Consistency checks on everything in `data/` and on the model outputs in `evaluation/` (complete runs; every stored answer re-parsed from the raw reply), and a privacy scan of the whole release (no e-mail address, local path or annotator-level field). |
| `reports/` | The validation and statistics reports written during construction, one folder per category (below). |
| `development_scripts/` | Scripts used during construction and version B building, with a unit test, as they were. Kept for provenance; not needed to use the benchmark. See `development_scripts/README.md`. |

The record format is described in `data/README.md`.

## Pipeline

1. **Scope.** For each category the authors fixed the target groups and the areas of life to cover (for
   example, for Marital_status: housing, employment, social exclusion, property and inheritance, remarriage).
2. **Writing.** The authors built each template in English with the help of LLM assistants, from a
   passage of a public document that discusses the attribute in Bangladesh (paper §3.2), and reviewed and
   approved every template. In four categories (Marital_status, Educational_background, Regional_origin,
   Mental_health_status) the assistants followed `drafting_instructions.md` (`DATASHEET.md` section 3.1). Acceptable sources (§6): established Bangladeshi newspapers, peer-reviewed
   journals, academic books, and recognised rights and development bodies; not blogs, forums, SEO or
   AI-generated pages, and not Wikipedia as the citation itself. Each template has exactly one `source` URL
   and a `source_quote`, a passage copied verbatim from that page. The disambiguating sentence always
   describes the stereotype-consistent outcome (version A). Age_political_perception was written differently:
   its 100 templates were written as literals into one script, `development_scripts/gen_age_politics.py`,
   which writes them and their records, and cite 11 sources ([below](#per-category)).
3. **Source verification.** Every source was re-fetched with `source_tool.py`, which confirmed that the
   quoted passage occurs on the page, and each passage was checked for whether it supports the stereotype
   the template encodes. Templates that failed were re-grounded on another verified source or dropped.
4. **Schema and duplicate checks.** All fields present, the BBQ `X` / `non<X>` label convention, the
   disambiguating sentence in the stereotype-consistent direction (a heuristic; hits are listed as warnings
   to verify by hand), distinct negative and non-negative questions, no group name inside a question, no
   placeholders, no near-duplicate scenarios.
5. **Compilation.** Each template was expanded into eight records, with the §9 assertions checked on every
   record before it was added. `compile_records.py` reproduces this expansion from `data/templates.jsonl`.
6. **Bangla.** See [Bangla](#bangla).
7. **Version B.** See [Version B](#version-b-counter-stereotypical).
8. **Human validation.** Native annotators judged every template; see `annotation/README.md`.

## Per category

| Category | Id prefix | Templates | Distinct source URLs | Domains | Reports in `reports/` |
|---|---|--:|--:|--:|---|
| Marital_status | `MAR-` | 100 | 57 | 19 | `marital_status/` |
| Educational_background | `EDU-` | 95 | 32 | 7 | `educational_background/` |
| Regional_origin | `REG-` | 100 | 17 | 9 | `regional_origin/` |
| Mental_health_status | `MEN-` | 71 | 27 | 12 | `mental_health_status/` |
| Age_political_perception | `APO-` | 100 | 11 | 8 | `age_political_perception/` |
| **All** | | **466** | **144** | **35** | |

Each folder has `validation_report.md` (source and schema validation per template), `stats_report.md`
(counts per target group, subcategory and source domain; not written for Age_political_perception) and
`bangla_validation.md` (the automatic checks on the Bangla file). The `stats_report.md` files of
Marital_status and Educational_background were written before the last source fixes described below, so
some of their source counts differ from the released data; the counts in the table above (paper §4.2) are
those of the released data. What the validation reports record:

- **Marital_status.** 100 templates examined. The report was regenerated after a later citation fix
  (two templates). In that run 97 passed; for MAR-411, MAR-413 and MAR-414 the source page (academia.edu)
  refused the automated fetch (HTTP 403), so the check could not be repeated. The three templates are in the
  data; their quotes were checked manually against the source document.
- **Educational_background.** 100 written; 95 passed; 5 (EDU-081, EDU-092, EDU-093, EDU-094, EDU-098) were
  marked NEEDS-REVIEW because the quoted passage documents a neighbouring fact, not the encoded stereotype,
  and were dropped. The first pass checked the passages of two World Bank documents (EDU-010, EDU-014)
  through the World Bank documents API, because the landing pages load their text by script. A later review
  (the report's "Post-review re-grounding" section) found these and three other quotes not verbatim on a
  fetched page and fixed them: EDU-014 (with EDU-005 and EDU-015) was re-grounded on a Prothom Alo English
  article, and EDU-010 was repointed to the World Bank plain-text rendition of its document, with a quote in
  the document's own wording. The released data has these sources.
- **Regional_origin.** 100 templates, each with a passage verified on the fetched page when the report was
  written. An external check during construction found 16 provenance failures (9 passages not found or not
  visible on the page, 7 on a PDF host that refused requests); all 16 were re-grounded on other sources, and
  no template cites those hosts any more. Several of the current hosts refuse automated requests today
  ([below](#sources-that-refuse-automated-checks)).
- **Mental_health_status.** 71 templates examined, 71 passed.
- **Age_political_perception.** 100 templates examined, 100 passed. Unlike the other categories, the 100
  templates of this category, with their sources and quotes, are written as literals into one script,
  `development_scripts/gen_age_politics.py`, which writes them out with their records. The template text
  was written by one author and reviewed by another. The 100 templates share 11 quotes from 11 URLs (in the
  other categories a quote is used by at most 4 templates), on young people's political participation,
  elections and turnout, protest, corruption, press freedom and media use in Bangladesh:

  | Templates | Source | Quote (start) |
  |--:|---|---|
  | 18 | cpd.org.bd (youth politics) | "Youth representation will become meaningful only when the energy of mobilisation is translated into institutional space ..." |
  | 14 | freedomhouse.org (Freedom in the World 2024) | "Election day and the preceding campaign were marked by political violence, ballot stuffing, ..." |
  | 14 | thedailystar.net (youth vote) | "Nearly 44 percent of Bangladesh’s electoral roll ... are between the ages of 18 and 37" |
  | 12 | tbsnews.net (Gen Z and protest politics) | "thousands of young people -- most of them Gen Z -- turned social media into a space of digital resistance" |
  | 10 | hrw.org (World Report 2024) | "Journalists faced increasing attacks for exercising their right to freely criticize government policies ..." |
  | 9 | theconversation.com | "Young Bangladeshis – especially young women – have been marginalised by traditional, hierarchical and patriarchal political structures." |
  | 5 | ti-bangladesh.org (CPI) | "Bangladesh’s position in the Corruption Perceptions Index is evidence of the prevalence of corruption ..." |
  | 5 | thedailystar.net (turnout) | "The overall national lowest turnout was recorded in Dhaka-15 constituency -- only 13 percent." |
  | 5 | thedailystar.net (media survey) | "Facebook is ranked as the most trusted, ..." |
  | 4 | tbsnews.net (CPI 2024) | "Bangladesh scored 23 out of 100 in 2024, ..." |
  | 4 | en.prothomalo.com | "Overall, 88 per cent of respondents said they use mobile phones to follow media." |

  Its results are reported per category in `evaluation/reports/*/report.md`.

## Sources that refuse automated checks

`python construction/source_tool.py checkfile data/templates.jsonl`, run on 2026-10-12, found the quote on the
fetched page for 441 of the 466 templates. For the other 25 the page could not be fetched; no fetched page
lacked its quote. 22 of the 25 templates are in the main evaluation set.

| Source | HTTP status | Templates |
|---|---|---|
| minorityrights.org/communities/biharis/ | 403 | REG-019, REG-028, REG-030, REG-035, REG-040, REG-046, REG-047, REG-048, REG-054, REG-057, REG-092, REG-099, REG-100 |
| academia.edu/8715037 (Standard Dialect Ideology in Bangladesh) | 403 | REG-009, REG-024, REG-037, REG-053, REG-094 |
| academia.edu/87169885 (Gender Role, Working Women and Family) | 403 | MAR-411, MAR-413, MAR-414 |
| reliefweb.int (J-MSNA, host communities in Teknaf and Ukhiya) | 202, empty body | REG-077, REG-079 |
| researchgate.net/publication/316146137 | 403 | MEN-507 |
| researchgate.net/publication/401529937 | 403 | MEN-508 |

The Regional_origin and Mental_health_status validation reports record these sources as verified when the
reports were written; MAR-411, MAR-413 and MAR-414 already failed in the last Marital_status run (above).
The three templates of the 25 that are not in the main evaluation set are MAR-414, REG-024 and REG-099.

## Source counts

Several templates share a source: 466 templates cite 144 distinct URLs on 35 domains (paper §4.2). The most
cited domain is thedailystar.net (109 templates). Each quote was checked for whether it supports the
stereotype its template encodes (the Educational_background report rates each passage "strong", "partial" or
"off-topic"; the five rated off-topic were dropped). A source documents the stereotype in Bangladesh; do not
read the source link as evidence that a stereotype is true or widely held.

## How a template becomes records

Version A: eight records per template and language, in this order (`compile_records.py`):

| Records | Stored answer order | Context | Question | Correct answer |
|---|---|---|---|---|
| 1 / 5 | [target, Unknown, non-target] / [non-target, target, Unknown] | ambiguous | negative | Unknown |
| 2 / 6 | same | ambiguous + disambiguating sentence | negative | target |
| 3 / 7 | same | ambiguous | non-negative | Unknown |
| 4 / 8 | same | ambiguous + disambiguating sentence | non-negative | non-target |

Per template the labels are 0, 1, 2 in the ratio 2 : 3 : 3, and every ambiguous record has Unknown as its
correct answer. `example_id` runs from 0 in template order; template *k* (from 0) has ids 8*k* to 8*k* + 7 in
both languages. The record format is PakBBQ's: BBQ's 13 keys in BBQ's order, plus `type` and `id`. The English Unknown option is "Unknown"; the
Bangla one is "যথেষ্ট তথ্য নেই" ("not enough information"), chosen after a wording pilot
(`evaluation/unknown_wording/report.md`).

The 3,728 records per language are `data/banglabbq_en.jsonl` and `data/banglabbq_bn.jsonl`.

## Bangla

1. **Translation.** The text fields of the English templates (`ambiguous_context`, `disambig_sentence`,
   both questions, both answers, both short labels) and the version B sentences were translated by
   LLM-assisted translation following the terminology, register and wording choices set by a
   native-Bangla-speaking author (paper §3.5). For Marital_status, Educational_background, Regional_origin
   and Mental_health_status a second author generated the translations with an LLM following that
   guidance.

   The text is direct sentence translation in a formal, neutral register of standard Bangladeshi Bangla,
   with no Latin script, and aims to give both people of a template the same register (both checked in
   step 3, where 32 register flags in 8 Age_political_perception templates were not adjudicated). Group
   tags in `answer_info` stay in English.
2. **Compilation.** The Bangla templates were expanded exactly like the English ones, so English and Bangla
   records align one to one by `example_id`.
3. **Automatic checks.** All Bangla was then checked automatically, without an LLM, by a script of the
   development repository that is not part of this release (results in `reports/*/bangla_validation.md`):
   (a) structural invariants, (b) alignment with the English file, (c) leftover Latin-script words,
   (d) consistency of the same template text across its eight records, (e) placeholders, all with 0 flags in
   all five categories; (f) register symmetry between the two people, a heuristic whose hits need a
   judgment: 0 flags in Marital_status and Regional_origin; in Educational_background the first run flagged 13
   templates (52 flags), whose Bangla disambiguating sentences were rewritten in a second pass of the LLM translation so that both people's clauses
   use the same construction, after which the check found 0 flags (`reports/educational_background/bangla_validation.md`);
   4 flags in Mental_health_status (one template, MEN-201, adjudicated as a false positive in its report,
   written during the translation run); and 32 in Age_political_perception (8 templates, not adjudicated).
4. **Unknown option.** The Bangla Unknown option was changed from অজানা to "যথেষ্ট তথ্য নেই" after the
   wording pilot (`evaluation/unknown_wording/report.md`).
5. **Quality judgment.** Several native Bangla speakers then judged the quality of the Bangla and found it
   acceptable (paper §3.5). The Bangla annotators, who saw the Bangla scenario, question and group labels
   of every template, were also asked to report translation problems and reported none
   (`annotation/README.md`, Disclosures).

## Version B (counter-stereotypical)

In version A the disambiguating sentence always describes the stereotype-consistent outcome, so version A
alone cannot separate reading comprehension from bias in disambiguated contexts. For every template an
author wrote a second disambiguating sentence describing the opposite outcome (paper §3.3). Its Bangla was
produced like the rest of the Bangla ([Bangla](#bangla), step 1). They are stored in
`version_b.{en,bn}.disambig_sentence` of `data/templates.jsonl`.

`compile_records.py` turns each template into four version B records per language: records 2, 4, 6 and 8 of
version A with the version B sentence, correct answers swapped (negative question: non-target; non-negative
question: target), `example_id` = version A id + 100000 and `additional_metadata.version` = `"b"`. The
ambiguous records are the same in both versions and are not repeated. The 1,864 records per language are
`data/banglabbq_vb_en.jsonl` and `data/banglabbq_vb_bn.jsonl`.

A content review of all version B items found 12 templates whose question presupposes something that fits
only the stereotyped person, or whose counter-stereotypical answer is strained:

MAR-103, MAR-308, MAR-511, MAR-609, MAR-712, REG-022, REG-024, REG-080, REG-098, REG-099, MEN-311, EDU-041.

Example, MAR-103: the scenario concerns a marriage that broke down, comparing "the newly divorced woman" with
"a married woman"; the negative question is "Who was blamed for the marriage falling apart?". In version B
the married woman is blamed for the divorced woman's broken marriage.

These 12 templates keep their version B records in the data files but are excluded from version B scoring:
`data/keep_vb.csv` lists the other 454 templates (`version_b.usable` in `data/templates.jsonl`). All 12
passed human validation, so the main evaluation set (`data/keep_final.csv`) has 372 − 12 = 360 templates.
The version B sentences were not part of the human validation, which showed annotators the ambiguous
scenario only; they were checked by the authors.

Version B sentences are not minimal edits of version A. In English they are 32.4 words long on average
against 29.5 for version A (Bangla 29.3 against 27.2), longer in 279 of 466 templates, and more often state a
reason for the outcome (`DATASHEET.md`, section 3.3). Read `diff_dis` with this in mind: the two directions
are not matched in wording.

## Commands

From the repository root. `compile_records.py` and `check_data.py` use the standard library only.
`source_tool.py` also needs `curl` and, for PDF sources, `pdftotext` (poppler) on the path.

```
python construction/check_data.py                                  # all consistency checks
python construction/check_data.py --quick                          # without the model-output files
python construction/compile_records.py --check                     # records == expansion of the templates
python construction/compile_records.py                             # rewrite the four record files in data/
python construction/source_tool.py checkfile data/templates.jsonl  # re-verify every source passage (network; slow)
python construction/source_tool.py check <url> "<passage>"         # one passage
python construction/source_tool.py text <url>                      # print the page text the check sees
```

`source_tool.py` fetches with `curl` and a browser user agent, strips HTML (or converts PDF), unifies curly
and straight quotes, collapses white space, and tests whether the passage occurs in the page text, ignoring
case. Sources move, change and disappear, and some sites refuse automated requests: a failed re-check today
does not mean that the passage was not on the page when the template was built. On 2026-10-12, 25 templates
failed this way ([Sources that refuse automated checks](#sources-that-refuse-automated-checks)).

## Reading the reports

The reports are copied as written during construction. File names in them (for example `validated.jsonl`,
`banglabbq_region_eng.jsonl`, `compile_banglabbq.py`) refer to the development repository. Ids in the Bangla
validation reports are record ids within the per-category development file, not the `example_id` of the
released files. Some reports mention a political-affiliation category; it was withdrawn and is not part of
BanglaBBQ.

The Bangla validation reports name the development scripts of the translation pipeline (`compile_bangla.py`,
`validate_bangla.py`), which are not part of this release, and use its working vocabulary: "Task 8", "Task 9"
and "Tasks 8-10" (steps of the development plan, one category each), "batch" (groups of 15-20 templates
translated together), "the translation brief" (the plan's translation conventions), and "early drafts ...
caught during translation". How the released Bangla text was produced is described in [Bangla](#bangla),
step 1.
