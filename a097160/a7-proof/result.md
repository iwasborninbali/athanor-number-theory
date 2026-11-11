# Certified seventh term of OEIS A097160

**Established: a(7) = 4481.** The longest run of consecutive nonzero quadratic residues modulo 4481 has length exactly seven, and **every prime p > 4481 has a run of at least eight**. The same certificate system independently reproduces **a(6) = 2153**.

This is a complete all-primes result, using the standard Weil character-sum theorem and explicit finite certificates. The theorem handles every prime above an explicit cutoff; the files list a residue-run witness for every remaining prime above the claimed endpoint. No probabilistic primality test, heuristic extrapolation, unproved analytic hypothesis, or assumption about an unscanned tail is used.

The method differs from the proposed SAT route. After reading Reble, I found that an explicit Weil cutoff makes the remaining search very small. I used that complete argument instead of rebuilding his case tree or producing a global SAT refutation. **There is no SAT part and no DRAT file.** The finite exclusion is exhaustive, with completeness independently checked. The standard mathematical input and the precise scope of the checker are stated below.

## 1. The analytic reduction

Write χ for the Legendre symbol modulo an odd prime p, extended by χ(0) = 0. For an integer k with 2 ≤ k < p, let

\[
N_k(p)=\#\{a\in\mathbb F_p:\chi(a)=\chi(a+1)=\cdots=\chi(a+k-1)=1\}.
\]

Zero is excluded by this definition. A run that avoids zero has a representative wholly within 1,...,p−1; hence this is exactly the relevant notion of a nonzero residue run.

**Standard theorem used.** If f is a squarefree polynomial of degree d ≥ 1 over F_p, then

\[
\left|\sum_{a\in\mathbb F_p}\chi(f(a))\right|\le(d-1)\sqrt p.
\]

For our application, f is monic and splits into distinct linear factors. This form of Weil's bound is stated in [Keith Conrad, *Quadratic residue patterns modulo a prime*, equation (2.3)](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/QuadraticResiduePatterns.pdf), and used in [Kiritchenko–Tsfasman–Vlăduţ–Zakharevich, Section 2.2](https://arxiv.org/html/2403.16326v2). It is unconditional. The original reference is A. Weil, *On some exponential sums*, Proc. Natl. Acad. Sci. USA 34 (1948), 204–207; a proof of this classical theorem itself is not part of the certificate.

Here is the complete derivation of the cutoff. Put

\[
T_k(p)=\sum_{a\in\mathbb F_p}\prod_{i=0}^{k-1}(1+\chi(a+i)).
\]

At a point where none of a,...,a+k−1 is zero, the product is 2^k if all k symbols are +1 and zero otherwise. There are exactly k points with a zero factor argument, because p > k. At each of those points the product is nonnegative and at most 2^(k−1). Therefore

\[
T_k(p)=2^kN_k(p)+E,\qquad 0\le E\le k2^{k-1}.
\tag{1}
\]

Expand the product. The empty subset contributes p. For every nonempty subset S of {0,...,k−1}, the remaining character sum has polynomial

\[
f_S(X)=\prod_{i\in S}(X+i).
\]

Its roots are distinct modulo p, so the standard theorem applies with d = |S|. Consequently

\[
T_k(p)\ge p-\sum_{j=1}^k {k\choose j}(j-1)\sqrt p
       =p-B_k\sqrt p,
\quad B_k=(k-2)2^{k-1}+1.
\tag{2}
\]

Combining (1) and (2), with C_k = k 2^(k−1), gives

\[
\boxed{N_k(p)\ge\frac{p-B_k\sqrt p-C_k}{2^k}.}
\tag{3}
\]

This retains the actual degree in each summand, rather than replacing every degree by k. It is an immediate specialization of the standard character expansion, not a new analytic theorem.

All cutoff arithmetic can be checked with integers. Choose a positive integer M such that 2M ≥ B_k and

\[
D=M^2-B_kM-C_k>0.
\]

For every real t ≥ M,

\[
t^2-B_kt-C_k=D+(t-M)(t+M-B_k)\ge D>0.
\]

Taking t = √p proves N_k(p) > 0 for every prime p ≥ M². There is no floating-point step in this implication.

| Result | Required run k | B_k | C_k | M | M² | D |
|---|---:|---:|---:|---:|---:|---:|
| a(6) = 2153 | 7 | 321 | 448 | 330 | 108900 | 2522 |
| a(7) = 4481 | 8 | 769 | 1024 | 775 | 600625 | 3626 |

In particular,

