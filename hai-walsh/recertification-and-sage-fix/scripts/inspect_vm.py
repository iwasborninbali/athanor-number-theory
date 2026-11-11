import inspect
import os
from sage.all import *
from sage.schemes.elliptic_curves import period_lattice

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
print(version())
print(os.sched_getaffinity(0), os.nice(0))
print(inspect.getfile(period_lattice))
print([s for s in dir(ComplexBallField()(1)) if 'elliptic' in s])
print(inspect.signature(EllipticCurve([0,0,0,-2,1]).integral_points))
print(inspect.getsource(period_lattice.PeriodLattice_ell.elliptic_logarithm))
