**Independent adversarial verification of the Hai–Walsh computation**  
2026-11-11. Audit begun 00:53 UTC; substantive checks completed by 01:06 UTC. English report. Target: `../a04-haiwalsh/result.md`, SHA-256 `c28963f09f0f6062790cf1965e75481c86bade3af5b0c4287e0f39261cad8c16`.

**Overall verdict: PROOF_GAP in the claimed certified, unbounded completeness.** The algebra, fourteen witnesses, sampled ranks, saturated bases and reproduced point lists pass. I found an executed, mathematically unjustified step in Sage 10.9's integral-point coefficient-bound calculation. Consequently, the supplied finite enumerations do not certify that there are no additional points outside their boxes. This finding does **not** refute the proposed solution list. No counterexample was found, including in larger diagnostic coefficient boxes and an independent search through (z=10^6).

| Claim | Verdict |
|---|---|
| Elliptic reduction, domain exceptions and inverse filtering | **CONFIRMED**, exact algebra |
| Thirteen family members and the exceptional witness | **CONFIRMED** as solutions; exhaustiveness has the gap below |
| (y=4): ranks 3 and 1, and the stated full bases | **CONFIRMED**, fresh descent and saturation |
| Sampled rank upper bounds require no GRH/BSD | **CONFIRMED** for the descent path used |
| Full saturation before integral enumeration | **CONFIRMED** in the fresh sample; original accepted records are consistent |
| (y=4): listed 29 and 3 affine integral points | **REPRODUCED** and arithmetically valid; certified completeness **NOT ESTABLISHED** |
| Certified integral-point completeness for all 179 accepted curves | **PROOF_GAP**: all 144 positive-rank curves execute the invalid bound substitution |
| Eighteen direct congruence exclusions | **CONFIRMED**, independent of elliptic height bounds |
| Claimed unbounded classification of the 197 quartics | **PROOF_GAP**, not a demonstrated false classification |
| Plus fibres 73, 91, 97 left unresolved | **CONFIRMED** as an appropriate limitation of the computation |
| General open problem or novelty of this fixed-fibre calculation | **NOT ESTABLISHED**; no later settlement located, with specific full-text gaps |

**The algebra.** I interpret the domain exactly as the target report states it: integers (y\ge1,x>1,z>0), and (s\in\{-1,1\}). Put (D=y^2+1). The original equation is

\[
x^2=Dz^4+2sDz^2+D+1.
\]

Multiplication by (D^2z^2), followed by (U=Dz^2,V=Dxz), gives exactly

\[
V^2=U^3+2sDU^2+D(D+1)U
    =U\big((U+sD)^2+D\big).
\]

For (V^2=U^3+aU^2+bU), the Weierstrass discriminant is (16b^2(a^2-4b)); here it is (-64D^3(D+1)^2\ne0). The second factor in the displayed cubic is positive for every real (U), so no affine real point has (U<0). No squarefreeness assumption on (D) is needed.

Conversely, take an integral point with (U,V>0); require (D\mid U), (U/D=z^2) for an integer (z>0), and (Dz\mid V). Then (x=V/(Dz)) is integral and division of the curve equation by (D^2z^2) proves the original equation. Retain (x>1). These tests are necessary and sufficient. The curve is not being identified with all quartic solutions without these tests. Enumeration is on the original model; the minimal-model change used for saturation is inverted before this step.

The point at infinity has no finite image. The affine point ((0,0)) cannot yield a permitted (z>0); (z=0) in the original equation would require (x^2=y^2+2), strictly between (y^2) and ((y+1)^2). For (z=1,s=-1), (x=1) is excluded. For (z=1,s=1), ((x-2y)(x+2y)=5), giving only ((x,y)=(3,1)). Positive (x,z) give positive (V); taking both signs of every integral (V) and then filtering loses no solution. If arbitrary signed integers were intended instead, the corresponding sign variants and the excluded (x=\pm1,z=\pm1,s=-1) cases would have to be stated separately.

The family follows from ((2y^2+1)^2-1=4y^2(y^2+1)). Since (z^2+s=2y), positive integral (y) forces odd (z). Direct arithmetic verifies all thirteen listed family members and ((2177,4,23,-1)). In particular (2177^2-1=17\cdot528^2), and (528=23^2-1).

**Fresh rank, saturation and integral-point computations.** I wrote separate drivers; I did not import the original search scripts. Local GP was exactly the requested executable, with `-q -f -s 1G`, at niceness 19. I changed the random seed to 20261111, real precision to 100 decimal digits and `ellrank` effort to 4. The ten random values were selected reproducibly by `random.Random(20261111).sample` from 1 through 100 excluding 4:

