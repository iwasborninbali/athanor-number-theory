# Sage integral-point soundness repair

Started 2026-11-11 01:26 UTC. Six-hour limit: approximately 07:26 UTC.

## 01:30 UTC — initial audit and upstream confirmation

Read the independent verification report in full, the extracted installed
`integral_points`, `audit_bound.py`, and the high-precision diagnostic. Read the
Hai–Walsh report and located the 179 accepted curve records and exact checker.
The current upstream `develop` source contains the same unjustified assignment
in `integral_points`, the real reduction in `S_integral_points`, and its p-adic
reduction. The Gram–Schmidt denominator also needs checking: the source divides
by a ratio of lengths, although squared lengths are required.

Initial VM inspection and three baseline runs used
CPU 1, niceness 19 and single-thread environment settings, in `~/sage-intpts`.
The installed Sage environment will remain unchanged. No publications,
installations, paid calls or messages are authorized or used.

Upstream is pinned to `026e931e47064f0a7fc095580119365518bfe7c0`
(11.0.beta6, 2026-11-08). Baseline Sage 10.9 misses the known integral
seventh multiple on 1701d1 and thirteenth multiple on 2082a1.
An exact prior report is John Cremona's 2013-09-06 comment on #10973:
https://github.com/sagemath/sage/issues/10973#issuecomment-1417380642
It identifies the failed inequality, arbitrary adjustment and scale repair.
Open PR #43044 (2026-10-24) also addresses this explicitly; its latest head
is saved for read-only comparison. Other known issues concern David's initial
bound and the final floating-point enumeration, so a local fallback repair
alone cannot automatically certify the whole algorithm.

Next: implement scale/precision retries with an actual lattice lower bound;
test separately from any broader certificate, with explicit attribution to
prior work.

## 01:50 UTC — repair and certificate tests in progress

The first scale/precision repair recovers the known omissions on 1701d1,
2082a1 and 1848f1. The focused patch was then strengthened to use Arb
enclosures for normalized logarithms, an exact period column, the torsion
exponent, and the minimum exact squared Gram–Schmidt length. A separate
optional patch makes the two S-integral fallback sites fail closed; it is
not a claimed repair of the p-adic algorithm.

Independent bounds have succeeded for all 179 accepted lab curves (144
positive rank, 35 rank zero), using exact duplication-map Bezout identities,
Arb, and David's original theorem instead of the legacy initial bound.
The exact finite checker has matched the first 177 lists; the rank-five
case is still running. Fresh full saturation succeeded for all 144 supplied
positive-rank bases with index 1; the rank-zero cases are retained from the
certified descent records.

The first long-doctest run passed all mathematical outputs but failed the
hard-coded verbose bound line, which necessarily changed. The final suite
uses an updated verbose expectation and adds regression examples. It also
tests the iteration cap, equality failure, 317 ecdata curves (including all
11 listed in #27015), three exact LMFDB point lists, and all 179 patched
function calls. The certificate proof is written in `certificate-proof.md`.

All mathematical computation remains on VM CPU 1 at niceness 19; installed
Sage is unchanged. Current elapsed wall time is about 24 minutes.

## 02:10 UTC — completed

All final tests pass: 27 long doctests, 317 ecdata lists, three full LMFDB
lists, all 179 patched lab calls, 454 exact lattice-certificate checks and
179 exact torsion checks. Fresh baseline tests reproduce the twelve missing
x-coordinates on all eleven historical counterexamples. A fresh execution of
the pinned current upstream method reproduces the invalid fallback and exact
counterwitness on all 144 positive-rank lab curves. Nonempty S-integral calls
also execute the invalid real fallback in two supplied-basis examples.

The independent certificate exhausts 1,848,523 MW combinations and the complete
small-coordinate intervals. All 179 point lists match, with 1,161 affine
points and the same fourteen recovered solutions. Fresh full saturation has
index 1 on every positive-rank supplied basis. Eighteen direct congruence
exclusions are checked again; only plus fibres 73, 91 and 97 remain open.

Deliverables: `result.md`, `fix.patch`, `pr-draft.md`, `explanation.md`,
`certificate-proof.md`, `reproduce.md`, and `certificates/`. The optional
S-integral guard is explicitly separate from a full S-integral repair.
Original lab/audit files and installed Sage are unchanged. No research
process remains on the VM. Elapsed time is about 44 minutes, within the
six-hour limit. Final artifact integrity checks are recorded in
`evidence/integrity.json`.
