from pathlib import Path
import os,time,json
pid=1143339;p=Path('/proc')/str(pid)
assert p.joinpath('cwd').resolve()==Path.home()/'a097160/extend'
a=p.joinpath('cmdline').read_bytes().split(b'\0')
assert a[:2]==[b'./scan',b'13']
assert len(list(p.joinpath('task').iterdir()))==1
assert os.getpriority(os.PRIO_PROCESS,pid)==10
before=sorted(os.sched_getaffinity(pid));os.sched_setaffinity(pid,{2,3})
d=dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),pid=pid,threads=1,nice=10,affinity_before=before,affinity_after=sorted(os.sched_getaffinity(pid)),reason='one scanner thread may migrate between the two permitted cores as other VM jobs move')
(Path.home()/'a097160/extend/logs/affinity-adjustment.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d))
