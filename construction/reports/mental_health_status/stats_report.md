# Template summary — templates/mental_health_validated.jsonl

- Template count: **71**  (cap 100)  -> projected records: **568**
- Duplicate template_id: none

## Per target group (stereotyped_groups)
  - people with mental illness                    40
  - people with depression                        18
  - people with schizophrenia                     5
  - people with anxiety                           4
  - women with depression                         2
  - women with mental illness                     2

## Per subcategory
  - family                         14
  - community                      12
  - healthcare                     9
  - workplace                      5
  - marriage                       5
  - education                      3
  - social                         3
  - help_seeking                   3
  - legal                          2
  - online                         1
  - school                         1
  - university                     1
  - housing                        1
  - childcare                      1
  - employment                     1
  - public_space                   1
  - religion                       1
  - neighbourhood                  1
  - parenting                      1
  - hiring                         1
  - leadership                     1
  - pay                            1
  - finance                        1
  - social_visit                   1

## Per target_label
  - mentallyIll          42
  - depressed            20
  - schizophrenic        5
  - anxious              4

## Per source domain (over-concentration flag if one dominates)
  - pmc.ncbi.nlm.nih.gov                24  (34%)
  - ncbi.nlm.nih.gov                    16  (23%)
  - thedailystar.net                    8  (11%)
  - cambridge.org                       6  (8%)
  - archive.dhakatribune.com            3  (4%)
  - tbsnews.net                         3  (4%)
  - newagebd.net                        3  (4%)
  - link.springer.com                   3  (4%)
  - researchgate.net                    2  (3%)
  - bmcpsychiatry.biomedcentral.com     1  (1%)
  - journals.plos.org                   1  (1%)
  - dhakatribune.com                    1  (1%)

## Scenario density (target_label × subcategory)
  - mentallyIll    / community                10
  - mentallyIll    / family                   7
  - depressed      / family                   5
  - mentallyIll    / healthcare               5
  - mentallyIll    / marriage                 5
  - schizophrenic  / healthcare               3
  - depressed      / help_seeking             3
  - depressed      / education                2
  - depressed      / workplace                2
  - depressed      / community                2
  - mentallyIll    / workplace                2
  - mentallyIll    / legal                    2
  - anxious        / workplace                1
  - anxious        / education                1
  - anxious        / family                   1
  - depressed      / social                   1
  - anxious        / social                   1
  - depressed      / online                   1
  - depressed      / school                   1
  - depressed      / university               1
  - mentallyIll    / housing                  1
  - mentallyIll    / childcare                1
  - schizophrenic  / employment               1
  - mentallyIll    / public_space             1
  - mentallyIll    / social                   1
  - mentallyIll    / religion                 1
  - mentallyIll    / neighbourhood            1
  - schizophrenic  / family                   1
  - depressed      / parenting                1
  - mentallyIll    / hiring                   1
  - mentallyIll    / leadership               1
  - mentallyIll    / pay                      1
  - mentallyIll    / finance                  1
  - depressed      / healthcare               1
  - mentallyIll    / social_visit             1

# Compiled-record invariant check — output/banglabbq_mental_health_eng.jsonl

- Total records: **568**
- label distribution: {0: 142, 1: 213, 2: 213}  (expect ratio 2:3:3)
  expected for 71 templates: {0:142, 1:213, 2:213}
- context_condition: {'ambig': 284, 'disambig': 284}  (expect 50/50)
- question_polarity: {'neg': 284, 'nonneg': 284}  (expect 50/50)
- question_index groups: 71; any != 8 rows: none
- ambiguous rows whose correct answer is NOT Unknown: none
- disambig rows whose correct answer IS Unknown: none
- per-template label multiset != {0:2,1:3,2:3}: none
- duplicate example_id: none
- example_id contiguous 0..N-1: True
- id == example_id for all rows: True
- additional_metadata has exactly 4 keys everywhere: True

## Verdict: PASS — all invariants hold
