"""Run the independent certified bound, then exact rational exhaustion."""
import argparse
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import time
import traceback
from sage.all import EllipticCurve, QQ, proof
from certified_bounds import coefficient_bound

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
parser = argparse.ArgumentParser()
parser.add_argument('--y', type=int, nargs='*')
parser.add_argument('--bounds-only', action='store_true')
args = parser.parse_args()
curves = json.loads(Path('classification.json').read_text())['curves']
for row in curves:
    if row['method'] != 'elliptic_integral_points' or (args.y and row['y'] not in args.y):
        continue
    begin = time.monotonic()
    record = dict(y=row['y'],sign=row['sign'],rank=row['rank'],
                  original_bound=row['coefficient_bound'])
    try:
        E = EllipticCurve(row['ainvs'])
        B = [E([QQ(c) for c in p]) for p in row['lll_basis']]
        bound,certificate = coefficient_bound(E,B)
        record.update(status='bound_certified',bound=bound,certificate=certificate,
                      basis=row['lll_basis'],ainvs=row['ainvs'])
        if not args.bounds_only:
            raise NotImplementedError('use independent_exact.py after generating bounds')
    except Exception as exc:
        record.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    record['seconds'] = time.monotonic()-begin
    print(json.dumps(record),flush=True)
