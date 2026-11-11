import json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
rows=json.load(open(ROOT/'../a04-haiwalsh/certificates/classification.json'))['curves']
rows=[r for r in rows if r['method']=='elliptic_integral_points' and r.get('rank') and r['y'] in [4,25,93,100]]
program='CURVES = '+repr(rows)+'\n'+(ROOT/'scripts/high_precision_bound.py').read_text()
command='cd ~/haiwalsh-verify && OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 19 taskset -c 1 ~/athanor-vm/stark-83a/sage-env/bin/python -u -'
with open(ROOT/'evidence/high_precision_bound.jsonl','w') as f:
 p=subprocess.run(['ssh','-o','BatchMode=yes','personal-vps',command],input=program,text=True,stdout=f,stderr=subprocess.STDOUT,timeout=300)
print('exit',p.returncode)
