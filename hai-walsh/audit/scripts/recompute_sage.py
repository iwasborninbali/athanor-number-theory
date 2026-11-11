"""Run via stdin, with DATA injected; no remote output files or database calls."""
import contextlib, hashlib, inspect, io, json, math, os, re, time, traceback
from sage.all import EllipticCurve, QQ, proof
from sage.version import version
from sage.libs.eclib.all import mwrank_MordellWeil
proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
def emit(r): print('AUDIT '+json.dumps(r),flush=True)
def coords(p): return [str(t) for t in p]
emit(dict(event='environment',sage=version,affinity=list(os.sched_getaffinity(0)),nice=os.nice(0)))
src=inspect.getsource(EllipticCurve([0,1]).integral_points)
emit(dict(event='integral_points_source',sha256=hashlib.sha256(src.encode()).hexdigest(),source=src))
for d in DATA:
    y,s=d['y'],d['sign']; D=y*y+1
    lo,hi,sha,raw=d['rank_data']
    record=dict(event='curve',y=y,sign=s,pari_bounds=[lo,hi],pari_point_count=len(raw))
    begin=time.monotonic()
    try:
        if lo!=hi or len(raw)!=hi:
            if s==1 and (y%2==0 or y%3==0):
                m=8 if y%2==0 else 3
                assert all((1+D*(z*z+1)**2)%m not in {x*x%m for x in range(m)} for z in range(m))
                record.update(status='quartic_excluded',modulus=m)
            else: record.update(status='not_recomputed',reason='no witnessed full-rank starting set')
        else:
            E=EllipticCurve([0,2*s*D,0,D*(D+1),0])
            G=[E([QQ(a),QQ(b)]) for a,b in raw]
            if G:
                F=E.minimal_model(); phi=E.isomorphism_to(F)
                vectors=[]
                for p in G:
                    a,b=phi(p).xy(); c=a.denominator().lcm(b.denominator())
                    vectors.append([int(a*c),int(b*c),int(c)])
                W=mwrank_MordellWeil(F.mwrank_curve(),verbose=True)
                W.process(vectors)
                good,index,left=W.saturate(max_prime=-1,min_prime=2)
                B=[(~phi)(F(p)) for p in W.points()]
                assert good and not re.findall(r'\d+',str(left)) and int(W.rank())==hi==len(B)
                record.update(saturation_success=bool(good),saturation_index=int(index),unsaturated=str(left),rank=int(W.rank()))
            else:
                B=[];record.update(saturation_success=True,saturation_index=1,unsaturated='[ ]',rank=0)
            assert {tuple(coords(p)) for p in E.torsion_points()}=={('0','1','0'),('0','0','1')}
            record['basis']=[coords(p) for p in B]
            P=E.integral_points(mw_base=B,both_signs=True,verbose=True)
            actual={(int(p[0]),int(p[1])) for p in P}
            expected={(int(p[0]),int(p[1])) for p in d['original_points']}
            assert actual==expected, ('different integral list',actual^expected)
            recovered=[]
            for u,v in sorted(actual):
                assert v*v==u**3+2*s*D*u*u+D*(D+1)*u
                if u<=0 or v<=0 or u%D: continue
                z=math.isqrt(u//D)
                if z*z!=u//D or not z or v%(D*z): continue
                x=v//(D*z)
                if x>1:
                    assert x*x-1==D*(z*z+s)**2
                    recovered.append([x,y,z,s])
            record.update(status='complete',integral_points=sorted(actual),solutions=recovered,point_count=len(actual),matches_original=True)
    except Exception as e:
        record.update(status='error',error=repr(e),traceback=traceback.format_exc())
    record['seconds']=time.monotonic()-begin
    emit(record)
