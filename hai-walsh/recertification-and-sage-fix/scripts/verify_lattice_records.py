"""Exact independent checks of the saved Bezout and lattice certificates."""
import importlib.util
import json
import os
from fractions import Fraction as F
from pathlib import Path
import time

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
spec = importlib.util.spec_from_file_location('original_checker','original_check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def add(p,q):
    v = [F(0)]*max(len(p),len(q))
    for i,x in enumerate(p):v[i]+=x
    for i,x in enumerate(q):v[i]+=x
    while len(v)>1 and not v[-1]:v.pop()
    return v


def mul(p,q):
    v = [F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):v[i+j]+=F(x)*F(y)
    while len(v)>1 and not v[-1]:v.pop()
    return v


def gs_lengths(rows):
    stars = []
    lengths = []
    dot = lambda a,b: sum(x*y for x,y in zip(a,b))
    for row in rows:
        v = list(map(F,row))
        for star,d in zip(stars,lengths):
            t = dot(v,star)/d
            v = [x-t*y for x,y in zip(v,star)]
        d = dot(v,v)
        assert d > 0
        stars.append(v)
        lengths.append(d)
    return lengths


begin = time.monotonic()
curves = steps = retries = torsion_checks = 0
for rec in map(json.loads,Path('certified-all.jsonl').read_text().splitlines()):
    assert rec['status'] == 'bound_certified'
    curves += 1
    order,good_reductions = checker.torsion_bound(checker.Curve(rec['ainvs'][1],rec['ainvs'][3]))
    assert order == 2
    torsion_checks += 1
    if not rec['rank']:
        continue
    cert = rec['certificate']
    a,b = rec['ainvs'][1],rec['ainvs'][3]
    F1 = mul([-b,0,1],[-b,0,1])
    G1 = [0,4*b,4*a,4]
    F2 = mul([1,0,-b],[1,0,-b])
    G2 = [0,4,4*a,4*b]
    for chart,f,g in zip(cert['duplication']['charts'],[F1,F2],[G1,G2]):
        assert add(mul(chart['U'],f),mul(chart['V'],g)) == [chart['R']]
        assert sum(map(abs,chart['U']))+sum(map(abs,chart['V'])) == chart['K']
    for event in cert['steps']:
        if 'new_bound' not in event:
            retries += 1
            continue
        assert event['accepted']
        r = rec['rank']
        N,C = int(event['N']),int(event['scale'])
        column = list(map(int,event['last_column']))
        assert column[-1] == C
        rows = [list(map(int,row)) for row in event['reduced']]
        changes = []
        for row in rows:
            k,rem = divmod(row[-1]-sum(row[i]*column[i] for i in range(r)),C)
            assert rem == 0
            changes.append(row[:r]+[k])
        assert checker.determinant(changes) in [1,-1]
        lengths = gs_lengths(rows)
        assert lengths == list(map(F,event['gs_squared']))
        delta = min(lengths)
        assert delta == F(event['d2'])
        errors = list(map(F,event['errors']))
        threshold = 4*(r*N*N+(N*sum(errors))**2)  # exponent two, independently checked below
        assert threshold == F(event['threshold'])
        assert delta > threshold
        assert 0 < F(event['lower'][0]) <= F(event['lower'][1])
        steps += 1
    assert rec['bound'] == cert['bound']
print(json.dumps(dict(status='PASS',curves=curves,torsion_checks=torsion_checks,lattice_steps=steps,
                      failed_attempts_recorded=retries,seconds=time.monotonic()-begin)))
