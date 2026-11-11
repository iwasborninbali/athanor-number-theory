#!/usr/bin/env python3
import os, json, time, signal, inspect, pathlib, traceback
from sage.all import EllipticCurve, proof, pari
from sage.version import version

proof.all(True)
assert os.sched_getaffinity(0) == {1}
print(json.dumps({'event':'environment','sage':version,'pari':str(pari.version()),
                  'affinity':list(os.sched_getaffinity(0)), 'nice':os.nice(0)}),flush=True)

def timeout(signum, frame):
    raise TimeoutError('pilot curve wall limit 600 seconds')
signal.signal(signal.SIGALRM, timeout)
for y in [4,1,2,3,5]:
    for sign in [-1,1]:
        signal.alarm(600)
        start=time.monotonic()
        E=EllipticCurve([0,2*sign*(y*y+1),0,(y*y+1)*(y*y+2),0])
        def emit(event, **kw):
            print(json.dumps(dict(y=y,sign=sign,event=event,seconds=time.monotonic()-start,**kw)),flush=True)
        try:
            emit('start',ainvs=[int(a) for a in E.a_invariants()])
            gens=E.gens(proof=True)
            emit('gens',gens=[[str(c) for c in p] for p in gens],rank=int(E.rank(proof=True)))
            sat, index, reg=E.saturation(gens,verbose=True)
            emit('saturation',gens=[[str(c) for c in p] for p in sat],index=int(index),regulator=str(reg))
            points=E.integral_points(mw_base=sat,both_signs=True,verbose=True)
            emit('integral_points',points=[[str(c) for c in p] for p in points],count=len(points))
        except Exception as e:
            emit('error',error=repr(e),traceback=traceback.format_exc())
        finally:
            signal.alarm(0)
