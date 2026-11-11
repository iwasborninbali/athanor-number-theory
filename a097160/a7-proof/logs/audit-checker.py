"""Fault-injection checks; run from the workspace with python3 logs/audit-checker.py."""
import gzip
import importlib.util
import json
from pathlib import Path
import tempfile

root=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('certificate_checker',root/'check.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def rejects(name, call):
    try:
        call()
    except ValueError as e:
        print('PASS reject',name,':',e)
    else:
        raise RuntimeError('accepted corrupt certificate: '+name)

with tempfile.TemporaryDirectory(dir=root/'logs') as td:
    tmp=Path(td)
    with gzip.open(root/'certificates/a7-witnesses.txt.gz','rt') as f:
        sample=[line for line in f if int(line.split()[0])<=4500]
    path=tmp/'sample.gz'
    path.write_bytes(gzip.compress(''.join(sample).encode()))
    print('PASS short baseline',m.finite_witnesses(path,4481,4500,8))
    path.write_bytes(gzip.compress(''.join(sample[1:]).encode()))
    rejects('omitted first prime',lambda:m.finite_witnesses(path,4481,4500,8))
    path.write_bytes(gzip.compress(('4483 1\n'+''.join(sample[1:])).encode()))
    rejects('invalid residue run',lambda:m.finite_witnesses(path,4481,4500,8))
    path.write_bytes(gzip.compress((''.join(sample)+sample[-1]).encode()))
    rejects('duplicate trailing prime',lambda:m.finite_witnesses(path,4481,4500,8))
    data=json.loads((root/'certificates/a7-endpoint.json').read_text())
    data['maximum_run']=8
    ep=tmp/'bad-endpoint.json';ep.write_text(json.dumps(data))
    rejects('incorrect endpoint maximum',lambda:m.endpoint(ep,4481,7))
    rejects('bad subset coefficient',lambda:m.analytic_cutoff(8,775,600625,768,1024))
    rejects('insufficient cutoff',lambda:m.analytic_cutoff(8,750,562500,769,1024))
