"""Exact search of all 200 boxes. Modular sieves only discard nonsquares."""
import json,math,pathlib,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
start=time.monotonic()
limit=10**6
mods=[64,63,65,11]
squares={m:{a*a % m for a in range(m)} for m in mods}
found=[];tested=0;passed=0
for y in range(1,101):
    d=y*y+1
    for s in [-1,1]:
        # Fixed-period wheel, exhaustive residue classes modulo lcm(64,63,65).
        period=64*63*65
        allowed=[]
        for z in range(period):
            if all((1+d*(z*z+s)**2)%m in squares[m] for m in mods[:3]):
                allowed.append(z)
        for residue in allowed:
            for z in range(residue or period,limit+1,period):
                n=1+d*(z*z+s)**2
                tested+=1
                if n%11 not in squares[11]:continue
                passed+=1
                x=math.isqrt(n)
                if x>1 and x*x==n:found.append(dict(x=x,y=y,z=z,sign=s))
    if y%10==0: print(y,round(time.monotonic()-start,2),flush=True)
found.sort(key=lambda r:(r['y'],r['sign'],r['z']))
out=dict(domain=dict(y_min=1,y_max=100,z_min=1,z_max=limit,x_min=2),solutions=found,exact_isqrt_tests=passed,wheel_candidates=tested,seconds=time.monotonic()-start)
(ROOT/'evidence/bruteforce.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out),flush=True)
