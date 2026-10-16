# BanglaBBQ evaluation report

Result files: 8  ·  keep filter: yes (94 templates)  ·  bootstrap over templates: 1000

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | 0.122 [0.07,0.18] | 0.979 [0.95,1.00] | +0.197 [0.07,0.32] | +0.957 [0.90,1.00] | +0.191 [0.06,0.31] | — | 0.013 [0.00,0.03] | 0.747 [0.71,0.78] |
| Qwen/Qwen3-4B | en | 0.346 [0.27,0.43] | 1.000 [1.00,1.00] | +0.218 [0.09,0.33] | +1.000 [1.00,1.00] | +0.197 [0.09,0.29] | — | 0.032 [0.02,0.05] | 0.769 [0.73,0.80] |
| Qwen/Qwen3-8B | bn | 0.761 [0.69,0.82] | 0.984 [0.96,1.00] | +0.007 [-0.07,0.09] | +0.968 [0.93,1.00] | +0.005 [-0.06,0.07] | — | 0.027 [0.01,0.04] | 0.840 [0.80,0.88] |
| Qwen/Qwen3-8B | en | 0.777 [0.70,0.85] | 1.000 [1.00,1.00] | +0.127 [0.05,0.20] | +1.000 [1.00,1.00] | +0.112 [0.04,0.19] | — | 0.013 [0.00,0.03] | 0.806 [0.77,0.85] |
| google/gemini-2.5-flash | bn | 0.894 [0.84,0.94] | 1.000 [1.00,1.00] | +0.050 [0.00,0.10] | +1.000 [1.00,1.00] | +0.048 [0.00,0.10] | — | 0.003 [0.00,0.01] | 0.941 [0.92,0.97] |
| google/gemini-2.5-flash | en | 0.918 [0.87,0.96] | 1.000 [1.00,1.00] | +0.026 [-0.03,0.08] | +1.000 [1.00,1.00] | +0.024 [-0.02,0.07] | — | 0.003 [0.00,0.01] | 0.960 [0.94,0.98] |
| openai/gpt-4.1-mini | bn | 0.598 [0.52,0.69] | 1.000 [1.00,1.00] | +0.184 [0.09,0.28] | +1.000 [1.00,1.00] | +0.170 [0.08,0.26] | — | 0.015 [0.00,0.03] | 0.868 [0.84,0.90] |
| openai/gpt-4.1-mini | en | 0.593 [0.50,0.69] | 1.000 [1.00,1.00] | +0.179 [0.08,0.28] | +1.000 [1.00,1.00] | +0.176 [0.08,0.28] | — | 0.004 [0.00,0.01] | 0.880 [0.85,0.91] |

## By category (s_amb / s_dis, acc_amb)

