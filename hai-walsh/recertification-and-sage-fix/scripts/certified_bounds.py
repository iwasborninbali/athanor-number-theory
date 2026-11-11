"""Independent bounds for the lab's curves, with exact/Arb certificates.

The lattice and analytic geometry follow the elliptic-logarithm method.
Carlson-integral formulas and the use of exact doubling to enclose heights
were informed by Manvir Jaswal's GPL Sage PR #43044 (head 9be54a7f).
This module does not import that implementation or use Sage's old bound.

The height-difference bound here is derived from exact Bezout identities for
the duplication map. See certificate-proof.md for the complete derivation.
"""
from sage.all import (ZZ, QQ, QQbar, PolynomialRing, RealBallField,
                      ComplexBallField, matrix, RDF)


def upper(x):
    return x.upper().exact_rational()


def ceil_upper(x):
    return ZZ(upper(x).ceil())


def endpoints(x):
    return [str(x.lower().exact_rational()), str(upper(x))]


def duplication_bound(E):
    """Certify |H(P)-h(x(P))| <= B from the degree-four duplication map."""
    assert E.a1() == E.a3() == E.a6() == 0
    a, b = E.a2(), E.a4()
    ring = PolynomialRing(QQ, 't')
    t = ring.gen()
    charts = [((t*t-b)**2, 4*t*(t*t+a*t+b)),
              ((1-b*t*t)**2, 4*t*(1+a*t+b*t*t))]
    records = []
    for f, g in charts:
        d, u, v = f.xgcd(g)
        assert d == 1
        denominator = ZZ(1)
        for c in list(u) + list(v):
            denominator = denominator.lcm(c.denominator())
        u, v = denominator*u, denominator*v
        assert u*f+v*g == denominator
        assert all(c in ZZ for c in list(u)+list(v))
        size = sum(abs(c) for c in u) + sum(abs(c) for c in v)
        records.append(dict(R=int(denominator), K=int(size),
                            U=[int(c) for c in u], V=[int(c) for c in v]))
    K = max(records[0]['K']*records[1]['R'], records[1]['K']*records[0]['R'])
    C = max((1+abs(b))**2, 4*(1+abs(a)+abs(b)))
    D = ZZ(max(C, K))
    B = ceil_upper(RealBallField(128)(D).log()/3)
    return B, dict(charts=records, C=int(C), K=int(K), D=int(D), B=int(B))


def positive_definite(H):
    """Interval LDL; a successful check certifies every enclosed matrix."""
    r = len(H)
    L = [[0]*r for _ in range(r)]
    diagonal = []
    for j in range(r):
        d = H[j][j] - sum(L[j][k]**2*diagonal[k] for k in range(j))
        if not d > 0:
            return False
        diagonal.append(d)
        for i in range(j+1, r):
            L[i][j] = (H[i][j]-sum(L[i][k]*L[j][k]*diagonal[k]
                                   for k in range(j)))/d
    return True


def height_matrix(E, basis, B):
    R = RealBallField(160)
    r = len(basis)
    pairs = [(i,j) for i in range(r) for j in range(i)]
    points = list(basis) + [basis[i]+basis[j] for i,j in pairs]
    doubled = [8*P for P in points]
    for n in range(3, 10):
        heights = []
        for P in doubled:
            if not P:
                heights.append(R(0))
            else:
                x = P[0]
                h = R(max(abs(x.numerator()),x.denominator())).log()/ZZ(4)**n
                heights.append(h.add_error(R(B)/ZZ(4)**n))
        H = [[R(0) for _ in range(r)] for _ in range(r)]
        for i in range(r):
            H[i][i] = heights[i]
        for h,(i,j) in zip(heights[r:],pairs):
            H[i][j] = H[j][i] = (h-heights[i]-heights[j])/2
        estimate = min(x.real() for x in matrix(RDF, [[float(v.mid()) for v in row]
                                                     for row in H]).eigenvalues())
        uncertainty = max(sum(upper(abs(x-R(x.mid()))) for x in row) for row in H)
        if estimate <= 0 or uncertainty > QQ(estimate)/32:
            doubled = [2*P for P in doubled]
            continue
        candidate = QQ(estimate)*QQ(7)/8
        for _ in range(16):
            if candidate > 0 and positive_definite([
                    [H[i][j]-(candidate if i == j else 0) for j in range(r)]
                    for i in range(r)]):
                return candidate, heights[:r], dict(
                    doublings=n, lambda_lower=str(candidate),
                    height_matrix=[[endpoints(x) for x in row] for row in H])
            candidate /= 2
        doubled = [2*P for P in doubled]
    raise ArithmeticError('could not certify a positive height eigenvalue')


class Geometry:
    def __init__(self, E, basis):
        self.E = E
        self.doubles = [2*P for P in basis]
        ring = PolynomialRing(QQ, 's')
        f = ring([-E.c6()/864, -E.c4()/48, 0, 1])
        self.roots = f.roots(QQbar, multiplicities=False)
        assert len(self.roots) == 3
        self.real = sorted(z for z in self.roots if z.imag() == 0)
        self.root = self.real[-1]

    def enclose(self, precision):
        E = self.E
        C = ComplexBallField(precision)
        R = RealBallField(precision)
        e1 = C(self.root)
        e2,e3 = [C(z) for z in self.roots if z != self.root]
        w = (2*C(0).elliptic_rf(e1-e2,e1-e3)).real()
        if E.discriminant() > 0:
            a,b,c = self.real
            v = (2*C(0).elliptic_rf(C(b-a),C(c-a))).real()
        else:
            v = C(0).elliptic_rf(e2-e1,e3-e1).real()
        if not (w > 0 and v > 0):
            raise ArithmeticError('period enclosure is not positive')
        logs = []
        for P in self.doubles:
            s = P[0]+E.b2()/12
            if not R(s)-e1.real() > 0:
                raise ArithmeticError('logarithm meets a branch point')
            u = C(C(s)-e1).elliptic_rf(C(s)-e2,C(s)-e3).real()
            if P[1]+(E.a1()*P[0]+E.a3())/2 > 0:
                u = -u
            logs.append(u/w)
        root_bound = max(upper(abs(C(z))) for z in self.roots)
        return logs,w,w*v,root_bound


