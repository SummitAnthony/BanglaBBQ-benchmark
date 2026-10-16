# BanglaBBQ evaluation report

Result files: 8  ·  keep filter: yes (372 templates)  ·  bootstrap over templates: 1000

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | 0.071 [0.05,0.09] | 0.984 [0.97,0.99] | +0.329 [0.26,0.40] | +0.968 [0.95,0.98] | +0.321 [0.26,0.39] | — | 0.011 [0.01,0.02] | 0.769 [0.75,0.79] |
| Qwen/Qwen3-4B | en | 0.172 [0.14,0.20] | 0.999 [1.00,1.00] | +0.418 [0.35,0.49] | +0.997 [0.99,1.00] | +0.401 [0.34,0.47] | — | 0.017 [0.01,0.02] | 0.804 [0.79,0.82] |
| Qwen/Qwen3-8B | bn | 0.556 [0.51,0.60] | 0.995 [0.99,1.00] | +0.211 [0.16,0.26] | +0.992 [0.98,1.00] | +0.176 [0.13,0.22] | — | 0.037 [0.03,0.05] | 0.778 [0.76,0.80] |
| Qwen/Qwen3-8B | en | 0.458 [0.41,0.50] | 1.000 [1.00,1.00] | +0.290 [0.23,0.35] | +1.000 [1.00,1.00] | +0.276 [0.22,0.33] | — | 0.013 [0.01,0.02] | 0.802 [0.78,0.82] |
| google/gemini-2.5-flash | bn | 0.684 [0.65,0.72] | 0.999 [1.00,1.00] | +0.219 [0.18,0.26] | +0.997 [0.99,1.00] | +0.210 [0.17,0.25] | — | 0.006 [0.00,0.01] | 0.873 [0.86,0.89] |
| google/gemini-2.5-flash | en | 0.792 [0.76,0.83] | 0.999 [1.00,1.00] | +0.148 [0.11,0.18] | +1.000 [1.00,1.00] | +0.144 [0.11,0.18] | — | 0.003 [0.00,0.01] | 0.912 [0.90,0.93] |
| openai/gpt-4.1-mini | bn | 0.380 [0.34,0.42] | 0.995 [0.99,1.00] | +0.402 [0.34,0.46] | +0.992 [0.98,1.00] | +0.399 [0.34,0.45] | — | 0.002 [0.00,0.01] | 0.849 [0.83,0.86] |
| openai/gpt-4.1-mini | en | 0.368 [0.33,0.41] | 1.000 [1.00,1.00] | +0.475 [0.42,0.52] | +1.000 [1.00,1.00] | +0.468 [0.42,0.52] | — | 0.004 [0.00,0.01] | 0.869 [0.85,0.89] |

## By category (s_amb / s_dis, acc_amb)

