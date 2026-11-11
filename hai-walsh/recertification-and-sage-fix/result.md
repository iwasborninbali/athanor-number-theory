# Sage integral-point soundness repair and Hai–Walsh re-certification

2026-11-11. Work began at 01:26 UTC; the final report was prepared at approximately
02:10 UTC. All mathematical computation used the specified VM, CPU 1, niceness
19, and single-thread settings. No installed Sage files were edited, packages
installed, paid services called, or issues, PRs, comments or messages posted.

**Outcome.** The audit is correct. Current Sage `develop` still contains the
unjustified substitution. It can cause actual omissions: fresh Sage 10.9 runs
reproduce all **12 missing x-coordinates on the 11 curves** listed in #27015.
The focused repair passes all requested tests. A separate, explicitly derived
certificate re-certifies **all 179 accepted Hai–Walsh integral-point lists**:
1,161 affine points, no changes, and the same fourteen quartic solutions.
Together with the eighteen exact congruence exclusions, the classification is
complete for the 197 covered quartics; **only the plus fibres 73, 91 and 97
remain unresolved** in this work. The proof dependencies and limits below
are part of that statement.

## Confirmation against upstream and prior reports

The checked `develop` commit is
[`026e931e47064f0a7fc095580119365518bfe7c0`](https://github.com/sagemath/sage/commit/026e931e47064f0a7fc095580119365518bfe7c0),
Sage 11.0.beta6, dated 2026-11-08. Its
[`integral_points` lines 6117–6119](https://github.com/sagemath/sage/blob/026e931e47064f0a7fc095580119365518bfe7c0/src/sage/schemes/elliptic_curves/ell_rational_field.py#L6117)
contain the same assignment as the installed Sage 10.9. Both copies are saved
under `sources/`; the separately fetched develop and pinned files matched
byte-for-byte. Fresh execution of that pinned method reproduced the bad branch
on **all 144 positive-rank lab curves**, with exact lattice-membership and
short-vector checks; the 35 rank-zero cases bypass it. See
[upstream-bound-audit.jsonl](evidence/upstream-bound-audit.jsonl).
The same assignment occurs in `S_integral_points` at the
[finite-place reduction](https://github.com/sagemath/sage/blob/026e931e47064f0a7fc095580119365518bfe7c0/src/sage/schemes/elliptic_curves/ell_rational_field.py#L6440)
and [real-place reduction](https://github.com/sagemath/sage/blob/026e931e47064f0a7fc095580119365518bfe7c0/src/sage/schemes/elliptic_curves/ell_rational_field.py#L6785).

This is **not a new discovery**. John Cremona identified this exact failed
inequality and unjustified adjustment in
[#10973, comment:45, 2013-09-06](https://github.com/sagemath/sage/issues/10973#issuecomment-1417380642),
including the 2082a1 omission and the remedy of increasing the scale.
[#10152](https://github.com/sagemath/sage/issues/10152) had reported the missing
point in 2010; [#27015](https://github.com/sagemath/sage/issues/27015) lists the
eleven problematic curves. The migrated GitHub comments preserve the old Trac
discussion; direct Trac access was unavailable.

There is also an existing, unmerged
[PR #43044 by Manvir Jaswal](https://github.com/sagemath/sage/pull/43044), opened
2026-10-24, which explicitly addresses this fallback and broader certification
problems. Its checked head is `9be54a7fd40ae95a495d91580434bd2aedf0faff`.
Cremona's 2026-11-10 review asks for a narrower revision that separates basis
discovery from bounds/enumeration. That PR informed the Carlson/Arb approach
here and is credited; it was neither installed nor treated as an accepted proof.

Indexed sage-devel searches found the original method discussions but no
additional exact-fallback report. The related
[sage-support discussion from 2016](https://groups.google.com/g/sage-support/c/pHr3prSdVpk)
also identifies final-search precision failures and a Smart/David period-order
error. Search scope, URLs, downloads and retrieval failures are recorded in
[search-notes.md](sources/search-notes.md) and [retrieval.json](evidence/retrieval.json).

## What the reduction lemma requires

Let a candidate produce a nonzero lattice vector relative to a target `y`.
Its first coordinates have squared norm at most `Q`; its last coordinate
approximates `C*Lambda` with error at most `T`. If `delta` is a **proved lower
bound** for the relevant squared lattice distance, then

\[
 \delta\le Q+(C|\Lambda|+T)^2,
 \qquad |\Lambda|\ge\frac{\sqrt{\delta-Q}-T}{C}.
\]

For `y` outside the lattice the distance is the usual nearest-point distance.
For `y=0` it means the shortest **nonzero** vector length; the zero vector
must be excluded. The lower bound is useful only after proving
`delta > T^2+Q`. Combining it with the exponential elliptic-logarithm upper
bound then reduces the coefficient box. This is the de Weger/Smart mechanism;
an explicit primary example is [Stroeker–de Weger (1999), pp.354–355](https://deweger.net/papers/%5B29%5DStdW-EllCubic-ActaArith%5B1999%5D.pdf).

Replacing `delta` by a larger number proves nothing about the lattice and
can incorrectly exclude a point. Scale growth changes the actual lattice;
precision must grow with the scale so that its rounding errors are controlled.

There is a second problem in the old expression: it divides a squared length
by a ratio of lengths. The 0.99-LLL-reduced integer basis

\[
 \begin{pmatrix}2000&0&0\\1000&1722&0\\0&861&1484\end{pmatrix}
\]

has squared Gram–Schmidt lengths `4000000, 2965284, 2202256`. The old
expression gives `2968000`, but its third row has squared norm `2943577`.
Thus that expression is not a general lattice lower bound. The replacement
uses `min ||b_i^*||^2` exactly: the last nonzero integer coefficient of any
lattice vector proves this lower bound. [guards.log](evidence/guards.log)
contains the exact counterexample check.

## Actual impact

The installed Sage 10.9 still misses the following x-coordinates when given
the same bases used in the patched comparison:

| Cremona curve | Old bound | Patched bound | Missing x-coordinates in Sage 10.9 |
|---|---:|---:|---|
| 1701d1 | 6 | 9 | 20829482 |
| 1848f1 | 12 | 18 | 176, 179 |
| 2082a1 | 12 | 18 | 507525709 |
| 3510n1 | 16 | 23 | 40498647 |
| 6514b1 | 6 | 9 | 2201303312 |
| 177211a1 | 3 | 5 | 531603 |
| 23808e1 | 6 | 9 | 22259471153 |
| 268740c1 | 4 | 6 | 34012368 |
| 285928a1 | 3 | 4 | 592473667 |
| 66432f1 | 3 | 4 | 2981089 |
| 92554e1 | 16 | 23 | 74833788396 |

On 1701d1, `P=(2,-2)` has integral `7P`, with x-coordinate 20829482; bound 6
excludes it. On 2082a1, `P=(13,29)` has integral `13P`, with x-coordinate
507525709; bound 12 excludes it. These demonstrate actual loss through an
insufficient coefficient bound, not merely an unexecuted proof gap.

Not every omission above should be attributed to the fallback alone.
For example, on 1848f1 the missing points are fifth and sixth multiples,
already inside the old coefficient bound 12. This exposes the separate
floating-point final-enumeration defect. The repaired bound also increases
the precision selected by that legacy search and recovers these examples,
but does not prove that the legacy numerical enumeration is universally safe.

The patched results match all **317** saved Cremona ecdata lists: 306 curves
of conductor at most 100, plus the eleven above. Full affine point sets,
including both signs, also match the LMFDB pages for
[1701d1](https://www.lmfdb.org/EllipticCurve/Q/1701d1),
[1848f1](https://www.lmfdb.org/EllipticCurve/Q/1848f1), and
[2082a1](https://www.lmfdb.org/EllipticCurve/Q/2082/a/1).
The redirects matter: Cremona and LMFDB isogeny letters need not agree.
Evidence: [baseline-known11.jsonl](evidence/baseline-known11.jsonl),
[crosscheck.jsonl](evidence/crosscheck.jsonl), and the hashed source snapshots.

For nonempty `S`, instrumented installed `S_integral_points([2])` reaches
the same invalid real-place fallback on the y=4 minus curve and on 2082a1.
The first example compares approximately `8.66e9` with `5.11e185` and would
substitute `6.11e371`. See [s-integral-audit-final.jsonl](evidence/s-integral-audit-final.jsonl).
No S-integral missing-point example or full S-integral certification is claimed.

## Repair and validation

[fix.patch](fix.patch) changes only the rational integral-point method and
its doctests. It normalizes centered real logarithms by the real period,
clears torsion with its exponent, and uses an exact integer period column.
Arb encloses the logarithms and their individual rounding errors. If the
rounded entries approximate `C*e*u(P_i)/w` with errors `epsilon_i`, the
candidate has `Q=rH^2`, `T=H*sum(epsilon_i)`, and the lower logarithm bound is

\[
 |u(P)|\ge\frac{w}{eC}\left(\sqrt{\delta-Q}-T\right).
\]

The free-basis signs may be changed when centering without changing the
absolute coefficient box. The torsion term becomes an integer period offset.
Exact squared Gram–Schmidt lengths and a strict rational inequality establish
the hypothesis before this formula is used. Failed attempts multiply the
integer scale by ten, increase precision and rebuild. After sixteen failures
the method raises `RuntimeError` before enumeration. The existing initial
power of ten is also made an integer at the successful binary-search endpoint.

| Check | Result |
|---|---|
| Apply patch to pinned develop source; compare resulting bytes | PASS |
| Sage function/helper doctests, including long rank-five and Zagier examples | **27 tests, PASS** |
| Failed inequality and exact equality | **16 retries, then error; no enumeration** |
| Exact Gram–Schmidt counterexample | PASS |
| Cremona ecdata | **317/317 complete-list matches** |
| LMFDB full affine point lists | **3/3 matches** |
| Patched legacy procedure on lab curves | **179/179 matches** |
| Fresh full saturation | **144/144 index 1; no unsaturated primes** |
| Independent certified coefficient bounds | **179/179 successful** |
| Exact certificate replay: lattice membership, unimodularity, GS lengths, hypotheses | **454 reductions checked** |
| Exact torsion verification by good reductions | **179/179 order 2** |
| Independent exact finite exhaustion | **1,848,523 combinations; all 179 lists match** |
| Arb geometry versus independent 512-bit Sage/PARI AGM calculations | **179/179 pass** |

The final doctest run took 352.7 s wall / 204.7 s CPU; the 317-curve
cross-check took 56.4 s wall, and the final patched 179-curve run took 115.9 s
wall. More conservative coefficient boxes can increase runtime. The first
doctest iteration failed only the old hard-coded verbose bound; the updated
expectation and all final tests pass. Full transcripts and the asserted
CPU/niceness settings are in [suite.jsonl](evidence/suite.jsonl),
[doctests-final.log](evidence/doctests-final.log),
[patched-all.log](evidence/patched-all.log), and
[lattice-certificates.log](evidence/lattice-certificates.log).

Testing used the copied develop method in Sage **10.9**, as authorized,
without modifying the installation. A full Sage 11.0 build and whole-tree
doctest run were not performed. Nonempty `S_integral_points` is unchanged by
the main patch. The optional [s-integral-fail-closed.patch](s-integral-fail-closed.patch),
applied after it, replaces the two bad S-integral assignments by errors and
uses the exact squared GS bound; it is an interim safeguard, not a full
real/p-adic S-integral repair.

## Hai–Walsh re-certification

The focused patch alone is **not** a certificate for every legacy constant
or the floating-point final search. To close the lab's gap, the independent
procedure in [certified_bounds.py](scripts/certified_bounds.py) instead uses:

1. Exact polynomial Bezout identities for the duplication map to prove a
   global canonical/naive-height difference bound.
2. Exact doubling and Arb enclosures for the height matrix, with a positive
   rational eigenvalue lower bound certified by interval LDL.
3. David's **original** 1995 Theorem 2.1, conservatively specialized and
   majorized, avoiding the reported Smart/Cohen period convention problem.
4. Arb Carlson integrals, exact lattice bounds, and proved positive reduction
   inequalities, with capped retries.
5. The previously audited standard-library checker to exhaust the complete
   remaining coefficient boxes and small-coordinate intervals, using exact
   rational group arithmetic and both torsion translates.

The complete derivation is [certificate-proof.md](certificate-proof.md).
The exact bound generation took 31.9 s summed wall time. Exact exhaustion
took 765.1 s summed wall time while sharing core 1 with other checks; the
rank-five y=100 minus box accounts for 1,419,857 combinations. There are
454 accepted lattice reductions and 675 failed scale attempts that were
properly retried. Saved lattice certificates were checked independently with
standard-library rational arithmetic. An additional comparison with Sage/PARI
AGM periods and logarithms verifies normalization, but is a diagnostic rather
than the proof of the Arb enclosures.

The requested examples, all with unchanged affine point lists, are:

| y | Sign | Rank | Old bound | Patched legacy bound | Independently certified box bound | Affine points |
|---:|:---:|---:|---:|---:|---:|---:|
| 4 | − | 3 | 6 | 7 | 8 | 29 |
| 4 | + | 1 | 3 | 3 | 4 | 3 |
| 25 | − | 3 | 5 | 6 | 7 | 23 |
| 25 | + | 3 | 3 | 4 | 4 | 5 |
| 93 | − | 4 | 5 | 6 | 8 | 19 |
| 93 | + | 0 | 0 | 0 | 0 | 1 |
| 100 | − | 5 | 5 | 7 | 8 | 29 |
| 100 | + | 2 | 3 | 3 | 4 | 3 |

The certified box is accompanied by a separately exhausted small-x interval.
Its larger bound is compatible with the same point list. Across the final
patched calls, 111 bounds increase and 68 stay unchanged, including the
35 rank-zero cases; none decrease. Every curve's before/after values are in
[bounds-comparison.csv](certificates/bounds-comparison.csv).

The original proved PARI rank upper bounds are retained and their raw records
checked for consistency; a new PARI descent was not run. All 144 positive-rank
supplied bases passed fresh full eclib saturation with index 1 and success,
and exact unimodular changes to the enumeration bases were verified.
The quadratic descent path's unconditional status is documented in the
[independent audit](../../stalled-solve/a04-verify/verify.md).

**Classification.** For integers `1<=y<=100`, `x>1`, `z>0` and `s=±1`, the
covered equations

\[
 x^2-1=(y^2+1)(z^2+s)^2
\]

have precisely the thirteen family members
`y=(z^2+s)/2`, `x=2y^2+1`, with odd `z` and `1<=y<=100`, and the known
exception `(x,y,z,s)=(2177,4,23,-1)`. There is no new exceptional solution.
All minus fibres are covered. The plus fibres 73, 91 and 97 remain open;
no nonexistence claim is made for them. The eighteen additional plus quartics
are excluded exactly modulo 3 or 8; this does not certify the entire integral
point lists of those eighteen elliptic curves.

The original completeness defect is therefore closed **for this classification
under the explicit software/proof dependencies**: original unconditional PARI
rank bounds, fresh eclib saturation, exact algebraic roots and rational
arithmetic, Arb enclosures, and the stated specialization of David's theorem.
This is not a proof-assistant formalization or an independent human review
of the new implementation. It is also not a universal certification of the
remaining legacy Sage algorithm. The general parametric Hai–Walsh problem
is not settled here.

## Deliverables and reproduction

- [fix.patch](fix.patch): focused patch against the pinned develop commit.
- [pr-draft.md](pr-draft.md): human submission/review material, with AI
  disclosure and attribution to the existing reports and PR.
- [explanation.md](explanation.md): plain-English explanation.
- [classification-recertified.json](certificates/classification-recertified.json)
  and [summary](certificates/recertification-summary.json): all 200 curve
  dispositions, the 179 re-certified lists and fourteen solutions.
- [certificate-proof.md](certificate-proof.md), [reproduce.md](reproduce.md),
  and [progress.md](progress.md): proof, executable reproduction instructions
  and progress record. `SHA256SUMS` identifies the saved inputs and outputs.

The original lab and audit artifacts are preserved. This folder supplies the
new completion record. No upstream submission has been made; the Guide and
Alex decide what to submit after independent review. The work was prepared
with OpenAI Codex AI assistance, with the GPL Carlson/Arb design in Jaswal's
existing PR explicitly acknowledged.
