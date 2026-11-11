#!/usr/bin/env python3
"""Unconditional PARI 2-descent and field certification, one process at a time."""
import datetime, json, os, pathlib, subprocess, time, shutil

ROOT=pathlib.Path(__file__).resolve().parents[1]
GP=pathlib.Path.home()/'athanor-foundation/instruments/hammer/core/workspace/bsd-dialogue/local-pari/install/bin/gp'
output=ROOT/'certificates/pari_descent.jsonl'
for y in [4]+[j for j in range(1,101) if j!=4]:
    for sign in [-1,1]:
        if shutil.disk_usage(ROOT).free < 3*1024**3:
            raise RuntimeError('free space below 3 GiB')
        d=y*y+1
        program=f'''default(realprecision,80);
setrand(1);
ee=ellinit([0,{2*sign*d},0,{d*(d+1)},0]);
rr=ellrankinit(ee);
cc=vector(#rr[3]);
for(j=1,#rr[3],bb=bnfinit(rr[3][j],1); cc[j]=bnfcertify(bb); print("FIELD ",j," ",bb.pol," DISC ",bb.disc," CLASSNO ",bb.no," CERT ",cc[j]));
zz=ellrank(rr,2);
print("RANK ",zz);
print("CERTS ",cc);
print("FIELDS ",vector(#rr[3],j,rr[3][j].pol));
print("DISCS ",vector(#rr[3],j,rr[3][j].disc));
print("VERSION ",version());
'''
        start=time.monotonic()
        rec=dict(y=y,sign=sign,D=d,ainvs=[0,2*sign*d,0,d*(d+1),0],
                 utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input=program)
        try:
            p=subprocess.run(['nice','-n','19',str(GP),'-q','-f','-s','1G'],input=program,text=True,
                             capture_output=True,timeout=180)
            rec.update(stdout=p.stdout,stderr=p.stderr,returncode=p.returncode)
            for line in p.stdout.splitlines():
                if line.startswith('RANK '):
                    # PARI's rational point coordinates are kept as exact strings in stdout.
                    lo,hi,sha=line[5:].strip()[1:].split(',',3)[:3]
                    rec.update(rank_lower=int(lo),rank_upper=int(hi),sha2_quotient=int(sha))
                if line.startswith('CERTS '): rec['field_certifications']=json.loads(line[6:])
            rec['certified_rank']=(not p.stderr and p.returncode==0 and
                  rec.get('rank_lower')==rec.get('rank_upper') and
                  all(v==1 for v in rec.get('field_certifications',[])) and bool(rec.get('field_certifications')))
        except Exception as e:
            rec.update(error=repr(e),certified_rank=False)
        rec['seconds']=time.monotonic()-start
        with output.open('a') as f: f.write(json.dumps(rec)+'\n')
        print(json.dumps({k:rec[k] for k in ['y','sign','seconds','certified_rank','rank_lower','rank_upper'] if k in rec}),flush=True)
