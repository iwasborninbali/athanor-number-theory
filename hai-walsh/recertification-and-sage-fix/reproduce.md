The deliverable patch is `fix.patch`, against Sage develop
`026e931e47064f0a7fc095580119365518bfe7c0`. It can be reviewed or applied with
`git apply --check fix.patch` and `git apply fix.patch` in a checkout at that
commit. No installed Sage source was edited in this investigation.

The saved inputs and scripts are sufficient to reproduce all mathematical
checks without fetching data, installing packages, or calling paid services.
The original rank/descent inputs are in `sources/original_pari_descent.jsonl`;
the accepted curves and full bases are in `sources/input-classification.json`.
The exact finite checker is the previously independently audited lab checker,
saved verbatim as `sources/original_check.py`.

On the Mac, prepare and copy files only:

```sh
python3 scripts/stage_vm_inputs.py
ssh -o BatchMode=yes personal-vps 'mkdir -p ~/sage-intpts'
scp -q vm-inputs/* personal-vps:sage-intpts/
```

Run the mathematical work on the VM:

```sh
ssh -o BatchMode=yes personal-vps \
  'cd ~/sage-intpts && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 19 taskset -c 1 ~/athanor-vm/stark-83a/sage-env/bin/python reproduce_vm.py'
```

All mathematical scripts assert CPU affinity `{1}` and niceness at least 19.
The driver also checks the three single-thread environment settings. It
runs the certified bounds, exact finite exhaustion, full saturation, final
test suite, geometric normalization comparison, original-bound reproduction,
old-method counterexamples, and certificate export. The exporter refuses to
package the result if any of the required point-list comparisons, lattice
certificates or rank/saturation records fail.

The important final files are `classification-recertified.json`,
`recertification-summary.json`, `bounds-comparison.csv`, and the JSONL/log
files. Copies from this run are under `certificates/` and `evidence/`.
The function and its bounded-enumeration helper were tested with Sage's own
doctest parser/controller, including long tests; the source was extracted
into `scripts/upstream_doctests.py` with a local monkey patch preamble.

The proof is in `certificate-proof.md`. The separate optional
`s-integral-fail-closed.patch` applies **after** `fix.patch`; it is an interim
error guard for two S-integral fallback sites, not a complete S-integral repair.
