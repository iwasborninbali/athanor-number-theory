"""Copy the already saved sources, inputs and drivers into a flat VM bundle."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
dest = ROOT/'vm-inputs'
dest.mkdir(exist_ok=True)
for name in ['certified_bounds.py','recertify.py','independent_exact.py',
             'fresh_saturation.py','load_fixed.py','test_all_fixed.py',
             'test_crosscheck.py','upstream_doctests.py','run_doctests.py',
             'test_guards.py','run_suite.py','verify_lattice_records.py',
             'export_certificate.py','check_geometry.py','audit_upstream_bounds.py',
             'baseline_known11.py','audit_s_integral.py','reproduce_vm.py']:
    shutil.copyfile(ROOT/'scripts'/name,dest/name)
for source,name in [
        ('sources/ell_rational_field.fixed.py','ell_rational_field.fixed.py'),
        ('sources/ell_rational_field.pinned.py','ell_rational_field.pinned.py'),
        ('sources/input-classification.json','classification.json'),
        ('sources/original_check.py','original_check.py'),
        ('sources/original_pari_descent.jsonl','original_pari_descent.jsonl'),
        ('evidence/crosscheck-input.json','crosscheck-input.json')]:
    shutil.copyfile(ROOT/source,dest/name)
print('Prepared',dest)