`16, 22, 25, 36, 42, 46, 58, 60, 76, 85`.

I additionally selected (24,40,72,84,93,98,99,100), covering all rank-4 cases and the rank-5 case, and checked the three unresolved values. Thus I recomputed 44 descents on 22 fibres and obtained 88 successful `bnfcertify` results. The GP work took 3.37 seconds in total. Raw inputs, outputs, exact rational starting points and certifications are in [pari_fresh.jsonl](evidence/pari_fresh.jsonl).

The descent cubic has a rational linear factor and an irreducible quadratic factor. I inspected the actual local PARI 2.19 source, copied to [pari_ellrank_actual.c](sources/pari_ellrank_actual.c). `makevbnf` uses `nfinit` for factors of degree at most two; `ell2selmer` dispatches to `bnfselmerQ` and `nf2selmer_quad`. The latter uses exact Hilbert-symbol, quadratic-form and ideal calculations, not a conditional cubic-field class-group computation. The independently certified `bnf` objects are additional checks, not the objects consumed by that quadratic routine. Thus the report correctly avoids the common mistake of treating an unrelated `bnfcertify` call as certification of a conditional descent. The [PARI documentation](https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html#ellrank) also distinguishes the descent bound from an analytic-rank/BSD calculation.

On the VM I ran Sage 10.9 only under `nice -n 19 taskset -c 1`, with single-thread environment settings, from `~/haiwalsh-verify/`. That directory initially did not exist and was created for the explicitly requested execution location; scripts and data were fed on stdin, with all audit output saved here. No script or result file was installed on the VM.

For each witnessed full-rank set, I independently converted its points to the minimal model, called eclib `mwrank_MordellWeil.process`, then `saturate(max_prime=-1,min_prime=2)`, and checked its Boolean success, empty unsaturated-prime list and resulting rank. Each fresh saturation index was 1. Full rank plus full saturation proves generation modulo torsion, rather than merely a finite-index subgroup. This is the documented meaning of `max_prime=-1`: the [Sage saturation interface](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/ell_rational_field.html#sage.schemes.elliptic_curves.ell_rational_field.EllipticCurve_rational_field.saturation) computes the necessary prime bound. Torsion was ({O,(0,0)}).

I then ran `integral_points(mw_base=B,both_signs=True,verbose=True)` and compared entire point sets, not just the quartic solutions. There were 37 successful point-list recomputations, four direct congruence exclusions, and three explicitly unresolved plus curves. All 37 lists matched. The summed saturation/enumeration time was 38.79 seconds. Evidence: [sage_fresh.jsonl](evidence/sage_fresh.jsonl), [full transcript](evidence/sage_fresh.log), [summary](evidence/sage_summary.log).

Here (r_\pm) denotes the witnessed rank and (N_\pm) the number of affine integral points returned, including both signs. `C8` means a direct quartic exclusion modulo 8, not an elliptic enumeration; `open` means no full basis.

| (y) | (r_-) | (N_-) | (r_+) | (N_+) |
|---:|---:|---:|---:|---:|
| 4 | 3 | 29 | 1 | 3 |
| 16 | 3 | 13 | 2 | 3 |
| 22 | 1 | 7 | 0 | 1 |
| 24 | 4 | 29 | 1 | 1 |
| 25 | 3 | 23 | 3 | 5 |
| 36 | 3 | 13 | 2 | 3 |
| 40 | 4 | 17 | 2 | 3 |
| 42 | 1 | 7 | 0 | 1 |
| 46 | 2 | 7 | — | C8 |
| 58 | 2 | 11 | 0 | 1 |
| 60 | 2 | 9 | — | C8 |
| 72 | 4 | 17 | 1 | 1 |
| 73 | 2 | 11 | — | open |
| 76 | 1 | 7 | 0 | 1 |
| 84 | 4 | 13 | — | C8 |
| 85 | 2 | 9 | 1 | 3 |
| 91 | 3 | 13 | — | open |
| 93 | 4 | 19 | 0 | 1 |
| 97 | 2 | 7 | — | open |
| 98 | 2 | 7 | 1 | 1 |
| 99 | 1 | 7 | — | C8 |
| 100 | 5 | 29 | 2 | 3 |

I also audited the original records across all 179 accepted curves: returned-point count equals the certified upper bound, the saturated rank agrees, success flags are true, and bases, point lists and filters match the packaged certificate. The original standard-library checker passed all 63 manifest hashes and exhausted all 240,881 recorded MW combinations. See [records_audit.json](evidence/records_audit.json) and [original_checker.log](evidence/original_checker.log). This verifies consistency and finite arithmetic; it does not fix the height-bound defect.

**The decisive completeness defect.** The [documented basis requirement](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/ell_rational_field.html#sage.schemes.elliptic_curves.ell_rational_field.EllipticCurve_rational_field.integral_points) is real: a supplied finite-index set does not suffice. That requirement was met in the sample. The separate problem occurs inside the bound calculation itself.

I extracted the actual installed method to [sage_integral_points_actual.py](sources/sage_integral_points_actual.py). Its lines 313–320 compute a purported lattice lower bound `d_L_0`, form (Q=rH^2) and (T=(1+3rH/2)/2), and then execute:

```python
if d_L_0 < R(T**2+Q):
    d_L_0 = 10*(T**2*Q)
low_bound = (R(d_L_0 - Q).sqrt() - T) / c
```

The failed inequality is a hypothesis needed to obtain a positive logarithmic lower bound. Assigning a larger number does not prove that hypothesis. Increasing lattice scale/precision and recomputing would be necessary. `proof.all(True)` does not validate this assignment; `integral_points` has no separate proof-parameter branch that repairs it.

To distinguish an abstract source concern from an executed failure, [audit_bound.py](scripts/audit_bound.py) makes only the bound-failure branch raise with its local data, and stops before the final finite enumeration. Applied to every claimed positive-rank basis, **all 144** curves enter that branch. The remaining 35 accepted curves have rank zero and take the torsion-only path. Full local data, including integer lattice columns, are in [bound_hypothesis.jsonl](evidence/bound_hypothesis.jsonl).

For (y=4,s=-1), the first coefficient bound is approximately (10^{58}), the computed lattice lower bound is (6.13467683962059\times10^{10}), and the required threshold is (8.0625\times10^{116}). The assignment substitutes (1.51875\times10^{234}). But the actual integer lattice has the nonzero vector

\[
(-77167,231552,-72310,0),\qquad \|v\|^2=64,799,810,693.
\]

Its coefficients in the original lattice-row basis are exactly ((-77167,231552,-72310,-46690)). Therefore the substituted number cannot be a lower bound for the squared length of nonzero vectors in that lattice. I checked lattice membership and squared norms with exact integer arithmetic for **all 144** counterwitnesses; [check_records.py](scripts/check_records.py) reproduces that check. For the plus curve at (y=4), the analogous short vector is ((-9514346325173898,0)), of squared norm (90522785995350057219479940514404), whereas the code substitutes (5.625\times10^{88}).

The final small coefficient boxes are downstream of this step. An exact exhaustive search of those boxes proves only that those boxes contain the recorded points. It cannot prove that every integral point lies in them. This is a concrete failure of the trusted software dependency, stronger than a general observation that floating-point calculations lack interval certificates.

As a diagnostic, I used 4096-bit periods/logarithms, the exact minimum squared Gram–Schmidt length as a valid lower bound for the constructed integer lattice, and increased the lattice scale until its required inequality actually held. For the minus curves at (y=4,25,93,100), this gave coefficient bounds (7,6,7,7), versus the original (6,5,5,5); the plus bounds at (4,25,100) were (3,4,3). Exact exhaustion of these seven boxes, including torsion and the small-coordinate intervals, visited 816,357 combinations and produced no additional points. This used the inspected standard-library checker for the finite group arithmetic. See [high_precision_bound.py](scripts/high_precision_bound.py), [diagnostic bounds](evidence/high_precision_bound.jsonl) and [exact exhaustion](evidence/diagnostic_exhaustion.jsonl). **These are supporting diagnostics, not a repaired rigorous certificate:** I have not supplied certified error enclosures for all real constants and elliptic logarithms.

**The full (y=4) recomputation.** Fresh GP gives ranks 3 and 1. Both field certifications succeed; the quadratic discriminant is (-68) and its class number is 4. Fresh eclib returns the exact stated bases, fully saturated modulo ((0,0)):

\[
E_-:\ (2,22),(9,27),(18,18),\qquad
E_+:\ (72,756).
\]

The returned integral points, represented by ((U,|V|)), are exactly:

\[
\begin{split}
E_-:\ & (0,0),(2,22),(8,28),(9,27),(17,17),(18,18),\\
& (25,45),(32,88),(34,102),(72,468),(153,1683),\\
& (338,5902),(1224,42228),(3042,166842),(8993,851207);\\
E_+:\ & (0,0),(72,756).
\end{split}
\]

Filtering returns precisely ((x,z)=(33,3),(2177,23)) for the minus sign: these lift from ((153,1683)) and ((8993,851207)). No plus point passes the filter; moreover (y=4) plus is independently impossible modulo 8. Thus the positive witnesses and ranks/bases are confirmed. I do not sign the minus list's **unbounded completeness** from this Sage transcript because of the demonstrated bound defect.

**Congruences and bounded sanity check.** For even (y), (D\equiv1) or 5 modulo 8. In the plus equation, even (z) gives (x^2\equiv2) or 6, and odd (z) gives (x^2\equiv5), all impossible. If (3\mid y), the plus equation gives (x^2\equiv2\pmod3). These arguments prove the eighteen exclusions in the target report and, in fact, apply to every (y) satisfying the respective hypotheses.

My independent [bruteforce.py](scripts/bruteforce.py) covers every (1\le y\le100), both signs, and every (1\le z\le10^6), with no separate (x) cutoff. It uses complete residue wheels modulo 64, 63 and 65, a further square-residue test modulo 11, and exact Python `isqrt` for all survivors. It performed 9,082,549 exact square-root tests in 46.76 seconds and found **exactly the fourteen reported solutions**, including none on the three unresolved plus fibres. See [bruteforce.json](evidence/bruteforce.json). This establishes only the stated finite box.

**Priority and later literature.** I made fresh searches and independently fetched primary sources; URLs, retrieval outcomes and SHA-256 hashes are in [fetch_primary.json](evidence/fetch_primary.json), with search records in `evidence/literature_*.json`.

- [Hai–Walsh 2010](https://www.impan.pl/shop/publication/transaction/download/product/83626), p.131, states this precise positive-domain question as open. The [WNT 2017 problem list](https://westcoastnumbertheory.org/wp-content/uploads/2018/12/wcnt-problems-2017.pdf), 017:17(2), poses it again, supplies the family and the exception. The endpoint ((3,1,1)) is valid despite the printed family parameter starting at 1.
- [Li 2024](https://nntdm.net/papers/nntdm-30/NNTDM-30-4-825-831.pdf), pp.826–827, cites the **minus-denominator** problem ((x^2-1)/(y^2-1)=(z^2-1)^2). The new theorem addresses ((x^k-1)(y^k-1)^2=z^k-1), for (k\ge10) under size restrictions. It supplies neither this plus-denominator fixed-fibre classification nor a solution of the open problem. Confusing its citation of the solved 2010 equation with this open equation would be a sign error.
- Walsh's [2024 survey](https://www.cs.umd.edu/~gasarch/open/garyw.pdf) and [2026 paper](https://arxiv.org/abs/2603.05809) were fetched and read. The latter solves Bumby's (3X^4-2Y^2=1). Neither inspected text supplies the classification at issue.
- The publisher's abstract and references for [*Squares in recurrences using elliptic curves*](https://doi.org/10.1142/S1793042124500106), online 2023 / journal 2024, concern square terms and pure quartics (X^2-dY^4=k). Full-text access returned HTTP 403. I cannot claim to have excluded a relevant result hidden in that full text.
- **An additional concrete prior-art lead:** Lin, Walsh and Yuan, [*Sharp bounds for the number of integral points on (y^2=x^3\pm2tx^2+tpx)*](https://publi.math.unideb.hu/paper/2444), 98 (2021), 455–465. The displayed curve form matches this reduction with (t=D,p=D+1). Its accessible abstract does not state the parameter restrictions or definition of nontrivial point. Full-text retrieval explicitly redirected to a subscription restriction. I therefore cannot decide which, if any, of these fixed fibres its theorem already covers; the title alone is insufficient to apply or dismiss it.

**Literature verdict:** no post-2010 settlement of the general problem, and no previous publication of this exact fixed-fibre classification, was located. This is a bounded search finding, not a proof of present open status or novelty. The two inaccessible later Walsh papers are explicit limitations. In any event, even a correct unbounded classification for these finitely many (y) would not settle the general problem.

**Disposition.** Retain the solution list as strongly supported computational evidence, retain the sampled rank/basis certifications and direct congruence proofs, and downgrade the unbounded completeness claim until valid elliptic-logarithm/lattice bounds are supplied. A repair must establish the actual lattice inequality, with adequate numerical error control, before the exact finite checker can complete the argument. No installs, paid model calls, publications or messages were used. All audit artifacts are in this folder; no instrument or target-report files were modified.
