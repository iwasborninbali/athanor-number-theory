**Verdict: holds.** The submitted argument proves **A097160(7) = 4481** and independently reproduces **A097160(6) = 2153**, using the stated classical character-sum theorem. I found no analytic, definitional, arithmetic, or certificate gap. I did not execute or import any submitted program.

**Priority is a separate concern:** the literature audit missed substantial earlier work by Buell and Hudson (1984, 1986). Their published descriptions cover an all-primes computation sufficient to settle this target. I obtained the full 1986 follow-up, but not the 1984 numerical tables. Thus the mathematical result is verified; a claim that this is the first proof of the seventh term is **not established**. The distinction between directly read evidence and inference is detailed below.

Verification performed on 11 November 2026 (Bali), beginning 10 November 23:51 UTC. All new files are in this directory; no installs, paid calls, agents, publication, or messages to other people were used.

The analytic argument checks as follows.

1. Let p be an odd prime, 2 <= k < p, and extend the Legendre symbol by chi(0) = 0. For each a, ordinary distributivity and multiplicativity give

   $$\prod_{i=0}^{k-1}(1+\chi(a+i))
   =1+\sum_{\varnothing\ne S\subseteq\{0,\ldots,k-1\}}
   \chi\!\left(\prod_{i\in S}(a+i)\right).$$

   Multiplicativity remains valid when an argument vanishes. Summing the constant 1 over the **whole field** contributes exactly p. There is no missing boundary term in this expansion.

2. For a nonempty S, the polynomial f_S(X) = product over i in S of (X+i) is monic of degree j = |S|. Its roots -i are distinct: a difference of two indices has absolute value between 1 and k-1, below p. Therefore f_S is squarefree, nonconstant, and is not a square over the algebraic closure. Weil's quadratic-character estimate applies to each summand. For j = 1 the sum is exactly zero, consistent with the coefficient j-1 = 0. The empty subset is not subjected to Weil's bound.

   I checked **the supplied Conrad PDF**, printed page 4, equation (2.3). It states the absolute-value estimate for nonconstant polynomials without repeated roots, with right side (deg f - 1) sqrt(p). This is precisely the theorem used here. Theorem 2.1 subsequently replaces each individual degree by a common upper bound; retaining the individual degrees is valid. [Conrad, *Quadratic residue patterns modulo a prime*](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/QuadraticResiduePatterns.pdf). The supplied PDF SHA-256 is `db3df9e1f7133db69aee2e784a7bf1e5feddbee8e11d6579741a2594e850c71e`; my extracted copy is [conrad-extracted.txt](conrad-extracted.txt).

3. The exact coefficient sum is

   $$\begin{aligned}
   B_k&=\sum_{j=1}^k {k\choose j}(j-1)\\
      &=k2^{k-1}-(2^k-1)\\
      &=(k-2)2^{k-1}+1.
   \end{aligned}$$

   Here the two identities are respectively the derivative of (1+x)^k evaluated at 1 and the sum of its nonconstant coefficients. In particular B_7 = 321 and B_8 = 769. Consequently T_k >= p - B_k sqrt(p).

4. There are exactly k exceptional field elements a = 0,-1,...,-(k-1). At each, **one argument** of chi vanishes; its factor 1+chi(0) is 1, not 0. Each other factor is 0 or 2. The exceptional product is therefore either 0 or 2^(k-1), and is always nonnegative. Away from these elements the product is exactly 2^k for an all-residue window and 0 otherwise. Thus

   $$T_k=2^kN_k+E,\qquad 0\le E\le k2^{k-1}=C_k.$$

   Subtracting the upper bound for E gives the claimed **lower** bound

   $$N_k(p)\ge\frac{p-B_k\sqrt p-C_k}{2^k}.$$

   The sign and factor in the zero correction are correct. No zero is being counted as a residue.

5. With D = M^2-B_k M-C_k, the factorization

   $$t^2-B_kt-C_k=D+(t-M)(t+M-B_k)$$

   is exact. If t >= M and 2M >= B_k, both factors in the extra product are nonnegative. D > 0 therefore implies positivity for every such t, not merely at the endpoint. Taking t = sqrt(p) proves N_k(p) > 0 for every prime p >= M^2. All these primes satisfy the earlier p > k hypothesis.

   | k | B_k | C_k | M | M^2 | 2M-B_k | D |
   |---:|---:|---:|---:|---:|---:|---:|
   | 7 | 321 | 448 | 330 | 108900 | 339 | 2522 |
   | 8 | 769 | 1024 | 775 | 600625 | 781 | 3626 |

   Both cutoffs are valid, though optimization is unnecessary. The finite intervals include their upper endpoints; the analytic tails start there too. There is no uncovered prime at either join. The square cutoffs themselves are composite.

