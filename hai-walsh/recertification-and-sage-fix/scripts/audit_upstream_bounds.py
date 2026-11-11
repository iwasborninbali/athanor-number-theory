"""Execute the pinned current upstream method, stopping at its bad assignment."""
import json
import os
from fractions import Fraction
from pathlib import Path
from sage.all import EllipticCurve, QQ
from load_fixed import load_method

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
class AuditStop(Exception):
    pass


def transform(source):
    needle = 'd_L_0 = 10*(T**2*Q)'
    assert source.count(needle) == 1
    return source.replace(needle,'''raise AuditStop(dict(computed=str(d_L_0),required=str(T**2+Q),H=str(H_q),fabricated=str(10*T**2*Q),short_vector=[int(x) for x in m_LLL.row(0)],column=[int(m[i,r]) for i in range(r+1)]))''')


function = load_method(filename='ell_rational_field.pinned.py',transform=transform)
function.__globals__['AuditStop'] = AuditStop
count = 0
for row in json.loads(Path('classification.json').read_text())['curves']:
    if row['method'] != 'elliptic_integral_points' or not row['rank']:
        continue
    E = EllipticCurve(row['ainvs'])
    B = [E([QQ(c) for c in P]) for P in row['basis']]
    try:
        function(E,mw_base=B)
    except AuditStop as exc:
        data = exc.args[0]
        v,col = data['short_vector'],data['column']
        coefficient,remainder = divmod(v[-1]-sum(a*b for a,b in zip(v[:-1],col[:-1])),col[-1])
        assert remainder == 0
        norm2 = sum(x*x for x in v)
        assert norm2 > 0 and Fraction(norm2) < Fraction(data['fabricated'])
        print(json.dumps(dict(y=row['y'],sign=row['sign'],status='invalid_fallback_reproduced',
                              norm2=str(norm2),row_coefficients=v[:-1]+[coefficient],**data)),flush=True)
        count += 1
    else:
        raise AssertionError('expected the fallback on this positive-rank lab curve')
assert count == 144
