"""Gate and package the newly certified classification; run on the VM."""
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import re

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19


def records(name):
    return [json.loads(line) for line in Path(name).read_text().splitlines()]


def index(rows):
    return {(r['y'],r['sign']):r for r in rows}


original = json.loads(Path('classification.json').read_text())
bounds = index(records('certified-all.jsonl'))
exact = index(records('exact-all.jsonl'))
saturation = index(records('fresh-saturation.jsonl'))
patched = index(records('patched-all.log'))
crosscheck = records('crosscheck.log')
assert len(crosscheck) == 317
assert all(r['status'] == 'ok' and r['matches_table'] for r in crosscheck)
assert sum(r.get('matches_lmfdb',False) for r in crosscheck) == 3
assert 'All tests passed!' in Path('doctests-final.log').read_text()
lattice = json.loads(Path('lattice-certificates.log').read_text())
assert lattice['status'] == 'PASS' and lattice['curves'] == lattice['torsion_checks'] == 179
rank_records = index(records('original_pari_descent.jsonl'))
out = copy.deepcopy(original)
out['format'] = 'hai-walsh-fixed-y-recertified-v1'
out['trusted_dependencies'] = [
    'Original PARI 2.19 unconditional rational/quadratic 2-descent upper ranks',
    'Fresh eclib full saturation, index 1 for all 144 positive-rank bases',
    'Exact QQbar roots, Arb enclosures for log and Carlson RF',
    'David 1995 Theorem 2.1 specialized as proved in certificate-proof.md',
    'Exact rational coefficient-box and small-interval enumeration',
]
out['source_classification_sha256'] = hashlib.sha256(Path('classification.json').read_bytes()).hexdigest()
out['proof'] = 'certificate-proof.md'
out['certificate_files'] = ['evidence/certified-all.jsonl','evidence/exact-all.jsonl',
                            'evidence/fresh-saturation.jsonl','evidence/lattice-certificates.log']
solutions = []
accepted = exclusions = rank_zero = 0
open_cases = []
for row in out['curves']:
    key = row['y'],row['sign']
    if row['method'] == 'elliptic_integral_points':
        b,x,s,p = bounds[key],exact[key],saturation[key],patched[key]
        assert b['status'] == 'bound_certified'
        assert x['status'] == 'exact_exhaustion_passed' and x['matches_original']
        assert s['success'] and s['index'] == 1 and not s['unsaturated']
        assert p['status'] == 'ok' and p['matches_original']
        d = rank_records[key]
        assert d['field_certifications'] == [1,1] and d['returncode'] == 0 and not d['stderr']
        rankline = next(line[5:] for line in d['stdout'].splitlines() if line.startswith('RANK '))
        rank = json.loads(re.sub(r'(-?\d+)/(\d+)',r'"\1/\2"',rankline))
        assert rank[1] == row['rank'] == len(rank[3])
        row['previous_coefficient_bound'] = row['coefficient_bound']
        row['coefficient_bound'] = b['bound']
        row['small_x_interval'] = x['small_x_interval']
        row['integral_points'] = [[str(u),str(v),'1'] for u,v in x['integral_points']]
        row['proof_status'] = 'recertified_with_explicit_dependencies'
        row['coefficient_bound_source'] = 'exact duplication / David1995 / Arb / exact lattice'
        row['finite_combinations_checked'] = x['visited']
        row['patched_legacy_coefficient_bound'] = p['bound']
        row.pop('x_bound_diagnostic',None)
        accepted += 1
        rank_zero += row['rank'] == 0
        for sol in x['solutions']:
            sol = dict(sol)
            sol['known_family'] = sol['x'] == 2*sol['y']**2+1 and sol['z']**2+sol['sign'] == 2*sol['y']
            solutions.append(sol)
    elif row['method'] == 'congruence_exclusion':
        m = row['modulus']
        squares = {v*v % m for v in range(m)}
        assert all((row['D']*(z*z+row['sign'])**2+1) % m not in squares for z in range(m))
        row['proof_status'] = 'quartic_excluded_by_exact_congruence'
        exclusions += 1
    else:
        open_cases.append(dict(y=row['y'],sign=row['sign']))
        row['proof_status'] = 'open'
sort_key = lambda r:(r['y'],r['sign'],r['z'],r['x'])
assert sorted(solutions,key=sort_key) == sorted(original['solutions'],key=sort_key)
assert accepted == 179 and exclusions == 18 and rank_zero == 35
assert open_cases == [dict(y=y,sign=1) for y in [73,91,97]]
out['solutions'] = sorted(solutions,key=sort_key)
out['summary'] = dict(accepted_curves=accepted,positive_rank_curves=accepted-rank_zero,
                      rank_zero_curves=rank_zero,quartic_exclusions=exclusions,
                      open_cases=open_cases,integral_points=sum(len(r['integral_points']) for r in exact.values()),
                      coefficient_combinations=sum(r['visited'] for r in exact.values()),
                      solutions=len(solutions),new_exceptions=0)
Path('classification-recertified.json').write_text(json.dumps(out,indent=2)+'\n')
Path('recertification-summary.json').write_text(json.dumps(out['summary'],indent=2)+'\n')
with open('bounds-comparison.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['y','sign','rank','old_bound','patched_bound','certified_bound',
                     'integral_points','exact_combinations'])
    for row in sorted(out['curves'],key=lambda r:(r['y'],r['sign'])):
        if row['method'] == 'elliptic_integral_points':
            writer.writerow([row['y'],row['sign'],row['rank'],row['previous_coefficient_bound'],
                             row['patched_legacy_coefficient_bound'],row['coefficient_bound'],
                             len(row['integral_points']),row['finite_combinations_checked']])
print(json.dumps(dict(status='PASS',**out['summary'])))
