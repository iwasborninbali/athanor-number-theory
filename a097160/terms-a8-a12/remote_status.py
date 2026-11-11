from pathlib import Path
import json,time,os
r=Path.home()/'a097160/extend'
d={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'reports':{},'progress':{}}
for n in range(8,13):
 for stage in ['scan','check']:
  p=r/f'logs/{stage}-a{n}.json'
  if p.exists():
   try:d['reports'][f'{stage}-a{n}']=json.loads(p.read_text())
   except (ValueError,OSError):pass
for name in ['scan-a11','scan-a12','check-a10-full','scan-a9-array','scan-a11-array-pilot','scan-a11-ordered-pilot']:
 p=r/f'logs/{name}.log'
 if p.exists():d['progress'][name]=p.read_text().splitlines()[-1:]
for name in ['scan-a11','scan-a12']:
 if name in d['reports']:d['progress'].pop(name,None)
if d['reports'].get('check-a10',{}).get('mode')=='full':d['progress'].pop('check-a10-full',None)
if 'scan-a12' in d['reports'] and 'check-a12' not in d['reports']:
 p=r/'logs/check-a12.log'
 if p.exists():
  lines=p.read_text().splitlines()
  d['progress']['scan-a12']=['independent a12 check: '+(lines[-1] if lines else 'initializing')]
d['active']=[]
for proc in Path('/proc').iterdir():
 if not proc.name.isdigit():continue
 try:
  if proc.joinpath('cwd').resolve()!=r:continue
  args=proc.joinpath('cmdline').read_bytes().split(b'\0')
  if not args or args[0]!=b'./scan':continue
  fields=proc.joinpath('stat').read_text().rsplit(')',1)[1].split()
  ticks=os.sysconf('SC_CLK_TCK')
  cpu=(int(fields[11])+int(fields[12]))/ticks
  elapsed=float(Path('/proc/uptime').read_text().split()[0])-int(fields[19])/ticks
  active=dict(pid=int(proc.name),k=int(args[1]),cpu_seconds=round(cpu,2),elapsed_seconds=round(elapsed,2),nice=os.getpriority(os.PRIO_PROCESS,int(proc.name)),affinity=sorted(os.sched_getaffinity(int(proc.name))))
  d['active'].append(active)
  if active['k']==13:
   previous=d['progress'].get('scan-a12') or ['k=13 initializing']
   d['progress']['scan-a12']=[previous[-1]+f' live_cpu={cpu:.1f}s elapsed={elapsed:.1f}s']
 except (OSError,ValueError,IndexError):pass
d['complete']=(r/'logs/finished.txt').exists() and (r/'logs/full-a10-finished.txt').exists()
d['array_selected']=(r/'logs/array-selected.txt').exists()
print(json.dumps(d))
