#!/usr/bin/env python3
"""Read-only VM monitor, local hourly progress record; no mathematical scan."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,time
root=Path(__file__).resolve().parent
next_hour=datetime(2026,11,11,0,51,39,tzinfo=timezone.utc).timestamp()
seen=set()
while True:
 t=time.time()
 cmd=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','-o','ServerAliveInterval=10','-o','ServerAliveCountMax=1','personal-vps','python3 ~/a097160/extend/remote_status.py']
 try:
  response=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
  if response.returncode:raise RuntimeError(response.stderr.strip())
  d=json.loads(response.stdout)
  with (root/'logs/monitor.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
  (root/'logs/latest-status.json').write_text(json.dumps(d,indent=2)+'\n')
  parts=[d['utc']]
  for name,report in sorted(d['reports'].items()):
   if name not in seen or (name=='check-a10' and report['mode']=='full' and 'full-a10' not in seen):
    parts.append(f'{name}: endpoint={report["endpoint"]}, primes={report["prime_count"]}, exceptions={report["exception_count"]}'+(f', mode={report["mode"]}' if 'mode' in report else ''))
    seen.add(name)
    if name=='check-a10' and report.get('mode')=='full':seen.add('full-a10')
  for name in ['scan-a11','scan-a12','check-a10-full']:
   if d['progress'].get(name):parts.append(name+': '+d['progress'][name][-1])
  if d['array_selected']:parts.append('array scanner selected')
  print('\n'.join(parts),flush=True)
  if time.time()>=next_hour:
   with (root/'progress.md').open('a') as f:
    f.write('\n## '+d['utc']+' (hourly monitor)\n\n')
    for p in parts[1:]:f.write('- '+p+'\n')
   while next_hour<=time.time():next_hour+=3600
  if d['complete']:print('ALL COMPUTATIONS COMPLETE',flush=True);break
 except Exception as e:print('monitor retry: '+str(e),flush=True)
 time.sleep(max(1,55-(time.time()-t)))
