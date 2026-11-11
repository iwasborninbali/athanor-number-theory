#!/usr/bin/env python3
import os,signal,json,time,traceback
from sage.all import EllipticCurve,proof
proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
def timeout(*args):raise TimeoutError('300-second basis-search limit')
signal.signal(signal.SIGALRM,timeout)
signal.alarm(300)
start=time.monotonic()
y=91;d=y*y+1;E=EllipticCurve([0,2*d,0,d*(d+1),0])
try:
    gs=E.gens(proof=True,use_database=False,descent_second_limit=20,verbose=True)
    print(json.dumps({'event':'basis','gens':[[str(c) for c in p] for p in gs],
          'certain':bool(E.gens_certain()),'seconds':time.monotonic()-start}),flush=True)
except Exception as e:
    print(json.dumps({'event':'error','error':repr(e),'seconds':time.monotonic()-start}),flush=True)
