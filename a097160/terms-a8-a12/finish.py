#!/usr/bin/env python3
"""Package finished, audited computations. Does no large mathematical scan."""
from pathlib import Path
import hashlib
import json
import math
import gzip
import io
import tarfile
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p):return json.loads((ROOT/p).read_text())

def main():
    audit=data('logs/audit-final.json')
    assert audit['status']=='PASS'
    cases=audit['cases'];ns=[x['n'] for x in cases]
    assert ns==list(range(8,max(ns)+1)) and all(x['square_audited'] and x['sample_witnesses_checked'] for x in cases)
    last=max(ns)
    rows={n:[tuple(map(int,l.split())) for l in (ROOT/f'certificates/a{n}.tsv').read_text().splitlines()[1:]] for n in ns}
    for c in cases:
        n=c['n']
        assert sha(ROOT/f'certificates/a{n}.tsv') == c['certificate_sha256'], 'audit/certificate hash mismatch'
        check=data(f'logs/check-a{n}.json')
        assert check['mode']==c['independent_mode'] and check['checked_count']==c['independent_checked'], 'stale checker metadata'
    for n in ns[:-1]:
        assert rows[n]==[r for r in rows[last] if r[1]<n+1]
    terms={m:max(p for p,length,s in rows[last] if length==m) for m in range(1,last+1)}
    assert [terms[m] for m in range(1,8)]==[5,17,53,193,457,2153,4481]
    sequence=','.join(str(terms[n]) for n in range(1,last+1))
    (ROOT/'b097160-certified.txt').write_text(''.join(f'{n} {terms[n]}\n' for n in range(1,last+1)))
    draft=f'''A097160 update draft -- Alex will submit; nothing has been published.

DATA
{sequence}

EXTENSIONS
Terms a(7)-a({last}) certified by an explicit Weil character-sum cutoff and exhaustive prime scans, with independent verification as detailed in the certificate archive. - _Alex_, Nov 11 2026

COMMENTS
For k=n+1 and an odd prime p>k, let N_k(p) count runs of k consecutive nonzero quadratic residues. Expanding the product of 1+Legendre symbols and applying Weil's squarefree character-sum bound gives N_k(p)>=(p-B_k*sqrt(p)-C_k)/2^k, where B_k=(k-2)*2^(k-1)+1 and C_k=k*2^(k-1). For the integer M_k in the certificate, M_k^2-B_k*M_k-C_k>0 and 2*M_k>=B_k, so every prime p>=M_k^2 has a k-run. A complete scan of all primes p<M_k^2 lists every exception and its exact longest run; the greatest exception of length n gives a(n). The archive contains source, full exceptional-prime lists, cutoff arithmetic and independent-check coverage: [CERTIFICATE_ARCHIVE_URL].

Suggested LINKS addition
Alex, <a href="[CERTIFICATE_ARCHIVE_URL]">Certified terms of A097160: proof, source and exceptional-prime certificates</a>.

Editorial note for submitter
The included b097160-certified.txt extends the n,a(n) table through the last certified term.
The old proposed-continuation comment and the 2015 extension remain useful history, but its phrase "are still unknown" should be marked as historical after accepting this update. This package independently recertifies a(7)=4481 as well as all six earlier terms. Independent complete rescans and sampled larger checks are distinguished in result.md; do not describe sampled checks as complete.
'''
    (ROOT/'oeis-draft.txt').write_text(draft)
    (ROOT/'progress-snapshot.md').write_text((ROOT/'progress.md').read_text())
    source_map = {str(n): ('scan-baseline.c' if n <= 9 else 'scan-mask.c' if n == 10 else 'scan-ordered.c' if n == 11 or not (ROOT/'logs/array-selected.txt').exists() else 'scan.c') for n in ns}
    (ROOT/'source-map.json').write_text(json.dumps({n:dict(source=f,sha256=sha(ROOT/f)) for n,f in source_map.items()},indent=2)+'\n')
    mainfiles=['source-map.json','progress-snapshot.md','algorithm-notes.md','b097160-certified.txt','verify_manifest.py','audit-timing.py','scan.c','scan-baseline.c','scan-table.c','scan-mask.c','scan-ordered.c','scan-array.c','independent.c','audit.py','validate.py','cutoffs.json','run.sh','README.md','oeis-draft.txt','finish.py','full-check-a10.sh','benchmark-array.sh','post-benchmark.sh','monitor.py','remote_status.py']
    paths=[ROOT/f for f in mainfiles]
    cache_hashes={str(p.relative_to(ROOT/'sources')):sha(p) for p in (ROOT/'sources').rglob('*') if p.is_file() and p.name not in ('source-audit.md','source-hashes.json')}
    (ROOT/'sources/source-hashes.json').write_text(json.dumps(dict(note='Raw literature caches retained locally; archive contains source audit, URLs and cache fingerprints only.',cache_sha256=cache_hashes),indent=2)+'\n')
    paths.extend([ROOT/'sources/source-audit.md',ROOT/'sources/source-hashes.json'])
    for d in ['certificates','logs']:
        paths.extend(p for p in (ROOT/d).rglob('*') if p.is_file() and p.stat().st_size)
    manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    paths.append(ROOT/'manifest.json')
    with (ROOT/'certificate-archive.tar.gz').open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
            with tarfile.open(fileobj=gz,mode='w') as tar:
                for p in sorted(paths):
                    rel=str(p.relative_to(ROOT));b=p.read_bytes();info=tarfile.TarInfo('a097160-extension/'+rel)
                    info.size=len(b);info.mtime=0;info.mode=0o644;info.uid=info.gid=0
                    tar.addfile(info,io.BytesIO(b))
    elapsed=(datetime.now(timezone.utc)-datetime(2026,11,10,23,51,39,tzinfo=timezone.utc)).total_seconds()
    result=[]
    add=result.append
    add('**Established: '+', '.join(f"a({n}) = {terms[n]}" for n in ns)+'.**\n')
    add(f'Together with the six previously certified terms and a(7)=4481, this gives `{sequence}`. Each new value is the greatest prime with longest run **exactly** its index. The finite scans include every prime below its explicit cutoff; the standard Weil theorem proves the infinite tail. The exception lists also independently reproduce all earlier terms, including a(7).\n')
    add(f'Programme wall elapsed from the initial audit to packaging: {elapsed/3600:.3f} hours.\n')
    add('All computation used the existing VM via SSH, with nice 10. Early scanner/checker processes shared core 2, with at most two running concurrently. During a(12), its single scanner thread was later allowed affinity {2,3}, still using at most one CPU at a time. The Costas processes were left running. No installations, paid calls, publication, delegation or messages to other people were used. Local work was source editing, literature retrieval and small metadata operations. Times below are measured wall/CPU seconds from the retained reports.\n')
    add('**Analytic certificate.** For an odd prime p>k, extend the Legendre symbol by chi(0)=0 and put T=sum over a in F_p of product over i=0,...,k-1 of (1+chi(a+i)). At the k distinct zero-containing starting points the product lies between 0 and 2^(k-1). At all remaining starting points it is 2^k for an all-residue block and zero otherwise. Thus T=2^k*N_k+E with 0<=E<=C_k=k*2^(k-1). No run crosses zero; every zero-free block has a representative in 1,...,p-1.\n')
    add('Expanding T gives p from the empty subset. For a nonempty subset S, the polynomial product of (X+i), i in S, has |S| distinct roots modulo p. Weil gives absolute character sum at most (|S|-1)*sqrt(p). Hence T>=p-B_k*sqrt(p), where the sum of binomial(k,j)*(j-1) over j=1,...,k is B_k=(k-2)*2^(k-1)+1. Therefore\n\n`N_k(p) >= (p-B_k*sqrt(p)-C_k)/2^k`.\n')
    add('This independently checks the predecessor’s lemma. The external mathematical input is the classical squarefree Weil bound, as in [Conrad, equation (2.3)](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/QuadraticResiduePatterns.pdf). It is a conventional computer-assisted proof, not a formalization of Weil.\n')
    add('For the minimal integer M below, D=M^2-B_k*M-C_k>0 and 2*M>=B_k. For every real t>=M, t^2-B_k*t-C_k=D+(t-M)*(t+M-B_k)>=D>0. Thus every prime p>=M^2 has a k-run. The excluded finite interval is exactly 2<=p<M^2. All arithmetic is integer; audit.py independently re-sums the subsets and checks minimality of M.\n')
    add('| n | k | B_k | C_k | M | M² | D |\n|---:|---:|---:|---:|---:|---:|---:|')
    for c in cases:add('| '+' | '.join(str(c[t]) for t in ['n','k','B','C','M','cutoff','margin'])+' |')
    add('\n**Exact finite certificates.** Each TSV is the complete list of primes in the finite interval that lack a k-run. Every row contains `prime exact_longest_run first_start_of_that_maximum`. The longest run is computed over the entire word at 1,...,p-1, including for every small prime; p=2 has maximum one. The endpoint is selected from rows of length exactly n.\n')
    add('| n | a(n) | First maximum start | All primes scanned | Exceptions | Certificate |\n|---:|---:|---:|---:|---:|---|')
    for c in cases:
        n=c['n'];p=terms[n];s=next(s for q,m,s in rows[n] if q==p)
        add(f'| {n} | {p} | {s} | {c["prime_count"]} | {c["exceptions"]} | [a{n}.tsv](certificates/a{n}.tsv) |')
    add('\nThe lists nest exactly: filtering the largest list for longest_run<k gives each earlier list. Existence of an n-run at each endpoint is checked as part of its full exact maximum; merely lacking an (n+1)-run is never used as a substitute.\n')
    add('**Independent checks.** The primary C scanner uses a segmented Eratosthenes sieve and binary Jacobi symbols. Exact small-denominator reciprocity tables and prime-exponent parity masks accelerate the evaluations. Candidate starts are skipped only after finding a nonresidue that blocks every skipped window. The first successful window is therefore the first k-run. Exceptions are rescanned fully. The final source is scan.c; the original scans used scan-baseline.c for n=8,9, scan-mask.c for n=10, scan-ordered.c for n=11, and the source recorded in source-map.json for later n. Complete pilot scans with the optimized versions gave byte-identical lists for a(8) and a(9).\n')
    add('The separately written independent.c imports no primary routines or witnesses. It implements its own odd-only bit sieve and sequential run counting. It evaluates prime arguments by Euler’s criterion, using modular exponentiation, and composite arguments by multiplicativity with its own factor sieve. In full mode it recomputes every prime’s presence or absence of a k-run and every exceptional prime’s full maximum and first maximum start. In sample mode it still enumerates every prime and checks every listed exception fully, but searches for a k-run only at the deterministically selected additional primes.\n')
    add('| n | Coverage | Total primes evaluated | Hash-selected primes | Exact exceptions checked |\n|---:|---|---:|---:|---:|')
    for c in cases:add(f'| {c["n"]} | {c["independent_mode"]} | {c["independent_checked"]} | {c["independent_random_sample"]} | {c["exceptions"]} |')
    add('\nThe sample and exception sets may overlap; the evaluated-prime count counts distinct primes. The deterministic sample is exactly those primes p for which `splitmix64(p XOR 0xa09716020261111) % 10000 == 0`, with the standard unsigned 64-bit constants in independent.c. Files `certificates/sample-aN.tsv` list the selected primes and recomputed truncated maxima/starts; positive maxima are truncated at k. In sampled cases the primary scan establishes completeness; the independent checker does **not** establish that no unlisted exception exists at an unselected prime. It checks all listed primes for primality, ordering, exact maxima and starts, and its independently enumerated total prime count agrees.\n')
    add('The third implementation, audit.py, trial-divides every listed exception and constructs its full residue word by enumerating nonzero squares. It confirms every exact maximum and first start, all endpoint selections, cutoff arithmetic and report agreement. It also validates every recorded sample selection, its union with the exceptions, and every sample run witness using Python Euler exponentiation; see logs/audit-final.json. The small boundary audit independently checks every prime below 1000 for k=2,...,14, and rejects five corrupted a(8) lists: omitted p=2, false maximum, inserted composite, duplicate tail, and omitted endpoint. See logs/validation.json. The Python audit’s p=2 square-word special case was corrected before its successful final audit.\n')
    add('**Measured times.** Primary times include sieve/table initialization and the complete finite scan. Independent times include its sieve and all indicated checks.\n')
    add('| n | Primary wall | Primary CPU | Independent wall | Independent CPU |\n|---:|---:|---:|---:|---:|')
    for c in cases:
        n=c['n'];p=data(f'logs/scan-a{n}.json');q=data(f'logs/check-a{n}.json')
        add(f'| {n} | {p["wall_seconds"]:.3f} | {p["cpu_seconds"]:.3f} | {q["wall_seconds"]:.3f} | {q["cpu_seconds"]:.3f} |')
    add('\nLogs preserve optimization pilots and any initially sampled check subsequently replaced by a complete check. README.md gives build and reproduction commands; cutoffs.json supplies every exact upper limit. No precomputed run witnesses are required by the independent checker.\n')
    add('**Comparison with the historical values.** The current [OEIS entry](https://oeis.org/A097160/internal) and its [b-file](https://oeis.org/A097160/b097160.txt) contain only six DATA terms. The [December 2015 history](https://oeis.org/history?seq=A097160&start=10) removes 17041 and 23473 in revision 12, then 4481 and 9857 as unproved in revision 18. Reble’s [August 2, 2014 note](https://oeis.org/A097160/a097160.txt) proves the first six terms and proposes 4481, 9857, 25793, 60961, 132113, 324673. The certified new values agree with that proposal wherever covered. The removed 17041 really has longest run nine, but 25793 is larger; 23473 has longest run ten, but 60961 is larger.\n')
    assert any(p==17041 and m==9 for p,m,s in rows[last])
    assert any(p==23473 and m==10 for p,m,s in rows[last])
    add('Reble’s mechanism uses multiplicativity and rational arithmetic progressions, with a separate finite check at exceptional prime divisors; it gives a(6) an upper bound of 12919 and reports about 660000 proof lines. This work uses the classical character-sum cutoff instead. It does not reconstruct his large case proof or claim a new general analytic method. Saved sources, revision markup and access notes are under sources/. The shareable archive includes URLs, the source audit and cache SHA-256 fingerprints; raw literature downloads remain local.\n')
    nextcut=next(c for c in data('cutoffs.json') if c['n']==last+1)
    add(f'**Stopping point.** No value of a({last+1}) is claimed. Its analogous cutoff is {nextcut["upper_exclusive"]:,}.\n')
    pilot_path=ROOT/'logs/scan-a13-pilot.json'
    if pilot_path.exists() and last==12:
        pilot=json.loads(pilot_path.read_text())
        estimate_primes=nextcut['upper_exclusive']/(math.log(nextcut['upper_exclusive'])-1)
        estimate_hours=estimate_primes*pilot['cpu_seconds']/pilot['prime_count']/3600
        add(f'The explicit timing pilot for k=14 scanned [{pilot["lower"]:,},{pilot["upper_exclusive"]:,}), containing {pilot["prime_count"]:,} primes, in {pilot["cpu_seconds"]:.3f} CPU seconds. Scaling that measured rate to roughly {estimate_primes/1e6:.1f} million primes below the next cutoff estimates {estimate_hours:.1f} CPU hours for this scanner, before independent checking. This is a planning estimate, not an exact prime count or a certificate for a(13); it exceeds the remaining allowance. The pilot and its full interval are retained in logs/scan-a13-pilot.json and certificates/a13-pilot.tsv.\n')
    else:
        add('Compared with the last completed scan, the larger prime population and doubled target-pattern search imply roughly an order of magnitude more work, exceeding the remaining six-hour allowance.\n')
    add('The completed scope and hourly record are in progress.md, with an archived snapshot in progress-snapshot.md.\n')
    add('**SHA-256.** These hashes identify the complete essential exception certificates.\n')
    add('| File | SHA-256 |\n|---|---|')
    for c in cases:
        n=c['n'];add(f'| certificates/a{n}.tsv | `{sha(ROOT/f"certificates/a{n}.tsv")}` |')
    add(f'\nThe full manifest covers {len(manifest)} files, including all proof/checker sources, reports, certificates, source audit/fingerprints and the OEIS draft. `manifest.json`: `{sha(ROOT/"manifest.json")}`.\n')
    add(f'\n[Certificate archive](certificate-archive.tar.gz), { (ROOT/"certificate-archive.tar.gz").stat().st_size:,} bytes: `{sha(ROOT/"certificate-archive.tar.gz")}`. The archive deliberately excludes this result report and the changing progress log, storing a fixed progress snapshot instead and avoiding a circular hash.\n')
    add('\n[oeis-draft.txt](oeis-draft.txt) is ready for Alex to review and submit; its archive URL is a placeholder. The plain table is b097160-certified.txt. Nothing has been submitted.\n')
    (ROOT/'result.md').write_text('\n'.join(result))
    print(json.dumps(dict(status='PACKAGED',terms=terms,archive_sha256=sha(ROOT/'certificate-archive.tar.gz'),manifest_sha256=sha(ROOT/'manifest.json')),indent=2))

if __name__=='__main__':main()
