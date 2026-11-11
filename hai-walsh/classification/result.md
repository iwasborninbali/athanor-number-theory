# Certified fixed-parameter Hai–Walsh classification

## Established statement

For every integer

\[
1\le y\le100,\qquad y\notin\{73,91,97\},
\]

the complete set of solutions with **unbounded** integers \(x>1,z>0\) to

\[
x^2-1=(y^2+1)(z^2+s)^2,\qquad s\in\{-1,+1\},
\]

is the following table. The minus-sign equation is classified for **all** \(1\le y\le100\), including the three omitted values; it has no solutions at those three values. The plus-sign equations at \(y=73,91,97\) remain open in this work.

| \(x\) | \(y\) | \(z\) | \(s\) | Identification |
|---:|---:|---:|:---:|---|
| 3 | 1 | 1 | + | Known family's endpoint |
| 33 | 4 | 3 | − | Known family |
| 2177 | 4 | 23 | − | Previously known exception |
| 51 | 5 | 3 | + | Known family |
| 289 | 12 | 5 | − | Known family |
| 339 | 13 | 5 | + | Known family |
| 1153 | 24 | 7 | − | Known family |
| 1251 | 25 | 7 | + | Known family |
| 3201 | 40 | 9 | − | Known family |
| 3363 | 41 | 9 | + | Known family |
| 7201 | 60 | 11 | − | Known family |
| 7443 | 61 | 11 | + | Known family |
| 14113 | 84 | 13 | − | Known family |
| 14451 | 85 | 13 | + | Known family |

Here the family is \(z^2+s=2y,\ x=2y^2+1\), with odd positive \(z\). There are thirteen family members and one previously known exception in the table. **No new exceptional triple is claimed.** Novelty of this fixed-fibre computation has not been established by the limited literature search.

The classification uses standard certified PARI/eclib/Sage algorithms, with no GRH or BSD assumption. Its independent Python checker verifies the exact arithmetic and the entire final finite search. Rank upper bounds, saturation-index bounds and elliptic-logarithm bounds are explicit trusted software proof dependencies; this is not a standalone formal proof of those algorithms or their real-number estimates.

## The priority case \(y=4\)

With \(D=17\), the two curves are

\[
E_-:V^2=U^3-34U^2+306U,\qquad
E_+:V^2=U^3+34U^2+306U.
\]

PARI 2.19 proves ranks **3** and **1**, respectively. The rational and quadratic fields in each descent were certified by `bnfcertify(bnfinit(field,1))=1`; the quadratic field has discriminant \(-68\) and class number 4. Full saturation gives the following bases modulo the torsion point \((0,0)\):

- \(E_-\): \((2,22),(9,27),(18,18)\).
- \(E_+\): \((72,756)\).

The complete integral points, recorded up to changing the sign of \(V\), are:

| Curve | \((U,|V|)\) |
|---|---|
| \(E_-\) | \((0,0),(2,22),(8,28),(9,27),(17,17),(18,18),(25,45),(32,88),(34,102),(72,468),(153,1683),(338,5902),(1224,42228),(3042,166842),(8993,851207)\) |
| \(E_+\) | \((0,0),(72,756)\) |

Thus there are 29 and 3 affine integral points when both signs are included. Applying the inverse-map tests gives exactly

\[
(x,z)=(33,3),(2177,23)\quad(s=-1),
\]

and no plus-sign solution. This conclusion has no height cutoff on \(x\) or \(z\).

## Reduction and completeness argument

Put \(D=y^2+1\). Every solution maps to an integral point

\[
U=Dz^2,\qquad V=Dxz,
\]

on

\[
E_{D,s}:V^2=U^3+2sDU^2+D(D+1)U.
\]

Its discriminant is \(-64D^3(D+1)^2\ne0\). In fact the cubic is
\(U((U+sD)^2+D)\); it is negative for \(U<0\), and has just one real root, at zero.

Conversely, for every recorded integral point, require \(U>0,V>0\), \(D\mid U\), and \(U/D=z^2\) for a positive integer \(z\). Require \(Dz\mid V\), set \(x=V/(Dz)\), and retain only \(x>1\). Substitution gives the original equation. These tests are both necessary and sufficient. The checker applies them to every point, without a bound on the recovered variables.

The exceptional cases lose no permitted solution:

