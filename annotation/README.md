# annotation/

Human validation of the 466 templates: what the annotators saw, what was hidden from them, the rule that
decided which templates count as validated, and the outcome.

| File | What it is |
|---|---|
| `annotator_guide.md` | The guide given to the annotators. |
| `labeling_config.xml` | The Label Studio labeling interface the annotators used. |
| `make_tasks.py` | Builds the Label Studio tasks (one screen per template) and a private answer key from template objects. |
| `agreement.md` | Agreement statistics per project and the number of templates kept per category. Aggregate only. |
| `agreement.py` | Recomputes every statistic of `agreement.md` from the vote counts in `data/validated_templates.csv` (`--check` compares). |

The per-template outcome (vote counts, mean relevance, validated or not) is in `data/validated_templates.csv`
and in the `validation` field of each template in `data/templates.jsonl`. Annotator-level answers are not
released (see [What is released](#what-is-released-and-what-is-not)).

## What the annotators saw

Annotators worked in Label Studio, one screen per template. A screen showed:

| On screen | Content |
|---|---|
| Instruction | "Judge it as MOST people in Bangladeshi society would — not your personal opinion." |
| Situation | The template's ambiguous context (`ambiguous_context`). |
| Question | The template's negative question (`negative_question`). The non-negative question was not shown. |
| Group A, Group B | The two short group labels (`target_short`, `nontarget_short`). |

and asked for three inputs:

| Input | Options | Required |
|---|---|---|
| ① Which group does the question point to? | Group A / Group B / Can't tell | yes |
| ② How common is this attitude in Bangladesh? | 1 to 3 stars (1 = rare, 2 = moderate, 3 = very common) | yes |
| ③ Anything tricky? | free text | no |

The order of the two groups is fixed per template by a hash of the template id (`flip()` in
`make_tasks.py`: SHA-256 of `template_id`, odd puts the target in Group B). It is the same for every annotator
and for both languages. The target is Group B in 238 of the 466 templates.

The guide asks annotators to pick the group that the common social stereotype points to, not their own view
and not what would be fair; to choose Can't tell only if they see no stereotype favouring either group; to
judge each screen on its own; not to search or ask anyone; and to work independently until everyone has
finished. It carries a content warning, allows pausing at any time, and tells annotators that their answers
are used only in aggregate. Label Studio records the time spent on each screen.

In the English projects the scenario, question and group labels were in English; in the Bangla projects they
were in Bangla, taken from the Bangla templates. The interface text in `labeling_config.xml` and the guide,
`annotator_guide.md`, are in English.

## What was hidden

Annotators never saw the disambiguating sentence (version A or B), the non-negative question, the answer
options (including Unknown), the source URL or the quoted passage, the intended target, or which letter the
target was shown under. The screen asks which group the stereotype is about, not who did what, so there is no
correct answer to read off the scenario.

`make_tasks.py` enforces this. A task carries only `template_id`, `category`, `scenario`, `question`,
`group_A` and `group_B`. The script refuses to write a task that contains any of `disambig_sentence`,
`source`, `source_quote`, `target_label`, `nontarget_label`, `target_answer` or `nontarget_answer`, and
searches the written `tasks.json` for answer fields afterwards. The intended target and its letter go to a
separate `answer_key.csv`, which was kept private and never imported into Label Studio. `template_id` and
`category` are not shown on the labeling screen and do not reveal the answer.

The authors checked that the screens the annotators answered are exactly what `make_tasks.py` produces from
the released templates: scenario, question and group order agree for all 466 templates in both languages.

## Rebuilding the tasks

`make_tasks.py` was written for the development repository; its docstring cites development documents
(`SPEC.md`, `scripts/make_annotation_sheets.py`) that are not part of this release. It reads flat template objects, one per line. `data/templates.jsonl` stores the text fields per language
(`en`, `bn`), so flatten one language and one category first:

```
python - <<'EOF'
import json
lang, cat = "bn", "Marital_status"          # en or bn; any of the five categories
with open("tmp_templates.jsonl", "w", encoding="utf-8") as out:
    for line in open("data/templates.jsonl", encoding="utf-8"):
        t = json.loads(line)
        if t["category"] == cat:
            flat = {"template_id": t["template_id"], "category": t["category"],
                    "subcategory": t["subcategory"], **t[lang]}
            out.write(json.dumps(flat, ensure_ascii=False) + "\n")
EOF
python annotation/make_tasks.py --category Marital_status --input tmp_templates.jsonl --out-dir tmp_tasks
```

`tmp_tasks/tasks.json` is what Label Studio imports (Project → Import). Paste `labeling_config.xml` into
Project → Settings → Labeling Interface. Do not import `tmp_tasks/answer_key.csv`.

## Rounds and annotators

| Language | Annotators per category | Notes |
|---|---|---|
| English | 3, the same three people for all five categories | Decides which templates are validated. |
| Bangla | 3 | Describes the Bangla annotation (agreement); does not keep or drop templates. Mental_health_status: four accounts, three answers per template. Age_political_perception: one template has two answers. |

Each category in each language was a separate Label Studio project (10 projects). The English-project
annotators annotated the English text, the Bangla-project annotators the Bangla text. Where an annotator
submitted a template twice, the last saved answer is used; drafts are dropped.

Apart from the incomplete Age_political_perception annotator (see [Disclosures](#disclosures)), no annotator
or session was set aside, for response time, answer patterns or any other reason, although section 4 of the
guide says that rushed or patterned sheets would be set aside.

**Recruitment and payment.** The English annotators were recruited through a job posting in
Facebook groups for undergraduate and graduate students of leading Bangladeshi universities, screened by
CV and interview, and selected for Bangla-medium schooling, training in anthropology or a related field,
writing or journalism experience, and knowledge of stereotypes in Bangladeshi society. They were paid
BDT 1,000 (about US$8) per hour of work. The Bangla annotators, native Bangla speakers, were
recruited and paid the same way. Each language's annotation gave the annotators about one week.
The annotators were mostly aged 20-25; both women and men took part, slightly more women. None of the
annotators is a dataset author.
The five English projects were annotated by the same three people (plus the incomplete
Age_political_perception annotator). The Bangla annotation used at least six annotator accounts, in a
different combination of three per category: an earlier anonymized export, which kept an account's
pseudonym across categories, shows six accounts in four Bangla projects; the Age_political_perception
Bangla project was exported separately and cannot be linked to them.

**Consent and ethics.** Each annotator gave written informed consent after a briefing on the study and its
harmful content: annotators were told that the data is a research benchmark of social stereotypes, that
their answers would be used only in aggregate, and that they could stop at any time. There was no
formal ethics review: the annotation was minimal-risk (adults judging short fictional scenarios written for
the benchmark). It collected no personal data beyond what recruitment, the annotation platform and payment
needed (CVs and interviews for screening, e-mail addresses for the Label Studio accounts); none of it is part
of the dataset or the release.

## Keep rule

A template is **validated** if all three hold:

1. at least two annotators judged it;
2. a strict majority chose the intended target (the group named by `target_short`); Can't tell counts
   against;
3. the mean relevance rating is at least 1.5 (scale 1-3).

The English judgments alone decide, for every category. The Bangla judgments are reported in
`agreement.md` to describe the Bangla annotation; they do not keep or drop templates.

The rule can be recomputed from the released vote counts; this reproduces the `validated` column for all 466
templates:

```
python - <<'EOF'
import csv
rows = list(csv.DictReader(open("data/validated_templates.csv", encoding="utf-8")))
def votes(r, langs):
    n = sum(int(r[f"{l}_annotators"]) for l in langs)
    tgt = sum(int(r[f"{l}_target"]) for l in langs)
    rel = sum(float(r[f"{l}_mean_relevance"]) * int(r[f"{l}_annotators"]) for l in langs) / n
    return n >= 2 and 2 * tgt > n and rel >= 1.5 - 1e-9
bad = [r["template_id"] for r in rows if votes(r, ["en"]) != (r["validated"] == "1")]
print(len(rows), "templates,", len(bad), "disagree with the validated column")
EOF
```

**Other rules, for comparison.** Templates kept per category when the same rule is applied to the English
answers (the released rule), to the Bangla answers, or required to hold in both languages (recomputed from
`data/validated_templates.csv` with the function above):

| Category | English only (released, `validated`) | Bangla only | Both languages pass |
|---|--:|--:|--:|
| Marital_status | 80 | 89 | 75 |
| Age_political_perception | 62 | 69 | 57 |
| Regional_origin | 85 | 83 | 77 |
| Educational_background | 77 | 85 | 72 |
| Mental_health_status | 68 | 70 | 67 |
| **All** | **372** | **396** | **348** |

The first two columns are the "Kept EN" and "Kept BN" columns of paper Table 1.

The two languages disagree on 72 of the 466 templates: 24 pass in English only (and are scored in Bangla
too) and 48 in Bangla only. In Bangla the relevance condition never fails (no template has a Bangla mean
relevance below 1.5; see [Uniform Bangla ratings](#uniform-bangla-ratings)), so the Bangla-only and
both-languages columns are driven by the target votes.

**Does the comparison of validated and rejected templates depend on the rule?** `s_amb` (version A, prompt
wording 1, all eight model runs) on the templates each rule keeps vs the templates it rejects, with 95%
bootstrap intervals over templates. Computed with `evaluation/score_banglabbq.py` and keep lists built from
`data/validated_templates.csv` with the function above; the released-rule column is
`evaluation/reports/validated_a/` vs `evaluation/reports/rejected_a/`.

| Model | Lang | English only (released): 372 vs 94 | Bangla only: 396 vs 70 | Both languages: 348 vs 118 |
|---|---|---|---|---|
| Qwen3-4B | bn | 0.329 [0.26, 0.40] vs 0.197 [0.07, 0.32] (overlap) | 0.325 [0.26, 0.39] vs 0.171 [0.02, 0.31] (overlap) | 0.342 [0.27, 0.41] vs 0.184 [0.07, 0.30] (overlap) |
| Qwen3-4B | en | 0.418 [0.35, 0.49] vs 0.218 [0.09, 0.33] | 0.407 [0.34, 0.47] vs 0.211 [0.06, 0.36] (overlap) | 0.423 [0.35, 0.50] vs 0.246 [0.14, 0.36] (overlap) |
| Qwen3-8B | bn | 0.211 [0.16, 0.26] vs 0.007 [-0.07, 0.09] | 0.190 [0.14, 0.24] vs 0.062 [-0.02, 0.15] (overlap) | 0.215 [0.16, 0.27] vs 0.034 [-0.04, 0.11] |
| Qwen3-8B | en | 0.290 [0.23, 0.35] vs 0.127 [0.05, 0.20] | 0.282 [0.23, 0.33] vs 0.113 [0.02, 0.21] | 0.297 [0.24, 0.35] vs 0.139 [0.07, 0.21] |
| gemini-2.5-flash | bn | 0.219 [0.18, 0.26] vs 0.050 [0.00, 0.10] | 0.213 [0.17, 0.25] vs 0.030 [-0.04, 0.10] | 0.226 [0.18, 0.27] vs 0.065 [0.01, 0.12] |
| gemini-2.5-flash | en | 0.148 [0.11, 0.18] vs 0.026 [-0.03, 0.08] | 0.146 [0.11, 0.18] vs -0.008 [-0.08, 0.06] | 0.157 [0.12, 0.19] vs 0.024 [-0.03, 0.08] |
| gpt-4.1-mini | bn | 0.402 [0.34, 0.46] vs 0.184 [0.09, 0.28] | 0.396 [0.35, 0.45] vs 0.143 [0.02, 0.26] | 0.415 [0.36, 0.47] vs 0.191 [0.09, 0.28] |
| gpt-4.1-mini | en | 0.475 [0.42, 0.52] vs 0.179 [0.08, 0.28] | 0.443 [0.39, 0.49] vs 0.257 [0.14, 0.37] | 0.468 [0.42, 0.52] vs 0.258 [0.17, 0.35] |

The point estimate is higher on the kept templates for every model and language under all three rules. The
intervals are disjoint except for Qwen3-4B in Bangla under the released rule, and overlap for two (both
languages) or three (Bangla only) of the eight pairs under the other rules. The released English-only rule
replaced an earlier rule that pooled the two languages for Age_political_perception after the model results
existed, so read the interval statement as specific to the released rule.

## Outcome

From `agreement.md` (paper Tables 1 and 2, in the paper's order). *Final set*: validated and with a usable
version B item (`data/keep_final.csv`; the 12 templates without a usable version B item are listed in
`construction/README.md`). AC1: Gwet's multi-rater AC1 of the English annotators over three categories coded
relative to the template (intended target, other group, Can't tell), with a 95% bootstrap interval over
templates.

| Category | Templates | Validated | Final set | AC1 (English) [95% CI] |
|---|--:|--:|--:|--:|
| Marital_status | 100 | 80 | 75 | 0.654 [0.557, 0.748] |
| Age_political_perception | 100 | 62 | 62 | 0.563 [0.463, 0.662] |
| Regional_origin | 100 | 85 | 80 | 0.658 [0.564, 0.744] |
| Educational_background | 95 | 77 | 76 | 0.667 [0.579, 0.752] |
| Mental_health_status | 71 | 68 | 67 | 0.798 [0.702, 0.875] |
| **All** | **466** | **372** | **360** | |

94 templates were not validated (`data/keep_rejected.csv`). `agreement.md` also gives the Bangla projects,
AC1 over the three raw options, Fleiss' kappa, the number of unanimous templates and the share of answers
naming the intended target. Fleiss' kappa is low in several projects (0.021 for Mental_health_status,
English) although most annotators chose the same group: when nearly all answers fall in one option, kappa's
chance correction removes most of the agreement (the prevalence effect). AC1 is reported for this reason.

### Uniform Bangla ratings

The Bangla relevance ratings are nearly constant: 89% of the Bangla ratings are 3 stars against 56% of the
English ratings; 323 of the 466 templates have a Bangla mean relevance of 3.0 against 83 in English
(Marital_status 98 of 100, Educational_background 91 of 95, Mental_health_status 55 of 71); and four Bangla
accounts gave 3 stars to every template. In Marital_status (BN) two accounts give the same group answer on
97 of 100 templates. Per project counts are in `agreement.md` ("Relevance ratings and answer patterns").
The uniform ratings may reflect broad agreement among the Bangla annotators that these attitudes are common;
they also mean that in Bangla the relevance condition of the keep rule hardly matters, and the higher Bangla
AC1 values may partly reflect uniform answering.

## Disclosures

- **Mental_health_status, English.** One answer for MEN-207 was changed from another annotator's account
  before export; the template's released counts (1 target, 2 Can't tell; not validated) include it.
- **Age_political_perception, English.** A fourth annotator answered only the first 22 templates and is left
  out.
- **Independence.** Annotators were asked to work independently; the annotation tool did not enforce it.
- **Translation.** The Bangla annotators saw the Bangla scenario, question and group labels. They were
  asked to report translation problems and reported none (the released guide's optional notes field
  mentions "unnatural wording"); the notes are not released. The quality of the Bangla was judged
  separately by native Bangla speakers, who found it acceptable (`construction/README.md`, "Bangla").
- **Guide and practice.** The guide (section 6) says that scenarios that fail are removed from the
  benchmark. The release keeps the 94 templates that failed, marked `validated` = 0 in
  `data/validated_templates.csv`; they are scored only separately (`evaluation/reports/rejected_a/`). The
  speed and pattern screening of the guide's section 4 was not applied (above).

## What is released and what is not

| Released | Not released |
|---|---|
| The guide and the interface (`annotator_guide.md`, `labeling_config.xml`) | Annotator-level answers |
| The task builder (`make_tasks.py`) | Free-text notes, response times, timestamps |
| Per-template vote counts and mean relevance per language (`data/validated_templates.csv`) | Annotator identities and accounts |
| The keep lists (`data/keep_validated.csv`, `keep_rejected.csv`, `keep_final.csv`) | The private answer keys |
| Agreement statistics (`agreement.md`) | |

Annotators were told that their answers would be used in aggregate, so only aggregate counts are released.
The counts are enough to recompute the keep rule (above), the keep lists and every statistic in
`agreement.md`: AC1 and Fleiss' kappa need only the number of answers per category and template, and the
letter coding of *AC1 raw* follows from `flip()` in `make_tasks.py`. `python annotation/agreement.py --check`
does this and reproduces every value of `agreement.md` (paper Table 1) exactly, bootstrap intervals
included.

## Limits

- Three annotators per category and language is few, and the English annotators were selected for similar
  profiles (recruited among university students; Bangla-medium schooling, training in anthropology or a
  related field). A validated template means that a majority of these annotators recognised the stereotype as
  being about the intended group, with an average relevance of at least 1.5; it does not measure how widely
  the stereotype is held.
- Annotators judged the ambiguous scenario and the negative question only. The disambiguating sentences of
  version A and version B and the non-negative question were checked by the authors only.
- Validation rests on the English text for every category; the Bangla judgments are reported but do not
  decide, and the two languages disagree on 72 of the 466 templates (above).
