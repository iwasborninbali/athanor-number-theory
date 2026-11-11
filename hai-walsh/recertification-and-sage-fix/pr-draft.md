# Draft for Alex — do not submit before human review

**Suggested title:** Require the lattice inequality in rational integral-point reduction

This is material for a human contribution or review on the existing work;
nothing has been posted. The exact defect and the scale remedy were already
identified by John Cremona in [#10973, comment:45 (2013)](https://github.com/sagemath/sage/issues/10973#issuecomment-1417380642).
The related open issue is [#27015](https://github.com/sagemath/sage/issues/27015),
and [PR #43044](https://github.com/sagemath/sage/pull/43044) already proposes
a broader replacement. Coordinate with that work; do not claim a new discovery.

## Proposed description

`EllipticCurve_rational_field.integral_points()` replaces a failed lattice
lower bound by `10*T^2*Q` and then uses it to shrink the coefficient search
box. That number need not be a lower bound for the actual lattice. On
2082a1, Sage 10.9 returns coefficient bound 12 and omits the integral point
with x-coordinate 507525709, which is a thirteenth multiple of a generator.
On 1701d1, bound 6 omits the seventh multiple with x-coordinate 20829482.

This patch retries at larger integer scales and working precision, rebuilding
the lattice each time. It uses the minimum exact squared Gram–Schmidt length
as the lattice lower bound and tests strict positivity before reducing the
coefficient bound. Arb enclosures account for the rounding errors of normalized
real logarithms. An exact period column and the torsion exponent handle the
rational torsion offset. Sixteen unsuccessful attempts raise `RuntimeError`
before the finite search. The initial power of ten is retained as an integer
at the successful endpoint of the existing binary search.

The existing verbose doctest is updated for the changed bound, and regression
doctests exercise both missing points. There is no change to the public API,
basis discovery or saturation policy.

## Validation

The final counts, timings, source hashes and raw transcripts are in the
accompanying `result.md` and `evidence/` directory. All 27 long doctests pass,
including the bounded-enumeration helper's Zagier examples. All 317 ecdata
comparisons pass (306 curves of conductor at most 100 and all 11 curves in
#27015), as do three LMFDB full point-list comparisons and the lab's 179
accepted curves. The installed method still misses the 12 x-coordinates
listed in #27015; the patched method matches the saved tables. Fault-injection
tests confirm both a failed inequality and exact equality exhaust the retry
cap and raise before enumeration.

The patch is against Sage develop commit
`026e931e47064f0a7fc095580119365518bfe7c0` (11.0.beta6). The copied method
is tested in Sage 10.9 without modifying the installed package. A full
Sage 11.0 build and full-tree doctest run have not been performed.

## Scope for reviewers

This is a focused repair of the lattice reduction. It does **not** claim
that every remaining constant in the legacy David/Smart/Cohen initial-bound
calculation, or its final floating-point enumeration, is certified. The
separate lab certificate uses David's original theorem, exact duplication
identities, Arb and exact rational exhaustion. Its proof and implementation
are supplied for independent review in `certificate-proof.md`.

`S_integral_points` contains the same fallback at both real and p-adic places.
Those sites are not changed by `fix.patch`. The accompanying optional
`s-integral-fail-closed.patch`, applied after `fix.patch`, replaces the two
assignments by errors and corrects their squared Gram–Schmidt bound. It is
an interim safeguard, not a completed S-integral algorithm repair.

## Attribution and disclosure

The analysis, patch and tests were prepared with OpenAI Codex AI assistance.
The human submitter must review and take responsibility for the submitted
code and claims. The normalized Carlson/Arb approach was informed by Manvir
Jaswal's GPL implementation in PR #43044, head
`9be54a7fd40ae95a495d91580434bd2aedf0faff`; the independent certificate
also acknowledges that work. The prior reports by John Cremona must be
credited. No novelty claim is intended.
