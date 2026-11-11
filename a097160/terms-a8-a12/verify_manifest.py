#!/usr/bin/env python3
"""Check the certificate archive's recorded SHA-256 hashes (stdlib only)."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
for name,expected in manifest.items():
    path=(root/name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('manifest path escapes archive: '+name)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:
        raise ValueError('SHA-256 mismatch: '+name)
print(f'PASS {len(manifest)} SHA-256 hashes')
