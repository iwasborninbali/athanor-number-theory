#!/usr/bin/env python3
"""Light certificate/metadata audit; independent full scans use independent.c.
Enumerates square residues to audit every listed exception. No Legendre/Jacobi
routine or primary witness is reused. Stdlib only; heavy audits belong on VM.
"""
import argparse
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent

def require(ok, why):
    if not ok:
        raise ValueError(why)

def load_certificate(path, k, upper):
    lines = path.read_text().splitlines()
    require(lines[0] == f'# prime longest_run first_maximum_start; k={k} interval=[2,{upper})', 'incorrect header')
    rows = [tuple(map(int, line.split())) for line in lines[1:]]
    require(all(len(r) == 3 for r in rows), 'incorrect row')
    require(all(rows[i][0] < rows[i+1][0] for i in range(len(rows)-1)), 'unsorted/duplicate prime')
    return rows

def mix64(x):
    mask=(1<<64)-1
    x=(x+0x9e3779b97f4a7c15)&mask
    x=((x^(x>>30))*0xbf58476d1ce4e5b9)&mask
    x=((x^(x>>27))*0x94d049bb133111eb)&mask
    return x^(x>>31)

def audit_sample(n, k, upper, rows, checker):
    lines=(ROOT/f'certificates/sample-a{n}.tsv').read_text().splitlines()
    require(lines and lines[0]=='# prime measured_or_truncated_maximum first_maximum_start; splitmix64 fixed seed 0xa09716020261111, modulus 10000', 'sample header')
    sample=[tuple(map(int,l.split())) for l in lines[1:]]
    require(len(sample)==checker['sample_count'], 'sample count')
    require(all(sample[i][0]<sample[i+1][0] for i in range(len(sample)-1)), 'sample sorting')
    exceptional={p:(m,a) for p,m,a in rows}
    for p,m,a in sample:
        require(2<=p<upper and mix64(p^0xa09716020261111)%10000==0, f'sample selection {p}')
        require(1<=m<=k and 1<=a<=p-m, f'sample bounds {p}')
        if p in exceptional:
            require((m,a)==exceptional[p], f'sample exception {p}')
        else:
            require(m==k, f'sample positive not truncated at k: {p}')
        require(all(pow(x,(p-1)//2,p)==1 for x in range(a,a+m)), f'Python Euler sample witness {p}')
    if checker['mode']=='sample':
        overlap=sum(p in exceptional for p,m,a in sample)
        require(checker['checked_count']==len(rows)+len(sample)-overlap, 'sample union count')
    return len(sample)

def audit_case(n, squares=True):
    k = n+1
    # Deliberately recompute B by enumerating subsets, rather than trust formula.
    B = sum(mask.bit_count()-1 for mask in range(1, 1 << k))
    C = sum(2**(k-1) for _ in range(k))
    M = B
    while M*M-B*M-C <= 0:
        M += 1
    upper = M*M
    require(2*M >= B and M > k, 'bad cutoff monotonicity/domain')
    require((M-1)**2-B*(M-1)-C <= 0, 'nonminimal M')
    expected = next(c for c in json.loads((ROOT/'cutoffs.json').read_text()) if c['n'] == n)
    require(expected == dict(n=n,k=k,B=B,C=C,M=M,upper_exclusive=upper,margin=M*M-B*M-C), 'cutoff metadata')
    rows = load_certificate(ROOT/f'certificates/a{n}.tsv', k, upper)
    require(rows and rows[0] == (2,1,1), 'p=2 boundary')
    for p, length, start in rows:
        require(2 <= p < upper and 1 <= length < k and 1 <= start <= p-length, f'row bounds {p}')
        require(all(p % d for d in range(2, isqrt(p)+1)), f'nonprime {p}')
        if squares:
            word = bytearray(p)
            if p == 2:
                word[1] = 1
            # r and p-r have the same square: enumerate one of each pair.
            for r in range(1, (p+1)//2):
                word[r*r % p] = 1
            run = maximum = first = 0
            for a in range(1, p):
                run = run+1 if word[a] else 0
                if run > maximum:
                    maximum, first = run, a-run+1
            require((maximum,first) == (length,start), f'wrong exact maximum/start {p}')
    endpoint = max(p for p,m,a in rows if m == n)
    primary = json.loads((ROOT/f'logs/scan-a{n}.json').read_text())
    checker = json.loads((ROOT/f'logs/check-a{n}.json').read_text())
    for label, data in [('primary',primary),('independent',checker)]:
        require(data['k'] == k and data['upper_exclusive'] == upper, f'{label} wrong interval/k')
        require(data['endpoint'] == endpoint and data['exception_count'] == len(rows), f'{label} exception metadata')
    require(primary['lower'] == 2, 'wrong lower bound')
    require(checker['status'] == 'PASS', 'checker did not pass')
    require(primary['prime_count'] == checker['prime_count'], 'prime count disagreement')
    require(checker['mode'] in ('full','sample'), 'checker mode')
    require(n > 9 or checker['mode'] == 'full', 'a8/a9 need full independent coverage')
    if checker['mode'] == 'full':
        require(checker['checked_count'] == checker['prime_count'], 'incomplete full check')
    audit_sample(n,k,upper,rows,checker)
    return dict(n=n,endpoint=endpoint,k=k,B=B,C=C,M=M,cutoff=upper,margin=M*M-B*M-C,
                prime_count=primary['prime_count'],exceptions=len(rows),
                independent_mode=checker['mode'],independent_checked=checker['checked_count'],
                independent_random_sample=checker['sample_count'],square_audited=squares,sample_witnesses_checked=True,
                certificate_sha256=hashlib.sha256((ROOT/f'certificates/a{n}.tsv').read_bytes()).hexdigest())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('n', type=int, nargs='+')
    parser.add_argument('--metadata-only',action='store_true')
    args = parser.parse_args()
    started = time.perf_counter()
    results = [audit_case(n,not args.metadata_only) for n in args.n]
    print(json.dumps(dict(status='PASS',cases=results,seconds=time.perf_counter()-started),indent=2))

if __name__ == '__main__':
    main()