- The point at infinity is not the image of finite \(x,z\).
- \(U=0\) forces \(V=0,z=0\), outside the domain. Even allowing \(z=0\) in the original quartic would require \(x^2=y^2+2\), strictly between consecutive squares for \(y\ge1\).
- For \(z=1,s=-1\), \(x=1\), which is excluded; these points are discarded explicitly.
- For \(z=1,s=+1\), \((x-2y)(x+2y)=5\), giving exactly \((x,y)=(3,1)\).
- Negative \(x,z,V\) introduce no additional positive-domain solutions; both signs of every integral \(V\) were retained before filtering.

For **179 curves**, the computation supplies a proved rank, a full saturated basis, and Sage's complete `integral_points(mw_base=basis, both_signs=True)` output. PARI `ellrankinit`/`ellrank` supplies the upper bound; eclib confirms that the supplied independent points have that rank and saturates at every necessary prime, using `max_prime=-1`. The success flag and unsaturated-prime list are checked explicitly, rather than trusting only Sage's wrapper, which can print a saturation failure without raising an exception.

All these curves have a rational 2-torsion point. PARI 2.19 uses its unconditional rational/quadratic Selmer routines here, rather than the cubic-field class-group path. We nevertheless computed and fully certified the class-group data for both factors of each descent algebra. The saved PARI source documents this distinction; the certifications are not a claim that the quadratic descent consumes an uncertified `bnf` object.

Sage uses elliptic logarithms and LLL to bound the coefficients of integral points in a changed MW basis, plus a finite small-\(U\) interval. The certificate records that basis, an exact unimodular change matrix, the final coefficient bound and the interval. The **independent checker**, using only `fractions`, integer arithmetic and other Python standard-library modules, enumerates every combination in each entire coefficient box, adds both rational torsion points, and exhausts every small-\(U\) interval. It reproduces every one of the 179 integral-point lists exactly. This also independently checks the final finite enumeration, which Sage accelerates using floating-point approximations. There are **240,881 exact MW combinations** across the lists. The checker separately proves that the rational torsion group has order 2 by counting points over small good primes and taking the gcd of their group orders.

For **18 additional plus-sign quartics**, a complete residue-class exclusion avoids an incomplete elliptic basis computation:

- If \(y\) is even, modulo 8, an even \(z\) makes \(x^2\equiv2\) or \(6\), and an odd \(z\) makes \(x^2\equiv5\). All are impossible.
- If \(3\mid y\), modulo 3 one has \((z^2+1)^2\equiv1\) and \(x^2\equiv2\), also impossible.

The affected values are \(27,38,39,45,46,48,52,56,57,60,62,80,81,84,87,92,94,99\). The checker tests every residue class for each certificate. These are complete exclusions of the **original quartics**. The associated elliptic-curve integral-point problems remain uncertified here; no full MW-basis or complete integral-point claim is made for those 18 curves. Consequently, 79 values of \(y\) have both curves completed by the elliptic method, and another 18 have a complete fixed-\(y\) classification using the direct congruence proof for the plus sign.

## What remains open

| \(y\) | Sign | \(D\) | Certified rank bounds | Obstruction |
|---:|:---:|---:|:---:|---|
| 73 | + | 5330 | [0,2] | Rank unresolved; no full basis/integral list |
| 91 | + | 8282 | [0,1] | PARI reports [1,1] but returns no point; we use only the witnessed lower bound 0 and certified upper bound 1; full basis unavailable |
| 97 | + | 9410 | [0,2] | Rank unresolved; no full basis/integral list |

No completeness or negative-solution claim is made for these three plus equations. Increasing local PARI point-search effort from 2 to 20 did not change the reported bounds or return the missing points. PARI's lower bound can include a parity increment without a returned point; the audit uses the number of returned independent points instead. Thus the \(y=91\) rank is not claimed certified to be 1 here. The raw descent records' preliminary `certified_rank` flag checked field certifications and coincident reported bounds only; it is superseded by the witnessed rank bounds and full-basis tests in `classification.json`. None of the 179 accepted curves depends on an unwitnessed lower bound. Failure of the search is not proof of rank zero or nonexistence of solutions. All three minus-sign equations are completely settled by the saved elliptic computations.

The general parametric Hai–Walsh problem remains open in this work. The literature search does not prove that these particular fixed fibres were previously unclassified.

## Pilot, resources and execution record

