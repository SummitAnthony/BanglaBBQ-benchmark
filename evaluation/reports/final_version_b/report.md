# BanglaBBQ evaluation report

Result files: 8  ·  keep filter: yes (360 templates)  ·  bootstrap over templates: 1000

Values are means over prompt wordings (± sd) when several wordings were run; with a single wording, brackets give 95% bootstrap CIs. Bias scores: positive = stereotype-aligned, negative = counter-stereotypical, 0 = no preference.

## Overall

| model | lang | acc_amb | acc_dis | s_amb | s_dis | diff_amb | diff_dis | out-of-choice | consistency |
|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | — | 0.942 [0.92,0.96] | — | -0.883 [-0.92,-0.85] | — | — | 0.000 [0.00,0.00] | 0.935 [0.92,0.95] |
| Qwen/Qwen3-4B | en | — | 0.986 [0.98,0.99] | — | -0.972 [-0.99,-0.95] | — | — | 0.000 [0.00,0.00] | 0.976 [0.97,0.99] |
| Qwen/Qwen3-8B | bn | — | 0.979 [0.97,0.99] | — | -0.972 [-0.99,-0.95] | — | — | 0.006 [0.00,0.01] | 0.960 [0.94,0.97] |
| Qwen/Qwen3-8B | en | — | 0.999 [1.00,1.00] | — | -0.997 [-1.00,-0.99] | — | — | 0.000 [0.00,0.00] | 0.993 [0.99,1.00] |
| google/gemini-2.5-flash | bn | — | 0.998 [0.99,1.00] | — | -0.996 [-1.00,-0.99] | — | — | 0.000 [0.00,0.00] | 0.999 [0.99,1.00] |
| google/gemini-2.5-flash | en | — | 0.999 [1.00,1.00] | — | -1.000 [-1.00,-1.00] | — | — | 0.000 [0.00,0.00] | 0.999 [1.00,1.00] |
| openai/gpt-4.1-mini | bn | — | 0.992 [0.99,1.00] | — | -0.986 [-1.00,-0.97] | — | — | 0.000 [0.00,0.00] | 0.997 [0.99,1.00] |
| openai/gpt-4.1-mini | en | — | 0.997 [0.99,1.00] | — | -0.997 [-1.00,-0.99] | — | — | 0.000 [0.00,0.00] | 0.996 [0.99,1.00] |

## By category (s_amb / s_dis, acc_amb)

| model | lang | category | templates | acc_amb | s_amb | s_dis | diff_amb |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-4B | bn | Age_political_perception | 62 | — | — | -0.952 | — |
| Qwen/Qwen3-4B | bn | Educational_background | 76 | — | — | -0.895 | — |
| Qwen/Qwen3-4B | bn | Marital_status | 75 | — | — | -0.853 | — |
| Qwen/Qwen3-4B | bn | Mental_health_status | 67 | — | — | -0.746 | — |
| Qwen/Qwen3-4B | bn | Regional_origin | 80 | — | — | -0.963 | — |
| Qwen/Qwen3-4B | en | Age_political_perception | 62 | — | — | -1.000 | — |
| Qwen/Qwen3-4B | en | Educational_background | 76 | — | — | -0.974 | — |
| Qwen/Qwen3-4B | en | Marital_status | 75 | — | — | -0.987 | — |
| Qwen/Qwen3-4B | en | Mental_health_status | 67 | — | — | -0.910 | — |
| Qwen/Qwen3-4B | en | Regional_origin | 80 | — | — | -0.988 | — |
| Qwen/Qwen3-8B | bn | Age_political_perception | 62 | — | — | -1.000 | — |
| Qwen/Qwen3-8B | bn | Educational_background | 76 | — | — | -0.987 | — |
| Qwen/Qwen3-8B | bn | Marital_status | 75 | — | — | -0.973 | — |
| Qwen/Qwen3-8B | bn | Mental_health_status | 67 | — | — | -0.908 | — |
| Qwen/Qwen3-8B | bn | Regional_origin | 80 | — | — | -0.988 | — |
| Qwen/Qwen3-8B | en | Age_political_perception | 62 | — | — | -1.000 | — |
| Qwen/Qwen3-8B | en | Educational_background | 76 | — | — | -1.000 | — |
| Qwen/Qwen3-8B | en | Marital_status | 75 | — | — | -1.000 | — |
| Qwen/Qwen3-8B | en | Mental_health_status | 67 | — | — | -1.000 | — |
| Qwen/Qwen3-8B | en | Regional_origin | 80 | — | — | -0.988 | — |
| google/gemini-2.5-flash | bn | Age_political_perception | 62 | — | — | -1.000 | — |
| google/gemini-2.5-flash | bn | Educational_background | 76 | — | — | -1.000 | — |
| google/gemini-2.5-flash | bn | Marital_status | 75 | — | — | -0.987 | — |
| google/gemini-2.5-flash | bn | Mental_health_status | 67 | — | — | -0.993 | — |
| google/gemini-2.5-flash | bn | Regional_origin | 80 | — | — | -1.000 | — |
| google/gemini-2.5-flash | en | Age_political_perception | 62 | — | — | -1.000 | — |
| google/gemini-2.5-flash | en | Educational_background | 76 | — | — | -1.000 | — |
| google/gemini-2.5-flash | en | Marital_status | 75 | — | — | -1.000 | — |
| google/gemini-2.5-flash | en | Mental_health_status | 67 | — | — | -1.000 | — |
| google/gemini-2.5-flash | en | Regional_origin | 80 | — | — | -1.000 | — |
| openai/gpt-4.1-mini | bn | Age_political_perception | 62 | — | — | -0.984 | — |
| openai/gpt-4.1-mini | bn | Educational_background | 76 | — | — | -1.000 | — |
| openai/gpt-4.1-mini | bn | Marital_status | 75 | — | — | -0.960 | — |
| openai/gpt-4.1-mini | bn | Mental_health_status | 67 | — | — | -1.000 | — |
| openai/gpt-4.1-mini | bn | Regional_origin | 80 | — | — | -0.988 | — |
| openai/gpt-4.1-mini | en | Age_political_perception | 62 | — | — | -1.000 | — |
| openai/gpt-4.1-mini | en | Educational_background | 76 | — | — | -0.993 | — |
| openai/gpt-4.1-mini | en | Marital_status | 75 | — | — | -1.000 | — |
| openai/gpt-4.1-mini | en | Mental_health_status | 67 | — | — | -0.993 | — |
| openai/gpt-4.1-mini | en | Regional_origin | 80 | — | — | -1.000 | — |
