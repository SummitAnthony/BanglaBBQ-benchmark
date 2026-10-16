# Datasheet for BanglaBBQ

This datasheet answers the questions of *Datasheets for Datasets* (Gebru et al., 2021) and adds the
elements of a data statement (Bender and Friedman, 2018). It covers the release of the paper
"BanglaBBQ: A Bias Benchmark for Question Answering in the Bangladeshi Context" (Gomes, Rahman, Tasnia
and Suhita, 2026). Most numbers below can be recomputed from a file in this release, which is named. The
exceptions come from runs or material that are not released: the 200-record pilot of the two
Bangla-specific models (section 6); the per-call outputs of the Unknown wording pilot (only its report,
`evaluation/unknown_wording/report.md`, is released); the annotation disclosures (section 3.4), taken from
the annotator-level exports; the relevance-rating and
answer-pattern figures also taken from those exports (the share of 3-star ratings, the number of accounts
with 3 stars on every template, and the number of templates on which two accounts chose the same option,
such as the two Bangla Marital_status accounts that agree on 97 of 100 templates; section 3.4 and
`annotation/agreement.md`, "Relevance ratings and answer patterns"; the counts of templates by mean
relevance can be recomputed from `data/validated_templates.csv`); the dates of section 3.5 that come
from the development repository's history; and the source re-check of 2026-10-12
(section 3.2), a network run that can be repeated with `construction/source_tool.py checkfile` but whose
result can change as pages change. `annotation/agreement.py` recomputes every value of the agreement table
in `annotation/agreement.md` (paper Table 1), intervals included, exactly from the released counts.

Section numbers such as "section 3.4" refer to this datasheet; the paper's sections and tables are cited as
"paper §N" and "paper Table N".

> **Content warning.** The data states harmful stereotypes about real social groups in Bangladesh.
> It is released for auditing language models only. Do not use it to train or fine-tune models to
> reproduce these stereotypes. A low bias score is not proof that a system is unbiased.

## 1. Motivation

**For what purpose was the dataset created?** To measure whether language models answering a
question fall back on stereotypes that are documented in Bangladesh, in English and in Bangla. The
format is that of BBQ (Parrish et al., 2022) as adapted by KoBBQ and PakBBQ: a model reads a short
scenario about two people and answers a question about them. When the scenario does not contain the
answer (ambiguous context), the correct answer is "Unknown"; choosing the stereotyped person instead
is evidence of reliance on the stereotype. When a disambiguating sentence gives the answer, the test
is whether the model follows the evidence.

**What gap does it fill?** Existing BBQ adaptations target other societies. BanglaBBQ adds five
newly authored categories specific to Bangladesh (type `NA`, newly authored; PakBBQ uses the same label
for its newly added templates, and KoBBQ calls such templates newly created, NC), each template grounded in
a public document about Bangladesh, with parallel English and Bangla text. It also adapts BBQ's own
templates to Bangladesh (`bbq_dt_tm/`, end of section 2).

**Who created it, and who funded it?** Sumit Anthony Gomes, Yasin Rahman, Taeeba Tasnia and Faiza Nooren
Suhita (BRAC University, Dhaka, Bangladesh). The work received no funding.

## 2. Composition

### What do the instances represent?

The unit of construction is a **template**: a fictional scenario about two people who differ in one
attribute (for example a divorced woman and a married woman). Each template has

- an ambiguous context that does not say which person the question is about;
- a disambiguating sentence for **version A**, which always describes the stereotype-consistent
  outcome, and one for **version B**, which describes the opposite outcome;
- a negative question (who has the negative attribute) and a non-negative question;
- three answers: the target group (the group the stereotype is about), the non-target group, and
  Unknown;
- one `source` URL and a `source_quote` copied verbatim from that page;
- the human validation result.

All 466 templates are in `data/templates.jsonl`, with the English and Bangla text side by side and
each template's source URL, verbatim quote and validation outcome (the 94 rejected templates are marked
`validated` = false there and in `data/validated_templates.csv`). The record files carry the source URL in
`additional_metadata.source`.

The unit of evaluation is a **record** in the PakBBQ format (BBQ's 13 keys in BBQ's order, plus `type`
and `id` as in PakBBQ). Version A
gives 8 records per template and language: 2 contexts (ambiguous, disambiguated) x 2 question
polarities x 2 stored answer orders.

### How many instances are there?

| Category (`category`) | Templates | Version A records per language | Validated | Validated and in the final set | Final-set records per language (8 version A + 4 version B per template) |
|---|--:|--:|--:|--:|--:|
| `Marital_status` | 100 | 800 | 80 | 75 | 900 |
| `Age_political_perception` | 100 | 800 | 62 | 62 | 744 |
| `Regional_origin` | 100 | 800 | 85 | 80 | 960 |
| `Educational_background` | 95 | 760 | 77 | 76 | 912 |
| `Mental_health_status` | 71 | 568 | 68 | 67 | 804 |
| **All** | **466** | **3,728** | **372** | **360** | **4,320** |

Rows in the order of paper Tables 1 and 2; the last four columns are the paper's Auth., Ret., Eval. and
Inst. (Table 2). Sources: `data/templates.jsonl`, `data/validated_templates.csv`, `annotation/agreement.md`.

