import json
import os
from sage.all import EllipticCurve, matrix, ZZ, QQ
from load_fixed import load_method

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
E = EllipticCurve([1,-1,1,-11,16])
for replacement in ['d_L_0 = 0', 'd_L_0 = T**2 + Q']:
    events = []
    def change(source):
        needle = 'd_L_0 = min(v.dot_product(v) for v in m_gram.rows())'
        assert needle in source
        return source.replace(needle,replacement)
    f = load_method(trace=events.append,transform=change)
    def forbid_enumeration(*args,**kwds):
        raise AssertionError('finite enumeration must not be reached')
    f.__globals__['integral_points_with_bounded_mw_coeffs'] = forbid_enumeration
    try:
        f(E,mw_base=[E(2,-2)])
    except RuntimeError as exc:
        assert str(exc) == 'unable to establish the integral-point lattice reduction inequality'
    else:
        raise AssertionError('expected capped failure')
    assert len(events) == 16
    assert all(int(b['scale']) == 10*int(a['scale']) for a,b in zip(events,events[1:]))
    assert all(b['precision'] > a['precision'] for a,b in zip(events,events[1:]))
    print(json.dumps(dict(test=replacement,status='PASS',attempts=len(events))),flush=True)

# A genuine 0.99-LLL-reduced basis for which the old length-ratio expression
# exceeds the squared length of an actual nonzero vector.
A = matrix(ZZ,[[2000,0,0],[1000,1722,0],[0,861,1484]])
assert A.is_LLL_reduced(delta=QQ(99)/100)
stars = A.gram_schmidt()[0]
assert [v.dot_product(v) for v in stars.rows()] == [4000000,2965284,2202256]
old_bound = ZZ(2000)*1484
witness = A.row(2)
assert witness.dot_product(witness) == 2943577 < old_bound
print(json.dumps(dict(test='Gram-Schmidt counterexample',status='PASS',
                      old_bound=int(old_bound),actual_norm2=2943577,
                      corrected_lower_bound=2202256)),flush=True)
