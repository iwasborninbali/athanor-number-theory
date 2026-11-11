import inspect
import os
from sage.all import EllipticCurve
assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
source = inspect.getsource(EllipticCurve([0,1]).S_integral_points)
for i,line in enumerate(source.splitlines(),1):
    if 'd_L_0' in line:
        print(i,repr(line))
