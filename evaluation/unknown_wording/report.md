> **Note (release).** Reproduced as written during development. Paths in it refer to the development
> repository: `scripts/compile_bangla.py` is a development script that is not part of this release, and
> `evaluation/kaggle/unknown_wording_test.py` is `evaluation/unknown_wording/unknown_wording_test.py`.
> The pilot ran Qwen3-4B, one of the evaluated models, on 150 records of the benchmark itself, so the
> Bangla Unknown wording was chosen on test items; Qwen3-4B's Bangla `acc_amb` is not fully independent
> of that choice. "The Bangla file of 2026-09-03" then held the political-affiliation category, which
> was withdrawn before release, instead of Age_political_perception: 30 of the 150 pilot records (10
> templates) come from that withdrawn category, and no Age_political_perception record was in the
> pilot. "The four categories shared with English" are the four categories that the Bangla file and
> the English file of the full Qwen3-4B run then had in common (Marital_status, Educational_background,
> Regional_origin, Mental_health_status).

# Bangla "Unknown" option wording test (2026-10-03)

**Decision:** the Bangla Unknown option changed from **অজানা** to **যথেষ্ট তথ্য নেই** ("not enough
information", one of the original BBQ unknown phrasings) in `scripts/compile_bangla.py`.

## Why

In the pilot runs both Qwen3-4B and Qwen3-8B chose অজানা on **0%** of ambiguous Bangla items
(200-record smoke tests, Marital_status) while choosing English "Unknown" on 14–40% of the same
items, and the avoidance held at every option position (unknown shown as A, B or C). অজানা usually
means "unknown / unfamiliar" (অজানা পথ, an unfamiliar road), so as an answer to "who …?" it can
read as "an unknown person" rather than "the context does not say".

## Method

- Model: Qwen/Qwen3-4B (fp16, Kaggle 2×T4), same protocol as the main evaluation: prompt 0,
  3 cyclic option orders, greedy decoding, thinking disabled.
- Items: 10 evenly spaced templates per category (5 categories, Bangla file of 2026-09-03), per
  template the first ambiguous-negative, ambiguous-nonnegative and disambiguated-negative record
  → 100 ambiguous + 50 disambiguated records.
- Only the Unknown option's text was replaced (in memory); everything else identical.
  5 wordings × 150 records × 3 orders = 2,250 calls. Script: `evaluation/kaggle/unknown_wording_test.py`.

## Results

| Unknown wording | ambiguous → Unknown | ambiguous records with majority Unknown | disambiguated correct | disambiguated → Unknown | out-of-choice |
|---|--:|--:|--:|--:|--:|
| অজানা (old) | 3.0% | 1/100 | 100% | 0% | 0.2% |
| বলা সম্ভব নয় ("cannot be said") | 27.3% | 25/100 | 100% | 0% | 0% |
| **যথেষ্ট তথ্য নেই ("not enough information")** | **13.7%** | **14/100** | **100%** | **0%** | **0%** |
| আমি জানি না ("I don't know") | 1.3% | 1/100 | 100% | 0% | 0.2% |
| আমি বলতে পারি না ("I can't say") | 2.0% | 1/100 | 99.3% | 0% | 0.2% |

English reference: on the 80 ambiguous records from the four categories shared with English, the
full English Qwen3-4B run chose "Unknown" 11.7% of the time; on the same 80 records অজানা = 1.7%,
যথেষ্ট তথ্য নেই = 9.2%, বলা সম্ভব নয় = 19.6%.

## Reading

- The near-zero Unknown rate in Bangla was an artifact of the word অজানা, not of the model:
  swapping only the option text raised it from 3.0% to 13.7–27.3% (300 calls per wording).
- No wording pulled answers onto Unknown when the context names the answer (disambiguated
  accuracy 99.3–100%, Unknown 0%), so the gain is not an "attractive option" effect.
- First-person wordings behave like অজানা and were rejected.
- যথেষ্ট তথ্য নেই was chosen over বলা সম্ভব নয় because its rate is closest to English "Unknown"
  (9.2% vs 11.7% on shared items), keeping English–Bangla comparisons about the model rather than
  the option wording.
