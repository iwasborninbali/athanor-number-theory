#!/usr/bin/env python3
"""Export exact changes of MW basis used by Sage's integral-points routine."""
import json,os
from sage.all import EllipticCurve,QQ,proof
proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
with open('sage_results.jsonl') as f: rows=list(map(json.loads,f))
for r in rows:
    if r['status']!='complete':continue
    E=EllipticCurve(r['ainvs'])
    base=[E([QQ(c) for c in p]) for p in r['basis']]
    if base:
        new,mat=E.lll_reduce(base,E.height_pairing_matrix(base))
        change=[[int(x) for x in row] for row in mat.rows()]
    else:new,change=[],[]
    print(json.dumps(dict(y=r['y'],sign=r['sign'],lll_basis=[[str(c) for c in p] for p in new],
                         basis_change=change)),flush=True)