\[
N_8(p)\ge\frac{p-769\sqrt p-1024}{256}>0
\quad\text{for every prime }p\ge600625.
\]

This is the argument for the infinite tail; the finite scan alone would not prove the result.

## 2. Finite certificates and completeness

For each endpoint, the JSON file contains its complete residue word at indices 0,...,p−1, the claimed maximum run, and a starting point for a run of that length. The checker proves the endpoint prime by trial division, reconstructs the full word by enumerating all nonzero squares, compares the word, and measures its longest block of ones.

- Modulo 2153, the maximum is six, attained at 28,...,33. Corresponding square roots are 551, 480, 626, 377, 914, 154.
- Modulo 4481, the maximum is seven, attained at 98,...,104. Corresponding square roots are 2006, 2165, 10, 1821, 1247, 913, 1190.

The compressed text files contain one line `p start` per prime in the indicated interval, in increasing order. A line certifies that `start,...,start+k-1` are nonzero residues modulo p. These are explicit lists of **all** the checked primes, not sampled primes or just their counts.

| File | Complete interval | Number of primes | First prime | Last prime |
|---|---|---:|---:|---:|
| `certificates/a6-witnesses.txt.gz` | 2153 < p ≤ 108900 | 10028 | 2161 | 108893 |
| `certificates/a7-witnesses.txt.gz` | 4481 < p ≤ 600625 | 48537 | 4483 | 600623 |

The search program uses an Eratosthenes sieve and a binary Jacobi-symbol calculation. The independent checker uses trial division to enumerate primes and Euler's criterion `pow(x,(p-1)//2,p) == 1` to verify each supplied residue. It neither imports nor executes either search/packaging program. Exact prime-by-prime correspondence rejects any gap, duplicate, unsorted entry, or composite substitution, and the checker rejects trailing data. It verifies `1 <= start <= p-k`, excluding zero and wraparound.

These two facts are sufficient for each result: the endpoint has maximum exactly n; every larger prime either has a listed (n+1)-run or is covered by (3). No verification of smaller primes is necessary for a greatest-prime assertion.

## 3. Pilot, full run and validation

The a(6) pilot was performed before the full a(7) run:

| Case | Jacobi evaluations in search | Search CPU time | Failures |
|---|---:|---:|---:|
| Seven-residue pilot | 2334618 | 0.104308 seconds | 0 |
| Eight-residue full target | 22954492 | 1.164406 seconds | 0 |

The full target required about ten times as many symbol evaluations as the pilot, comfortably within the limits. These figures time the C search loop, excluding its sieve construction, compilation, downloading and certificate checking; no SAT runtime estimate is claimed. The largest ending point of a supplied run was 1957 for the pilot and 5135 for the target.

The independent checker passed in approximately **0.9 seconds** under Python 3.14.6. Its exact recorded output is in `logs/check.log`. Fault-injection checks in `logs/audit-checker.py` / `logs/audit-checker.log` show rejection of an omitted prime, an invalid run, duplicate trailing data, a false endpoint maximum, an incorrect subset coefficient, and an insufficient cutoff.

The certificate payload is approximately 246 KiB. All files, including saved sources, occupy only a few MiB. Disk checks showed about 16 GiB free initially and 15 GiB at completion. One computational process was used at a time; no installs, paid calls, delegation, VM, publication or messages to other people were used.

## 4. Running the independent checker

From this folder, with Python 3.10 or newer and no third-party packages:

```sh
python3 check.py
```

Expected conclusions:

```text
PASS a(6) = 2153: endpoint maximum 6 at 28; 10028 primes in (2153, 108900]; Weil-cutoff margin 2522; largest witness endpoint 1957
PASS a(7) = 4481: endpoint maximum 7 at 98; 48537 primes in (4481, 600625]; Weil-cutoff margin 3626; largest witness endpoint 5135
```

The checker verifies file hashes, endpoint primality/residue words, completeness of the finite prime lists, every run witness, and the integer conditions making the displayed analytic bound positive throughout the remaining infinite range. **The trusted mathematical input is Weil's standard character-sum theorem.** This is a conventional computer-assisted proof with a written analytic lemma, not a formal proof of Weil in Python or a proof-assistant kernel.

To regenerate the witnesses, independently of checking them:

```sh
clang -O3 -Wall -Wextra -pedantic generate.c -o generate
./generate 7 2153 108900 > certificates/a6-witnesses.txt
./generate 8 4481 600625 > certificates/a7-witnesses.txt
python3 make_certificates.py
python3 check.py
```

