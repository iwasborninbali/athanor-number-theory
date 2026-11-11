"""Reproduce the certificate and tests on the pre-existing Sage VM."""
import os
from pathlib import Path
import subprocess
import sys

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    assert os.environ.get(name) == '1'
jobs = [
    ('certified-all.jsonl',['recertify.py','--bounds-only']),
    ('exact-all.jsonl',['independent_exact.py']),
    ('fresh-saturation.jsonl',['fresh_saturation.py']),
    ('suite-reproduction.jsonl',['run_suite.py']),
    ('geometry-crosscheck.jsonl',['check_geometry.py']),
    ('upstream-bound-audit.jsonl',['audit_upstream_bounds.py']),
    ('baseline-known11.jsonl',['baseline_known11.py']),
    ('s-integral-audit.jsonl',['audit_s_integral.py']),
    ('export.log',['export_certificate.py']),
]
for output,args in jobs:
    print('Running',args[0],flush=True)
    with open(output,'w') as handle:
        subprocess.run([sys.executable]+args,stdout=handle,check=True)
print(Path('recertification-summary.json').read_text())
