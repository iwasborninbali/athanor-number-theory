"""Fresh local descents, independent seed; writes only in the audit folder."""
import json, pathlib, random, re, subprocess, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
GP = pathlib.Path.home() / 'athanor-foundation/instruments/hammer/core/workspace/bsd-dialogue/local-pari/install/bin/gp'
sample = sorted(random.Random(20261111).sample([y for y in range(1,101) if y != 4], 10))
hard = [24,40,72,84,93,98,99,100]
ys = [4] + sorted(set(sample + hard + [73,91,97]))
(ROOT/'evidence/sample.json').write_text(json.dumps(dict(seed=20261111, random=sample, hard=hard, all=ys), indent=2)+'\n')
with (ROOT/'evidence/pari_fresh.jsonl').open('w') as f:
    for y in ys:
        for s in [-1,1]:
            D=y*y+1
            code=f'''default(realprecision,100);
setrand(20261111);
E=ellinit([0,{2*s*D},0,{D*(D+1)},0]);
R=ellrankinit(E);
for(j=1,#R[3], B=bnfinit(R[3][j],1); print("FIELD ",B.pol," DISC ",B.disc," H ",B.no," CERT ",bnfcertify(B)));
A=ellrank(R,4);
print("RANK ",A);
print("VERSION ",version());
'''
            start=time.monotonic()
            p=subprocess.run(['nice','-n','19',str(GP),'-q','-f','-s','1G'],input=code,text=True,capture_output=True,timeout=120)
            raw=next(l[5:] for l in p.stdout.splitlines() if l.startswith('RANK '))
            rank=json.loads(re.sub(r'(-?\d+)/(\d+)',r'"\1/\2"',raw))
            row=dict(y=y,sign=s,D=D,input=code,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,rank_data=rank,seconds=time.monotonic()-start)
            assert p.returncode==0 and not p.stderr
            assert len([l for l in p.stdout.splitlines() if l.startswith('FIELD ') and l.endswith('CERT 1')])==2
            f.write(json.dumps(row)+'\n');f.flush()
            print(y,s,rank[:3],len(rank[3]),round(row['seconds'],3),flush=True)
