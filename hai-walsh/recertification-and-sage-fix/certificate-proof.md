# Independent Hai–Walsh completeness certificate

This proof accompanies `scripts/certified_bounds.py` and the exact exhaustion
in `scripts/independent_exact.py`. It deliberately does not use the legacy
Sage/Cohen initial coefficient bound. Full Mordell–Weil bases and proved rank
upper bounds are inherited from the earlier PARI/eclib certificate, and are
checked again below. The numerical proof dependencies are Sage's exact
algebraic numbers, rational matrix arithmetic, and Arb enclosures for logarithms
and Carlson integrals. This is a mathematical software certificate, not a
formal proof checked in a proof assistant.

## Heights without numerical height algorithms

For the lab curves write

\[
 E:y^2=x^3+ax^2+bx,\qquad
 H(P)=\lim_{n\to\infty}4^{-n}h(x(2^nP)).
\]

Here `h(A/B)=log(max(|A|,B))` for coprime integers `A,B`, `B>0`, and
`h(infinity)=0`. The duplication map is

\[
 (A:B)\mapsto(F(A,B):G(A,B)),\quad
 F=(A^2-bB^2)^2,\quad G=4AB(A^2+aAB+bB^2).
\]

Its two dehomogenizations have exact polynomial Bezout identities
`U_i F_i+V_i G_i=R_i`, with integer coefficients and positive integer `R_i`.
The program records these identities. Put
`K_i=sum(abs(coefficients(U_i)))+sum(abs(coefficients(V_i)))`.
For `|A|<=B`, evaluation at `A/B` gives
`max(|F|,|G|)>=R_1 B^4/K_1`; for `B<=|A|`, the other chart gives
`max(|F|,|G|)>=R_2 |A|^4/K_2`.

Homogenizing the identities shows that `gcd(F,G)` divides both
`R_1 B^d` and `R_2 A^e` for suitable positive integers `d,e`. Since `A,B`
are coprime, it divides `lcm(R_1,R_2)`, hence is at most `R_1 R_2`.
Consequently the reduced image has height at least
`4h(A/B)-log(K)`, where `K=max(K_1 R_2,K_2 R_1)`.
The coefficient sums also give the upper bound
`4h(A/B)+log(C)`, where
`C=max((1+|b|)^2,4(1+|a|+|b|))`.

With `D=max(C,K)` and `B=ceil(log(D)/3)`, telescoping the duplication formula
proves `|H(P)-h(x(P))|<=B` for every rational point, including torsion and
infinity. The symbol `B` in the code denotes this height-difference integer,
not David's parameter below.

Exact doubling gives enclosures
`H(P_i) in 4^-n h(x(2^n P_i)) + [-B/4^n,B/4^n]`.
Polarizing these enclosures gives a matrix containing the full canonical
height pairing. Interval LDL decomposition of `matrix-lambda*I` proves
positive definiteness for the recorded positive rational `lambda`.
Thus, for `P=sum m_i P_i+T` and `M=max |m_i|`,

\[
 H(P)\ge\lambda\sum m_i^2\ge\lambda M^2.
\]

Floating-point eigenvalues only propose `lambda`; they never certify it.

## Elliptic integral upper bound and the finite small region

Put `s=x+b_2/12`. The short Weierstrass equation is
`Y^2=4(s-e_1)(s-e_2)(s-e_3)`. Exact algebraic numbers define its three
roots. For the largest real root `e_1`, Carlson's identity gives

\[
 |u(P)|=R_F(s-e_1,s-e_2,s-e_3),\quad
 w=2R_F(0,e_1-e_2,e_1-e_3).
\]

The formula for `u` is used only on the identity component. The code uses
`2P_i`, which always belongs to that component; the sign is determined by
`2y+a_1x+a_3`. Arb encloses these integrals. In the negative-discriminant
case, the lattice area is
`w*Re(R_F(0,e_2-e_1,e_3-e_1))`; it is the product of the real period and
the imaginary part of the other period. This also follows by integrating
along the real axis to the left of the real root. All Hai–Walsh curves have
negative discriminant. The positive-discriminant case is implemented by the
usual real complementary Carlson integral, but is not needed for this
classification.

Let `R` be a certified upper bound on all `|e_i|`,
`z=max(2R,|b_2/12|,1)`. If `s<=z`, then the lab's `x>=0` gives
`0<=x<=z+|b_2/12|`. The entire recorded integer interval is searched exactly;
no coefficient bound is required for those points.

For `s>z`, each `|t-e_i|>=t/2` for `t>=s`, so the defining elliptic integral
gives `|u(P)|<=2sqrt(2)/sqrt(s)`. Since `x<=2s`, the height comparison yields

\[
 |2u(P)|\le K\exp(-\lambda M^2/2),\qquad
 \log K=\log(4\sqrt2)+(B+\log2)/2.
\]

## A conservative initial bound directly from David

