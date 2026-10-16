# Human validation: agreement and outcome

Aggregate statistics only. Annotator-level answers are not released: annotators were told that their
answers would be used in aggregate. The per-template vote counts are in `data/validated_templates.csv`,
and every statistic of the agreement table except the *Raters* column (the number of annotator accounts,
taken from the annotation exports) can be recomputed from them with `python annotation/agreement.py`: every
value, bootstrap intervals included, is reproduced exactly (`--check` compares). The agreement table and the
"Templates kept" table give paper Table 1, in the paper's order of categories.
The rating and answer-pattern counts at the end also come from the exports.

- **English**: three annotators (the same three people for all five categories), who annotated the English
  text (`annotation/README.md`).
- **Bangla**: three annotators per category, who annotated the Bangla text (four accounts in
  Mental_health_status; three answers per template).
- **Intended target**: the group the template's stereotype is about (`target_short`).
- **Keep rule**: at least two annotators, a strict majority chose the intended target, and the mean relevance
  rating is at least 1.5 (scale 1-3). The English judgments alone decide, for every category. The
  Bangla annotation is reported here to describe it; it does not keep or drop templates.
- **AC1 target**: Gwet's multi-rater AC1 over three categories coded relative to the template: intended
  target, other group, Can't tell. 95% percentile bootstrap interval over templates (2,000 resamples,
  seed 0). *AC1 raw*: the same coefficient over the three options as displayed (A / B / Can't tell).
- **Fleiss' kappa** (target / other group / Can't tell coding) is given for comparison, over the templates
  with the full number of answers: for Age_political_perception (BN) the 99 templates with three answers
  (APO-067 has two; AC1 includes it). Kappa is low where nearly all annotators choose the same answer
  (the prevalence effect that AC1 corrects).
- *Raters* counts annotator accounts; *Unanimous* counts templates on which all answers agree;
  *% target* is the share of answers naming the intended target.

## Agreement per project

| Project | Templates | Raters | Ratings/template | AC1 target [95% CI] | AC1 raw A/B/CT | Fleiss' κ | Unanimous | % target |
|---|--:|--:|---|--:|--:|--:|--:|--:|
| Marital_status (EN) | 100 | 3 | 3×100 | **0.654** [0.557, 0.748] | 0.607 | 0.351 | 60 | 73.7% |
| Marital_status (BN) | 100 | 3 | 3×100 | **0.821** [0.753, 0.888] | 0.785 | 0.360 | 77 | 86.3% |
| Age_political_perception (EN) | 100 | 3 | 3×100 | **0.563** [0.463, 0.662] | 0.553 | 0.446 | 55 | 57.0% |
| Age_political_perception (BN) | 100 | 3 | 3×99, 2×1 | **0.617** [0.523, 0.711] | 0.597 | 0.438 | 58 | 65.2% |
| Regional_origin (EN) | 100 | 3 | 3×100 | **0.658** [0.564, 0.744] | 0.590 | 0.224 | 59 | 77.7% |
| Regional_origin (BN) | 100 | 3 | 3×100 | **0.678** [0.572, 0.772] | 0.617 | 0.221 | 64 | 79.7% |
| Educational_background (EN) | 95 | 3 | 3×95 | **0.667** [0.579, 0.752] | 0.600 | 0.286 | 57 | 75.4% |
| Educational_background (BN) | 95 | 3 | 3×95 | **0.716** [0.614, 0.803] | 0.662 | 0.177 | 62 | 83.2% |
| Mental_health_status (EN) | 71 | 3 | 3×71 | **0.798** [0.702, 0.875] | 0.742 | 0.021 | 52 | 89.7% |
| Mental_health_status (BN) | 71 | 4 | 3×71 | **0.880** [0.805, 0.942] | 0.848 | 0.028 | 59 | 93.9% |

Ratings/template is written as answers x templates (3×99, 2×1 = 99 templates with three answers and one with two).

## Templates kept

| Category | Templates | Validated (kept by the English answers) | Kept by the Bangla answers (not used) | Validated and with a usable version B item |
|---|--:|--:|--:|--:|
| Marital_status | 100 | 80 | 89 | 75 |
| Age_political_perception | 100 | 62 | 69 | 62 |
| Regional_origin | 100 | 85 | 83 | 80 |
| Educational_background | 95 | 77 | 85 | 76 |
| Mental_health_status | 71 | 68 | 70 | 67 |
| **All** | **466** | **372** | **396** | **360** |

## Relevance ratings and answer patterns

Aggregate counts from the annotation exports; the template counts also follow from `en_mean_relevance` and
`bn_mean_relevance` in `data/validated_templates.csv`. The Bangla relevance ratings are nearly constant:
89% of the Bangla ratings are 3 stars against 56% of the English ratings, and 323 of
the 466 templates have a Bangla mean relevance of 3.0 against 83 in English. In Bangla the relevance
condition of the keep rule fails for 0 templates (English: 6), so a Bangla keep decision rests on the
target votes alone. The higher Bangla AC1 values may partly reflect uniform answering: in Marital_status (BN)
two accounts give the same group answer on 97 of 100 templates. *Same answers*: the highest number of
templates, over pairs of accounts with at least 20 templates in common, on which two accounts chose the same
option (A / B / Can't tell), out of the templates they have in common. Across the Bangla projects, four
accounts gave 3 stars to every template (no English account did); this count is not broken down by project,
so that no account's ratings can be recovered from the released per-template means.

| Project | 3-star ratings | Templates with mean relevance 3.0 | Same answers (two accounts) |
|---|--:|--:|--:|
| Marital_status (EN) | 50% | 11 | 74/100 |
| Marital_status (BN) | 99% | 98 | 97/100 |
| Age_political_perception (EN) | 66% | 28 | 88/100 |
| Age_political_perception (BN) | 85% | 58 | 86/100 |
| Regional_origin (EN) | 52% | 19 | 83/100 |
| Regional_origin (BN) | 70% | 21 | 81/100 |
| Educational_background (EN) | 53% | 17 | 75/95 |
| Educational_background (BN) | 99% | 91 | 76/95 |
| Mental_health_status (EN) | 58% | 8 | 60/71 |
| Mental_health_status (BN) | 92% | 55 | 64/70 |
