"""Read-only source retrieval; no model calls or mathematical computation."""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
refs = {
    'issue-10152': 'https://api.github.com/repos/sagemath/sage/issues/10152',
    'issue-12095': 'https://api.github.com/repos/sagemath/sage/issues/12095',
    'issue-10973-comments': 'https://api.github.com/repos/sagemath/sage/issues/10973/comments?per_page=100',
    'sage-devel-projects': 'https://groups.google.com/g/sage-devel/c/dXKF2IQ7Oso',
    'sage-support-2016': 'https://groups.google.com/g/sage-support/c/pHr3prSdVpk',
    'lmfdb-2082a1': 'https://www.lmfdb.org/EllipticCurve/Q/2082/a/1',
    'lmfdb-1701d1': 'https://www.lmfdb.org/EllipticCurve/Q/1701/d/1',
    'lmfdb-1848f1': 'https://www.lmfdb.org/EllipticCurve/Q/1848/f/1',
    'cremona-intpts-000000-009999': 'https://raw.githubusercontent.com/JohnCremona/ecdata/master/intpts/intpts.000000-009999',
    'stroeker-deweger-1999': 'https://deweger.net/papers/%5B29%5DStdW-EllCubic-ActaArith%5B1999%5D.pdf',
}
records = []
for name, url in refs.items():
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Athanor-research-audit'})
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            destination = ROOT / 'sources' / name
            destination.write_bytes(data)
            rec = dict(name=name, url=url, final_url=response.url, bytes=len(data),
                       sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        rec = dict(name=name, url=url, error=repr(exc))
    print(json.dumps(rec), flush=True)
    records.append(rec)
(ROOT / 'evidence' / 'retrieval.json').write_text(json.dumps(records, indent=2) + '\n')
