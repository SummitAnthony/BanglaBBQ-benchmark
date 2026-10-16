# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""
Generate version b (counter-stereotypical) Bangla compiled records for all 5 NA categories
using bn.disambig_counterbiased sentences from templates_with_counter.jsonl.

For each category:
  - Loads Bangla version a compiled JSONL (_bng_v2)
  - Replaces disambig context with bn.ambiguous_context + bn.disambig_counterbiased
  - Flips labels on disambig rows (neg -> nontarget_idx, nonneg -> target_idx)
  - Keeps ambig rows identical
  - Resets example_id sequentially

Output files (in output/):
  banglabbq_marital_bng_vb.jsonl
  banglabbq_age_politics_bng_vb.jsonl
  banglabbq_educational_bng_vb.jsonl
  banglabbq_region_bng_vb.jsonl
  banglabbq_mental_health_bng_vb.jsonl
"""
import json, copy, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

with open('kaggle_eval/dataset_upload/templates_with_counter.jsonl', encoding='utf-8') as f:
    all_templates = [json.loads(l) for l in f]

CATEGORIES = {
    'Marital_status': {
        'va_file': 'output/banglabbq_marital_bng_v2.jsonl',
        'vb_file': 'output/banglabbq_marital_bng_vb.jsonl',
    },
    'Age_political_perception': {
        'va_file': 'output/banglabbq_age_politics_bng_v2.jsonl',
        'vb_file': 'output/banglabbq_age_politics_bng_vb.jsonl',
    },
    'Educational_background': {
        'va_file': 'output/banglabbq_educational_bng_v2.jsonl',
        'vb_file': 'output/banglabbq_educational_bng_vb.jsonl',
    },
    'Regional_origin': {
        'va_file': 'output/banglabbq_region_bng_v2.jsonl',
        'vb_file': 'output/banglabbq_region_bng_vb.jsonl',
    },
    'Mental_health_status': {
        'va_file': 'output/banglabbq_mental_health_bng_v2.jsonl',
        'vb_file': 'output/banglabbq_mental_health_bng_vb.jsonl',
    },
}

def load_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f]

for category, cfg in CATEGORIES.items():
    print(f'\n{"="*60}')
    print(f'Processing: {category}')

    cat_templates = [t for t in all_templates if t['category'] == category]
    idx_to_tmpl = {str(i + 1): t for i, t in enumerate(cat_templates)}

    va_records = load_jsonl(cfg['va_file'])
    print(f'  Loaded {len(va_records)} version a Bangla records')

    vb_records = []
    skipped = 0
    new_id = 0

    for row in va_records:
        rec = copy.deepcopy(row)
        q_idx = rec['question_index']
        tmpl = idx_to_tmpl.get(q_idx)

        if tmpl is None:
            print(f'  WARNING: no template for question_index {q_idx}')
            skipped += 1
            continue

        bn = tmpl.get('bn', {})
        counter_sent = bn.get('disambig_counterbiased', '')
        if not counter_sent:
            print(f'  WARNING: no bn.disambig_counterbiased for {tmpl["template_id"]}')
            skipped += 1
            continue

        ambig_ctx_bn = bn.get('ambiguous_context', '')
        if not ambig_ctx_bn:
            print(f'  WARNING: no bn.ambiguous_context for {tmpl["template_id"]}')
            skipped += 1
            continue

        rec['additional_metadata']['version'] = 'b'

        if rec['context_condition'] == 'ambig':
            pass  # unchanged

        else:
            rec['context'] = ambig_ctx_bn + ' ' + counter_sent

            en = tmpl.get('en', {})
            target_ans    = bn.get('target_answer', en.get('target_answer', ''))
            nontarget_ans = bn.get('nontarget_answer', en.get('nontarget_answer', ''))

            target_idx    = None
            nontarget_idx = None
            for idx in [0, 1, 2]:
                val = rec[f'ans{idx}']
                if val == target_ans:
                    target_idx = idx
                elif val == nontarget_ans:
                    nontarget_idx = idx

            if target_idx is None or nontarget_idx is None:
                print(f'  WARNING: cannot find ans indices for {tmpl["template_id"]} eid={rec["example_id"]}')
                skipped += 1
                continue

            if rec['question_polarity'] == 'neg':
                rec['label'] = nontarget_idx
            else:
                rec['label'] = target_idx

        rec['id'] = new_id
        rec['example_id'] = new_id
        new_id += 1
        vb_records.append(rec)

    with open(cfg['vb_file'], 'w', encoding='utf-8') as f:
        for rec in vb_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    print(f'  Written: {len(vb_records)} records -> {cfg["vb_file"]}')
    if skipped:
        print(f'  Skipped: {skipped}')

    disambig = [r for r in vb_records if r['context_condition'] == 'disambig']
    ambig    = [r for r in vb_records if r['context_condition'] == 'ambig']
    from collections import Counter
    lc = Counter(r['label'] for r in vb_records)
    print(f'  ambig={len(ambig)}, disambig={len(disambig)}, labels={dict(lc)}')

    for r in [x for x in disambig if x['question_polarity'] == 'neg'][:2]:
        lbl = r['label']
        q = r['question_index']
        t = idx_to_tmpl[q]
        print(f'    {t["template_id"]} label={lbl} -> {r[f"ans{lbl}"][:40]}')

print('\nDone. All 5 Bangla version b files written.')
