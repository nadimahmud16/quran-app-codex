#!/usr/bin/env python3
"""Merge data/sum/day-N.json into data/summaries.json ({"1": {...}, ...})."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, missing = {}, []
for n in range(1, 366):
    p = os.path.join(BASE, 'data', 'sum', f'day-{n}.json')
    if os.path.exists(p): out[str(n)] = json.load(open(p, encoding='utf8'))
    else: missing.append(n)
json.dump(out, open(os.path.join(BASE, 'data', 'summaries.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(f'{len(out)} days written; missing: {missing or "none"}')
