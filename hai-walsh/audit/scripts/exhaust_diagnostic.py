"""Exact exhaustion of diagnostic larger boxes, using the audited group-law checker.

Bounds are still diagnostics: this does not claim a certified error bound on logs.
"""
import importlib.util,json,os,pathlib,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audited_checker',ROOT/'../a04-haiwalsh/check.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
original=json.load(open(ROOT/'../a04-haiwalsh/certificates/classification.json'))
old={(r['y'],r['sign']):r for r in original['curves']}
out=[]
for line in open(ROOT/'evidence/high_precision_bound.jsonl'):
    d=json.loads(line);assert d['status']=='diagnostic_pass'
    row=old[d['y'],d['sign']];D=row['D'];s=row['sign']
    E=module.Curve(2*s*D,D*(D+1))
    start=time.monotonic()
    points,n=module.finite_points(E,list(map(module.point,d['basis'])),d['coefficient_bound'],row['small_x_interval'])
    expected={tuple(map(int,p[:2])) for p in row['integral_points']}
    result=dict(y=d['y'],sign=s,bound=d['coefficient_bound'],combination_count=n,matches_original=points==expected,extra=sorted(points-expected),missing=sorted(expected-points),seconds=time.monotonic()-start)
    out.append(result)
    with open(ROOT/'evidence/diagnostic_exhaustion.jsonl','a') as f:f.write(json.dumps(result)+'\n')
    print(json.dumps(result),flush=True)
    assert result['matches_original']
