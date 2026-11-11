"""Diagnostic only: high-precision logs, exact Gram-Schmidt lower bound.

Does not certify real error bounds, and does not replace a complete proof.
"""
import inspect,json,os,textwrap,time,traceback
from sage.all import EllipticCurve,QQ,RealField,ComplexField,proof
proof.all(True)
assert os.sched_getaffinity(0)=={1} and os.nice(0)>=19
original=EllipticCurve([0,1]).integral_points
namespace=dict(original.__globals__)
PREC=4096
namespace.update(R=RealField(PREC),C=ComplexField(PREC),PREC=PREC)
class BoundDone(Exception):pass
namespace['BoundDone']=BoundDone
source=textwrap.dedent(inspect.getsource(original))
source=source.replace('def integral_points(', 'def diagnostic_integral_points(',1)
source=source.replace('self.height_pairing_matrix(mw_base)','self.height_pairing_matrix(mw_base, precision=PREC)')
source=source.replace('(mu + 2.14).exp()','R(mu + R(107)/50).exp()')
source=source.replace('self.height()','self.height(precision=PREC)')
source=source.replace('self.period_lattice().basis()','self.period_lattice().basis(prec=PREC)')
source=source.replace('.elliptic_logarithm().abs()','.elliptic_logarithm(precision=PREC).abs()')
source=source.replace('mw_base[i].height()','mw_base[i].height(precision=PREC)')
source=source.replace('H_q = R(10)**bound','H_q = Z(10)**bound')
source=source.replace('c = R((H_q**n)*10)','c = Z((H_q**n)*10)')
source=source.replace('d_L_0 = R(b1_norm**2 / c1_LLL)','d_L_0 = min(sum(t*t for t in row) for row in m_gram.rows())')
source=source.replace('''        if d_L_0 < R(T**2+Q):
            d_L_0 = 10*(T**2*Q)''','''        if d_L_0 <= T**2+Q:
            raise RuntimeError("lattice condition still failed at high precision")''')
start=source.index('        c = Z((H_q**n)*10)')
end=source.index('        low_bound = ',start)
source=source[:start]+'''        Q = r * H_q**2
        T = (1 + (Z(3)/2*r*H_q))/2
        for retry in range(16):
            c = Z(10)**(retry+1)*H_q**n
            m = copy(M.identity_matrix())
            for i in range(r):
                m[i,r] = R(c*mw_base_log[i]).round()
            m[r,r] = max(Z(1),R(c*w1).round())
            m_LLL = m.LLL()
            gs = m_LLL.gram_schmidt()[0]
            d_L_0 = min(sum(t*t for t in row) for row in gs.rows())
            if d_L_0 > T**2+Q:
                break
        else:
            raise RuntimeError("lattice hypothesis failed after scaling retries")
''' +source[end:]
source=source.replace('''    b2_12 = b2/12''','''    raise BoundDone(dict(coefficient_bound=int(H_q),basis=[[str(t) for t in p] for p in mw_base]))
    b2_12 = b2/12''')
exec(compile(source,'<high_precision_diagnostic>','exec'),namespace)
function=namespace['diagnostic_integral_points']
for r in CURVES:
    E=EllipticCurve(r['ainvs']); B=[E([QQ(t) for t in p]) for p in r['basis']]
    result=dict(y=r['y'],sign=r['sign'],precision=PREC,original_bound=r['coefficient_bound'])
    begin=time.monotonic()
    try:
        function(E,mw_base=B,both_signs=True)
    except BoundDone as e:result.update(status='diagnostic_pass',**e.args[0])
    except Exception as e:result.update(status='error',error=str(e),traceback=traceback.format_exc())
    result['seconds']=time.monotonic()-begin
    print(json.dumps(result),flush=True)
