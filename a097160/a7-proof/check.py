#!/usr/bin/env python3
"""Independent stdlib-only checker for the two complete cutoff certificates.

This file does not import or run the search/packaging programs. It checks:
  * the integer arithmetic of the analytic cutoff in result.md (Weil's
    standard character-sum theorem is the mathematical input);
  * endpoint primality and the complete residue word by enumerating squares;
  * EVERY prime in each remaining finite interval, by trial division;
  * the supplied run witness by Euler's criterion.

Run from any directory: python3 /path/to/check.py
"""
import gzip
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
CERT = ROOT / 'certificates'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def primes_through(limit):
    """Trial division, independent of the search program's Eratosthenes sieve."""
    if limit >= 2:
        yield 2
    divisors = [2]
    for n in range(3, limit + 1, 2):
        prime = True
        for q in divisors:
            if q*q > n:
                break
            if n % q == 0:
                prime = False
                break
        if prime:
            # Only divisors up to sqrt(limit) will ever be needed.
            if n <= isqrt(limit):
                divisors.append(n)
            yield n


def endpoint(path, expected_prime, expected_length):
    data = json.loads(path.read_text())
    p = data['prime']
    require(p == expected_prime, 'wrong endpoint prime')
    require(p >= 3 and all(p % q for q in range(2, isqrt(p) + 1)),
            f'endpoint {p} is not prime')
    residue = bytearray(p)
    for r in range(1, p):
        residue[r*r % p] = 1
    word = ''.join(map(str, residue))
    require(data['word_at_0_through_p_minus_1'] == word,
            f'incorrect complete residue word at {p}')
    maximum = max(map(len, word.split('0')))
    require(maximum == expected_length == data['maximum_run'],
            f'wrong maximum run length at {p}: {maximum}')
    start = data['start']
    require(isinstance(start, int) and 1 <= start <= p-expected_length,
            'endpoint witness out of range')
    require(word[start:start+expected_length] == '1'*expected_length,
            'bad endpoint witness')
    return maximum, start


def analytic_cutoff(k, M, upper, B, C):
    require(isinstance(k, int) and 2 <= k <= 16, 'bad run length')
    require(isinstance(M, int) and M > k, 'bad cutoff square root')
    # Enumerate subsets independently of the generator's closed formula.
    b = sum(mask.bit_count()-1 for mask in range(1, 1 << k))
    c = sum(1 << (k-1) for _ in range(k))
    require(B == b and C == c, 'incorrect analytic coefficients')
    require(upper == M*M, 'upper cutoff is not M squared')
    require(2*M >= B, 'quadratic need not increase beyond cutoff')
    margin = M*M - B*M - C
    require(margin > 0, 'Weil lower bound not strictly positive at cutoff')
    # For every real t >= M:
    # t^2-Bt-C = margin + (t-M)(t+M-B) >= margin > 0.
    return margin


def finite_witnesses(path, lower, upper, k):
    count = 0
    largest_end = 0
    with gzip.open(path, 'rt', encoding='ascii') as stream:
        for p in primes_through(upper):
            if p <= lower:
                continue
            line = stream.readline()
            require(bool(line), f'missing prime {p}')
            fields = line.split()
            require(len(fields) == 2, f'bad witness line for prime {p}')
            q, start = map(int, fields)
            require(q == p, f'coverage failure: expected prime {p}, got {q}')
            require(1 <= start <= p-k, f'run at {p} leaves 1..p-1')
            for x in range(start, start+k):
                require(pow(x, (p-1)//2, p) == 1,
                        f'nonresidue or zero in witness at {p}, {x}')
            count += 1
            largest_end = max(largest_end, start+k-1)
        require(stream.read() == '', 'unexpected trailing witness data')
    return count, largest_end


def hashes():
    manifest = json.loads((ROOT/'manifest.json').read_text())
    for name, expected in manifest.items():
        path = ROOT/name
        require(path.resolve().is_relative_to(ROOT), 'manifest path escapes folder')
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f'SHA-256 mismatch: {name}')
    return len(manifest)


def main():
    t0 = time.perf_counter()
    nhashes = hashes()
    meta = json.loads((CERT/'theorem.json').read_text())
    require(meta['format'] == 'quadratic-residue-cutoff-v1', 'unknown format')
    cases = meta['cases']
    require([(c['index'], c['candidate']) for c in cases] == [(6, 2153), (7, 4481)],
            'wrong claimed results')
    for case in cases:
        n, p, k = case['index'], case['candidate'], case['run_length']
        require(k == n+1, 'wrong exclusion length')
        margin = analytic_cutoff(k, case['M'], case['upper'], case['B'], case['C'])
        maximum, start = endpoint(CERT/case['endpoint'], p, n)
        count, last = finite_witnesses(CERT/case['witnesses'], p, case['upper'], k)
        print(f'PASS a({n}) = {p}: endpoint maximum {maximum} at {start}; '
              f'{count} primes in ({p}, {case["upper"]}]; '
              f'Weil-cutoff margin {margin}; largest witness endpoint {last}')
    print(f'PASS {nhashes} file hashes; elapsed {time.perf_counter()-t0:.3f} seconds')
    print('Mathematical input: Weil\'s standard bound, as stated and applied in result.md.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, EOFError, json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