The OEIS definition agrees with the proof. Its operative wording is “Greatest prime p such that there are n, but not n+1, consecutive quadratic residues mod p”; its fallback is -1 if none exists. This means that the **maximum** run length equals n. The title does not explicitly say nonzero, but the entry's Mathematica program uses `Range[Prime[n] - 1]`, and its example lists the nonzero residues modulo 17 and assigns maximum 2. Thus zero is excluded. [A097160, internal entry](https://oeis.org/A097160/internal).

A consecutive modular window is formed by repeated addition of 1. Crossing from p-1 to 1 would pass through 0, which is forbidden here. Gluing those two nonzero representatives directly would skip a residue class and change the definition. Accordingly, every admissible window has a representative entirely in 1,...,p-1; using the whole field in N_k gives the same answer. The explicitly zero-inclusive, wrapping convention belongs to a different entry, [A048280](https://oeis.org/A048280/internal). For example it gives length 5 modulo 17 through 15,16,0,1,2.

Write L(p) for the maximum under A097160's convention. The verified endpoint L(4481) = 7 supplies a member of the defining set. Every larger prime has N_8(p) > 0, hence L(p) >= 8 and cannot be in that set. These two facts prove that its greatest member is 4481. A scan of smaller primes is not required. The identical implication with 6 and 7 proves the pilot.

The independent computation is reproducible using [independent_scan.c](independent_scan.c) and [independent_audit.py](independent_audit.py):

```sh
clang -O3 -std=c11 -Wall -Wextra -Wconversion -pedantic independent_scan.c -o independent_scan
./independent_scan > independent-scan.log
python3 independent_audit.py
```

The C program determines primality by exact trial division. For **each prime independently**, it clears a byte table and marks all nonzero squares by the addition recurrence s_1 = 1 and s_(x+1) = s_x + 2x + 1 modulo p, for 1 <= x <= (p-1)/2. This enumerates every nonzero square exactly once: x^2 = y^2 implies x = +/-y, and only one of that pair is in the enumerated half interval. Before each reduction s_x < p and 2x+1 <= p, so one subtraction suffices. All intermediate values are below 2p and comfortably within the integer type. A direct scan of the table finds the first k-run. This uses no Jacobi routine or modular exponentiation and reads no submitted witness file.

The subsequent Python audit independently constructs endpoint words with ordinary `x*x % p` for 1 <= x < p, measures every block, and compares both complete submitted words. It also constructs a second complete prime list using Eratosthenes, cross-checking the C program's trial division. Results are recorded in [independent-scan.log](independent-scan.log) and [independent-audit.log](independent-audit.log).

| Endpoint | Independent maximum | First longest run | Number of longest blocks | Complete submitted word |
|---:|---:|---|---:|---|
| 2153 | 6 | 28,...,33 | 8 | Identical |
| 4481 | 7 | 98,...,104 | 10 | Identical |

All starts of longest blocks modulo 4481 are 98, 1036, 1436, 1930, 2213, 2262, 2545, 3039, 3439, 4377. Modulo 2153 they are 28, 62, 581, 839, 1309, 1567, 2086, 2120. Endpoint primality was also checked independently.

| Independent scan | Prime count | First / last prime | Failures | Largest first-witness endpoint | C CPU seconds |
|---|---:|---|---:|---:|---:|
| 7-runs, (2153,108900] | 10028 | 2161 / 108893 | 0 | 1957 | 0.515 |
| 8-runs, (4481,600625] | 48537 | 4483 / 600623 | 0 | 5135 | 13.564 |

**Every byte of both decompressed submitted witness files equals the corresponding independently generated list.** Thus every witness, every prime, their ordering, and the absence of extra lines were checked. The second prime enumeration independently confirms completeness; all starts also satisfy 1 <= start <= p-k. SHA-256 of the decompressed lists is:

- a(6): `5f26da9e07ff6b9d13a8dcf146d9bea772fcd3529588cceeab6d2a9aef862c6f`
- a(7): `cbc590ec5f2d6da8b03e6b6a802ee99fb1393f24340af21eb4ba2053ffdaa979`

All eight submitted manifest entries match their files. The Python audit also checks the theorem JSON against independently calculated coefficients and margins, and checks the full subset expansion, the exceptional-zero identity, and the squared character-sum inequalities in 147 small-prime cases. Sixty of those have nonzero exceptional error, so the zero correction was exercised. These finite checks supplement the written derivation; they do not replace Weil's theorem. The Python audit used 0.310 CPU seconds; the main scan used about 14.1 total CPU seconds, well below the CPU limit.

The priority evidence changes the interpretation of the result.

I retrieved and read all **28 OEIS revisions**, saved as the three `sources/oeis-history*.html` files. Revision 1 (2004) already contained 4481, alongside later incorrect terms; revision 3 (2007) clarified the exact-maximum wording. Revision 12 removed the incorrect ninth and tenth entries; revision 18 on 11 December 2015 removed the unproved seventh and eighth entries. Later revisions through #28 (30 May 2026) supply no new proof. Consequently, appearing in the old data is not proof, and the current six-term entry does not establish that the wider literature lacks one. [OEIS history](https://oeis.org/history?seq=A097160), [older revisions](https://oeis.org/history?seq=A097160&start=10), [earliest revisions](https://oeis.org/history?seq=A097160&start=20).

Reble's complete 2 August 2014 note certifies six terms, gives a(6) <= 12919 before finite computation, and treats 4481 and subsequent candidates as likely continuations. It does not prove the seventh term. [Reble's original note](https://oeis.org/A097160/a097160.txt).

However, **D. A. Buell and R. H. Hudson, *On runs of consecutive quadratic residues and quadratic nonresidues*, BIT 24 (1984), 243-247, DOI 10.1007/BF01937490**, is directly relevant prior art. Its publisher abstract states a Weil/Burgess bound guaranteeing both kinds of 9-run for every prime at least 414463, and exhaustive longest-run computations for primes below 420000, explicitly in [1,p-1]. **Inference:** the stated theorem and completed scan cover every possible counterexample to the seventh-term claim; this is evidence of an earlier all-primes computational resolution, not merely a related asymptotic estimate. I could read the abstract and references, but the full article requires subscription access and no public copy was obtained. I therefore cannot attest that its printed tables explicitly contain the numeral 4481 or audit that older computation. [Publisher's primary record](https://link.springer.com/article/10.1007/BF01937490). The abstract is saved in `sources/buell-hudson-1984.html`.

The same authors' **1986 follow-up**, *Sequences in power residue classes*, International Journal of Mathematics and Mathematical Sciences 9(2), 261-266, DOI 10.1155/S0161171286000315, was obtained and read in full. Its introduction attributes explicit largest-prime cutoff work to the 1984 paper. Section 2, printed page 262, defines n(p) as the longest run and the barred m(l) as the **largest prime with n(p) = l**, exactly the statistic at issue. Its displayed numerical cutoff table concerns fourth powers, so it is not a direct printed confirmation of 4481. [Institutional record](https://scholarcommons.sc.edu/csce_facpub/94/), [full paper on the EMIS mirror](https://www.maths.tcd.ie/EMIS/journals/HOA/IJMMS/Volume9_2/516483.pdf). The saved PDF `sources/bh1986-emis-volume.pdf` has SHA-256 `e953f56202483854e06120338b02b511f0aa44a83fe262c605b86edc705c80ce`; extracted text and inspected page images are beside it.

The 1984 title was already among the 27 citing works in the submission's `sources/openalex-citing.json`. Screening those titles without following this paper's explicit scope was insufficient for a priority conclusion. The later [2024 Kiritchenko et al. paper](https://arxiv.org/html/2403.16326v2) contains no occurrence of 4481 and does not directly settle the historical question.

The defensible priority answer is therefore: **not proved in the OEIS/Reble material checked; very strong evidence that it was already resolved within Buell-Hudson's 1984 work; exact printed numerical attribution remains unconfirmed in this audit. Do not claim a first proof.** The independently checked certificate package is valid regardless of that bibliographic issue. Retrieval URLs, dates, hashes, and access failures are preserved in [sources/retrieval.json](sources/retrieval.json).
