#!/usr/bin/env python3
"""Full-basis saturation followed by Sage's complete integral-point algorithm.

Run on the allowed VM under nice 19 / taskset CPU 1. This does not use a
bounded z or x search. Verbose output is retained as computational evidence.
"""
import os, json, time, signal, traceback, math, sys, re
from sage.all import EllipticCurve, proof, pari, QQ
from sage.version import version
from sage.libs.eclib.all import mwrank_MordellWeil

proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
print(json.dumps({'event':'environment','sage':version,'pari':str(pari.version()),
                  'affinity':list(os.sched_getaffinity(0)), 'nice':os.nice(0)}),flush=True)

def timeout(signum,frame): raise TimeoutError('curve wall limit 180 seconds')
signal.signal(signal.SIGALRM,timeout)

def coordinates(P): return [str(c) for c in P]

def saturate_checked(E,points):
    """Use eclib's success flag, which E.saturation() only prints on failure."""
    if not points: return [],1,[],True,0
    Emin=E.minimal_model()
    iso=E.isomorphism_to(Emin)
    v=[]
    for P in points:
        x,y=iso(P).xy()
        den=x.denominator().lcm(y.denominator())
        v.append((x*den,y*den,den))
    mw=mwrank_MordellWeil(Emin.mwrank_curve(),verbose=True)
    mw.process(v)
    ok,index,unsat=mw.saturate(max_prime=-1,min_prime=2)
    sat=[(~iso)(Emin(P)) for P in mw.points()]
    # eclib returns the unsaturated-prime list as a printed vector string.
    unsat_primes=[int(p) for p in re.findall(r'\d+',str(unsat))]
    return sat,int(index),unsat_primes,bool(ok),int(mw.rank())

ys=[4]+[y for y in range(1,101) if y!=4]
if len(sys.argv)>1: ys=[int(y) for y in sys.argv[1:]]
with open('pari_descent.jsonl') as f:
    descent={(a['y'],a['sign']):a for a in map(json.loads,f)}
for y in ys:
    for sign in [-1,1]:
        signal.alarm(180)
        start=time.monotonic()
        d=y*y+1
        E=EllipticCurve([0,2*sign*d,0,d*(d+1),0])
        rec=dict(y=y,D=d,sign=sign,ainvs=[int(a) for a in E.ainvs()],sage=version,
                 algorithm='PARI 2.19 certified 2-descent; eclib saturation max_prime=-1; Sage integral_points both_signs=True')
        def emit(event,**kw):
            print(json.dumps(dict(y=y,sign=sign,event=event,seconds=time.monotonic()-start,**kw)),flush=True)
        try:
            emit('start',ainvs=rec['ainvs'])
            des=descent[y,sign]
            rec.update(pari_rank_lower=des.get('rank_lower'),pari_rank_upper=des.get('rank_upper'),
                       field_certifications=des.get('field_certifications'))
            if not des['certified_rank']:
                raise RuntimeError('local PARI rank bounds do not coincide; this curve remains open')
            rank_line=next(l[5:] for l in des['stdout'].splitlines() if l.startswith('RANK '))
            rank_data=pari(rank_line)
            gens=[E([QQ(p[0]),QQ(p[1])]) for p in rank_data[3]]
            rec.update(gens_initial=[coordinates(p) for p in gens],rank=int(des['rank_upper']))
            assert len(gens)==rec['rank'], 'descent did not return enough points'
            emit('gens',rank=rec['rank'],gens=rec['gens_initial'])
            sat,index,unsat,ok,mw_rank=saturate_checked(E,gens)
            rec.update(basis=[coordinates(p) for p in sat],saturation_index=index,unsaturated_primes=unsat,
                       saturation_success=ok,rank_of_saturated_points=mw_rank)
            assert ok and not unsat and len(sat)==mw_rank==rec['rank']
            emit('saturation',basis=rec['basis'],index=index,success=ok)
            torsion=E.torsion_points()
            rec['torsion']=[coordinates(p) for p in torsion]
            points=E.integral_points(mw_base=sat,both_signs=True,verbose=True)
            rec['integral_points']=[coordinates(p) for p in points]
            # Rank-zero integral_points handles torsion directly. Points at infinity excluded.
            recovered=[]
            for P in points:
                u,v=P.xy()
                assert u.denominator()==1 and v.denominator()==1
                u,v=int(u),int(v)
                if u<=0 or v<=0 or u%d: continue
                z=math.isqrt(u//d)
                if z*z!=u//d or z==0 or v%(d*z): continue
                x=v//(d*z)
                if x<=1: continue
                assert x*x-1==d*(z*z+sign)**2
                recovered.append(dict(x=x,y=y,z=z,sign=sign,
                                      known_family=(x==2*y*y+1 and z*z+sign==2*y)))
            rec.update(solutions=recovered,status='complete',seconds=time.monotonic()-start)
            emit('complete',rank=rec['rank'],integral_point_count=len(points),solutions=recovered)
        except Exception as e:
            rec.update(status='open',error=repr(e),traceback=traceback.format_exc(),seconds=time.monotonic()-start)
            emit('error',error=repr(e))
        finally:
            signal.alarm(0)
            with open('sage_results.jsonl','a') as f: f.write(json.dumps(rec)+'\n')