The source is Sinnou David, *Minorations de formes linéaires de logarithmes
elliptiques*, Mémoires SMF 62 (1995), Theorem 2.1, printed pp.9–10:
https://smf.emath.fr/system/files/filepdf/MSMF_1995_2_62__1_0.pdf
The theorem and its normalization were inspected in the original scan, saved
as `sources/david1995.pdf` and `sources/david-theorem.png`.

Apply it over the rational numbers (`D=1`) to the `r` real logarithms of
`2P_i` and to the real period, viewed as a logarithm of the origin; put
`k=r+1`. Clear torsion by its exponent `e` in the nonzero form `e*2u(P)`.
The integer coefficients have absolute values at most `e(r+2)M` for `M>=1`:
the centered generator logarithms have size at most `w/2`, while
`|2u(P)|<=w`, and torsion only changes the rational period coefficient.

Choose an integer `h>=max(1,h(1,g_2,g_3),h(j))`, and a common
`log(V_i)=A`, with

\[
 A\ge\max(1,h,3\pi w^2/\operatorname{area}(L),8H(P_i)).
\]

These are all David's height and analytic requirements. The canonical
projective height of `2P_i` in the cubic embedding is `6H(P_i)`, so the
factor 8 is an enlargement. All logarithms, including the period, have
absolute value at most `w`. The expression
`|omega_1|^2 Im(tau)=area(L)` is invariant under a change of period basis;
this avoids the period-order convention error reported for Smart/Cohen.
David's auxiliary `E` can be Euler's number.

For `s=log(M)`, take
`beta=s+A+3h+ceil(log(e(r+2)))`. It majorizes the necessary `log(B_David)`
and makes `log(B_David)>=A` and `>=Euler_e*h`. Replace
`log(log(B_David))` by the larger `beta`. The integer

\[
 C_*=3\,10^{6k+12}4^{2(k+1)^2}(k+2)^{2k^2+13k+30}
\]

exceeds David's printed constant
`2.9*10^6*10^(6k)*4^(2k^2)*(k+1)^(2k^2+9k+12.3)`.
It follows, with still more harmless enlargement, that

\[
 \log|2u(P)|>
 -C_*A^k(\beta+1)(\beta+h+1)^{k+1}-\log e.
\]

The program doubles an integer exponent `p` until Arb proves, at `M=10^p`,
that `lambda*M^2/2` exceeds this negative-bound magnitude plus `log(K)`.
The same exclusion holds for every larger `M`: the logarithmic derivative
of the polynomial in `log M` is at most `(k+2)/beta<2`, while that of
`M^2` is 2. The additional check `2*log(M)>k+2` is recorded; `beta>log M`.
Thus `N=10^p`, enlarged if needed, is a valid initial coefficient bound.

## Certified lattice reductions

Let `ell_i=u(2P_i)/w`. At an integer scale `C` the row lattice has an
identity block, last entries `round(C ell_i)`, and final row `(0,...,0,C)`.
The last period entry is exact. Arb supplies rational upper bounds
`epsilon_i>=|C ell_i-round(C ell_i)|`.

For an integral point with `|m_i|<=N`, clearing torsion gives the lattice
vector with first coordinates `e*m_i` and last coordinate approximating
`e*C*2u(P)/w`, with error at most `e*N*sum epsilon_i`.
The vector is nonzero unless all free coefficients vanish; those torsion
points are handled explicitly. Exact rational Gram–Schmidt gives

\[
 \delta=\min_i\|b_i^*\|^2\le\lambda_1(L)^2.
\]

Indeed, the last nonzero integer coefficient of a lattice vector in this
basis contributes at least the squared length of that orthogonal vector.
This bound does not require trusting LLL's reducedness: any independent
integer basis works. LLL only makes the estimate useful.

Only after the exact inequality

\[
 \delta>e^2\big(rN^2+(N\sum\epsilon_i)^2\big)
\]

and the Arb positivity check pass do we obtain

\[
 \left|2u(P)/w\right|\ge
 \frac{\sqrt{\delta/e^2-rN^2}-N\sum\epsilon_i}{C}>0.
\]

Combining with the preceding exponential upper bound gives the new
coefficient bound, rounded upwards using Arb. Failed inequalities enlarge
the scale by 16 and recompute the enclosures at at least `nbits(C)+96` bits.
Both inner and outer loops have caps and raise on failure.

The proof then consists of an exact finite coefficient-box enumeration,
both torsion translates and both signs, plus the exact small-coordinate
interval. No final real-arithmetic integrality sieve is trusted.

## Attribution and limits

The Carlson formulas, doubling-based height enclosures, and normalized
lattice design were informed by Manvir Jaswal's GPL PR #43044, pinned head
`9be54a7fd40ae95a495d91580434bd2aedf0faff`. That PR is unmerged and the report
does not treat its author or its claimed tests as authority. The implementation
here independently derives its height-difference estimate from Bezout
identities, uses only an exact Gram–Schmidt lower bound, exposes the
inequalities, and uses the previously audited standard-library finite checker.
Alex should obtain independent human review of this proof and implementation
before relying on or publishing the classification.
