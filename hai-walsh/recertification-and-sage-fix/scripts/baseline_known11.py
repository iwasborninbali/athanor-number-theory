"""Assess the installed method on all eleven historically problematic curves."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import time
import traceback
from sage.all import EllipticCurve, QQ, proof

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
inputs = {r['label']:r for r in json.loads(Path('crosscheck-input.json').read_text())}
for fixed in map(json.loads,Path('crosscheck.log').read_text().splitlines()):
    if not fixed['known_miss']:
        continue
    begin = time.monotonic()
    label = fixed['label']
    E = EllipticCurve(inputs[label]['ainvs'])
    B = [E([QQ(c) for c in p]) for p in fixed['basis']]
    rec = dict(label=label,expected_x=fixed['expected_x'],patched_bound=fixed['bound'])
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            points = E.integral_points(mw_base=B,both_signs=True,verbose=True)
        xs = sorted({int(p[0]) for p in points})
        match = re.search(r'using coefficient bound (\d+)',output.getvalue())
        rec.update(status='ok',old_bound=int(match[1]) if match else 0,actual_x=xs,
                   missing_x=sorted(set(fixed['expected_x'])-set(xs)),
                   extra_x=sorted(set(xs)-set(fixed['expected_x'])),
                   torsion_order=int(E.torsion_order()))
    except Exception as exc:
        rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    rec.update(log=output.getvalue(),seconds=time.monotonic()-begin)
    print(json.dumps(rec),flush=True)