The first pilot treated \(y=4,1,2,3,5\), both signs, on VM CPU 1 at niceness 19. For \(y=4\), complete rank/basis/integral-point work took 3.31 s for minus and 0.44 s for plus. The other completed pilot curves took 0.55–0.86 s each. An initial rank-zero logging error (`saturation([])` returns a `None` index) was identified and corrected; the pilot did not make a completeness claim for that failed entry.

The full local PARI pass took 8.27 s for 200 curves. It returned coincident reported rank bounds for 194 curves and certified all 400 field records; 15 coincident-bound cases still lacked enough points. The definitive Sage pass took 79.58 s summed over curves; the slowest was the rank-5 minus curve at \(y=100\), 20.25 s. It completed 179 curves and retained 21 explicit failures. An earlier wrapper-compatibility error interpreting eclib's printed unsaturated-prime vector was corrected before that pass; its output is retained as `sage_attempt1.jsonl`, not accepted as proof.

The first full independent checker run took 19.10 s on the Mac. The final run, including file hashes, is recorded in `logs/independent_check.log`. All VM mathematical processes used `nice -n 19 taskset -c 1`, with BLAS/OpenMP threads limited to one. Only one heavy local process ran at a time. No packages, paid calls, publications or messages to researchers were used. The folder is under 10 MiB and observed local free space was 15 GiB.

An additional eclib search for the \(y=91\) basis, with `descent_second_limit=20`, was externally stopped after 6 min 53 s elapsed (6 min 41 s CPU), without a returned basis. Its Python 300-second alarm did not interrupt the native C++ call; the explicit process termination and resource measurements are saved. No research process remains running on the VM. This is an interrupted search, not evidence for nonexistence or for impossibility of completing the remaining fibres by other methods.

## Certificate files and reproduction

- `certificates/classification.json`: all 200 curve statuses, proved ranks/bases where available, complete integral lists, exact finite-search data, residue exclusions and recovered solutions.
- `certificates/solutions.json`: explicit fourteen-triple witness file.
- `certificates/pari_descent.jsonl`: every exact GP input, output, field polynomial, discriminant, class number and `bnfcertify` result.
- `certificates/sage_results_initial.jsonl`: definitive Sage pass, including every failure and full successful output.
- `certificates/sage_basis_changes.jsonl`: exact basis changes used for the finite search.
- `certificates/pari_retry.jsonl`: the higher-effort three-curve retry.
- `certificates/fibres.csv`: compact per-\(y\) status table.
- `certificates/source_errata.json`: independently checked correction to the paper's solved minus-denominator family.
- `logs/sage_classify2.log`: verbose saturation and integral-point proof transcript.
- `check.py`: independent standard-library checker; imports none of the search scripts.
- `certificates/SHA256SUMS`: hashes of certificates, checker, research scripts, proof transcripts and saved primary sources.

Run from this directory:

```sh
python3 check.py
python3 check.py --y 4
```

The first command verifies hashes, all fourteen witnesses, all eighteen residue exclusions, basis changes, torsion, all final finite enumerations and inverse-map filtering. `--quick` skips the finite MW exhaustion and is **not** a substitute for the full check. The checker explicitly reports its trusted unbounded-proof dependencies.

The search scripts are retained under `scripts/`. Local descent uses the specified GP 2.19 executable with `-q -f -s 1G`. On the VM the Sage scripts run from `~/haiwalsh/` under the prescribed CPU/niceness limits. No database rank or database generator assumption is used in the definitive pass: its points and upper ranks come from the saved local descent, and eclib certifies their independence and full saturation before Sage enumerates integral points.

## Prior art and “already solved?” search

The literature-only pass was performed first, within the requested twenty-minute maximum. Exact queries, captured search responses, API results, downloads, failures and hashes are in `sources/literature-search.md`, `sources/search_batch*.json`, `sources/fetch.jsonl` and the named source files. **No later resolution was located.**

