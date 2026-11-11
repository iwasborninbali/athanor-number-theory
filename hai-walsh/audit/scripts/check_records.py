import collections,json,pathlib,re
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
original=ROOT/'../a04-haiwalsh'
certificate=json.load(open(original/'certificates/classification.json'))
des={(r['y'],r['sign']):r for r in map(json.loads,open(original/'certificates/pari_descent.jsonl'))}
sage={(r['y'],r['sign']):r for r in map(json.loads,open(original/'certificates/sage_results_initial.jsonl'))}
count=0
for r in certificate['curves']:
 if r['method']!='elliptic_integral_points':continue
 d=des[r['y'],r['sign']];s=sage[r['y'],r['sign']]
 rankline=next(l[5:] for l in d['stdout'].splitlines() if l.startswith('RANK '))
 rank=json.loads(re.sub(r'(-?\d+)/(\d+)',r'"\1/\2"',rankline))
 assert not d['stderr'] and d['returncode']==0 and d['field_certifications']==[1,1]
 assert rank[1]==r['rank']==len(rank[3])==s['rank_of_saturated_points']
 assert s['saturation_success'] and not s['unsaturated_primes']
 for key in ['basis','integral_points','saturation_index','solutions']:
  assert s[key]==r[key]
 count+=1
witnesses=[]
for line in open(ROOT/'evidence/bound_hypothesis.jsonl'):
 row=json.loads(line);e=row['error'];v=e['short_vector'];col=e['lattice_last_column'];rank=len(v)-1
 last,rem=divmod(v[-1]-sum(v[i]*col[i] for i in range(rank)),col[-1])
 assert rem==0 and sum(t*t for t in v)==int(e['short_vector_norm2'])
 assert Fraction(e['fabricated_lower_bound'])>int(e['short_vector_norm2'])
 witnesses.append(dict(y=row['y'],sign=row['sign'],short_vector=v,row_combination=v[:-1]+[last],norm2=e['short_vector_norm2']))
assert len(witnesses)==sum(r.get('rank',0)>0 for r in certificate['curves'] if r['method']=='elliptic_integral_points')
out=dict(raw_certificate_consistency_count=count,exact_lattice_counterwitness_count=len(witnesses),y4_witnesses=[r for r in witnesses if r['y']==4])
(ROOT/'evidence/records_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
