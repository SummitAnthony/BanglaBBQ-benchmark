# BanglaBBQ evaluation report

Result files: 4  ·  keep filter: no (all templates)  ·  bootstrap over templates: 1000

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | 0.323 [0.27,0.38] | 0.838 [0.80,0.88] | +0.294 [0.23,0.36] | +0.058 [0.03,0.09] | +0.275 [0.21,0.34] | +0.060 [0.03,0.09] | 0.023 [0.02,0.03] | 0.734 [0.71,0.76] |
| Qwen/Qwen3-4B | en | 0.643 [0.58,0.71] | 0.899 [0.86,0.93] | +0.224 [0.16,0.29] | +0.035 [0.01,0.07] | +0.211 [0.15,0.27] | +0.044 [0.01,0.07] | 0.013 [0.01,0.02] | 0.825 [0.80,0.85] |
| Qwen/Qwen3-8B | bn | 0.707 [0.64,0.78] | 0.859 [0.82,0.90] | +0.178 [0.12,0.23] | +0.056 [0.02,0.09] | +0.151 [0.10,0.20] | +0.063 [0.03,0.10] | 0.027 [0.02,0.04] | 0.764 [0.73,0.80] |
| Qwen/Qwen3-8B | en | 0.858 [0.80,0.91] | 0.904 [0.87,0.94] | +0.106 [0.06,0.16] | +0.026 [0.00,0.05] | +0.101 [0.06,0.15] | +0.039 [0.01,0.07] | 0.005 [0.00,0.01] | 0.876 [0.85,0.90] |

## By category (s_amb / s_dis, acc_amb)

| model | lang | category | templates | acc_amb | s_amb | s_dis | diff_amb |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | Age | 21 | 0.247 | +0.132 | +0.048 | +0.125 |
| Qwen/Qwen3-4B | bn | Disability_status | 25 | 0.167 | +0.445 | +0.006 | +0.422 |
| Qwen/Qwen3-4B | bn | Gender_identity | 43 | 0.599 | +0.068 | +0.079 | +0.055 |
| Qwen/Qwen3-4B | bn | Physical_appearance | 22 | 0.360 | +0.253 | +0.043 | +0.241 |
| Qwen/Qwen3-4B | bn | Religion | 5 | 0.150 | +0.800 | +0.150 | +0.800 |
| Qwen/Qwen3-4B | bn | SES | 24 | 0.321 | +0.476 | +0.115 | +0.443 |
| Qwen/Qwen3-4B | en | Age | 21 | 0.512 | +0.224 | +0.012 | +0.211 |
| Qwen/Qwen3-4B | en | Disability_status | 25 | 0.578 | +0.281 | +0.003 | +0.261 |
| Qwen/Qwen3-4B | en | Gender_identity | 43 | 0.853 | +0.063 | +0.024 | +0.055 |
| Qwen/Qwen3-4B | en | Physical_appearance | 22 | 0.631 | +0.251 | +0.055 | +0.241 |
| Qwen/Qwen3-4B | en | Religion | 5 | 0.700 | +0.300 | +0.571 | +0.300 |
| Qwen/Qwen3-4B | en | SES | 24 | 0.682 | +0.260 | +0.034 | +0.247 |
| Qwen/Qwen3-8B | bn | Age | 21 | 0.631 | +0.137 | +0.072 | +0.098 |
| Qwen/Qwen3-8B | bn | Disability_status | 25 | 0.526 | +0.261 | +0.087 | +0.218 |
| Qwen/Qwen3-8B | bn | Gender_identity | 43 | 0.908 | +0.034 | +0.052 | +0.026 |
| Qwen/Qwen3-8B | bn | Physical_appearance | 22 | 0.670 | +0.251 | +0.059 | +0.244 |
| Qwen/Qwen3-8B | bn | Religion | 5 | 0.650 | +0.350 | +0.282 | +0.350 |
| Qwen/Qwen3-8B | bn | SES | 24 | 0.872 | +0.115 | -0.027 | +0.115 |
| Qwen/Qwen3-8B | en | Age | 21 | 0.720 | +0.211 | -0.019 | +0.202 |
| Qwen/Qwen3-8B | en | Disability_status | 25 | 0.871 | +0.075 | +0.018 | +0.072 |
| Qwen/Qwen3-8B | en | Gender_identity | 43 | 0.967 | +0.022 | +0.000 | +0.015 |
| Qwen/Qwen3-8B | en | Physical_appearance | 22 | 0.836 | +0.122 | +0.051 | +0.122 |
| Qwen/Qwen3-8B | en | Religion | 5 | 0.700 | +0.300 | +0.333 | +0.300 |
| Qwen/Qwen3-8B | en | SES | 24 | 0.946 | +0.054 | +0.046 | +0.051 |
