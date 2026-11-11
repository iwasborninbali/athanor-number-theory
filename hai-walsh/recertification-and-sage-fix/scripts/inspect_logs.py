import inspect
import os
from sage.all import *
assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
E = EllipticCurve([0,-34,0,306,0])
P = E(18,18)
print(inspect.getsource(P.elliptic_logarithm))
print(inspect.getsource(ComplexBallField()(0).elliptic_rf) if False else ComplexBallField()(0).elliptic_rf.__doc__[:3500])
for p in [P,-P,E(9,27),E(2,22)]:
    print(p, p.elliptic_logarithm(precision=100), E.period_lattice().elliptic_logarithm(p,prec=100))
