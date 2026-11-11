#!/usr/bin/env python3
"""Small reproducible downloader; all downloads stay under sources/."""
import hashlib, json, pathlib, sys, urllib.request, datetime

root = pathlib.Path(__file__).resolve().parents[1] / 'sources'
root.mkdir(exist_ok=True)
for name, url in zip(sys.argv[1::2], sys.argv[2::2]):
    rec = {'name': name, 'url': url,
           'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (academic literature check)'})
        with urllib.request.urlopen(req, timeout=40) as f:
            data = f.read(20_000_000)
            rec.update(final_url=f.url, content_type=f.headers.get('Content-Type'),
                       bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        (root / name).write_bytes(data)
    except Exception as e:
        rec['error'] = repr(e)
    with (root / 'fetch.jsonl').open('a') as f:
        f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec), flush=True)
