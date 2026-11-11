"""Reproduce known omissions and capture the unmodified bounds."""
import contextlib
import io
import json
import os
import time
import traceback
from sage.all import EllipticCurve, proof
from sage.version import version

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
print(json.dumps(dict(event='environment', sage=version,
                     affinity=list(os.sched_getaffinity(0)), nice=os.nice(0))), flush=True)
cases = [
    ('1701d1', [1,-1,1,-11,16]),
    ('2082a1', [1,0,1,-118,584]),
    ('1848f1', None),
]
for label, ainvs in cases:
    begin = time.monotonic()
    rec = dict(label=label)
    try:
        E = EllipticCurve(label) if ainvs is None else EllipticCurve(ainvs)
        rec['ainvs'] = [int(a) for a in E.ainvs()]
        B = E.gens()
        rec['basis'] = [[str(c) for c in P] for P in B]
        rec['known_multiples'] = {str(k): [str(c) for c in k*B[0]] for k in [5,6,7,13]}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            points = E.integral_points(mw_base=B, both_signs=True, verbose=True)
        rec.update(status='ok', points=[[str(c) for c in P] for P in points], log=output.getvalue())
        if label == '1701d1':
            rec['witness'] = [str(c) for c in 7*B[0]]
            rec['witness_missed'] = 7*B[0] not in points
        if label == '2082a1':
            rec['witness'] = [str(c) for c in 13*B[0]]
            rec['witness_missed'] = 13*B[0] not in points
    except Exception as exc:
        rec.update(status='error', error=repr(exc), traceback=traceback.format_exc())
    rec['seconds'] = time.monotonic()-begin
    print(json.dumps(rec), flush=True)
