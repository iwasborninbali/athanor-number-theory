"""Run final tests sequentially; the driver and all children inherit CPU 1/nice 19."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
jobs = [
    ('guards',[sys.executable,'test_guards.py']),
    ('doctests-final',[sys.executable,'run_doctests.py']),
    ('crosscheck',[sys.executable,'test_crosscheck.py']),
    ('patched-all',[sys.executable,'test_all_fixed.py']),
    ('lattice-certificates',[sys.executable,'verify_lattice_records.py']),
]
source_sha = hashlib.sha256(Path('ell_rational_field.fixed.py').read_bytes()).hexdigest()
for name,command in jobs:
    begin = time.monotonic()
    print(json.dumps(dict(event='start',job=name,source_sha256=source_sha,
                          utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                          affinity=list(os.sched_getaffinity(0)),nice=os.nice(0))),flush=True)
    try:
        with open(name+'.log','w') as output:
            result = subprocess.run(command,stdout=output,stderr=subprocess.STDOUT,timeout=1800)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 'timeout'
    print(json.dumps(dict(event='finish',job=name,exit_code=code,
                          seconds=time.monotonic()-begin)),flush=True)