def coefficient_bound(E, basis):
    r = len(basis)
    if not r:
        return 0, dict(rank=0, steps=[])
    B, duplication = duplication_bound(E)
    lam, heights, heights_record = height_matrix(E,basis,B)
    geometry = Geometry(E,basis)
    precision = 160
    logs,w,area,root_bound = geometry.enclose(precision)
    R = w.parent()
    shift = abs(E.b2()/12)
    z = max(2*root_bound,shift,QQ(1))
    small_height = R(max(QQ(1),z+shift)).log()+B
    small_bound = ceil_upper((small_height/lam).sqrt())
    log_K = (R(4)*R(2).sqrt()).log()+(R(B)+R(2).log())/2

    # Direct specialization of David (1995), Theorem 2.1, with D=1, E=e,
    # k=r+1 and a common log(V_i)=A. These are enlarged upper constants.
    g2,g3 = E.c4()/12,E.c6()/216
    d = g2.denominator().lcm(g3.denominator())
    j = E.j_invariant()
    h = max(ZZ(1),ceil_upper(R(max(d,abs(d*g2),abs(d*g3))).log()),
            ceil_upper(R(max(abs(j.numerator()),j.denominator())).log()))
    A = max(ZZ(1),h,ceil_upper(3*R.pi()*w**2/area),
            *(ceil_upper(8*H) for H in heights))
    exponent = E.torsion_subgroup().exponent()
    k = r+1
    constant = (ZZ(3)*10**(6*k+12)*4**(2*(k+1)**2)
                *(k+2)**(2*k*k+13*k+30))
    offset = A+3*h+ceil_upper(R(exponent*(r+2)).log())
    power = ZZ(k+1)
    for _ in range(16):
        s = power*R(10).log()
        beta = s+offset
        rhs = constant*R(A)**k*(beta+1)*(beta+h+1)**(k+1)+log_K+R(exponent).log()
        lhs = R(lam)*R(10)**(2*power)/2
        if lhs > rhs and 2*s > k+2:
            break
        power *= 2
    else:
        raise ArithmeticError('David initial bound failed')
    N = max(ZZ(10)**power,small_bound)
    record = dict(rank=r,duplication=duplication,heights=heights_record,
                  david=dict(h=int(h),A=int(A),k=k,constant=str(constant),
                             offset=int(offset),power=int(power),
                             initial_bound=str(N),lhs=endpoints(lhs),rhs=endpoints(rhs)),
                  small_bound=int(small_bound),steps=[])

    # The bounded x-region is exhausted separately. Its (potentially much
    # larger) coefficient bound need not enlarge the remaining search box.
    record['small_x_interval'] = [0, int(ceil_upper(R(z+shift)))]

    for step in range(32):
        if N <= 1:
            break
        scale = (exponent*N)**(r+1)
        for attempt in range(32):
            precision = max(precision,scale.nbits()+96)
            logs,w,area,_ = geometry.enclose(precision)
            R = w.parent()
            rounded = [ZZ((scale*x).mid().round()) for x in logs]
            errors = [upper(abs(scale*x-a)) for x,a in zip(logs,rounded)]
            lattice = matrix(ZZ,r+1,r+1,1)
            for i,a in enumerate(rounded):
                lattice[i,r] = a
            lattice[r,r] = scale
            reduced = lattice.LLL()
            gs = reduced.gram_schmidt()[0]
            lengths = [v.dot_product(v) for v in gs.rows()]
            delta = min(lengths)
            gap = delta/exponent**2-r*N**2
            threshold = exponent**2*(r*N**2+(N*sum(errors))**2)
            event = dict(step=step,attempt=attempt,N=str(N),scale=str(scale),
                         precision=int(precision),d2=str(delta),
                         threshold=str(threshold),accepted=bool(delta > threshold))
            record['steps'].append(event)
            if gap > 0:
                lower = (R(gap).sqrt()-N*sum(errors))/scale
                if lower > 0:
                    # Bound 2*u(P)/w using the exact lattice and Arb errors.
                    log_K = (R(4)*R(2).sqrt()).log()+(R(B)+R(2).log())/2
                    square = 2*(log_K-w.log()-lower.log())/lam
                    new_bound = (ZZ(0) if square < 0 else ceil_upper(square.sqrt()))
                    event.update(lower=endpoints(lower),new_bound=int(new_bound),
                                 last_column=[str(x) for x in rounded]+[str(scale)],
                                 errors=[str(x) for x in errors],
                                 reduced=[[str(x) for x in row] for row in reduced.rows()],
                                 gs_squared=[str(x) for x in lengths])
                    break
            scale *= 16
        else:
            raise ArithmeticError('lattice inequality failed after 32 attempts')
        if new_bound >= N:
            break
        N = ZZ(new_bound)
    else:
        raise ArithmeticError('coefficient reduction did not terminate')
    record['bound'] = int(N)
    return int(N),record
