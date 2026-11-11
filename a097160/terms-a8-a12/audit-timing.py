from pathlib import Path
import json,datetime
r=Path.home()/'a097160/extend'
rows=[]
for p in sorted((r/'logs').glob('scan-*.json')):
 d=json.loads(p.read_text());end=p.stat().st_mtime;start=end-d['wall_seconds']
 rows.append((start,end,p.name,d['cpu_seconds']))
for name in ['check-a8.json','check-a9.json','check-a10-full.json','check-a11.json','check-a12.json']:
 if not (r/'logs'/name).exists():continue
 p=r/'logs'/name;d=json.loads(p.read_text());end=p.stat().st_mtime
 rows.append((end-d['wall_seconds'],end,name,d['cpu_seconds']))
fmt=lambda t:datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat(timespec='milliseconds')
for a,b,n,cpu in sorted(rows):print(fmt(a),fmt(b),n,'cpu=',cpu)
events=sorted([(a,1,n) for a,b,n,c in rows]+[(b,-1,n) for a,b,n,c in rows])
active=set();over=[];last=None
for t,change,name in events:
 if last is not None and len(active)>2:over.append(dict(start_utc=fmt(last),end_utc=fmt(t),seconds=t-last,jobs=sorted(active)))
 if change==1:active.add(name)
 else:active.remove(name)
 last=t
print('OVERLAPS',json.dumps(over))
(r/'logs/timing-audit.json').write_text(json.dumps(dict(intervals=[dict(start_utc=fmt(a),end_utc=fmt(b),name=n,cpu_seconds=c) for a,b,n,c in sorted(rows)],overlaps_above_two=over),indent=2)+'\n')
