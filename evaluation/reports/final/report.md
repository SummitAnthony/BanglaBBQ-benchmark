# BanglaBBQ evaluation report

Result files: 16  ·  keep filter: yes (360 templates)  ·  bootstrap over templates: 1000

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | 0.069 [0.05,0.09] | 0.963 [0.95,0.97] | +0.336 [0.27,0.40] | +0.042 [0.02,0.06] | +0.328 [0.26,0.39] | +0.042 [0.03,0.06] | 0.007 [0.00,0.01] | 0.825 [0.81,0.84] |
| Qwen/Qwen3-4B | en | 0.169 [0.14,0.20] | 0.992 [0.99,1.00] | +0.425 [0.36,0.49] | +0.012 [0.00,0.02] | +0.407 [0.34,0.47] | +0.012 [0.00,0.02] | 0.012 [0.01,0.02] | 0.862 [0.85,0.88] |
| Qwen/Qwen3-8B | bn | 0.554 [0.51,0.60] | 0.988 [0.98,0.99] | +0.210 [0.16,0.26] | +0.013 [0.00,0.02] | +0.176 [0.13,0.22] | +0.017 [0.01,0.03] | 0.026 [0.02,0.03] | 0.839 [0.82,0.85] |
| Qwen/Qwen3-8B | en | 0.461 [0.42,0.51] | 0.999 [1.00,1.00] | +0.293 [0.24,0.35] | +0.001 [0.00,0.00] | +0.278 [0.23,0.33] | +0.001 [0.00,0.00] | 0.009 [0.01,0.01] | 0.866 [0.85,0.88] |
| google/gemini-2.5-flash | bn | 0.690 [0.65,0.73] | 0.998 [1.00,1.00] | +0.218 [0.17,0.26] | +0.001 [0.00,0.00] | +0.209 [0.17,0.25] | +0.001 [0.00,0.00] | 0.004 [0.00,0.01] | 0.916 [0.90,0.93] |
| google/gemini-2.5-flash | en | 0.798 [0.76,0.83] | 0.999 [1.00,1.00] | +0.146 [0.11,0.18] | -0.000 [-0.00,0.00] | +0.142 [0.11,0.18] | -0.001 [-0.00,0.00] | 0.002 [0.00,0.00] | 0.940 [0.93,0.95] |
| openai/gpt-4.1-mini | bn | 0.384 [0.35,0.43] | 0.993 [0.99,1.00] | +0.399 [0.34,0.45] | +0.002 [-0.00,0.01] | +0.396 [0.34,0.45] | +0.002 [-0.00,0.01] | 0.002 [0.00,0.00] | 0.897 [0.88,0.91] |
| openai/gpt-4.1-mini | en | 0.372 [0.33,0.41] | 0.999 [1.00,1.00] | +0.475 [0.42,0.52] | +0.002 [0.00,0.00] | +0.469 [0.41,0.52] | +0.003 [0.00,0.01] | 0.003 [0.00,0.00] | 0.910 [0.90,0.92] |

## By category (s_amb / s_dis, acc_amb)