| model | lang | category | templates | acc_amb | s_amb | s_dis | diff_amb |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | Age_political_perception | 38 | 0.066 | +0.374 | +1.000 | +0.368 |
| Qwen/Qwen3-4B | bn | Educational_background | 18 | 0.278 | +0.389 | +0.944 | +0.389 |
| Qwen/Qwen3-4B | bn | Marital_status | 20 | 0.150 | -0.159 | +0.950 | -0.150 |
| Qwen/Qwen3-4B | bn | Mental_health_status | 3 | 0.000 | +0.000 | +0.333 | +0.000 |
| Qwen/Qwen3-4B | bn | Regional_origin | 15 | 0.067 | +0.000 | +1.000 | +0.000 |
| Qwen/Qwen3-4B | en | Age_political_perception | 38 | 0.197 | +0.268 | +1.000 | +0.224 |
| Qwen/Qwen3-4B | en | Educational_background | 18 | 0.278 | +0.549 | +1.000 | +0.528 |
| Qwen/Qwen3-4B | en | Marital_status | 20 | 0.475 | +0.025 | +1.000 | +0.025 |
| Qwen/Qwen3-4B | en | Mental_health_status | 3 | 0.000 | +0.000 | +1.000 | +0.000 |
| Qwen/Qwen3-4B | en | Regional_origin | 15 | 0.700 | +0.000 | +1.000 | +0.000 |
| Qwen/Qwen3-8B | bn | Age_political_perception | 38 | 0.750 | +0.068 | +1.000 | +0.039 |
| Qwen/Qwen3-8B | bn | Educational_background | 18 | 0.778 | +0.222 | +0.944 | +0.194 |
| Qwen/Qwen3-8B | bn | Marital_status | 20 | 0.775 | -0.169 | +0.950 | -0.150 |
| Qwen/Qwen3-8B | bn | Mental_health_status | 3 | 0.000 | +0.000 | +0.667 | +0.000 |
| Qwen/Qwen3-8B | bn | Regional_origin | 15 | 0.900 | -0.100 | +1.000 | -0.100 |
| Qwen/Qwen3-8B | en | Age_political_perception | 38 | 0.816 | +0.128 | +1.000 | +0.118 |
| Qwen/Qwen3-8B | en | Educational_background | 18 | 0.694 | +0.306 | +1.000 | +0.278 |
| Qwen/Qwen3-8B | en | Marital_status | 20 | 0.725 | +0.138 | +1.000 | +0.100 |
| Qwen/Qwen3-8B | en | Mental_health_status | 3 | 0.167 | -0.167 | +1.000 | -0.167 |
| Qwen/Qwen3-8B | en | Regional_origin | 15 | 0.967 | -0.033 | +1.000 | -0.033 |
| google/gemini-2.5-flash | bn | Age_political_perception | 38 | 0.974 | -0.026 | +1.000 | -0.013 |
| google/gemini-2.5-flash | bn | Educational_background | 18 | 0.889 | +0.111 | +1.000 | +0.111 |
| google/gemini-2.5-flash | bn | Marital_status | 20 | 0.825 | +0.125 | +1.000 | +0.125 |
| google/gemini-2.5-flash | bn | Mental_health_status | 3 | 0.167 | +0.167 | +1.000 | +0.167 |
| google/gemini-2.5-flash | bn | Regional_origin | 15 | 0.933 | +0.000 | +1.000 | +0.000 |
| google/gemini-2.5-flash | en | Age_political_perception | 38 | 0.974 | -0.026 | +1.000 | -0.013 |
| google/gemini-2.5-flash | en | Educational_background | 18 | 0.931 | +0.069 | +1.000 | +0.069 |
| google/gemini-2.5-flash | en | Marital_status | 20 | 0.875 | +0.075 | +1.000 | +0.075 |
| google/gemini-2.5-flash | en | Mental_health_status | 3 | 0.333 | +0.000 | +1.000 | +0.000 |
| google/gemini-2.5-flash | en | Regional_origin | 15 | 0.933 | +0.000 | +1.000 | +0.000 |
| openai/gpt-4.1-mini | bn | Age_political_perception | 38 | 0.533 | +0.110 | +1.000 | +0.105 |
| openai/gpt-4.1-mini | bn | Educational_background | 18 | 0.694 | +0.306 | +1.000 | +0.278 |
| openai/gpt-4.1-mini | bn | Marital_status | 20 | 0.625 | +0.260 | +1.000 | +0.225 |
| openai/gpt-4.1-mini | bn | Mental_health_status | 3 | 0.000 | +0.000 | +1.000 | +0.000 |
| openai/gpt-4.1-mini | bn | Regional_origin | 15 | 0.733 | +0.190 | +1.000 | +0.167 |
| openai/gpt-4.1-mini | en | Age_political_perception | 38 | 0.507 | +0.192 | +1.000 | +0.184 |
| openai/gpt-4.1-mini | en | Educational_background | 18 | 0.569 | +0.431 | +1.000 | +0.431 |
| openai/gpt-4.1-mini | en | Marital_status | 20 | 0.713 | +0.137 | +1.000 | +0.138 |
| openai/gpt-4.1-mini | en | Mental_health_status | 3 | 0.000 | -0.333 | +1.000 | -0.333 |
| openai/gpt-4.1-mini | en | Regional_origin | 15 | 0.800 | +0.000 | +1.000 | +0.000 |

> **Note:** every disambiguated context in this data is written in the stereotype-aligned direction, so s_dis equals 1 whenever the model answers correctly and diff_dis is undefined. Read disambiguated results as accuracy only; bias is measured by the ambiguous-context scores.
