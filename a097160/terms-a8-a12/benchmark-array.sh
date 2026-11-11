#!/bin/bash
set -euo pipefail
cd "$HOME/a097160/extend"
while [[ ! -f logs/full-a10-finished.txt ]]; do sleep 10; done
./scan-array 10 16801801 2 certificates/a9-array.tsv logs/scan-a9-array.json 5000000 > logs/scan-a9-array.stdout 2> logs/scan-a9-array.log
cmp certificates/a9.tsv certificates/a9-array.tsv
./scan-array 12 10000000 2 certificates/a11-array-pilot.tsv logs/scan-a11-array-pilot.json 2000000 > logs/scan-a11-array-pilot.stdout 2> logs/scan-a11-array-pilot.log
./scan-ordered 12 10000000 2 certificates/a11-ordered-pilot.tsv logs/scan-a11-ordered-pilot.json 2000000 > logs/scan-a11-ordered-pilot.stdout 2> logs/scan-a11-ordered-pilot.log
cmp certificates/a11-array-pilot.tsv certificates/a11-ordered-pilot.tsv
python3 - <<'PY'
import json,os
from pathlib import Path
x=json.loads(Path('logs/scan-a11-array-pilot.json').read_text())
y=json.loads(Path('logs/scan-a11-ordered-pilot.json').read_text())
if x['cpu_seconds']<y['cpu_seconds']:
 os.replace('scan-array','scan')
 Path('logs/array-selected.txt').write_text('array scanner selected after exact pilot comparisons\n')
PY
