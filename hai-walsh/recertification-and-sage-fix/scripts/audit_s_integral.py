"""Stop the installed S-integral method when it would fabricate a bound."""
import inspect
import json
import os
import textwrap
import traceback
from sage.all import EllipticCurve, ZZ, proof

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
proof.all(True)
original = EllipticCurve([0,1]).S_integral_points
namespace = dict(original.__globals__)
class FailedHypothesis(Exception):
    pass
namespace['FailedHypothesis'] = FailedHypothesis
source = 'if True:\n'+inspect.getsource(original)
needle = 'd_L_0 = 10*(T**2*Q)'
assert source.count(needle) == 2
for site in ['finite','real']:
    source = source.replace(needle,'''raise FailedHypothesis(dict(site="SITE",computed=str(d_L_0),required=str(T**2+Q),H=str(H_q),fabricated=str(10*T**2*Q)))'''.replace('SITE',site),1)
exec(compile(source,'<audit_S_integral_points>','exec'),namespace)
for ainvs,coords in [([0,-34,0,306,0],[[2,22],[9,27],[18,18]]),
                     ([1,0,1,-118,584],[[13,29]])]:
    E = EllipticCurve(ainvs)
    rec = dict(ainvs=ainvs,S=[2])
    try:
        namespace['S_integral_points'](E,[ZZ(2)],mw_base=[E(p) for p in coords],proof=True)
        rec.update(status='fallback_not_reached')
    except FailedHypothesis as exc:
        rec.update(status='invalid_fallback_executed',**exc.args[0])
    except Exception as exc:
        rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    print(json.dumps(rec),flush=True)
