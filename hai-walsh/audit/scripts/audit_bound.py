"""Inspect every claimed positive-rank bound, stopping before finite searches.

CURVES injected by the launcher. This checks the hypothesis of the lattice
reduction step that the implementation otherwise replaces by an arbitrary value.
"""
import contextlib,inspect,io,json,os,textwrap,traceback
from sage.all import EllipticCurve,QQ,proof
proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
original=EllipticCurve([0,1]).integral_points
namespace=dict(original.__globals__)
class AuditDone(Exception):pass
namespace['AuditDone']=AuditDone
source=textwrap.dedent(inspect.getsource(original))
source=source.replace('def integral_points(', 'def audited_integral_points(',1)
needle='''        if d_L_0 < R(T**2+Q):
            d_L_0 = 10*(T**2*Q)'''
assert needle in source
source=source.replace(needle,'''        if d_L_0 < R(T**2+Q):
            raise RuntimeError(dict(problem="unjustified_lattice_override",computed_lower_bound=str(d_L_0),required_threshold=str(T**2+Q),coefficient_bound=str(H_q),short_vector=[int(t) for t in m_LLL.row(0)],short_vector_norm2=str(sum(t*t for t in m_LLL.row(0))),fabricated_lower_bound=str(10*(T**2*Q)),lattice_last_column=[int(m[i,r]) for i in range(r+1)]))''')
source=source.replace('''    x_int_points3 = integral_points_with_bounded_mw_coeffs(self,mw_base,H_q,x_bound)''','''    raise AuditDone(dict(coefficient_bound=int(H_q),basis=[[str(t) for t in p] for p in mw_base],small_interval=[int(x0),int(x1)],x_bound=str(x_bound)))''')
exec(compile(source,'<audited_integral_points>','exec'),namespace)
function=namespace['audited_integral_points']
for r in CURVES:
    if not r.get('rank'):continue
    E=EllipticCurve(r['ainvs']);B=[E([QQ(t) for t in p]) for p in r['basis']]
    log=io.StringIO()
    result=dict(y=r['y'],sign=r['sign'])
    try:
        with contextlib.redirect_stdout(log):function(E,mw_base=B,both_signs=True)
        raise RuntimeError('did not reach bound inspection')
    except AuditDone as e:
        result.update(status='bound_hypothesis_passed',**e.args[0])
        result['matches_original_coefficient_bound']=result['coefficient_bound']==r['coefficient_bound']
    except Exception as e:result.update(status='error',error=e.args[0] if e.args and isinstance(e.args[0],dict) else str(e),traceback=traceback.format_exc())
    print(json.dumps(result),flush=True)
