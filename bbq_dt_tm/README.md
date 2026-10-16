# BanglaBBQ: DT and TM templates adapted from BBQ

This folder holds the parts of BanglaBBQ that come from the original BBQ benchmark
(Parrish et al., 2022). We follow the scheme used by KoBBQ and PakBBQ: each BBQ template was
sorted as

- **DT (directly translated):** the scenario and the stereotype both hold in Bangladesh, so only
  the language changes. Removing US-only entries from a template's word lists (for example
  "jock" or "a red head") keeps a template DT, because the sentence itself is untouched.
- **TM (target-modified):** the stereotype holds, but an American detail (a brand, place,
  institution, name, job or custom) had to be replaced with a Bangladeshi one, for example
  Walmart → Shwapno, 911 → 999, *Jeopardy* → a TV quiz show, "on welfare" → "living on government
  relief", cocaine → yaba. Fixing an error in BBQ's template (a typo, a formatting error, a wrong
  answer key or direction) does not by itself make it TM
  ([below](#errors-in-bbqs-templates-that-were-fixed)).
- **SR (removed):** the stereotype does not hold or means something different in Bangladesh.

BanglaBBQ's own newly authored categories (NA) are not in this folder.

The English files and their Bangla translation (`BanglaBBQ_BN/`) are both included. The DT and TM
templates were not annotated, as in PakBBQ, which validated only its newly added templates. The
Bangla was translated by an LLM with the conventions of the newly authored part,
and native Bangla speakers judged the translation acceptable (`pipeline/bangla/README.md`).

## Contents

| Category | DT templates | TM templates | SR templates | DT rows | TM rows | Rows per language |
|---|--:|--:|--:|--:|--:|--:|
| Age | 14 | 7 | 4 | 1,576 | 912 | 2,488 |
| Disability_status | 20 | 5 | 0 | 1,056 | 376 | 1,432 |
| Gender_identity | 13 | 30 | 7 | 152 | 4,656 | 4,808 |
| Physical_appearance | 15 | 7 | 3 | 752 | 544 | 1,296 |
| Religion | 4 | 1 | 20 | 128 | 32 | 160 |
| SES | 10 | 14 | 1 | 2,264 | 2,880 | 5,144 |
| **Total** | **76** | **64** | **35** | **5,928** | **9,400** | **15,328** |

This is paper Table 3. The row counts are the same in `BanglaBBQ_ENG/` and `BanglaBBQ_BN/`.

Five BBQ categories were removed entirely (SR): Nationality, Race_ethnicity,
Sexual_orientation, Race_x_SES and Race_x_gender (168 templates). With the 175 templates of the six
categories above, all 343 templates of BBQ's released template files were sorted.

```
bbq_dt_tm/
├─ BanglaBBQ_ENG/                   one file per category, as in PakBBQ_ENG/:
│   Age.jsonl  Disability_status.jsonl  Gender_identity.jsonl
│   Physical_appearance.jsonl  Religion.jsonl  SES.jsonl
├─ BanglaBBQ_BN/                    Bangla translation (same file names, same rows in the
│                                   same order; see pipeline/bangla/README.md)
├─ sorting_logs/                    one log per category, one row per BBQ template:
│   Age_sorting_log.csv  Disability_status_sorting_log.csv  Gender_identity_sorting_log.csv
│   Physical_appearance_sorting_log.csv  Religion_sorting_log.csv  SES_sorting_log.csv
├─ bangladeshi_first_names.csv      first names used in the name templates
├─ pipeline/                        scripts that rebuild every file in BanglaBBQ_ENG/ exactly
│   └─ bangla/                      Bangla translation: translated templates and fillers, and the
│                                   scripts that rebuild BanglaBBQ_BN/ (see its README.md)
└─ README.md
```

Each category file holds the DT rows first and then the TM rows, as in PakBBQ.

The sorting logs in `sorting_logs/` list every BBQ template in the category, including the SR
ones. Their columns are `category`, `bbq_question_index`, `decision` (DT, TM or SR),
`banglabbq_question_index`, `rows_eng`, `what_changes_or_why` (the exact before-and-after
wording of every change, or the reason for removal), BBQ's ambiguous context and negative
question, and `source`. The logs were written during sorting; the pipeline does not produce them.

## File format

Every row uses PakBBQ's fields, in PakBBQ's order:

`example_id, question_index, question_polarity, context_condition, category, answer_info,
additional_metadata {subcategory, stereotyped_groups, version, source},
context, question, ans0, ans1, ans2, label, type, id`

- **Rows come in blocks of four,** as in BBQ and PakBBQ: ambiguous/negative,
  disambiguated/negative, ambiguous/non-negative, disambiguated/non-negative. Each block uses one
  pair of people and one answer order.
- **Numbering.** `question_index` numbers templates within a category in BBQ order: DT templates
  first (1..k), then TM templates (k+1..), as in PakBBQ. SES template BBQ 8 was built last and
  appended as SES TM 24, so the other SES TM numbers stayed unchanged. The rows themselves do not
  carry BBQ's number (PakBBQ's rows do not either); the sorting logs map each BanglaBBQ number to
  its original BBQ template (`bbq_question_index` → `banglabbq_question_index`).
- **Other metadata.** `subcategory`, `stereotyped_groups`, `version` and `source` are BBQ's own
  values for that template.
- **Answers.** The unknown option is always "Unknown", as in PakBBQ. The person labels in
  `answer_info` follow BBQ; for example, gender word templates use man/woman/boy/girl, and name
  templates use F/M.
- **IDs.** `example_id` runs 0..n-1 within each file, as in PakBBQ. PakBBQ's `id` is one running
  number across the whole benchmark; in this release `id` equals `example_id` in every
  file, so ids repeat across files and overlap with the ids in `data/`. `pipeline/assign_ids.py`
  (see below) numbers rows across files for anyone who merges them; it was not run for this release.

## How the rows were generated

The rows were generated with BBQ's own script (`generate_from_template_all_categories.py`),
copied into `pipeline/generate_bbq.py`. The script changes are:

- **Settings:** file paths, the list of categories, the unknown option set to "Unknown" only,
  and a fixed random seed (2026).
- **Same-religion pairs:** when a template uses first names, both people are drawn from the same
  religion.
- **Balanced names in SES 8:** BBQ draws 6 random names for each version. With same-religion
  pairs, a random draw gives each version a different number of pairs (a lone Hindu name, for
  example, has no partner), so the two versions differed in size. Each version now draws 4 Muslim
  and 2 Hindu names, which gives 112 rows per version.
- **Proper-name flag:** the "use first names" flag is checked robustly. BBQ's check fails when
  pandas reads the flag as a boolean, which put job titles where names belong. PakBBQ's SES file
  shows this error ("landlord and farm worker are old friends…").

`pipeline/utils.py` is BBQ's helper file with one fix. When one person's description contains the
other's ("tattoos" / "no tattoos"), BBQ's matching could give both people the same label; the
longer, exact match is now assigned last.

On BBQ's original templates, the script reproduces BBQ's released data exactly, except for the
words BBQ itself picks at random (WORD slots and a sample of jobs or names).

### Shared lists

- **Jobs (SES):** dropped bartender, line cook, parking attendant and optometrist. The remaining
  9 lower-status and 11 higher-status jobs are all used.
- **Religions:** the other person is drawn only from Muslim, Hindu, Buddhist, Christian and
  Atheist. Jewish, Sikh, Mormon, Protestant and Catholic were dropped.
- **First names:** BBQ's 40 US names were replaced with 60 common Bangladeshi names: 30 female
  and 30 male, each 20 Muslim and 10 Hindu (`bangladeshi_first_names.csv`). Every pair is one
  woman and one man, or two people of any gender in SES 8, and both share a religion.

### Errors in BBQ's templates that were fixed

The wording of the scenarios is unchanged; each fix is listed in the sorting logs.

- **Lost directions:** Disability 4 and 19 had formatting errors (a semicolon inside a list, NAME
  lists in the wrong order, `{[NAME1}}`), so BBQ's release lost their "b" direction. Both now
  generate both directions.
- **Wrong correct answers:** Physical appearance 6 and 10, version b, had answer keys that
  contradicted the text. They now match the text.
- **Directions that cancelled out:** SES 9 and 10, version b, swapped the groups and also reversed
  the sentence, so b repeated a. Version b now gives the other direction.
- **Typos:** "monther", "on who was", "already already", "dressed in the a …", "load it to",
  "listening the advice", "talk the teacher", "heroine", "The on …", a missing full stop,
  lowercase "the" at the start of answers, and a sentence starting with a lowercase word.

### Checks

Every file passes these checks (`pipeline/finalize.py`):

- no unfilled slots;
- every answer slot is filled and the two people have different labels;
- exactly one unknown option per row;
- the correct answer is always "Unknown" in ambiguous rows and never in disambiguated rows;
- none of the dropped or replaced US terms remain. The term check matches substrings, so `finalize.py`
  also reports "welfare" in 128 Age TM rows; these are false positives from the intended replacement
  setting "the neighbourhood welfare society", not the dropped US term (welfare as public assistance);
- **disambiguated rows split exactly 50/50** between stereotype-consistent and inconsistent, for
  every template (as in BBQ and PakBBQ).

### Kept as in BBQ and PakBBQ

- **Repeated rows.** BBQ's script builds each pair of people in both orders. When both people of
  a pair are in the sample it starts from, the pair is built twice; versions a and b also share
  their ambiguous context. So the same question about the same two people can appear more than
  once. In BBQ's release such rows usually differ only in answer order or in the wording of the
  unknown option (BBQ has 436 such rows in SES and 118 in Disability). With the unknown option
  fixed to "Unknown", some become exact copies: 64 rows in SES and 18 in Disability_status here,
  against 104 and 12 in PakBBQ. They were kept, as in PakBBQ, because removing them would break
  the blocks of four and the 50/50 split.
- **Trailing space.** 76 answers in Disability_status DT 9 and 16 (BBQ 10 and 20) end in a space
  ("The classmate "), as the same answers do in BBQ and PakBBQ.

## Sources

- **Source field:** every template keeps BBQ's source for that template and version, as
  PakBBQ did. All 15,328 rows match BBQ's own data. The exception is Disability 4b and 19b,
  which BBQ's release lacked; they carry the source of BBQ's template rows.
- **Link status:** the 68 distinct links were checked on 6 Oct 2026.
  - 33 open.
  - 28 could not be checked automatically: the site blocks automated access (PubMed/PMC,
    PsycNet, Wiley, Taylor & Francis, Hindawi, the Washington Post, CNN and others).
  - 7 are broken:

| Link | Problem | Used by (BBQ template → BanglaBBQ) |
|---|---|---|
| atlascorps.org …negative-stereotypes-and-attitudes-linked-to-disability | 404 | Disability 11 → DT 10, 14 → DT 12 |
| idp.springer.com/authorize/casa?… (s11199-011-0051-0) | sign-in link with an expired token | Gender 6 → DT 5, 20 → TM 18, 31 → TM 26, 39 → TM 32 |
| bakerlaw.com …UPS-Ban-on-Deaf-Drivers… | 404 | Disability 4 → DT 4 |
| connecthear.org …top-10-misconceptions-about-deaf-people… | goes to the homepage | Disability 16 → DT 14 |
| dvrcv.org.au …rigid-gender-roles-and-stereotypes | goes to the homepage | Gender 43 → TM 36, 44 → TM 37 |
| easterseals.com …myths-facts.html | 404 | Disability 17 → TM 23 |
| webmd.com …eye-deformity-prejudice | goes to an unrelated page | Physical appearance 13 → DT 9 |

BBQ's own data also gives different sources for versions a and b of a few templates (Age 8, 14
and 20, and Disability 3, whose two DOIs differ in the last digit, .019 and .020). These are
kept as BBQ has them.

