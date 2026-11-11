#!/usr/bin/env python3
"""Hash immutable evidence; exclude this manifest and its checker's own output."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
files=[root/'check.py']
for directory in ['certificates','scripts','sources']:
 files.extend(p for p in (root/directory).rglob('*') if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts)
for name in ['sage_api.txt','sage_pilot.log','sage_classify.log','sage_classify2.log','sage_metadata.err','pari_descent.log','pari_retry.log','sage_try91.log','sage_try91_stop.txt']:
 p=root/'logs'/name
 if p.exists():files.append(p)
files=sorted(set(files))
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(root)) for p in files]
(root/'certificates/SHA256SUMS').write_text('\n'.join(lines)+'\n')
print(f'Hashed {len(files)} files')
