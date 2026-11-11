"""Audit local submission data and independently generated square-sieve outputs.

This file never imports or executes a submitted program. Run after independent_scan.
Only Python's standard library is used. All writes remain in this directory.
"""
import gzip
import hashlib
import json
import math
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBMITTED = HERE.parent / "a02-a097160"
begin = time.process_time()
log = []


def record(text):
    print(text)
    log.append(text)


def need(condition, description):
    if not condition:
        raise RuntimeError(description)


def prime_sieve(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[:2] = b"\0\0"
    for d in range(2, math.isqrt(limit) + 1):
        if sieve[d]:
            sieve[d*d::d] = bytes((limit - d*d)//d + 1)
    return [a for a in range(2, limit+1) if sieve[a]]


all_primes = prime_sieve(600625)
record(f"Independent Eratosthenes cross-check: pi(600625)={len(all_primes)}")
theorem = json.loads((SUBMITTED / "certificates/theorem.json").read_text())
for n, p, k, m, upper, count, b, c in [
    (6, 2153, 7, 330, 108900, 10028, 321, 448),
    (7, 4481, 8, 775, 600625, 48537, 769, 1024),
]:
    need(p in all_primes, f"Composite endpoint {p}")
    # Ordinary multiplication/modulus: independent of the C square recurrence.
    residues = {x*x % p for x in range(1, p)}
    need(0 not in residues and len(residues) == (p-1)//2, "Bad endpoint residue set")
    word = "".join("1" if a in residues else "0" for a in range(p))
    c_word = (HERE / f"independent-endpoint-{p}.txt").read_text().strip()
    endpoint = json.loads((SUBMITTED / f"certificates/a{n}-endpoint.json").read_text())
    need(word == c_word == endpoint["word_at_0_through_p_minus_1"], "Endpoint word mismatch")
    runs = list(re.finditer("1+", word))
    maximum = max(len(match[0]) for match in runs)
    starts = [match.start() for match in runs if len(match[0]) == maximum]
    need(endpoint["prime"] == p and maximum == n == endpoint["maximum_run"], "Endpoint maximum mismatch")
    need(endpoint["start"] in starts, "Submitted endpoint start is invalid")
    record(f"PASS endpoint {p}: maximum {maximum}; all longest-run starts {starts}; complete words equal")

    independent = (HERE / f"independent-a{n}-witnesses.txt").read_bytes()
    supplied = gzip.decompress((SUBMITTED / f"certificates/a{n}-witnesses.txt.gz").read_bytes())
    need(independent == supplied, f"Witness lists differ in case {n}")
    lines = independent.decode("ascii").splitlines()
    need(all(re.fullmatch(r"[0-9]+ [0-9]+", s) for s in lines), "Invalid witness line")
    rows = [tuple(map(int, line.split())) for line in lines]
    expected = [q for q in all_primes if p < q <= upper]
    need(len(rows) == count == len(expected), "Prime count mismatch")
    need([q for q, start in rows] == expected, "Missing, repeated, out-of-order, or composite prime")
    need(all(1 <= start <= q-k for q, start in rows), "Witness crosses zero/boundary")
    record(f"PASS a({n}) witnesses: {count} exact primes; first {rows[0]}; last {rows[-1]}; byte-for-byte equal to independent square-sieve list")
    record(f"SHA256 decompressed a({n}) witnesses: {hashlib.sha256(independent).hexdigest()}")

    actual_b = sum(math.comb(k, j)*(j-1) for j in range(1, k+1))
    need(actual_b == b == (k-2)*2**(k-1)+1, "Incorrect B coefficient")
    need(c == k*2**(k-1), "Incorrect C coefficient")
    margin = m*m-b*m-c
    need(upper == m*m and margin > 0 and 2*m >= b, "Invalid integer cutoff")
    case = next(case for case in theorem["cases"] if case["index"] == n)
    for key, value in {"candidate": p, "run_length": k, "M": m, "upper": upper, "B": b, "C": c}.items():
        need(case[key] == value, "Theorem JSON differs from verified arithmetic")
    record(f"PASS cutoff k={k}: B={b}; C={c}; M={m}; M^2={upper}; D={margin}")

# Attack the exceptional zero points and subset expansion on small examples.
cases_checked = 0
nonzero_error_cases = 0
for p in [q for q in all_primes if 11 <= q <= 97]:
    squares = {x*x % p for x in range(1, p)}
    chi = [0 if a == 0 else 1 if a in squares else -1 for a in range(p)]
    for k in range(2, 9):
        products = [math.prod(1+chi[(a+i) % p] for i in range(k)) for a in range(p)]
        count = sum(all(chi[(a+i) % p] == 1 for i in range(k)) for a in range(p))
        error = sum(products[(-i) % p] for i in range(k))
        need(sum(products) == 2**k * count + error, "Exceptional-point identity failed")
        need(0 <= error <= k*2**(k-1), "Exceptional-point error bound failed")
        sums = []
        for mask in range(1, 2**k):
            subset = [i for i in range(k) if mask & (1 << i)]
            total = sum(math.prod(chi[(a+i) % p] for i in subset) for a in range(p))
            need(total*total <= (len(subset)-1)**2 * p, "Character-sum bound failed in small check")
            sums.append(total)
        need(sum(products) == p + sum(sums), "Subset expansion failed")
        cases_checked += 1
        nonzero_error_cases += error != 0
record(f"PASS exact small-prime expansion/zero/character-bound checks: {cases_checked} cases, {nonzero_error_cases} with nonzero exceptional error")

for name, expected_hash in json.loads((SUBMITTED / "manifest.json").read_text()).items():
    need(hashlib.sha256((SUBMITTED / name).read_bytes()).hexdigest() == expected_hash, f"Submitted hash mismatch {name}")
record("PASS all 8 submitted manifest hashes (source files hashed, never executed)")
record(f"Total Python audit CPU seconds: {time.process_time()-begin:.3f}")
(HERE / "independent-audit.log").write_text("\n".join(log)+"\n")