| File | Records | Content |
|---|--:|---|
| `data/banglabbq_en.jsonl`, `data/banglabbq_bn.jsonl` | 3,728 each | Version A, all 466 templates |
| `data/banglabbq_vb_en.jsonl`, `data/banglabbq_vb_bn.jsonl` | 1,864 each | Version B, the 4 disambiguated records of every template |
| `data/validated/banglabbq_{en,bn}.jsonl` | 2,976 each | Version A, the 372 validated templates |
| `data/validated/banglabbq_vb_{en,bn}.jsonl` | 1,440 each | Version B, the 360 templates of the final set |
| `data/keep_validated.csv` / `keep_rejected.csv` | 372 / 94 ids | Validated / not validated templates |
| `data/keep_vb.csv` | 454 ids | Templates with a usable version B item |
| `data/keep_final.csv` | 360 ids | Validated and usable in version B: the main evaluation set |
| `data/validated_templates.csv` | 466 rows | Per-template vote counts and outcome |
| `data/template_map.csv` | 466 rows | `template_id` to (`category`, `question_index`) |

Version B records have `example_id` = version A `example_id` + 100000, the counter-stereotypical
sentence in `context`, the swapped label and `additional_metadata.version = "b"`. The ambiguous
records of version B are the same as those of version A and are not repeated.

The release also contains model outputs (`evaluation/results/`, `evaluation/results_vb/`,
`evaluation/results_dt_tm/`: one line per model call, raw answer included) and `bbq_dt_tm/`, BBQ's
own templates sorted for Bangladesh (see "bbq_dt_tm/" at the end of this section).

### Labels and annotations

- `label` in each record: the index of the correct answer. Ambiguous records: always Unknown.
  Version A disambiguated records: the target for the negative question, the non-target for the
  non-negative question. Version B: the reverse. Version A label counts are 932 / 1,398 / 1,398 for
  `ans0` / `ans1` / `ans2` (ratio 2:3:3) in each language.
- `answer_info`: for each answer, a short label and a group tag (`X` / `non<X>` / `unknown`, BBQ
  convention); the tags identify the stereotype-aligned answer for the bias scores.
  `additional_metadata.stereotyped_groups` names the stereotyped group; the scorer does not string-match
  it for these records (paper §3.3).
