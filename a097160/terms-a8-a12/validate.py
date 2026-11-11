#!/usr/bin/env python3
"""Small exact cross-algorithm cases and targeted corruption rejection.
Run on VM after compiling scan and independent. Does not alter certificates.
"""
from pathlib import Path
import json
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent

def invoke(args, expected=0):
    r=subprocess.run(list(map(str,args)),capture_output=True,text=True)
    if (r.returncode==0)!=(expected==0):
        raise RuntimeError((args,r.returncode,r.stdout,r.stderr))
    return r

with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
    base=Path(tmp)
    lengths=[]
    for p in range(2,1000):
        if any(p%d==0 for d in range(2,__import__('math').isqrt(p)+1)):
            continue
        w=bytearray(p)
        for r in range(1,p):w[r*r%p]=1
        run=longest=start=0
        for x in range(1,p):
            run=run+1 if w[x] else 0
            if run>longest:longest,start=run,x-run+1
        lengths.append((p,longest,start))
    for k in range(2,15):
        cert,report=base/'ex.tsv',base/'scan.json'
        invoke([ROOT/'scan',k,1000,2,cert,report,0])
        actual=[tuple(map(int,l.split())) for l in cert.read_text().splitlines()[1:]]
        assert actual==[x for x in lengths if x[1]<k],(k,actual)
        invoke([ROOT/'independent',k,1000,'full',cert,base/'check.json',base/'sample.tsv'])
    text=(ROOT/'certificates/a8.tsv').read_text().splitlines()
    faults={
        'omitted_p2':text[:1]+text[2:],
        'false_maximum_p2':[text[0],'2 2 1']+text[2:],
        'composite_inserted':text[:3]+['4 1 1']+text[3:],
        'duplicate_tail':text+[text[-1]],
        'omitted_endpoint':[s for s in text if not s.startswith('9857 ')],
    }
    for name,lines in faults.items():
        cert=base/(name+'.tsv');cert.write_text('\n'.join(lines)+'\n')
        invoke([ROOT/'independent',9,3222025,'full',cert,base/'bad.json',base/'bad.tsv'],expected=1)
    print(json.dumps(dict(status='PASS',exact_small_cases=list(range(2,15)),prime_interval='[2,1000)',
                          independently_enumerated_primes=len(lengths),rejected_faults=list(faults)),indent=2))
