import json
import os
import re
import time
import traceback
from pathlib import Path
from sage.all import EllipticCurve, QQ, proof
from sage.libs.eclib.all import mwrank_MordellWeil

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
for row in json.loads(Path('classification.json').read_text())['curves']:
    if row['method'] != 'elliptic_integral_points':
        continue
    begin = time.monotonic()
    rec = dict(y=row['y'],sign=row['sign'],rank=row['rank'])
    try:
        E = EllipticCurve(row['ainvs'])
        assert row['rank_bounds'] == [row['rank']]*2
        if not row['rank']:
            rec.update(status='rank_zero',success=True,index=1,unsaturated=[])
        else:
            minimal = E.minimal_model()
            iso = E.isomorphism_to(minimal)
            points = []
            for p in row['basis']:
                x,y = iso(E([QQ(c) for c in p])).xy()
                denominator = x.denominator().lcm(y.denominator())
                points.append((x*denominator,y*denominator,denominator))
            mw = mwrank_MordellWeil(minimal.mwrank_curve(),verbose=False)
            mw.process(points,saturation_bound=0)
            success,index,unsaturated = mw.saturate(max_prime=-1,min_prime=2)
            unsaturated = [int(p) for p in re.findall(r'\d+',str(unsaturated))]
            assert success and not unsaturated and index == 1
            assert mw.rank() == row['rank']
            rec.update(status='full_saturation_confirmed',success=bool(success),
                       index=int(index),unsaturated=unsaturated)
    except Exception as exc:
        rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    rec['seconds'] = time.monotonic()-begin
    print(json.dumps(rec),flush=True)
