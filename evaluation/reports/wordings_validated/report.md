# BanglaBBQ evaluation report

Result files: 14  ·  keep filter: yes (372 templates)  ·  bootstrap over templates: 1000

Excluded runs (`--exclude`): Qwen/Qwen3-8B en prompt_id 2 (11,184 calls)

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | 0.071 [0.05,0.09] | 0.984 [0.97,0.99] | +0.329 [0.26,0.40] | +0.968 [0.95,0.98] | +0.321 [0.26,0.39] | — | 0.011 [0.01,0.02] | 0.769 [0.75,0.79] |
| Qwen/Qwen3-4B | en | 0.172 [0.14,0.20] | 0.999 [1.00,1.00] | +0.418 [0.35,0.49] | +0.997 [0.99,1.00] | +0.401 [0.34,0.47] | — | 0.017 [0.01,0.02] | 0.804 [0.79,0.82] |
| Qwen/Qwen3-8B | bn | 0.652 ±0.163 | 0.995 | +0.181 ±0.043 | +0.992 | +0.151 ±0.039 | — | 0.028 ±0.011 | 0.795 ±0.024 |
| Qwen/Qwen3-8B | en | 0.531 ±0.103 | 0.998 ±0.003 | +0.275 ±0.021 | +0.999 ±0.002 | +0.260 ±0.022 | — | 0.012 ±0.001 | 0.811 ±0.013 |
| google/gemini-2.5-flash | bn | 0.775 ±0.084 | 0.997 ±0.001 | +0.155 ±0.058 | +0.997 ±0.000 | +0.149 ±0.055 | — | 0.005 ±0.002 | 0.876 ±0.008 |
| google/gemini-2.5-flash | en | 0.870 ±0.073 | 0.998 ±0.001 | +0.095 ±0.052 | +1.000 | +0.092 ±0.050 | — | 0.002 ±0.002 | 0.935 ±0.024 |
| openai/gpt-4.1-mini | bn | 0.572 ±0.205 | 0.994 ±0.000 | +0.285 ±0.133 | +0.991 ±0.001 | +0.278 ±0.132 | — | 0.005 ±0.004 | 0.857 ±0.045 |
| openai/gpt-4.1-mini | en | 0.551 ±0.168 | 0.999 ±0.001 | +0.351 ±0.110 | +1.000 | +0.326 ±0.134 | — | 0.015 ±0.017 | 0.857 ±0.023 |

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
| Qwen/Qwen3-8B | bn | Age_political_perception | 62 | 0.790 ±0.043 | +0.135 ±0.020 | +1.000 | +0.089 ±0.016 |
| Qwen/Qwen3-8B | bn | Educational_background | 77 | 0.631 ±0.123 | +0.313 ±0.086 | +0.996 ±0.007 | +0.295 ±0.070 |
| Qwen/Qwen3-8B | bn | Marital_status | 80 | 0.540 ±0.303 | +0.131 ±0.062 | +0.987 ±0.000 | +0.102 ±0.064 |
| Qwen/Qwen3-8B | bn | Mental_health_status | 68 | 0.458 ±0.280 | +0.282 ±0.108 | +0.985 ±0.000 | +0.262 ±0.095 |
| Qwen/Qwen3-8B | bn | Regional_origin | 85 | 0.830 ±0.088 | +0.040 ±0.029 | +0.992 ±0.007 | +0.025 ±0.016 |
| Qwen/Qwen3-8B | en | Age_political_perception | 62 | 0.815 ±0.137 | +0.168 ±0.113 | +1.000 | +0.161 ±0.103 |
| Qwen/Qwen3-8B | en | Educational_background | 77 | 0.503 ±0.078 | +0.462 ±0.068 | +1.000 | +0.438 ±0.060 |
| Qwen/Qwen3-8B | en | Marital_status | 80 | 0.391 ±0.075 | +0.240 ±0.040 | +0.994 ±0.009 | +0.228 ±0.040 |
| Qwen/Qwen3-8B | en | Mental_health_status | 68 | 0.272 ±0.146 | +0.347 ±0.027 | +1.000 | +0.335 ±0.036 |
| Qwen/Qwen3-8B | en | Regional_origin | 85 | 0.688 ±0.092 | +0.157 ±0.033 | +1.000 | +0.141 ±0.025 |
| google/gemini-2.5-flash | bn | Age_political_perception | 62 | 0.976 ±0.018 | +0.023 ±0.020 | +1.000 | +0.020 ±0.018 |
| google/gemini-2.5-flash | bn | Educational_background | 77 | 0.866 ±0.059 | +0.134 ±0.059 | +1.000 | +0.130 ±0.057 |
| google/gemini-2.5-flash | bn | Marital_status | 80 | 0.679 ±0.126 | +0.226 ±0.066 | +0.988 | +0.214 ±0.062 |
| google/gemini-2.5-flash | bn | Mental_health_status | 68 | 0.567 ±0.115 | +0.196 ±0.056 | +1.000 | +0.189 ±0.053 |
| google/gemini-2.5-flash | bn | Regional_origin | 85 | 0.802 ±0.098 | +0.170 ±0.087 | +1.000 | +0.167 ±0.086 |
| google/gemini-2.5-flash | en | Age_political_perception | 62 | 0.995 ±0.009 | +0.005 ±0.009 | +1.000 | +0.005 ±0.009 |
| google/gemini-2.5-flash | en | Educational_background | 77 | 0.933 ±0.033 | +0.067 ±0.033 | +1.000 | +0.067 ±0.033 |
| google/gemini-2.5-flash | en | Marital_status | 80 | 0.763 ±0.086 | +0.163 ±0.051 | +1.000 | +0.160 ±0.049 |
| google/gemini-2.5-flash | en | Mental_health_status | 68 | 0.809 ±0.123 | +0.097 ±0.069 | +1.000 | +0.088 ±0.067 |
| google/gemini-2.5-flash | en | Regional_origin | 85 | 0.873 ±0.105 | +0.119 ±0.091 | +1.000 | +0.116 ±0.086 |
| openai/gpt-4.1-mini | bn | Age_political_perception | 62 | 0.720 ±0.211 | +0.212 ±0.150 | +0.984 | +0.203 ±0.142 |
| openai/gpt-4.1-mini | bn | Educational_background | 77 | 0.591 ±0.180 | +0.383 ±0.148 | +1.000 | +0.380 ±0.151 |
| openai/gpt-4.1-mini | bn | Marital_status | 80 | 0.488 ±0.268 | +0.325 ±0.160 | +0.975 | +0.318 ±0.159 |
| openai/gpt-4.1-mini | bn | Mental_health_status | 68 | 0.355 ±0.204 | +0.264 ±0.057 | +1.000 | +0.262 ±0.055 |
| openai/gpt-4.1-mini | bn | Regional_origin | 85 | 0.701 ±0.175 | +0.228 ±0.149 | +0.998 ±0.003 | +0.218 ±0.150 |
| openai/gpt-4.1-mini | en | Age_political_perception | 62 | 0.692 ±0.258 | +0.243 ±0.162 | +1.000 | +0.220 ±0.169 |
| openai/gpt-4.1-mini | en | Educational_background | 77 | 0.537 ±0.188 | +0.442 ±0.162 | +1.000 | +0.424 ±0.184 |
| openai/gpt-4.1-mini | en | Marital_status | 80 | 0.485 ±0.129 | +0.391 ±0.074 | +1.000 | +0.365 ±0.103 |
| openai/gpt-4.1-mini | en | Mental_health_status | 68 | 0.491 ±0.178 | +0.264 ±0.067 | +1.000 | +0.249 ±0.076 |
| openai/gpt-4.1-mini | en | Regional_origin | 85 | 0.571 ±0.127 | +0.383 ±0.100 | +1.000 | +0.338 ±0.150 |

> **Note:** every disambiguated context in this data is written in the stereotype-aligned direction, so s_dis equals 1 whenever the model answers correctly and diff_dis is undefined. Read disambiguated results as accuracy only; bias is measured by the ambiguous-context scores.
