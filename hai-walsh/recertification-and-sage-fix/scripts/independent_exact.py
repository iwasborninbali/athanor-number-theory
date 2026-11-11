"""Exhaust certified boxes by exact group arithmetic from the earlier checker.

The checker was independently written for a04-haiwalsh and inspected during
the adversarial audit. Here it receives the newly certified bounds, including
the separately bounded x-interval. No floating-point sieve is used.
"""
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
spec = importlib.util.spec_from_file_location('original_checker','original_check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
original = json.loads(Path('classification.json').read_text())['curves']
original = {(r['y'],r['sign']):r for r in original}
records = [json.loads(line) for line in Path('certified-all.jsonl').read_text().splitlines()]
for rec in records:
    begin = time.monotonic()
    row = original[rec['y'],rec['sign']]
    result = dict(y=rec['y'],sign=rec['sign'],rank=row['rank'],bound=rec['bound'])
    try:
        assert rec['status'] == 'bound_certified'
        curve = checker.Curve(row['ainvs'][1],row['ainvs'][3])
        B = [checker.point(P) for P in rec['basis']]
        C = row['basis_change']
        full = [checker.point(P) for P in row['basis']]
        assert checker.determinant(C) in [1,-1]
        for j,P in enumerate(B):
            Q = None
            for i,A in enumerate(full):
                Q = curve.add(Q,curve.mul(C[i][j],A))
            assert Q == P
        if row['rank']:
            interval = rec['certificate']['small_x_interval']
        else:
            interval = [0,0]
        found,visited = checker.finite_points(curve,B,rec['bound'],interval)
        expected = {tuple(map(int,P[:2])) for P in row['integral_points']}
        added = found-expected
        removed = expected-found
        recovered = []
        for u,v in found:
            d = row['D']
            if u <= 0 or v <= 0 or u % d:
                continue
            z = math.isqrt(u//d)
            if z*z != u//d or v % (d*z):
                continue
            x = v//(d*z)
            if x <= 1:
                continue
            assert x*x-1 == d*(z*z+row['sign'])**2
            recovered.append(dict(x=x,y=row['y'],z=z,sign=row['sign']))
        result.update(status='exact_exhaustion_passed',visited=visited,
                      integral_points=sorted(found),added=sorted(added),removed=sorted(removed),
                      matches_original=not added and not removed,solutions=sorted(recovered,key=str),
                      small_x_interval=interval)
    except Exception as exc:
        result.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    result['seconds'] = time.monotonic()-begin
    print(json.dumps(result),flush=True)
