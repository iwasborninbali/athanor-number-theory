"""Extract upstream function doctests, prepended by a local monkey patch."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'sources/ell_rational_field.fixed.py').read_text()
tree = ast.parse(source)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
           and n.name == 'EllipticCurve_rational_field')
nodes = {n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
doc = ast.get_docstring(nodes['integral_points'],clean=False)
helper = next(n for n in tree.body if isinstance(n,ast.FunctionDef)
              and n.name == 'integral_points_with_bounded_mw_coeffs')
doc += '\n'+ast.get_docstring(helper,clean=False)
prefix = '''r"""
    sage: from load_fixed import load_method
    sage: from sage.schemes.elliptic_curves.ell_rational_field import EllipticCurve_rational_field
    sage: original_method = EllipticCurve_rational_field.integral_points
    sage: EllipticCurve_rational_field.integral_points = load_method()
'''
suffix = '''
    sage: EllipticCurve_rational_field.integral_points = original_method
"""
'''
(ROOT/'scripts/upstream_doctests.py').write_text(prefix+doc+suffix)
