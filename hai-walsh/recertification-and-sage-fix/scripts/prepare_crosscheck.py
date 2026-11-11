"""Read public point tables and prepare exact, explicitly named test cases."""
import ast
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
labels = ['1701d1','1848f1','2082a1','3510n1','6514b1','177211a1',
          '23808e1','268740c1','285928a1','66432f1','92554e1']
files = json.loads((ROOT/'sources/ecdata-intpts-files.json').read_text())
needed = []
for f in files:
    match = re.fullmatch(r'intpts\.(\d+)-(\d+)', f['name'])
    if not match:
        continue
    lo,hi = map(int,match.groups())
    if any(lo <= int(re.match(r'\d+',label)[0]) <= hi for label in labels):
        needed.append(f)
records = {}
retrieval = []
for f in needed:
    path = ROOT/'sources'/('cremona-'+f['name'])
    if not path.exists():
        path.write_bytes(urllib.request.urlopen(f['download_url'],timeout=60).read())
    data = path.read_bytes()
    retrieval.append(dict(url=f['download_url'],file=str(path.relative_to(ROOT)),
                          sha256=hashlib.sha256(data).hexdigest()))
    for line in data.decode().splitlines():
        label,ainvs,xs = line.split()
        conductor = int(re.match(r'\d+',label)[0])
        if label in labels or conductor <= 100:
            records[label] = dict(label=label,ainvs=ast.literal_eval(ainvs),
                                  expected_x=ast.literal_eval(xs),
                                  source=str(path.relative_to(ROOT)),
                                  known_miss=label in labels)
assert all(label in records for label in labels)
for label, name, url in [
        ('1701d1','lmfdb-cremona1701d1','https://www.lmfdb.org/EllipticCurve/Q/1701d1'),
        ('1848f1','lmfdb-cremona1848f1','https://www.lmfdb.org/EllipticCurve/Q/1848f1'),
        ('2082a1','lmfdb-2082a1','https://www.lmfdb.org/EllipticCurve/Q/2082/a/1')]:
    text = (ROOT/'sources'/name).read_text()
    text = text[text.index('<p><h2> <a title="Integral points'):]
    raw = re.search(r'<textarea[^>]*>(.*?)</textarea>',text,re.S)[1]
    points = ast.literal_eval('['+raw+']')
    records[label]['lmfdb_points'] = [list(p) for p in points]
    records[label]['lmfdb_url'] = url
    records[label]['lmfdb_sha256'] = hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest()
    assert sorted(set(p[0] for p in points)) == records[label]['expected_x']
(ROOT/'evidence/crosscheck-input.json').write_text(json.dumps(list(records.values()),indent=2)+'\n')
(ROOT/'evidence/crosscheck-retrieval.json').write_text(json.dumps(retrieval,indent=2)+'\n')
print('Prepared',len(records),'curves, including',len(labels),'known problematic curves.')