| model | lang | category | templates | acc_amb | s_amb | s_dis | diff_amb |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | Age_political_perception | 62 | 0.056 | +0.315 | +0.000 | +0.315 |
| Qwen/Qwen3-4B | bn | Educational_background | 76 | 0.059 | +0.457 | +0.039 | +0.447 |
| Qwen/Qwen3-4B | bn | Marital_status | 75 | 0.040 | +0.357 | +0.060 | +0.347 |
| Qwen/Qwen3-4B | bn | Mental_health_status | 67 | 0.000 | +0.579 | +0.112 | +0.575 |
| Qwen/Qwen3-4B | bn | Regional_origin | 80 | 0.175 | +0.000 | +0.000 | +0.000 |
| Qwen/Qwen3-4B | en | Age_political_perception | 62 | 0.218 | +0.378 | +0.000 | +0.347 |
| Qwen/Qwen3-4B | en | Educational_background | 76 | 0.118 | +0.775 | +0.013 | +0.763 |
| Qwen/Qwen3-4B | en | Marital_status | 75 | 0.067 | +0.419 | +0.000 | +0.413 |
| Qwen/Qwen3-4B | en | Mental_health_status | 67 | 0.015 | +0.299 | +0.045 | +0.299 |
| Qwen/Qwen3-4B | en | Regional_origin | 80 | 0.406 | +0.232 | +0.006 | +0.200 |
| Qwen/Qwen3-8B | bn | Age_political_perception | 62 | 0.742 | +0.123 | +0.000 | +0.089 |
| Qwen/Qwen3-8B | bn | Educational_background | 76 | 0.553 | +0.375 | +0.010 | +0.342 |
| Qwen/Qwen3-8B | bn | Marital_status | 75 | 0.400 | +0.140 | +0.007 | +0.113 |
| Qwen/Qwen3-8B | bn | Mental_health_status | 67 | 0.269 | +0.353 | +0.053 | +0.321 |
| Qwen/Qwen3-8B | bn | Regional_origin | 80 | 0.794 | +0.038 | +0.000 | +0.025 |
| Qwen/Qwen3-8B | en | Age_political_perception | 62 | 0.718 | +0.248 | +0.000 | +0.234 |
| Qwen/Qwen3-8B | en | Educational_background | 76 | 0.447 | +0.525 | +0.000 | +0.493 |
| Qwen/Qwen3-8B | en | Marital_status | 75 | 0.347 | +0.199 | +0.000 | +0.187 |
| Qwen/Qwen3-8B | en | Mental_health_status | 67 | 0.172 | +0.357 | +0.000 | +0.351 |
| Qwen/Qwen3-8B | en | Regional_origin | 80 | 0.625 | +0.143 | +0.006 | +0.131 |
| google/gemini-2.5-flash | bn | Age_political_perception | 62 | 0.968 | +0.032 | +0.000 | +0.024 |
| google/gemini-2.5-flash | bn | Educational_background | 76 | 0.796 | +0.204 | +0.000 | +0.197 |
| google/gemini-2.5-flash | bn | Marital_status | 75 | 0.557 | +0.303 | +0.000 | +0.287 |
| google/gemini-2.5-flash | bn | Mental_health_status | 67 | 0.437 | +0.260 | +0.004 | +0.250 |
| google/gemini-2.5-flash | bn | Regional_origin | 80 | 0.713 | +0.262 | +0.000 | +0.256 |
| google/gemini-2.5-flash | en | Age_political_perception | 62 | 0.984 | +0.016 | +0.000 | +0.016 |
| google/gemini-2.5-flash | en | Educational_background | 76 | 0.901 | +0.099 | +0.000 | +0.099 |
| google/gemini-2.5-flash | en | Marital_status | 75 | 0.693 | +0.198 | +0.000 | +0.193 |
| google/gemini-2.5-flash | en | Mental_health_status | 67 | 0.668 | +0.170 | +0.000 | +0.164 |
| google/gemini-2.5-flash | en | Regional_origin | 80 | 0.762 | +0.224 | -0.002 | +0.212 |
| openai/gpt-4.1-mini | bn | Age_political_perception | 62 | 0.496 | +0.368 | +0.000 | +0.351 |
| openai/gpt-4.1-mini | bn | Educational_background | 76 | 0.414 | +0.520 | -0.002 | +0.520 |
| openai/gpt-4.1-mini | bn | Marital_status | 75 | 0.267 | +0.453 | +0.007 | +0.453 |
| openai/gpt-4.1-mini | bn | Mental_health_status | 67 | 0.153 | +0.285 | +0.000 | +0.284 |
| openai/gpt-4.1-mini | bn | Regional_origin | 80 | 0.572 | +0.353 | +0.006 | +0.353 |
| openai/gpt-4.1-mini | en | Age_political_perception | 62 | 0.395 | +0.430 | +0.000 | +0.415 |
| openai/gpt-4.1-mini | en | Educational_background | 76 | 0.336 | +0.612 | +0.003 | +0.612 |
| openai/gpt-4.1-mini | en | Marital_status | 75 | 0.363 | +0.475 | +0.000 | +0.470 |
| openai/gpt-4.1-mini | en | Mental_health_status | 67 | 0.317 | +0.332 | +0.004 | +0.325 |
| openai/gpt-4.1-mini | en | Regional_origin | 80 | 0.444 | +0.494 | +0.003 | +0.494 |
