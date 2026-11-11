import contextlib
import io
import json
import os
import re
import time
import traceback
from pathlib import Path
from sage.all import EllipticCurve, QQ, proof
from load_fixed import load_method

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
curves = json.loads(Path('classification.json').read_text())['curves']
for row in curves:
    if row['y'] not in [4,25,93,100] or row['method'] != 'elliptic_integral_points':
        continue
    E = EllipticCurve(row['ainvs'])
    B = [E([QQ(c) for c in P]) for P in row['basis']]
    events = []
    fixed = load_method(trace=events.append)
    out = io.StringIO()
    rec = dict(y=row['y'], sign=row['sign'], rank=row['rank'],
               original_bound=row['coefficient_bound'])
    begin = time.monotonic()
    try:
        with contextlib.redirect_stdout(out):
            points = fixed(E, mw_base=B, both_signs=True, verbose=True)
        expected = {tuple(QQ(c) for c in p) for p in row['integral_points']}
        actual = {tuple(p) for p in points}
        match = re.search(r'using coefficient bound (\d+)', out.getvalue())
        rec.update(status='ok', matches_original=actual == expected,
                   points=[[str(c) for c in P] for P in points],
                   bound=int(match[1]) if match else 0)
    except Exception as exc:
        rec.update(status='error', error=repr(exc), traceback=traceback.format_exc())
    rec.update(events=events, log=out.getvalue(), seconds=time.monotonic()-begin)
    print(json.dumps(rec), flush=True)

for label, ainvs in [('1701d1', [1,-1,1,-11,16]),
                     ('2082a1', [1,0,1,-118,584]),
                     ('1848f1', [0,1,0,44,-847])]:
    E = EllipticCurve(ainvs)
    B = E.gens()
    events = []
    out = io.StringIO()
    begin = time.monotonic()
    rec = dict(label=label)
    try:
        with contextlib.redirect_stdout(out):
            points = load_method(trace=events.append)(E, mw_base=B, both_signs=True, verbose=True)
        rec.update(status='ok', points=[[str(c) for c in P] for P in points])
    except Exception as exc:
        rec.update(status='error', error=repr(exc), traceback=traceback.format_exc())
    rec.update(events=events, log=out.getvalue(), seconds=time.monotonic()-begin)
    print(json.dumps(rec), flush=True)