1. Yang Hai and P. G. Walsh, *On a Diophantine problem of Bennett*, Acta Arith. 145 (2010), 129–136, [DOI 10.4064/aa145-2-3](https://doi.org/10.4064/aa145-2-3), p.131 poses the exact plus-denominator problem. Its solved minus-denominator analogue is a different equation. The original PDF is saved.
2. [WNT 2017, problem 017:17(2), p.7](https://westcoastnumbertheory.org/wp-content/uploads/2018/12/wcnt-problems-2017.pdf) gives the family and \((2177,4,23)\). Its printed range \(r=1,2,\ldots\) in \(z=2r+1\) omits the valid endpoint \((3,1,1)\), obtained with \(r=0\) and the plus sign. This is a small endpoint omission, not a new exceptional solution. For the stated \(y>0,z>0\) domain, the accompanying “one more solution” remark therefore needs this endpoint qualification.
3. The [Carleton 2009 contributed problems, Problem IV](https://www.fields.utoronto.ca/programs/scientific/08-09/numtheory/CarletonProbs.pdf) already states the exact equation, predating the source paper.
4. Fresh [OpenAlex source and citing-work records](https://api.openalex.org/works/W2315525133) report and return one citing work: Yangcheng Li (2024), *A note on the Diophantine equation \((x^k-1)(y^k-1)^2=z^k-1\)*, [primary PDF](https://nntdm.net/papers/nntdm-30/NNTDM-30-4-825-831.pdf). Its introduction cites the solved minus-denominator equation, and its new result concerns \(k\ge10\); it does not settle this target.
5. Walsh's [current bibliography](https://sites.google.com/view/gary-walsh/research-articles), later-author OpenAlex queries, exact-equation/title searches, OEIS searches and thesis searches yielded no direct resolution. The source-linked OpenAlex author IDs contain unrelated people, so their lists are not reliable exhaustive bibliographies. OEIS searches `"Hai" "Walsh"` and `2177,528` returned no matching entry.
6. Walsh's *Squares in recurrences using elliptic curves*, [DOI 10.1142/S1793042124500106](https://doi.org/10.1142/S1793042124500106), online 2023 / journal 2024, concerns pure quartics and square terms according to its accessible abstract/references. **Its full text could not be obtained** (HTTP 403); legacy author URLs redirected to an HTML homepage. This overlap gap is preserved, rather than claiming the paper was read.
7. Walsh's [2024 survey](https://www.cs.umd.edu/~gasarch/open/garyw.pdf) and [March 2026 preprint arXiv:2603.05809](https://arxiv.org/abs/2603.05809) were downloaded and inspected. They discuss pure-quartic/integral-point problems; the latter solves Bumby's \(3X^4-2Y^2=1\). Neither inspected text supplies the requested classification.

No exact quotation of a later settlement is supplied because no settlement was found. This remains a search finding with the full-text and indexing limitations above.

**Additional source error, visually confirmed on p.130.** Corollary 1.1 prints \((4t^3-2t,t,2t)\) for its first minus-denominator family. The first coordinate must be \(4t^3-3t\):

\[
(4t^3-3t)^2-1=(t^2-1)(4t^2-1)^2.
\]

At \(t=2\), the printed \((28,2,4)\) fails both signs, whereas \((26,2,4)\) satisfies the minus equation. The saved page image, explicit error witness and checker preserve this finding. It does not alter the open target or the classification above.

## SHA-256 of principal deliverables

The expanded manifest is `certificates/SHA256SUMS`. Principal file hashes:

| File | SHA-256 |
|---|---|
| `certificates/classification.json` | `c37297886a0d1a94217bc2d6a5fb7083f4f1866244850ae61992aab0e72183aa` |
| `certificates/solutions.json` | `10e34fb34fc2466bb411ba24e4398ea033cca7492359aca124468f307afa3a48` |
| `certificates/pari_descent.jsonl` | `f7ecb683aab72781b363e679482a930efa5c26b6e39100cf6e72903c2239e49a` |
| `certificates/sage_results_initial.jsonl` | `4d6886919f45b93d8a355d4cb8a11dfb89e10bab31087da0588fb2684f3e5332` |
| `certificates/sage_basis_changes.jsonl` | `9e5a65213877616d740829803981ebb8b34a5a82566cb4ba4c8742e617d4d053` |
| `certificates/source_errata.json` | `7b29a3a9a4e761f03a1023da5849a514d7e9120516820f9c6807490ace95c1ed` |
| `check.py` | `5bcc94bebc019f3d3c5f50168a4ad9c9ce17735f31a6389508e96617514e2592` |
| `certificates/SHA256SUMS` | `85c019d2df1a81382a2f8a830f206a945b1dc6d03635fec9beba01927cd79e77` |
