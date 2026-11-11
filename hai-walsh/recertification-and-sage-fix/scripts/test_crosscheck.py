import contextlib
import io
import json
import os
from pathlib import Path
import re
import time
import traceback
from sage.all import EllipticCurve, proof
from load_fixed import load_method

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
fixed = load_method()
for row in json.loads(Path('crosscheck-input.json').read_text()):
    begin = time.monotonic()
    rec = dict(label=row['label'],known_miss=row['known_miss'],expected_x=row['expected_x'])
    output = io.StringIO()
    try:
        E = EllipticCurve(row['ainvs'])
        B = E.gens()
        rec['basis'] = [[str(c) for c in P] for P in B]
        with contextlib.redirect_stdout(output):
            points = fixed(E,mw_base=B,both_signs=True,verbose=True)
        xs = sorted({int(P[0]) for P in points})
        assert all(P[1]**2+E.a1()*P[0]*P[1]+E.a3()*P[1]
                   == P[0]**3+E.a2()*P[0]**2+E.a4()*P[0]+E.a6() for P in points)
        rec.update(status='ok',actual_x=xs,matches_table=xs == row['expected_x'],
                   points=[[str(c) for c in P] for P in points])
        match = re.search(r'using coefficient bound (\d+)',output.getvalue())
        rec['bound'] = int(match[1]) if match else 0
        if 'lmfdb_points' in row:
            rec.update(lmfdb_url=row['lmfdb_url'],
                       matches_lmfdb={tuple(p) for p in row['lmfdb_points']}
                       == {tuple(int(c) for c in P[:2]) for P in points})
    except Exception as exc:
        rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    rec.update(log=output.getvalue(),seconds=time.monotonic()-begin)
    print(json.dumps(rec),flush=True)