- Per template: annotator vote counts (intended target / other group / Can't tell), mean relevance,
  the keep decision, version B usability (`data/validated_templates.csv`; also the `validation` and
  `version_b.usable` fields of `data/templates.jsonl`).

### Groups described (subpopulations)

The 466 templates name 47 distinct `stereotyped_groups` strings (46 after merging the spellings
"people from Cumilla" and "people from Comilla"; the strings are not used for scoring, which uses the
answer tags) in 151 category and subcategory pairs. In Marital_status the subcategory is a free-text label
(65 of 100 contain spaces, e.g. "social respect"); the other categories use snake_case tags. Examples per
category:

| Category | Stereotyped groups (templates) |
|---|---|
| Marital_status | divorced women (20), widows (18), married women (18), unmarried women (15), unmarried men (12) (the never-married women and men of paper §4.1), deserted women (6), women in polygamous marriages (5), others |
| Educational_background | madrasa-educated people (35), English-medium educated people (25), people with little formal education (16), Bangla-medium educated people (15), people with vocational or technical education (4) |
| Regional_origin | Urdu-speaking Biharis (15), tea garden worker communities (12), Rohingya refugees (12), char dwellers (11), people from Noakhali (10), Indigenous people of the Chittagong Hill Tracts (10), people from Barishal (6), people from Rangpur (6), others |
| Mental_health_status | people with mental illness (40), people with depression (18), people with schizophrenia (5), people with anxiety (4), others |
| Age_political_perception | young adults (18-25) (49), older adults (60+) (22), senior citizens (60+) (14), middle-aged adults (41-60) (10), young voters (18-25) (5) |

The categories are not balanced: Mental_health_status has 71 templates, the others 95 or 100, and
some groups have one or two templates.

### Sources attached to the templates

Each template has one source URL and one verbatim quote: 144 distinct URLs on 35 domains (counting
`www.x` and `x` as one), 315 distinct quotes (`data/templates.jsonl`). All quotes are in English. Mean quote
length (whitespace tokens) is 19.1 words over the 466 template quotes and 18.1 words over the 315 distinct
quotes (maximum 53).

| Kind of source | Templates | Distinct URLs |
|---|--:|--:|
| Bangladeshi newspapers (The Daily Star, The Business Standard, Prothom Alo English, Dhaka Tribune, New Age, The Financial Express, UNB) | 276 | 95 |
| Research articles and academic commentary (PubMed Central, Springer, Cambridge, PLOS, The Conversation and others) | 96 | 34 |
| Reports of rights, development and policy organisations (HRW, Freedom House, CPD, TI Bangladesh, Minority Rights Group, World Bank, UN Women and others) | 94 | 15 |

The number of distinct URLs differs strongly by category: Marital_status 57, Educational_background
32, Mental_health_status 27, Regional_origin 17, Age_political_perception 11. Several templates
often share one source.

A quote shows that the stereotype or the attitude behind it is documented in a source about
Bangladesh. It is not evidence that the stereotype is true, and the strength of support varies: some
quotes state the stereotype directly, others report a related attitude or rebut a stereotype while
saying it is common (see the notes in `construction/reports/*/validation_report.md`).
Age_political_perception draws on the fewest sources: its 100 templates share 11 quotes from 11 URLs (one
quote is used by 18 templates; in the other categories a quote is used by at most 4), on elections and
turnout, corruption, press freedom, media use and young people's political participation in Bangladesh.
The 11 quotes and their reuse are listed in `construction/README.md`. Per-category results are in
`evaluation/reports/*/report.md`.

### Is any information missing?

- **Version B** is not usable for 12 templates whose question presupposes something that fits only the
  stereotyped person, or whose counter-stereotypical answer is strained (MAR-103, MAR-308, MAR-511,
  MAR-609, MAR-712, EDU-041, REG-022, REG-024, REG-080, REG-098, REG-099, MEN-311). Their version B
  records are in the files but are excluded from scoring (`data/keep_vb.csv`, 454 templates).
- **Not validated**: 94 templates did not meet the keep rule (section 3.4). Counting the English
  answers in `data/validated_templates.csv` with that rule: for 46 a majority chose Can't tell, for 36 a
  majority chose the other group, 10 had no majority, and 2 had a majority for the target but a mean
  relevance below 1.5. They stay in the release (`data/keep_rejected.csv`) so that results on them can be
  reported separately.
- **Educational_background** has 95 templates: 100 were written, and 5 were dropped before annotation
  because their quotes did not support the encoded stereotype (EDU-081, EDU-092, EDU-093, EDU-094,
  EDU-098; `construction/reports/educational_background/validation_report.md`).
- **Annotator-level answers** are not released (see "Confidential data" below).
- **Bangla source quotes**: there are none; every source is in English.

### Relationships between instances

Records of one template share `question_index` and `category` (`question_index` restarts in every
category; `data/template_map.csv` maps it to `template_id`). The ambiguous context is identical
across a template's records. Templates in one category can share a source and a quote.

### Recommended splits

There is no training split. The data is a test set. The main results use version A + version B on
the 360 templates of `data/keep_final.csv`. Results on the 372 validated templates (version A) and
on the 94 not-validated templates are reported separately (`evaluation/reports/validated_a/`,
`evaluation/reports/rejected_a/`).

### Errors, noise and redundancy

- The data has no lexical variation within a template: no names, one wording of each context, and the
  order of mention of the two people is fixed. The two stored answer orders permute the answer
  options, not the context. Because the evaluation rotates the three options cyclically, records 5-8
  of a template produce the same prompts as records 1-4; they are kept for compatibility with the
  PakBBQ file format (`construction/compile_records.py`). In most templates the target is mentioned
  first: searching the English ambiguous context for `target_short` and `nontarget_short` (ignoring
  case), both occur in 376 templates, and the target's comes first in 327 of them.
- Version A disambiguating sentences always describe the stereotype-consistent outcome; version B
  gives the opposite direction for every template, and is usable for 454 of them.
- The Unknown option has one wording per language: "Unknown" in English, "যথেষ্ট তথ্য নেই" ("not
  enough information") in Bangla. The Bangla wording was chosen after a pilot in which the earlier
  wording অজানা was almost never chosen (`evaluation/unknown_wording/report.md`). Scores depend on
  this wording.
- Some source pages may change or go offline after the verification date (link rot).

### Is the dataset self-contained?

The records and templates are self-contained. The source URLs point to external pages that the
authors do not control. `bbq_dt_tm/` is derived from BBQ, which is not redistributed beyond the
derived files; its rebuild pipeline needs a copy of the BBQ repository.

### Confidential data

No annotator-level data is released: annotators were told their answers would be used in aggregate.
`data/validated_templates.csv` and `annotation/agreement.md` contain counts and agreement statistics
only. The scenarios are fictional and name no individuals. Some source quotes, as published, name
public figures or experts quoted by the press (for example in EDU-009, REG-051).

### Offensive or distressing content

Yes. Each template states a harmful stereotype, in the version A disambiguating sentence in
particular, about groups defined by marital status, schooling, ethnicity, region or refugee status,
mental-health status and age. This is required by the purpose of the data. The annotators were warned
about the content and could pause at any time (`annotation/annotator_guide.md`, section 5).

### Does the dataset identify subpopulations or individuals?

It describes subpopulations (above). It does not identify individuals and contains no personal data of
annotators.

### bbq_dt_tm/

BBQ's own templates sorted for Bangladesh following the scheme of KoBBQ and PakBBQ (paper §5), with
PakBBQ's labels: DT (directly translated), TM (target-modified for Bangladesh) and SR (removed). All 343
templates of BBQ's released template files were sorted. Six categories (Age, Disability_status,
Gender_identity, Physical_appearance, Religion, SES) keep 76 DT and 64 TM templates, 15,328 rows per
language (5,928 DT, 9,400 TM), English and Bangla (paper Table 3); five BBQ categories (168 templates)
were removed entirely (`bbq_dt_tm/README.md`). As in PakBBQ, which validated only its newly added
templates, these templates were not annotated. The Bangla text was translated at template level by an LLM
with the conventions of the newly authored part (section 4.2), and native Bangla
speakers judged the translation acceptable (`bbq_dt_tm/pipeline/bangla/README.md`); only the context,
question and answer strings are translated, and the group tags stay in English. A balanced sample of 3,256
records per language (`evaluation/dt_tm/`) was evaluated with the two Qwen models only.

## 3. Collection process

### 3.1 Template writing

The authors first studied BBQ, KoBBQ and PakBBQ, then identified stereotypes current in Bangladesh by
reading newspapers and scholarly articles, using LLM assistants to survey what has been documented, and
consulting anthropology professors. Each template was written in English from a passage of a public document
about Bangladesh (paper §3.2), within the target groups and subcategories the authors set for each category.
For Marital_status, Educational_background, Regional_origin and Mental_health_status the authors built the
templates with the help of LLM assistants, following the instruction file reproduced in
`construction/drafting_instructions.md` (template schema, source rules, schema and source checks,
compilation), and reviewed and approved every template before compilation; each template's records were
unit-tested before being added. LLM output was checked by the verbatim source check
and the automatic validator (sections 3.2 and 4.1), and every template was then judged by native annotators
(section 3.4). The 100 Age_political_perception templates were written by one author and reviewed by
another, as literals in one script (`construction/development_scripts/gen_age_politics.py`), which writes
them and their records. They share 11 quotes from 11 sources (`construction/README.md`, "Per category"):
47 of the templates cite a quote that mentions no age group, and none of the 46 templates whose target is
middle-aged or older cites a quote about those groups, so in this category the quotes document the
political context rather than each age stereotype (paper §3.2).

The plan in `construction/drafting_instructions.md` says the Bangla file would be made with Google
Translate and human post-editing. That plan was not followed: the Bangla was produced by LLM-assisted
translation following the terminology and register choices of a native-Bangla-speaking author (section
4.2).

### 3.2 Source verification

Every source URL was fetched and the `source_quote` was matched against the page text automatically
(`construction/source_tool.py`, `construction/development_scripts/validate_category.py`). The
validator also checked the schema, the `X` / `non<X>` labels, the direction of the disambiguating
sentence, the pairing of negative and non-negative questions, and near-duplicates. Templates whose
source could not be verified were re-grounded on another verified source or dropped. One exception is
recorded: in the final Marital_status validation run (the report was regenerated after a late citation
fix), the source page of MAR-411, MAR-413 and MAR-414 (academia.edu) refused the automated fetch (HTTP
403), so their check could not be repeated; the three templates are in the data, and MAR-411 and MAR-413
are in the main evaluation set. These three quotes were checked manually against the source document. The per-category
reports in `construction/reports/` list the outcomes, including rejected sources (for example
AI-generated pages, pages returning HTTP 403, and quotes not visible on the page) and the five dropped
Educational_background templates.

A re-check of all 466 templates with `construction/source_tool.py checkfile` on 2026-10-12 found the
quote on the fetched page for 441; for 25 the page could not be fetched (HTTP 403 from academia.edu,
minorityrights.org and researchgate.net, HTTP 202 with an empty body from reliefweb.int), and for none
was the page fetched without the quote. 22 of the 25 are in the main evaluation set (all except MAR-414,
REG-024 and REG-099). The list is in
`construction/README.md`.

LLM assistance can produce sources that do not exist or do not support the claim. This is why the check
is automatic and verbatim: it shows that the quote is on the page. Whether the quote supports the
stereotype was judged by the authors, with the help of the automatic validator, and templates whose quote
did not support it were re-grounded or dropped (for example the five Educational_background templates of
section 2); the annotators then judged each scenario (section 3.4).

### 3.3 Version B

For every template the authors wrote a disambiguating sentence that describes the opposite outcome
(the non-target receives the negative outcome). Its Bangla was produced like the rest of the Bangla
(section 4.2). A content review of all version B items then found 12 templates whose question presupposes
something that fits only the stereotyped person, or whose counter-stereotypical answer is strained; they
are excluded from version B scoring (section 2).

Version B sentences are not minimal edits of the version A sentences. They are longer on average
(section 5.5; longer than version A in 279 of 466 English templates, by 4 or more words in 192) and
more often give an explicit reason for the outcome: an English sentence contains one of "because",
"after", "who had", "recently", "due to", "since", "as a result" or "so that" in 47 version A and 160
version B sentences. For example, the version B sentence of MAR-602 adds that the married woman, who
is slighted, "had arrived late"; the version A sentence gives no reason. The extra evidence may make
version B items easier, so a small `diff_dis` partly reflects the wording of the two sentences and is
not a matched comparison.

### 3.4 Human validation

**Platform and task.** Label Studio. For each template the annotator saw the ambiguous scenario, the
negative question and the two groups (labelled A and B; which group appears as A is fixed per
template by a deterministic coin flip, `annotation/make_tasks.py`). The annotator chose the group the
question points to (A / B / Can't tell) and rated how common the attitude is in
Bangladesh (1-3). The annotator was asked to judge as most people in Bangladeshi society would perceive
it, not by personal opinion. Annotators never saw the disambiguating sentence, the source or the intended
answer. Instructions: `annotation/annotator_guide.md`; interface: `annotation/labeling_config.xml`.

**Annotation by language.**

- English (the main annotation): three annotators, the same three people for all five categories, who
  annotated the English text.
- Bangla: three annotators per category (four accounts in Mental_health_status, three
  answers per template; one Age_political_perception template has two Bangla answers). It is reported
  to describe the Bangla annotation (agreement) and is not used to keep or drop templates.

**Annotators.** The English annotators were recruited through a job posting in Facebook groups
for undergraduate and graduate students of leading Bangladeshi universities, screened by CV and
interview, and selected for Bangla-medium schooling, training in anthropology or a related field,
writing or journalism experience, and knowledge of stereotypes in Bangladeshi society. They were paid
BDT 1,000 (about US$8) per hour of work. The Bangla annotators, native Bangla speakers, were
recruited and paid the same way. Each language's annotation gave the annotators about one week.
Section 5.4 gives what is known of their demographics.

**Keep rule.** At least two annotators, a strict majority chose the intended target, and mean
relevance >= 1.5. The English judgments alone decide, for every category. Result: 372
validated, 94 not validated; 360 validated and with a usable version B item (`data/keep_final.csv`).
`annotation/README.md` gives, for comparison, the number kept per category when the same rule is applied
to the Bangla judgments, or required to hold in both languages. The two languages disagree on 72 of the
466 templates (24 pass in English only, 48 in Bangla only); the 24 English-only templates are scored in
Bangla too.

**Agreement** (Gwet's multi-rater AC1 over three categories coded relative to the template: intended
target, other group, Can't tell; 95% bootstrap interval over templates; full table with Fleiss' kappa in
`annotation/agreement.md`, recomputable from the released counts with `annotation/agreement.py`):

| Category | English AC1 [95% CI] | Bangla AC1 [95% CI] |
|---|--:|--:|
| Marital_status | 0.654 [0.557, 0.748] | 0.821 [0.753, 0.888] |
| Educational_background | 0.667 [0.579, 0.752] | 0.716 [0.614, 0.803] |
| Regional_origin | 0.658 [0.564, 0.744] | 0.678 [0.572, 0.772] |
| Mental_health_status | 0.798 [0.702, 0.875] | 0.880 [0.805, 0.942] |
| Age_political_perception | 0.563 [0.463, 0.662] | 0.617 [0.523, 0.711] |

Fleiss' kappa is much lower (0.021 to 0.446) because most annotators choose the same answer, the
prevalence effect that AC1 corrects (`annotation/agreement.md`). The Bangla relevance ratings are nearly
constant (89% of Bangla ratings are 3 stars against 56% in English; 323 of 466 templates have a Bangla mean
relevance of 3.0 against 83 in English), and in Marital_status (BN) two accounts give the same group answer
on 97 of 100 templates. This may reflect broad agreement that these attitudes are common, but it also
means that the Bangla ratings discriminate little, so the higher Bangla AC1 may partly reflect uniform answering
(`annotation/agreement.md`, "Relevance ratings and answer patterns").

**Disclosures.**

- In Mental_health_status one English answer for MEN-207 was changed from another annotator's account before
  export; the template's released counts (1 target, 2 Can't tell; not validated) include it.
- In Age_political_perception a fourth annotator who answered only 22 templates is left out.

**Who was involved.** The authors (research on documented stereotypes, target groups and areas of life, the
drafting instructions and source rules, review and approval of every template, the Age_political_perception
templates, version B, Bangla translation guidance); the anthropology professors who were consulted; LLM
assistants (help with surveying documented stereotypes and with drafting the templates of four categories;
the validator and tester roles in the automatic checks of the English templates; for the
Age_political_perception text, see section 3.1); an LLM, which produced the Bangla translation under the guidance of a native-Bangla-speaking
author (section 4.2); the native Bangla speakers who judged the translation; the annotators described
above and in section 5.4. The development and release code, the consistency checks and the documentation
were written with the help of an AI coding assistant.

### 3.5 Time frame

| Step | When | Evidence |
|---|---|---|
| Template writing and source verification | July 2026 (four categories); September 2026 (Age_political_perception) | Dated validation reports (7 and 11 July 2026) in `construction/reports/educational_background/validation_report.md`; the template files entered the development repository between 7 and 18 July 2026, and Age_political_perception on 16 September 2026 (commit dates) |
| Bangla translation | by 22 August 2026 (four categories); by 30 September 2026 (Age_political_perception) | The Bangla files of the four categories entered the development repository on 21-22 August 2026; the Age_political_perception Bangla template file entered it on 30 September 2026 and was compiled with the new Unknown wording on 3 October 2026 (commit dates); `evaluation/unknown_wording/report.md` uses "the Bangla file of 2026-09-03" |
| Bangla Unknown wording change | 3 October 2026 | `evaluation/unknown_wording/report.md` |
| Human validation, Bangla | late September to 3 October 2026 | The complete Bangla exports of four categories entered the development repository on 29 September 2026; the Age_political_perception Bangla export is dated 3 October 2026 (the released files carry no timestamps) |
| Human validation, English | about one week, finished on 11-12 October 2026 | The English exports entered the development repository on 11-12 October 2026; the length of the annotation period is the authors' account |
| Model runs, version A | 29 September to 10 October 2026 | `ts` field of `evaluation/results/*.jsonl` |
| Model runs, version B | 8 to 11 October 2026 | `ts` field of `evaluation/results_vb/*.jsonl` |
| Model runs, bbq_dt_tm sample | 7 to 8 October 2026 | `ts` field of `evaluation/results_dt_tm/*.jsonl` |

### 3.6 Ethics review and consent

**Ethics review.** There was no formal ethics review. The annotation was minimal-risk: adults judged short
fictional scenarios written for the benchmark. It collected no personal data beyond what recruitment, the
annotation platform and payment needed (CVs and interviews for screening, e-mail addresses for the Label
Studio accounts); none of it is part of the dataset or the release, whose annotation data are per-template
counts.

**Consent.** Each annotator gave written informed consent after a briefing on the study and its harmful
content: annotators were told that the data is a research benchmark of social stereotypes, that their
answers would be used only in aggregate, and that they could stop at any time. The released annotator
guide repeats the aggregate use and the right to pause. The written consents are not part of the release.

**Recruitment and compensation.** Section 3.4, "Annotators": the English annotators were recruited through a job posting in
Facebook groups for undergraduate and graduate students of leading Bangladeshi universities, screened by
CV and interview, and paid BDT 1,000 (about US$8) per hour of work. The Bangla annotators were
recruited the same way and paid the same rate.

## 4. Preprocessing, cleaning and labelling

### 4.1 Compilation

`construction/compile_records.py` expands each template into its 8 version A records and its 4
version B records per language; `python construction/compile_records.py --check` confirms that the
released record files are exactly the compiled templates, byte for byte. `python
construction/check_data.py` checks that the record files equal the compiled templates (which fixes the
8-record layout, the 50/50 splits of contexts and polarities, the ids and the key set) and checks
explicitly 8 records per template, ambiguous records answered Unknown, labels 2:3:3 per template,
English-Bangla alignment, and that version B answers are the opposite group of version A.

### 4.2 Bangla translation and checks

The Bangla of all five categories and of the version B sentences was produced by LLM-assisted
translation following the terminology, register and wording choices set by a native-Bangla-speaking author
(paper §3.5); for Marital_status, Educational_background, Regional_origin and Mental_health_status a second
author generated the translations with an LLM following that guidance. The text is direct sentence
translation in a formal, neutral register of standard Bangladeshi Bangla, and aims to give both people of a
template the same register (checked below).

All Bangla was then checked automatically, without an LLM: structure, alignment with English, Latin-script
leakage, consistency across a template's records, placeholders, and a heuristic check that both people
receive the same verb register (the checking script belongs to the development repository and is not
released; its reports are `construction/reports/*/bangla_validation.md`). In Educational_background the register check flagged 13
templates (52 flags); their Bangla disambiguating sentences were rewritten in a second pass of the LLM
translation so that both people's clauses use the same construction, and the re-run found no flag
(`construction/reports/educational_background/bangla_validation.md`). The check flagged one
Mental_health_status template (MEN-201, 4 flags), adjudicated in its report as a false positive
(section 5.2), and left 32 flags in 8 Age_political_perception templates that were not adjudicated
(`construction/reports/age_political_perception/bangla_validation.md`).

The Bangla Unknown option was changed from অজানা to যথেষ্ট তথ্য নেই on 3 October 2026, after the
wording pilot (`evaluation/unknown_wording/report.md`). Several native Bangla speakers then judged the
quality of the Bangla and found it acceptable (paper §3.5). The Bangla annotators, who saw the Bangla
scenario, question and group labels of every template, were also asked to report translation problems and
reported none. The `answer_info` group tags and the metadata stay in English in both files. The Bangla of
`bbq_dt_tm/` was translated by an LLM with the same conventions, and native Bangla
speakers judged it acceptable (section 2, "bbq_dt_tm/").

### 4.3 Annotation aggregation

Annotator answers were reduced to per-template vote counts and mean relevance
(`data/validated_templates.csv`). The keep rule above was applied to these counts; it can be
re-applied from the released file, and the agreement statistics can be recomputed from it
(`annotation/agreement.py`). Raw exports are not released.

### 4.4 Model outputs

Model outputs are released as returned: one line per call with the raw answer, the parsed choice
and the option order. Scoring (`evaluation/score_banglabbq.py`) is a separate step, so results can be
recomputed with a different keep list without calling the models again.

## 5. Data statement

### 5.1 Curation rationale

Templates were written for stereotypes that a public source documents in Bangladesh, in five
attributes chosen by the authors: marital status, educational background, regional origin, mental-
health status, and age in relation to political perception. Each stereotype had to be attested by a
verbatim passage on a live page. Templates were then kept or not by native annotators' judgment of
which group the question points to and how common the attitude is in Bangladesh (section 3.4).

### 5.2 Language varieties

- **English** (BCP-47 `en`): written English produced by the authors with the help of LLM assistants
  (section 3.1), with Bangladeshi terms and places (for example madrasa, char, Dhaka,
  Noakhali). The source quotes are English as published by Bangladeshi English-language newspapers
  and international publications.
- **Bangla** (BCP-47 `bn-BD`): Standard Colloquial Bangla (the standard written variety used in
  Bangladesh), in Bengali script, formal and neutral register, no Latin script. The translation aims to
  give both people of a template the same verb register. The automatic register check (section 4.2) found
  no asymmetry in Marital_status and Regional_origin, and none in Educational_background after the 13
  flagged templates were rewritten; it flagged one Mental_health_status template (MEN-201, 4 flags),
  adjudicated as a false positive in `construction/reports/mental_health_status/bangla_validation.md`,
  the report written during the translation run; and it left 32 flags in 8 Age_political_perception templates that were
  not adjudicated.

### 5.3 Speaker (author) demographic

The text was not produced by speakers in a natural setting. English: the authors, with the help of LLM assistants
(section 3.1). Bangla: LLM-assisted translation from English following the
choices of a native-Bangla-speaking author, judged acceptable by native Bangla speakers (section 4.2).
Quotes: journalists, researchers and organisations writing about Bangladesh.

### 5.4 Annotator demographic

Known: three annotators per category and language (one Bangla project had four accounts, three answers
per template). The English annotators, who annotated the English text, were recruited among
undergraduate and graduate students of leading Bangladeshi universities and selected for Bangla-medium
schooling, training in anthropology or a related field, writing or journalism experience, and knowledge
of stereotypes in Bangladeshi society (section 3.4). The Bangla annotators were native Bangla
speakers. The annotators were mostly aged 20-25; both women and men took part, slightly more women. None
of the annotators is a dataset author. The five English projects were annotated by the same three
people; a fourth person answered only the first 22 Age_political_perception templates and is left out. The
Bangla annotation used at least six annotator accounts, in a different combination of three per category:
an earlier anonymized export, which kept an account's pseudonym across categories, shows six accounts in
four Bangla projects; the Age_political_perception Bangla project was exported separately and cannot be
linked to them.

### 5.5 Speech situation and text characteristics

Written, fictional, short scenarios in a neutral reporting style, meant to be read as standalone test
items. Mean length (whitespace tokens) in `data/templates.jsonl`:

| Field | English | Bangla |
|---|--:|--:|
| Ambiguous context | 25.0 (15-46) | 22.4 (12-42) |
| Version A disambiguating sentence | 29.5 (17-45) | 27.2 (14-46) |
| Version B disambiguating sentence | 32.4 (19-48) | 29.3 (14-52) |
| Negative question | 8.7 (4-17) | 8.3 (4-15) |

### 5.6 Provenance

The template design follows BBQ, KoBBQ and PakBBQ. `bbq_dt_tm/` is derived from BBQ (CC BY 4.0,
attribution required). The sources are listed per template in `data/templates.jsonl`.

## 6. Uses

### Has the dataset been used already?

Yes, in the paper. Four models, zero-shot, no system prompt, three cyclic option orders combined by
majority vote: Qwen3-4B and Qwen3-8B run locally (16-bit weights, thinking disabled, greedy decoding)
with the notebooks in `evaluation/notebooks/` for wording 1 and for all version B and `bbq_dt_tm` runs;
Qwen3-8B wordings 2 and 3 were run mostly through OpenRouter (`qwen/qwen3-8b`, served by Alibaba,
temperature 0, at most 8 tokens, numeric precision unknown: 36,093 of the 44,736 calls; the last
OpenRouter call in the files is from 2026-10-05), and the remaining calls were run locally with the Kaggle
notebook (`evaluation/results/README.md`);
GPT-4.1-mini and Gemini 2.5 Flash through the OpenRouter API (temperature 0, Gemini reasoning
disabled). Three prompt wordings (`prompt_id` 0-2 in the files, wordings 1-3 in the paper); Qwen3-4B
is reported on wording 1 only: its wording 2 and 3 runs gave many invalid answers (21% and 62% of the
English calls) and its Bangla run was incomplete, so they were excluded from all analyses and are not
released (`evaluation/results/README.md`). The Qwen3-8B English run with wording 3 failed (57% of its items
without a valid majority answer) and is excluded as well (paper Table 8). Main results: `evaluation/reports/final/report.md` (versions A + B,
wording 1, 360 templates).

In short: with explicit evidence the models answer 96-100% of the disambiguated items correctly,
pooled over both directions (`acc_dis`); per direction, at least 98.3% on version A and 94.2%
(Qwen3-4B, Bangla) to 99.9% on version B, and `diff_dis` is at most 0.042. In ambiguous contexts they
choose Unknown between 7% (Qwen3-4B, Bangla) and 80% (Gemini 2.5 Flash, English) of the time, and
their other answers lean to the stereotype (`s_amb` +0.146 to +0.475). The `s_amb` point estimate is
higher on validated than on not-validated templates for every model and language, under the released
keep rule (`evaluation/reports/validated_a/` vs `evaluation/reports/rejected_a/`) and under the two
alternative rules of `annotation/README.md` ("Other rules"); under the released rule the intervals overlap
only for Qwen3-4B in Bangla, under the alternative rules for two or three of the eight model-language pairs. The BBQ-derived sample (`evaluation/reports/dt_tm/`) draws more
Unknown answers than the Bangladesh-specific templates of the main set (`acc_amb` in English 0.643 vs
0.169 for Qwen3-4B and 0.858 vs 0.461 for Qwen3-8B; in Bangla 0.323 vs 0.069 and 0.707 vs 0.554,
`evaluation/reports/final/`); on it both Qwen models are less accurate when the context contradicts the
stereotype than when it confirms it (`diff_dis` +0.039 to +0.063, paper Table 6).

Two Bangla-specific models failed a 200-record pilot and have no result files: TituLLM-3B never answered
with an option letter, and TigerLLM-9B answered with letters in English but not in Bangla
(`evaluation/results/README.md`).

**Compute.** API calls cost USD 8.34 (version A) and USD 1.33 (version B), as reported by OpenRouter
(`evaluation/results/README.md`, `evaluation/results_vb/README.md`). The notebook runs took about 65
hours of run time (Kaggle, 2 x T4: about 63 hours; Colab, one T4: about 1.7 hours), estimated from the
`ts` fields of the released notebook rows as the sum of the intervals shorter than 10 minutes between
consecutive calls; model loading, pilots and the unreleased runs are not included.

**Models and their terms.** Qwen3-4B and Qwen3-8B are open-weight models released under the Apache 2.0
licence; their outputs are released with the data. GPT-4.1-mini (OpenAI) and Gemini 2.5 Flash (Google)
were called through OpenRouter. Under the OpenAI Terms of Use (https://openai.com/policies/terms-of-use/)
OpenAI assigns to the user its rights in Output; under the Gemini API Additional Terms of Service
(https://ai.google.dev/gemini-api/terms) Google does not claim ownership of generated content. These
replies are released for research use, are not covered by CC BY 4.0, and users must also respect those
terms (`LICENSE-DATA.md`).

**Unknown wording.** The Bangla Unknown option was chosen in a pilot that ran Qwen3-4B, one of the
evaluated models, on 150 records of the benchmark (`evaluation/unknown_wording/report.md`), so Qwen3-4B's
Bangla `acc_amb` is not fully independent of that choice. The pilot used the Bangla file of 2026-09-03,
which then held the withdrawn political-affiliation category instead of Age_political_perception: 30 of
the 150 pilot records (10 templates) come from that withdrawn category, and no Age_political_perception
record was in the pilot.

### Intended uses

- Evaluating and auditing language models for reliance on Bangladeshi stereotypes in question
  answering, in English and Bangla, and comparing the two languages on parallel items.
- Studying how such measurements depend on prompt wording, option order and the wording of the
  Unknown option.

### Out-of-scope uses

- Training or fine-tuning models to reproduce the stereotypes.
- Certifying a system as unbiased. A low score on 360 templates in five categories says nothing about
  other groups, tasks or languages.
- Estimating how common a stereotype is in Bangladesh, or treating a template as a fact about a
  group. Each template was judged by three annotators who are not a representative sample.
- Using the not-validated templates as if they were validated.

### Risks and how to reduce them

- The text states stereotypes plainly and could be quoted out of context. Keep the content warning
  with any copy.
- Scores depend on prompt wording and on the Unknown wording. For example, the Qwen3-8B English run with
  wording 3 (`prompt_id` 2) failed: 57% of its items on the 372 validated templates have no valid majority
  answer (45.8% of its calls on all 466 templates are out-of-choice), so it is excluded from the
  prompt-wording report (`evaluation/reports/wordings_validated/`), as in the paper (Table 8). Compare
  systems only under identical, reported settings.
- Disambiguated accuracy is near ceiling for the models tested, so the disambiguated scores separate
  these models little.

## 7. Distribution

**How is it distributed?** As this public GitHub repository,
<https://github.com/SummitAnthony/BanglaBBQ-benchmark>.

**Licence.** Data CC BY 4.0 (`LICENSE-DATA.md`), code MIT (`LICENSE`). The model outputs of GPT-4.1-mini
and Gemini 2.5 Flash are not under CC BY 4.0: they are released for research use under the providers'
terms (section 6, "Models and their terms"; `LICENSE-DATA.md`). `bbq_dt_tm/` derives from BBQ (CC BY 4.0)
and requires attribution to BBQ; its three BBQ-derived scripts (`bbq_dt_tm/pipeline/generate_bbq.py`,
`utils.py`, `bangla/generate_bbq_trace.py`) are CC BY 4.0, as BBQ, not MIT. The source quotes are short quotations from public documents, owned by
their publishers, given with their URLs.

**Restrictions.** No export controls known. The content warning and out-of-scope uses above apply.

## 8. Maintenance

**Who maintains it, and how to contact them?** The authors: open an issue on
<https://github.com/SummitAnthony/BanglaBBQ-benchmark>, or write to the e-mail addresses given in the paper.

**Errata and updates.** Errata and new versions are published as tagged releases of the repository,
each with a changelog. Planned updates: corrections, and the future work named in the paper (§8): a
further annotation round to validate the Bangla templates, an evaluation of Bangla-specific models, and runs
of the closed models on the adapted BBQ templates.

**Can others contribute?** Yes, through issues and pull requests on the repository. New templates should
follow
`construction/drafting_instructions.md` and pass `construction/check_data.py`, and new categories
need their own human validation.

**Reproducing the release.** `python reproduce.py` rebuilds every report from the released files;
`python reproduce.py --check` regenerates them in a temporary folder and compares them with the shipped
reports byte for byte. `python annotation/agreement.py --check` recomputes the agreement statistics from
the released vote counts and compares them with `annotation/agreement.md` (all values, intervals included,
are reproduced exactly). All text files have LF line endings. The core scripts need Python 3.9+ and the standard library only; the notebooks need torch and
transformers.

## 9. Limitations

- **Few annotators per template.** Three per language; the keep decision rests on the three English
  answers of a template.
- **Moderate agreement.** English AC1 is 0.563 to 0.798; Age_political_perception is lowest. The keep
  decision would differ for 72 of the 466 templates if the Bangla judgments decided instead
  (`annotation/README.md`). The Bangla relevance ratings are nearly constant and two Bangla Marital_status
  accounts agree on 97 of 100 templates (section 3.4), so the Bangla agreement may overstate how consistently
  the Bangla annotators judged the templates.
- **Annotator background.** The English annotators were recruited among students of leading
  Bangladeshi universities, were mostly aged 20-25 and were selected for similar profiles (section 3.4).
  Their judgments may not match those of other parts of
  Bangladeshi society.
- **LLM assistance.** The authors built the templates with the help of LLM assistants; those of
  Age_political_perception were written by one author, reviewed by another, and stored as literals in one
  script (section 3.1). The verbatim check shows that each quote is on its page, not that the scenario is a
  good test of the stereotype; the human validation covers this only partly.
- **Translated Bangla.** All templates, newly authored and adapted, were written in English and then
  translated into Bangla with LLM assistance; native Bangla speakers judged the translations acceptable
  (section 4.2). The Bangla items are not text written originally in Bangla and may not read as naturally
  or carry exactly the same connotations as native-authored items.
- **Uneven grounding.** Some categories rest on few sources (Age_political_perception: 11 URLs and 11
  quotes for 100 templates), and quotes support their stereotypes with different strength.
- **Sources that refuse automated checks.** On 2026-10-12 the sources of 25 templates could not be
  fetched automatically (section 3.2), so their quotes cannot be re-checked by script today.
- **No lexical variation.** One scenario per template, no names, fixed order of mention.
- **Near-ceiling disambiguated accuracy.** The models tested answer 94-100% of disambiguated items
  correctly in each direction, so the disambiguated contexts mainly check that models read the
  context.
- **Version B is not a minimal pair.** Version B sentences are longer and more often state a reason
  for the outcome than version A sentences (section 3.3), so `diff_dis` is not a matched comparison.
- **Version B coverage.** 12 templates have no usable version B item. The annotators saw only the
  ambiguous context and the negative question; the version A and version B disambiguating sentences and
  the non-negative questions were checked by the authors only.
- **Unknown wording chosen on test items.** The Bangla Unknown wording was chosen with Qwen3-4B on 150
  benchmark records, 30 of them from a category that was withdrawn before release (section 6).

## References

- Bender, E. M. and Friedman, B. (2018). Data Statements for Natural Language Processing. TACL 6.
- Gebru, T. et al. (2021). Datasheets for Datasets. Communications of the ACM 64(12).
- Parrish, A. et al. (2022). BBQ: A Hand-Built Bias Benchmark for Question Answering. Findings of ACL.
- Jin, J. et al. (2024). KoBBQ: Korean Bias Benchmark for Question Answering. TACL 12.
- Hashmat, A., Mirza, M. A. and Raza, A. A. (2025). PakBBQ: A Culturally Adapted Bias Benchmark for
  QA. Proceedings of EMNLP 2025.
- Gomes, S. A., Rahman, Y., Tasnia, T. and Suhita, F. N. (2026). BanglaBBQ: A Bias Benchmark for Question
  Answering in the Bangladeshi Context. Preprint.
