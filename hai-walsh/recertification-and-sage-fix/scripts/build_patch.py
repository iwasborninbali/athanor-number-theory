"""Build the focused repair against the pinned Sage develop source."""
from pathlib import Path
import difflib

ROOT = Path(__file__).resolve().parents[1]
original = (ROOT / 'sources/ell_rational_field.pinned.py').read_text()
start = original.index('            c = R((H_q**n)*10)', original.index('    def integral_points('))
end = original.index('            #new bound according to low_bound', start)
replacement = '''            # A failed lattice inequality cannot be repaired by replacing
            # its lower bound. Recompute at a larger scale and precision.
            c = 10 * Z(H_q)**n
            Q = r * Z(H_q)**2
            for attempt in range(16):
                lattice_prec = max(128, c.nbits() + 64*(attempt+1))
                C_lattice = ComplexBallField(lattice_prec)
                R_lattice = C_lattice(0).real().parent()
                root = C_lattice(real_root)
                other = [C_lattice(z) for z in lattice_roots if z != real_root]
                period = (2*C_lattice(0).elliptic_rf(root-other[0],
                                                    root-other[1])).real()
                # Carlson's integral encloses the absolute centered real log.
                # Preprocessing put the basis on the identity component.
                logs = []
                for P in mw_base:
                    x = C_lattice(P[0] + b2/12)
                    u = (x-root).elliptic_rf(x-other[0], x-other[1]).real()
                    logs.append(torsion_exponent*u/period)
                rounded = [Z((c*u).mid().round()) for u in logs]
                errors = [abs(c*u-a).upper().exact_rational()
                          for u, a in zip(logs, rounded)]
                T = Z(H_q)*sum(errors)
                m = copy(M.identity_matrix())
                for i in range(r):
                    m[i, r] = rounded[i]
                # Normalizing by the real period makes this column exact.
                # Multiplying logs by the torsion exponent clears its offset.
                m[r, r] = c

                # LLL operates on rows. Every nonzero vector has squared
                # length at least the minimum squared Gram-Schmidt length.
                # Keep this calculation and the positivity test exact.
                m_gram = m.LLL().gram_schmidt()[0]
                d_L_0 = min(v.dot_product(v) for v in m_gram.rows())
                if d_L_0 > T**2 + Q:
                    low = ((R_lattice(d_L_0 - Q).sqrt() - T)
                           * period / (torsion_exponent*c))
                    if low > 0:
                        low_bound = low.lower().exact_rational()
                        break
                c *= 10
            else:
                raise RuntimeError("unable to establish the integral-point "
                                   "lattice reduction inequality")
'''
modified = original[:start] + replacement + original[end:]
# The first bound is an integer, too; a rounded real power must not reduce it.
modified = modified.replace('        H_q = R(10)**bound\n', '        H_q = Z(10)**bottom\n', 1)
needle = '''        M = MatrixSpace(Z,n)
        while break_cond < 0.9:'''
setup = '''        from sage.rings.complex_arb import ComplexBallField
        from sage.rings.qqbar import QQbar
        lattice_roots = pol.roots(QQbar, multiplicities=False)
        real_root = max(z for z in lattice_roots if z.imag() == 0)
        torsion_exponent = self.torsion_subgroup().exponent()
        M = MatrixSpace(Z,n)
        while break_cond < 0.9:'''
assert needle in modified
modified = modified.replace(needle, setup, 1)

# Regression: the old fabricated bound omits these known multiples.
needle = '        ALGORITHM:\n\n        This function uses the algorithm given in [Coh2007I]_.\n'
tests = '''        The reduction must establish its lattice inequality before using
        a lower bound (see :issue:`27015`)::

            sage: E = EllipticCurve([1,-1,1,-11,16])
            sage: 20829482 in [P[0] for P in E.integral_points([E(2,-2)])]
            True
            sage: E = EllipticCurve([1,0,1,-118,584])
            sage: 507525709 in [P[0] for P in E.integral_points([E(13,29)])]
            True

'''
assert needle in modified
modified = modified.replace(needle, tests+needle, 1)
modified = modified.replace(
    'starting search of remaining points using coefficient bound 5 and |x| bound 1.53897183921...e25',
    'starting search of remaining points using coefficient bound ... and |x| bound ...', 1)

(ROOT / 'sources/ell_rational_field.fixed.py').write_text(modified)
patch = ''.join(difflib.unified_diff(
    original.splitlines(True), modified.splitlines(True),
    fromfile='a/src/sage/schemes/elliptic_curves/ell_rational_field.py',
    tofile='b/src/sage/schemes/elliptic_curves/ell_rational_field.py'))
(ROOT / 'fix.patch').write_text(patch)

# The same assignment in S_integral_points is unsafe at both finite and real
# places. Fail closed there: repairing p-adic precision requires separate work.
old = '''            if d_L_0 < R(T**2+Q):
                d_L_0 = 10*(T**2*Q)'''
new = '''            if d_L_0 <= T**2 + Q:
                raise RuntimeError("unable to establish the S-integral-point "
                                   "lattice reduction inequality")'''
assert modified.count(old) == 2
guarded = modified.replace(old, new)
guarded = guarded.replace('d_L_0 = R(b1_norm**2 / c1_LLL)',
                          'd_L_0 = min(v.dot_product(v) for v in m_gram.rows())')
patch = ''.join(difflib.unified_diff(
    modified.splitlines(True), guarded.splitlines(True),
    fromfile='a/src/sage/schemes/elliptic_curves/ell_rational_field.py',
    tofile='b/src/sage/schemes/elliptic_curves/ell_rational_field.py'))
(ROOT / 's-integral-fail-closed.patch').write_text(patch)
