import json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
original=json.load(open(ROOT/'../a04-haiwalsh/certificates/classification.json'))
old={(r['y'],r['sign']):r for r in original['curves']}
rows=[json.loads(l) for l in open(ROOT/'evidence/pari_fresh.jsonl')]
for r in rows:r['original_points']=old[r['y'],r['sign']].get('integral_points',[])
program='DATA = '+repr(rows)+'\n'+(ROOT/'scripts/recompute_sage.py').read_text()
command='cd ~/haiwalsh-verify && OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 19 taskset -c 1 ~/athanor-vm/stark-83a/sage-env/bin/python -u -'
with (ROOT/'evidence/sage_fresh.log').open('w') as f:
    p=subprocess.run(['ssh','-o','BatchMode=yes','personal-vps',command],input=program,text=True,stdout=f,stderr=subprocess.STDOUT,timeout=900)
print('ssh_exit',p.returncode)
records=[]
for line in (ROOT/'evidence/sage_fresh.log').read_text().splitlines():
    if line.startswith('AUDIT '): records.append(json.loads(line[6:]))
with (ROOT/'evidence/sage_fresh.jsonl').open('w') as f:
    for r in records:
        if r['event']=='integral_points_source':
            (ROOT/'sources/sage_integral_points_actual.py').write_text(r.pop('source'))
        f.write(json.dumps(r)+'\n')
for r in records:
    if r['event']=='curve':print(r['y'],r['sign'],r['status'],r.get('rank'),r.get('point_count'),r.get('seconds'),flush=True)
assert p.returncode==0
assert not [r for r in records if r.get('status')=='error']
