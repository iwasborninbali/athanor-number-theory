#!/usr/bin/env python3
"""Package saved computations and exact residue-class exclusions."""
import json,math,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(name):return [json.loads(l) for l in (ROOT/name).read_text().splitlines()]
des={(r['y'],r['sign']):r for r in read('certificates/pari_descent.jsonl')}
meta={(r['y'],r['sign']):r for r in read('certificates/sage_basis_changes.jsonl')}
iplog={};key=None
for line in (ROOT/'logs/sage_classify2.log').read_text().splitlines():
    if line.startswith('{'):
        try:a=json.loads(line)
        except json.JSONDecodeError:continue
        if a.get('event')=='start':key=(a['y'],a['sign']);iplog[key]={}
    if key is None:continue
    if line.startswith('Using mw_basis '):
        iplog[key]['basis']=[p.split(' : ') for p in re.findall(r'\(([^()]*)\)',line)]
    if line.startswith('starting search of remaining points using coefficient bound '):
        iplog[key]['coefficient_bound']=int(re.search(r'bound (\d+)',line).group(1))
        iplog[key]['x_bound_diagnostic']=line.strip()
    if line.startswith('x-coords of points on non-compact component with '):
        nums=re.findall(r'-?\d+',line)
        # Sage's log prints x1-1 but its interval method includes x1.
        iplog[key]['small_x_interval']=[int(nums[0]),int(nums[1])+1]
rows=read('certificates/sage_results_initial.jsonl')
certificate=dict(format='hai-walsh-fixed-y-v1',domain=dict(y_min=1,y_max=100,x_min=2,z_min=1),
    trusted_dependencies=['PARI 2.19 exact 2-descent and bnfcertify',
                          'eclib certified saturation-index bound and saturation',
                          'Sage 10.9 elliptic-logarithm/LLL coefficient bound'],curves=[])
solutions=[]
for r in rows:
    key=r['y'],r['sign'];d=des[key]
    row=dict(y=r['y'],sign=r['sign'],D=r['D'],ainvs=r['ainvs'],
             rank_bounds=[d['rank_lower'],d['rank_upper']],field_certifications=d['field_certifications'])
    row['pari_reported_rank_bounds']=row['rank_bounds'][:]
    rankline=next(l[5:] for l in d['stdout'].splitlines() if l.startswith('RANK '))
    pointpart=rankline.split(',',3)[3]
    point_count=len(re.findall(r'\[([^\[\]]+)\]',pointpart))
    row['rank_bounds']=[point_count,d['rank_upper']]
    row['rank_bound_note']='Lower bound uses returned independent points, not PARI parity increment without a point.'
    if r['status']=='complete':
        row.update(method='elliptic_integral_points',rank=r['rank'],basis=r['basis'],
                   torsion=r['torsion'],saturation_success=r['saturation_success'],
                   saturation_index=r['saturation_index'],unsaturated_primes=r['unsaturated_primes'],
                   integral_points=r['integral_points'],solutions=r['solutions'])
        row.update(meta[key])
        if r['rank']:
            assert meta[key]['lll_basis']==iplog[key]['basis'],key
            row.update({k:v for k,v in iplog[key].items() if k!='basis'})
        else:
            row.update(coefficient_bound=0,small_x_interval=[0,0])
        solutions.extend(r['solutions'])
    elif r['sign']==1 and (r['y']%2==0 or r['y']%3==0):
        row.update(method='congruence_exclusion',modulus=8 if r['y']%2==0 else 3,solutions=[],
                   elliptic_curve_status='no complete MW basis/integral-point list; not needed for this direct quartic exclusion',
                   elliptic_failure=r['error'])
    else:
        row.update(method='open',reason=r['error'])
    certificate['curves'].append(row)
certificate['solutions']=sorted(solutions,key=lambda r:(r['y'],r['sign'],r['z']))
(ROOT/'certificates/classification.json').write_text(json.dumps(certificate,indent=2)+'\n')
(ROOT/'certificates/solutions.json').write_text(json.dumps(certificate['solutions'],indent=2)+'\n')
print('methods:',{m:sum(r['method']==m for r in certificate['curves']) for m in sorted({r['method'] for r in certificate['curves']})})
print('open:',[(r['y'],r['sign']) for r in certificate['curves'] if r['method']=='open'])
print('solutions:',len(solutions))
