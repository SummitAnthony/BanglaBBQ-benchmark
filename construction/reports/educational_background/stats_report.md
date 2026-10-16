> **Note for readers of the release.** Written during construction, before the post-review re-grounding of
> EDU-005, EDU-010, EDU-014 and EDU-015 (`validation_report.md`, "Post-review re-grounding";
> `construction/README.md`). The released data has 32 distinct source URLs (not 33), with
> en.prothomalo.com grounding 48 templates and documents.worldbank.org 1; the other counts are unchanged.
> The release's source counts are in `construction/README.md` ("Per category") and paper §4.2.

# Pre-compile Statistics — Educational_background (validated set)

- Templates: **95** (cap 100) → projected records: **760**
- Duplicate template_ids: 0
- Distinct source URLs: 33

## Per target group

| target_label | templates |
|---|---|
| madrasa | 35 |
| englishMedium | 25 |
| lowEducation | 20 |
| banglaMedium | 15 |

## Per subcategory (raw, pre-normalization)

| subcategory | n |
|---|---|
| employment | 6 |
| leadership | 6 |
| language ability | 6 |
| social inclusion | 6 |
| employment/hiring | 6 |
| workplace competence | 5 |
| workplace_competence | 4 |
| marriage_proposals | 4 |
| social_inclusion | 4 |
| radicalization_suspicion | 4 |
| cultural identity | 4 |
| vocational stigma | 4 |
| technology_use | 3 |
| university_admission | 3 |
| patriotism/national values | 3 |
| peer relations | 3 |
| university admission | 3 |
| corporate presentation | 3 |
| creativity | 3 |
| criminal suspicion | 3 |
| tenancy | 2 |
| financial_trust | 2 |
| financial trust | 2 |
| parenting | 2 |
| community respect | 2 |
| marriage proposals | 1 |
| technology use | 1 |

## Per source domain

| domain | templates |
|---|---|
| en.prothomalo.com | 45 |
| www.dhakatribune.com | 22 |
| www.tbsnews.net | 16 |
| languagetestingasia.springeropen.com | 6 |
| documents.worldbank.org | 4 |
| multilingual-education.springeropen.com | 1 |
| www.thedailystar.net | 1 |

## Flags

1. **Subcategory naming is inconsistent** across authors (spaces vs underscores; "employment" vs "employment/hiring"). Recommend normalizing to snake_case with merges (employment+employment/hiring; workplace competence variants; etc.) at compile time.
2. **Source concentration**: en.prothomalo.com grounds 45/95 templates (47%). Acceptable but worth noting in the paper; ~14 of these draw on an admission-fair advertorial series (see validation report).
3. 5 templates (EDU-081/092/093/094/098) excluded as NEEDS-REVIEW per user decision; can be re-grounded later.

## Verdict

READY to compile: 95 templates, 0 schema failures, all sources live and credible, all quotes verified.

---

# Post-compile statistics (final file)

- rows: 760
- label counts: {0: 190, 1: 285, 2: 285}  (expect 2:3:3 = 190:285:285)
- ambig/disambig: {'ambig': 380, 'disambig': 380}  neg/nonneg: {'neg': 380, 'nonneg': 380}
- question_index blocks: 95, all 8 rows each: True
- ids sequential 0..759 and example_id==id: True

## Subcategories (normalized)

- employment: 96
- social_inclusion: 80
- workplace_competence: 72
- university_admission: 48
- leadership: 48
- language_ability: 48
- marriage_proposals: 40
- technology_use: 32
- radicalization_suspicion: 32
- financial_trust: 32
- cultural_identity: 32
- vocational_stigma: 32
- patriotism_national_values: 24
- peer_relations: 24
- corporate_presentation: 24
- creativity: 24
- criminal_suspicion: 24
- tenancy: 16
- parenting: 16
- community_respect: 16

**Verdict: all invariants pass. File ready for annotation pass / Bangla translation.**
