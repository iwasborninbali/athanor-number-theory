"""Independent normalization check against Sage/PARI's AGM logarithms.

The certificate uses Arb enclosures and the integral identities in the proof;
this comparison is a diagnostic, not the numerical proof itself.
"""
import json
import os
from pathlib import Path
from sage.all import EllipticCurve, QQ, RealBallField
from certified_bounds import Geometry

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
R = RealBallField(160)


def inside(ball,value):
    return ball.lower().exact_rational() <= value <= ball.upper().exact_rational()


for row in json.loads(Path('classification.json').read_text())['curves']:
    if row['method'] != 'elliptic_integral_points':
        continue
    E = EllipticCurve(row['ainvs'])
    B = [E([QQ(c) for c in p]) for p in row['lll_basis']]
    logs,w,area,root_bound = Geometry(E,B).enclose(160)
    w1,w2 = E.period_lattice().basis(prec=512)
    w1 = w1.real()
    assert inside(w,w1)
    assert inside(area,abs(w1*w2.imag()))
    for P,ball in zip(B,logs):
        z = (2*P).elliptic_logarithm(precision=512).real()/w1
        if z > QQ(1)/2:
            z -= 1
        assert inside(ball,z)
    print(json.dumps(dict(y=row['y'],sign=row['sign'],status='PASS',
                          logarithms_checked=len(logs),precision_arb=160,precision_pari=512)),flush=True)
