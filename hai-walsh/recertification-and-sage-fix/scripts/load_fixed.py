"""Load only copied methods into the installed method's global namespace.

This never writes to or imports a replacement for the installed Sage package.
"""
import ast
from pathlib import Path
import textwrap
from sage.all import EllipticCurve


def load_method(name='integral_points', filename='ell_rational_field.fixed.py', trace=None,
                transform=None):
    source = Path(filename).read_text()
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
               and n.name == 'EllipticCurve_rational_field')
    node = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name)
    lines = source.splitlines(True)
    method = textwrap.dedent(''.join(lines[node.lineno-1:node.end_lineno]))
    original = getattr(EllipticCurve([0,1]), name)
    namespace = dict(original.__globals__)
    if trace is not None:
        namespace['TRACE'] = trace
        method = method.replace('            if d_L_0 > T**2 + Q:',
                                '            TRACE(dict(H=str(H_q), scale=str(c), '
                                'precision=int(lattice_prec), d2=str(d_L_0), '
                                'threshold=str(T**2+Q), attempt=attempt))\n'
                                '            if d_L_0 > T**2 + Q:')
    if transform is not None:
        method = transform(method)
    exec(compile(method, filename, 'exec'), namespace)
    return namespace[name]
