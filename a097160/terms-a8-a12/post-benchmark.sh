#!/bin/bash
set -euo pipefail
cd "$HOME/a097160/extend"
while ! python3 - <<'PY'
from pathlib import Path
import json
try:
 x=json.loads(Path('logs/scan-a11-array-pilot.json').read_text())
 y=json.loads(Path('logs/scan-a11-ordered-pilot.json').read_text())
 if x['cpu_seconds']<y['cpu_seconds']:
  assert Path('logs/array-selected.txt').exists()
except (OSError,ValueError,AssertionError):
 raise SystemExit(1)
PY
do sleep 5; done
cmp certificates/a9.tsv certificates/a9-array.tsv
cmp certificates/a11-array-pilot.tsv certificates/a11-ordered-pilot.tsv
if [[ ! -f logs/array-selected.txt ]]; then cp scan-ordered.c scan.c; fi
cp logs/validation.json logs/validation-ordered.json
python3 validate.py > logs/validation.json 2> logs/validation-final.log
cp logs/validation.json logs/validation-finalscanner.json
set +e
timeout 180 ./scan 14 8005000000 8000000000 certificates/a13-pilot.tsv logs/scan-a13-pilot.json 1000000 > logs/scan-a13-pilot.stdout 2> logs/scan-a13-pilot.log
pilot_status=$?
set -e
printf '%s\n' "$pilot_status" > logs/a13-pilot-exit.txt
python3 - <<'PY'
from pathlib import Path
import os,signal,time
p=Path('/proc/1107185')
assert p.joinpath('cwd').resolve()==Path.home()/'a097160/extend'
assert p.joinpath('cmdline').read_bytes().split(b'\0')[:2]==[b'bash',b'run.sh']
os.kill(1107185,signal.SIGCONT)
Path('logs/driver-resumed.txt').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' after validation and a13 timing pilot\n')
PY
