# A097160 extension progress

All times UTC. Started 2026-11-10 23:51; six-hour deadline approximately 2026-11-11 05:51.

## 2026-11-10 23:56

Read and audited the predecessor's analytic proof: the subset sums are squarefree for p>k, the k zero-containing terms contribute between 0 and k*2^(k-1), and strict positivity at the integer square root controls the infinite tail. Recomputed minimal integer cutoffs for k=9,...,14. VM cores 2 and 3 are running Costas root checkers; this programme will use one nice-10 process on core 2 until they finish. No model calls, installs, publication, or messages.

Implementing a segmented sieve and a Jacobi scanner with safe skipping over windows blocked by a nonresidue. Independent checker will use Euler's criterion and its own prime enumeration.

## 2026-11-11 00:10

Established a(8)=9857 and a(9)=25793 with complete independent Euler rescans of all 231706 and 1079376 primes below their cutoffs. Primary scan establishes a(10)=60961 with 784 exceptions; all exceptions and 458 hash-selected primes independently checked. A complete independent rescan of a(10) is now running as an additional validation. The primary a(11) scan is underway.

Optimized primary evaluation in stages (saved baseline/table/mask sources): exact Jacobi reciprocity tables; exact masks of prime exponents for 251-smooth integers; cheap characters first inside each candidate window. Complete pilots agree byte for byte at a(8) and a(9). Validation across all 168 primes below 1000 for k=2,...,14 passed, as did five corruption-rejection cases. The separate Python square-word audit initially needed an explicit p=2 boundary case; corrected and rerun successfully for a(8),a(9). Historical OEIS source and 2015 revision markup recovered. All previous terms, including a(7), are also reproduced by these exception lists.

## 2026-11-11T00:52:10Z (hourly monitor)

- scan-a11: k=12 through=398458882 primes=21258458 exceptions=1427 wall=2821.384 cpu=1218.521
- check-a10-full: k=11 primes=4000000 checked=4000000 p=67867967 wall=2424.828

## 2026-11-11 01:16

The complete primary a(11) scan finished: a(11)=132113; 22322063 primes; 1427 exceptions. Its independent Euler check passed for all exceptions and 2237 hash-selected primes, 3662 distinct primes (two selected exceptions overlap). The complete independent a(10) rescan passed: 4943183 primes; 1178.806 CPU seconds, 2917.882 wall seconds. Full independent coverage now extends through a(10).

The final array scanner won the k=12 ten-million-modulus pilot: 21.656 versus 35.252 CPU seconds, with byte-identical exception lists. Its full a(9) pilot and all small-case/corruption checks passed. The parent driver was held between stages, then resumed automatically after those checks and the timing pilot; it is now scanning a(12) through the exact cutoff 2030313481. Current checkpoint: 125829122, 7154632 primes, 2760 exceptions. Current code is frozen for this full scan.

The k=14 planning pilot searched [8000000000,8005000000): 219483 primes, zero exceptions, 36.146697 CPU seconds. Scaling this rate to roughly 439.5 million primes gives about 20.1 CPU hours for a(13), before independent checking. This is a planning estimate, not a determination of a(13). It exceeds the six-hour allowance even with two free cores, so a(12) is the intended last complete term in this run.

The Python auditor now additionally verifies sample selection, distinct union counts, and every sampled witness by Python Euler exponentiation. A light local metadata/sample audit through a(11) passed. Final full square enumeration remains on the VM after a(12) finishes. Hourly monitoring continues. Environment snapshot confirms GCC 13.3.0, Python 3.12.3, AMD EPYC, nice 10 and affinity {2} for the active scan.

## 2026-11-11T01:51:45Z (hourly monitor)

- scan-a12: k=13 through=671088642 primes=34832027 exceptions=2760 wall=3080.210 cpu=2564.635 live_cpu=2590.5s elapsed=3106.2s
- array scanner selected
