A097160 extension certificate workspace. All heavy computations belong on the VM. Python helpers require Python 3.10 or later and the standard library only.

Build with an existing GCC or Clang (no packages required):

```sh
gcc -O3 -march=native -std=c11 -Wall -Wextra scan.c -o scan
gcc -O3 -march=native -std=c11 -Wall -Wextra independent.c -o independent
```

For example, to regenerate and independently recheck a(8) completely:

```sh
nice -n 10 taskset -c 2 ./scan 9 3222025 2 certificates/a8.tsv logs/scan-a8.json 1000000
nice -n 10 taskset -c 2 ./independent 9 3222025 full certificates/a8.tsv logs/check-a8.json certificates/sample-a8.tsv
nice -n 10 taskset -c 2 python3 audit.py 8
```

Each exception row is `prime exact_longest_run first_start_of_that_maximum`.
Every prime in `[2, cutoff)` is searched, including primes smaller than the target run length. Zero is excluded. A listed prime is exceptional for run k precisely when its longest run is less than k. The sequence endpoint is the largest listed prime with longest run exactly k-1; it is not inferred merely from lacking a k-run.

`scan.c` uses a segmented Eratosthenes sieve and exact Jacobi/Legendre evaluation. Small-denominator tables speed up quadratic reciprocity; exact prime-exponent masks handle smooth integers. Within a candidate window inexpensive mask evaluations precede the remaining evaluations; any nonresidue x safely rules out starts through x. Thus the first successful window is still the first actual k-run. Exceptions are rescanned in full for exact maximum and earliest maximum start. `scan-baseline.c`, `scan-table.c`, `scan-mask.c`, and `scan-ordered.c` preserve earlier equivalent implementations used during optimization; their output lists were compared against the final scanner.

`independent.c` imports no primary code and ignores primary run witnesses. It implements its own odd bit sieve and counts runs sequentially. Euler's criterion evaluates prime arguments; a separately built factor sieve supplies exact multiplicative evaluation at composite arguments. The checker fully re-derives a(8) and a(9). For larger results its documented sample mode enumerates all primes, checks every listed exception in full, and searches every prime selected by splitmix64(p XOR 0xa09716020261111) modulo 10000 equal to zero. In sample mode it does not certify the absence of unlisted exceptions at unselected primes; that completeness rests on the primary exhaustive scan.

`audit.py` recomputes the subset coefficient and integer cutoff, checks metadata agreement, trial-divides every exception for primality, and independently enumerates squares to check every exceptional maximum and first start. It does not replace the full prime scans. `--metadata-only` omits the square enumeration for a light local audit. `validate.py` checks small boundary cases against full square words and tests corruption rejection.

`run.sh` records the original serial job sequence. It inherits nice 10 and CPU 2 from its launcher. Retained logs record actual wall and CPU times; source-version mapping and any later continuation are documented in result.md. No primary or independent scan requires network access.

Historical optimization scripts assume their named variant binaries have been compiled. Main certificate regeneration needs only `scan` and `independent`. Exact source versions for retained primary reports are recorded in `source-map.json`.

In optimized primary reports the legacy key `jacobi_evaluations` counts exact symbol queries, including parity-mask and batched evaluations; it is not a count solely of calls to the binary Jacobi routine.

Check archive integrity with `python3 verify_manifest.py` before running the mathematical checkers. The external archive and manifest hashes are printed in result.md.

Program invariants, including the exact table/mask formulas and safe window skipping, are explained in algorithm-notes.md.