Gzip output is deterministic (`mtime=0`). The C binary is unnecessary for checking.

## 5. SHA-256

The checker reads `manifest.json`, which covers its own source, the search/packaging sources, and all five certificate files. The principal certificate and checker hashes are:

| File | SHA-256 |
|---|---|
| `check.py` | `ce13b2a88a2eb4c490c4ad2fe2457399de8ca405ff98f5dfffdf2680ee79664d` |
| `generate.c` | `8e0d34fe92f2c98647d4c7b69990c9dd7ae811ac46f564fe00394b107815f350` |
| `make_certificates.py` | `bded90f85ca20b140d689b31c3f5017f1c14b5489901e26cd0d44534fd38d9b0` |
| `certificates/a6-endpoint.json` | `0135475cbca54a0d504d619f757d5faac267fd0a955c89c500a2db7c83ab96e5` |
| `certificates/a6-witnesses.txt.gz` | `57f137f27e812e7bd37d9b0f3f6a5d85df43e604ac273a3eee70b33d600a76dd` |
| `certificates/a7-endpoint.json` | `4f7c8ec7574e663237a75d4ebbee9e711eddbe04f5729196274c6bfc3faf4793` |
| `certificates/a7-witnesses.txt.gz` | `dff8f44cd3b0365b7979864afe32576913480a51f8785fd289971ce5649f8335` |
| `certificates/theorem.json` | `d6740af2a4ab06881a33b3ea44aff526e82d454337759ea638bd3d3d26ac936f` |

SHA-256 of `manifest.json`: `6aaf3f5bde6821b7ea38a4126f865e096a48f4889639d81b362ae3b7f2ddc53d`.

Saved-source hashes are separately recorded in `sources/source-hashes.json`; exact downloaded URLs and access failures are in `sources/retrieval.json`.

## 6. Prior art and source audit

[Reble's 2 August 2014 note](https://oeis.org/A097160/a097160.txt) proves the first six terms by multiplicativity and rational arithmetic progressions. Under an assumption of no k-run, an arithmetic progression A,A+d,...,A+(k−1)d cannot have every numerator with the same character as d: division by d would give consecutive residues. Products and quotients relate these characters; a contradiction applies away from primes dividing the finitely many numerators and denominators used. Those exceptional moduli are then checked directly. His a(6) upper bound is 12919, and he reports approximately 660000 proof lines. I read the full note before computation. I found no error in its stated six-term result.

The [OEIS correction of 11 December 2015](https://oeis.org/A097160/internal) removed uncertified subsequent entries. The current entry still lists only six terms and gives 4481 as the proposed next term. That is the exact target verified here.

The classical analytic alternative is already explicit in [Conrad's Theorem 2.1 and subsequent discussion](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/QuadraticResiduePatterns.pdf). He works out the largest prime without three consecutive residues, and explains that general largest-prime questions reduce to a finite check. The present contribution is the explicit seventh-cutoff computation and its small, independently checkable witness package; no novelty is claimed for the character-sum method or cutoff principle.

[Kiritchenko et al. (2024 preprint / 2025 journal publication)](https://arxiv.org/html/2403.16326v2) also recalls the general character bound and develops the geometry further. **A source typo found:** its arXiv v2 equation (1) has summation upper limit `p-ell-1`; for the defined word on 1,...,p−1 this should be `p-ell`. For p=17 and ell=3, the NRR pattern occurs at starts 7 and 14, while the printed limit 13 misses the second occurrence. Their Example 2.1 gives the correct count two. Our proof sums over the whole field and explicitly corrects the zero points, so it does not use that endpoint convention. This observation concerns the saved arXiv version; I did not check the published typesetting.

No located later work asserted the exact seventh cutoff. Recent multiplicative-function papers and the October 2026 GPU-scan preprint concern related mechanisms or per-prime computation, not this all-primes certification. The complete bounded search record, including OpenAlex's 27 citing titles and exact web queries, is in **`sources/search-record.md`**. This search finding does not establish bibliographic priority.

## 7. What is not established or supplied

- No claim about a(8), a(9), later sequence terms, or any general congruence pattern for these terms.
- No reconstruction or verification of Reble's unavailable 660000-line proof, no new SAT/XOR implementation of his a(6) method, and no global length-eight SAT UNSAT/DRAT certificate. Those requested mechanisms were replaced by the complete analytic-plus-finite proof above; the mathematical target is fully established.
- No formalization of the Weil theorem, no claim to an elementary proof avoiding it, and no claim that the literature search exhausts unindexed or unpublished work.
