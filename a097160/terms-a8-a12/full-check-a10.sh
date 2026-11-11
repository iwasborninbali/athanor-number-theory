#!/bin/bash
set -euo pipefail
cd "$HOME/a097160/extend"
cp logs/check-a10.json logs/check-a10-sample.json
cp certificates/sample-a10.tsv certificates/sample-a10-initial.tsv
./independent 11 84989961 full certificates/a10.tsv logs/check-a10-full.json certificates/sample-a10-full.tsv > logs/check-a10-full.stdout 2> logs/check-a10-full.log
cp logs/check-a10-full.json logs/check-a10.json
cp certificates/sample-a10-full.tsv certificates/sample-a10.tsv
date -u +%FT%TZ > logs/full-a10-finished.txt
