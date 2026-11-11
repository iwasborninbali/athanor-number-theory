#!/usr/bin/env python3
"""Bounded extra point-search effort for the three fibres not excluded locally."""
import json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
GP=pathlib.Path.home()/'athanor-foundation/instruments/hammer/core/workspace/bsd-dialogue/local-pari/install/bin/gp'
old={(r['y'],r['sign']):r for r in map(json.loads,open(ROOT/'certificates/pari_descent.jsonl'))}
for y in [91,73,97]:
    rec=old[y,1].copy()
    rec['input']=rec['input'].replace('ellrank(rr,2)','ellrank(rr,20)')
    start=time.monotonic()
    try:
        p=subprocess.run(['nice','-n','19',str(GP),'-q','-f','-s','1G'],input=rec['input'],text=True,capture_output=True,timeout=120)
        rec.update(stdout=p.stdout,stderr=p.stderr,returncode=p.returncode)
        for line in p.stdout.splitlines():
            if line.startswith('RANK '):
                lo,hi,sha=line[5:].strip()[1:].split(',',3)[:3]
                rec.update(rank_lower=int(lo),rank_upper=int(hi),sha2_quotient=int(sha))
            if line.startswith('CERTS '):rec['field_certifications']=json.loads(line[6:])
        rec['certified_rank']=(not p.stderr and p.returncode==0 and
            rec['rank_lower']==rec['rank_upper'] and all(c==1 for c in rec['field_certifications']))
    except subprocess.TimeoutExpired as e:
        rec.update(error=repr(e),stdout=(e.stdout or b'').decode(),stderr=(e.stderr or b'').decode(),certified_rank=False)
    rec['seconds']=time.monotonic()-start
    with (ROOT/'certificates/pari_retry.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps({k:rec[k] for k in ['y','seconds','certified_rank','rank_lower','rank_upper','stdout','error'] if k in rec}),flush=True)