## Differences from PakBBQ's file structure

The files follow PakBBQ's layout: the same fields in the same order, the same four metadata keys,
one file per category with DT rows then TM rows, `example_id` 0..n-1 per file, blocks of four rows,
"Unknown" as the unknown option and both directions split 50/50. Two differences remain:

- **Benchmark-wide `id`:** not assigned in this release (`id` = `example_id`). To assign it, run
  `python pipeline/assign_ids.py <English folder>` on the folder holding every category file
  (NA, DT and TM), and the same on the Bangla folder; it numbers all rows across the files in
  alphabetical order of file name, as PakBBQ does.
- **Rows per template:** templates whose lists were not changed have exactly BBQ's number of rows
  (for example 200 per gender name template, as in BBQ and PakBBQ). Others differ because of the
  list changes above. PakBBQ's counts also differ from BBQ's wherever it changed lists (for
  example, 272 rows per SES job template against BBQ's 480).

## Rebuilding

```
git clone https://github.com/nyu-mll/BBQ
bash pipeline/build.sh BBQ/templates BanglaBBQ_ENG
```

Run these commands from inside `bbq_dt_tm/`. They need bash, Python 3 (called as `python3`) and pandas,
so they run on Linux or macOS; on Windows use WSL, or Git Bash with `python3` on the PATH. They reproduce
every file in `BanglaBBQ_ENG/` byte for byte on Linux, macOS and WSL. Under Git Bash on Windows, Python
writes CRLF line endings, so the rebuilt files differ from the shipped ones in line endings only.

## Licence and attribution

BBQ is released under CC BY 4.0. These files are adapted from BBQ's templates; cite Parrish et
al. (2022) wherever they are used. The DT/TM scheme follows KoBBQ (Jin et al., 2024) and PakBBQ
(Hashmat et al., 2025).
