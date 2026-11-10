#!/usr/bin/env python3
"""Usage:
  python3 -I tools/qtool.py show START END     -> print English ayahs for days START..END
  python3 -I tools/qtool.py check START END    -> validate sum/day-N.json for days START..END
"""
import json, re, sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAYS = {x['day']: x for x in json.load(open(os.path.join(BASE, '_source', 'en-days.json')))}
LEVELS = [(60,1,100,150),(120,2,150,200),(180,3,200,250),(240,4,250,300),(300,5,300,350),(365,6,350,400)]
def level(n):
    for hi,l,lo,up in LEVELS:
        if n<=hi: return l,lo,up
def nhard(l): return 4 if l<=2 else 5 if l<=4 else 6
def refs_of(day): return [a['ref'] for a in DAYS[day]['ayahs']]
def expand(r):
    m = re.fullmatch(r'(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?', r.strip())
    if not m: raise ValueError('bad ref '+r)
    s,a,s2,b = int(m[1]),int(m[2]),m[3],m[4]
    if b is None: return [f'{s}:{a}']
    if s2 is None: return [f'{s}:{x}' for x in range(a,int(b)+1)]
    # cross-surah: rely on day's list
    return ('X',s,a,int(s2),int(b))
def check(n):
    errs, warns = [], []
    p = os.path.join(BASE,'data','sum',f'day-{n}.json')
    if not os.path.exists(p): return ['missing file'], []
    try: d = json.load(open(p))
    except Exception as e: return ['bad json: '+str(e)], []
    l,lo,up = level(n)
    if d.get('day')!=n: errs.append('day field wrong')
    if d.get('level')!=l: errs.append(f'level should be {l}')
    t = d.get('title','')
    if not t or len(t.split())>9: errs.append('title missing or >9 words')
    ps = d.get('paragraphs') or []
    if not (1<=len(ps)<=5): errs.append(f'{len(ps)} paragraphs')
    want = refs_of(n); got = []
    for q in ps:
        e = expand(q.get('ref',''))
        if isinstance(e,tuple):
            _,s,a,s2,b = e
            try: i=want.index(f'{s}:{a}'); j=want.index(f'{s2}:{b}'); got += want[i:j+1]
            except ValueError: errs.append('bad ref '+q['ref'])
        else: got += e
        if not q.get('text','').strip(): errs.append('empty text')
    if got != want: errs.append(f'refs do not cover day ayahs in order: want {want[0]}..{want[-1]} ({len(want)})')
    w = sum(len(q.get('text','').split()) for q in ps)
    if d.get('words')!=w: errs.append(f'words field {d.get("words")} != actual {w}')
    if w>up+5: errs.append(f'{w} words > max {up}')
    if w<lo-25: warns.append(f'{w} words, under {lo} (ok only if the ayahs are very short)')
    hw = d.get('hardWords') or []
    if len(hw)!=nhard(l): errs.append(f'need {nhard(l)} hardWords, got {len(hw)}')
    alltext = ' '.join(q.get('text','') for q in ps).lower()
    for h in hw:
        if not all(h.get(k) for k in ('w','m','bn')): errs.append('hardWord missing field')
        elif h['w'].lower() not in alltext: warns.append(f'hard word "{h["w"]}" not found in text')
        elif not re.search(r'[ঀ-৿]', h['bn']): errs.append(f'bn for {h["w"]} not Bangla script')
    if re.search(r'\bGod\b', alltext, re.I): warns.append('contains "god" - make sure it is like "no god but Him", otherwise write Allah')
    if l==1:
        for s in re.split(r'(?<=[.!?])\s+', ' '.join(q['text'] for q in ps)):
            if len(s.split())>=12: warns.append(f'L1 sentence {len(s.split())} words: {s[:60]}')
    return errs, warns
if __name__=='__main__':
    cmd,a,b = sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    if cmd=='show':
        for n in range(a,b+1):
            l,lo,up=level(n); x=DAYS[n]
            print(f'\n===== DAY {n} | level {l} | {lo}-{up} words | {nhard(l)} hardWords | {len(x["ayahs"])} ayahs =====')
            for y in x['ayahs']: print(y['ref'], y['en'])
    else:
        bad=0
        for n in range(a,b+1):
            e,w = check(n)
            if e: bad+=1
            if e or w: print(f'day {n}:', '; '.join(['ERROR '+x for x in e]+['warn '+x for x in w]))
        print(f'checked {b-a+1} days, {bad} with errors')
