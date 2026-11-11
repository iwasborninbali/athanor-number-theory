#!/bin/bash
set -euo pipefail
cd "$HOME/a097160/extend"
date -u +%FT%TZ > logs/started.txt
./independent 9 3222025 full certificates/a8.tsv logs/check-a8.json certificates/sample-a8.tsv > logs/check-a8.stdout 2> logs/check-a8.log
for spec in '9 10 16801801 full' '10 11 84989961 sample' '11 12 419553289 sample' '12 13 2030313481 sample'; do
  read -r n k upper mode <<< "$spec"
  date -u +%FT%TZ > "logs/a$n-started.txt"
  ./scan "$k" "$upper" 2 "certificates/a$n.tsv" "logs/scan-a$n.json" 20000000 > "logs/scan-a$n.stdout" 2> "logs/scan-a$n.log"
  ./independent "$k" "$upper" "$mode" "certificates/a$n.tsv" "logs/check-a$n.json" "certificates/sample-a$n.tsv" > "logs/check-a$n.stdout" 2> "logs/check-a$n.log"
  date -u +%FT%TZ > "logs/a$n-finished.txt"
done
date -u +%FT%TZ > logs/finished.txt