| model | lang | category | templates | acc_amb | s_amb | s_dis | diff_amb |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | Age_political_perception | 62 | 0.056 | +0.315 | +0.952 | +0.315 |
| Qwen/Qwen3-4B | bn | Educational_background | 77 | 0.058 | +0.438 | +0.974 | +0.429 |
| Qwen/Qwen3-4B | bn | Marital_status | 80 | 0.037 | +0.359 | +0.975 | +0.350 |
| Qwen/Qwen3-4B | bn | Mental_health_status | 68 | 0.000 | +0.585 | +0.971 | +0.581 |
| Qwen/Qwen3-4B | bn | Regional_origin | 85 | 0.182 | -0.006 | +0.965 | -0.006 |
| Qwen/Qwen3-4B | en | Age_political_perception | 62 | 0.218 | +0.378 | +1.000 | +0.347 |
| Qwen/Qwen3-4B | en | Educational_background | 77 | 0.123 | +0.758 | +1.000 | +0.747 |
| Qwen/Qwen3-4B | en | Marital_status | 80 | 0.069 | +0.412 | +0.988 | +0.406 |
| Qwen/Qwen3-4B | en | Mental_health_status | 68 | 0.015 | +0.309 | +1.000 | +0.309 |
| Qwen/Qwen3-4B | en | Regional_origin | 85 | 0.406 | +0.225 | +1.000 | +0.194 |
| Qwen/Qwen3-8B | bn | Age_political_perception | 62 | 0.742 | +0.123 | +1.000 | +0.089 |
| Qwen/Qwen3-8B | bn | Educational_background | 77 | 0.558 | +0.370 | +1.000 | +0.338 |
| Qwen/Qwen3-8B | bn | Marital_status | 80 | 0.400 | +0.148 | +0.988 | +0.119 |
| Qwen/Qwen3-8B | bn | Mental_health_status | 68 | 0.265 | +0.364 | +0.985 | +0.331 |
| Qwen/Qwen3-8B | bn | Regional_origin | 85 | 0.800 | +0.036 | +0.988 | +0.024 |
| Qwen/Qwen3-8B | en | Age_political_perception | 62 | 0.718 | +0.248 | +1.000 | +0.234 |
| Qwen/Qwen3-8B | en | Educational_background | 77 | 0.448 | +0.511 | +1.000 | +0.481 |
| Qwen/Qwen3-8B | en | Marital_status | 80 | 0.338 | +0.212 | +1.000 | +0.200 |
| Qwen/Qwen3-8B | en | Mental_health_status | 68 | 0.169 | +0.367 | +1.000 | +0.360 |
| Qwen/Qwen3-8B | en | Regional_origin | 85 | 0.624 | +0.134 | +1.000 | +0.124 |
| google/gemini-2.5-flash | bn | Age_political_perception | 62 | 0.968 | +0.032 | +1.000 | +0.024 |
| google/gemini-2.5-flash | bn | Educational_background | 77 | 0.799 | +0.201 | +1.000 | +0.195 |
| google/gemini-2.5-flash | bn | Marital_status | 80 | 0.547 | +0.296 | +0.988 | +0.281 |
| google/gemini-2.5-flash | bn | Mental_health_status | 68 | 0.445 | +0.257 | +1.000 | +0.246 |
| google/gemini-2.5-flash | bn | Regional_origin | 85 | 0.694 | +0.270 | +1.000 | +0.265 |
| google/gemini-2.5-flash | en | Age_political_perception | 62 | 0.984 | +0.016 | +1.000 | +0.016 |
| google/gemini-2.5-flash | en | Educational_background | 77 | 0.903 | +0.097 | +1.000 | +0.097 |
| google/gemini-2.5-flash | en | Marital_status | 80 | 0.675 | +0.210 | +1.000 | +0.206 |
| google/gemini-2.5-flash | en | Mental_health_status | 68 | 0.673 | +0.167 | +1.000 | +0.162 |
| google/gemini-2.5-flash | en | Regional_origin | 85 | 0.759 | +0.216 | +1.000 | +0.206 |
| openai/gpt-4.1-mini | bn | Age_political_perception | 62 | 0.496 | +0.368 | +0.984 | +0.351 |
| openai/gpt-4.1-mini | bn | Educational_background | 77 | 0.409 | +0.526 | +1.000 | +0.526 |
| openai/gpt-4.1-mini | bn | Marital_status | 80 | 0.263 | +0.450 | +0.975 | +0.450 |
| openai/gpt-4.1-mini | bn | Mental_health_status | 68 | 0.151 | +0.295 | +1.000 | +0.294 |
| openai/gpt-4.1-mini | bn | Regional_origin | 85 | 0.562 | +0.356 | +1.000 | +0.356 |
| openai/gpt-4.1-mini | en | Age_political_perception | 62 | 0.395 | +0.430 | +1.000 | +0.415 |
| openai/gpt-4.1-mini | en | Educational_background | 77 | 0.331 | +0.617 | +1.000 | +0.617 |
| openai/gpt-4.1-mini | en | Marital_status | 80 | 0.347 | +0.476 | +1.000 | +0.472 |
| openai/gpt-4.1-mini | en | Mental_health_status | 68 | 0.312 | +0.342 | +1.000 | +0.335 |
| openai/gpt-4.1-mini | en | Regional_origin | 85 | 0.447 | +0.482 | +1.000 | +0.476 |

> **Note:** every disambiguated context in this data is written in the stereotype-aligned direction, so s_dis equals 1 whenever the model answers correctly and diff_dis is undefined. Read disambiguated results as accuracy only; bias is measured by the ambiguous-context scores.
