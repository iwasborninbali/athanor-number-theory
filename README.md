# athanor-number-theory

**Archived release v1.1** (12 Nov 2026, a(12) second rescan): Zenodo [10.5281/zenodo.24163515](https://doi.org/10.5281/zenodo.24163515); v1.0: [10.5281/zenodo.24139689](https://doi.org/10.5281/zenodo.24139689) (all versions: [10.5281/zenodo.24139688](https://doi.org/10.5281/zenodo.24139688)).

Certified computations on long-stalled number-theory questions (November 2026). See also [fourcover-search](https://github.com/iwasborninbali/fourcover-search): generators for two Mordell curves left open in the Best–Matschke data.

| Folder | Question (source) | Result | Status |
|---|---|---|---|
| [`a097160/`](a097160/) | OEIS [A097160](https://oeis.org/A097160): the largest prime whose longest run of consecutive quadratic residues has length n. Six terms were certified; a(7) and a(8) were removed as unproved in 2015. | **a(7) = 4481, a(8) = 9857, a(9) = 25793, a(10) = 60961, a(11) = 132113, a(12) = 324673** | See below |
| [`hai-walsh/`](hai-walsh/) | All integer solutions of (x²−1)/(y²+1) = (z²±1)² (Hai–Walsh, Acta Arith. 145, 2010, Open Problem) | Complete classification for every 1 ≤ y ≤ 100 except the plus sign at y = 73, 91, 97: 13 members of the known family plus the known exception (2177, 4, 23) | Independently verified, with the dependencies stated in the folder |

### A097160

- **Own repository:** this sequence now has its own repository, [oeis-A097160](https://github.com/iwasborninbali/oeis-A097160), which the OEIS entry links. The `a097160/` folder here is kept as archived in the Zenodo releases.

- **Method.** Weil's character-sum bound gives an explicit cutoff above which every prime has a run of n+1 residues. Below the cutoff a complete scan **determines** a(n), it does not only check a candidate.
- **a(7):** the proof is independently audited (`a097160/a7-audit/`). Buell and Hudson (BIT 24, 1984) very likely covered a(7) and a(8) already; their tables were not accessible to us.
- **a(8)–a(12):** each was reproduced by a separately written full rescan (the `guide_check_*` programs in `terms-a8-a12/`), and a(10) also by a third program.
- **a(12):** the second full rescan (`guide_check_qrrun2.c`, 2 shards, all primes below 2,030,313,481) finished on 12 Nov 2026. Its list of 2,760 exceptional primes, with their longest runs, is identical to the primary certificate `certificates/a12.tsv`, and gives a(12) = 324673 (`terms-a8-a12/logs/guide-check-a12.json`).
- **Old OEIS values:** revisions once listed a(9) = 17041 and a(10) = 23473. Both were removed as incorrect, and these scans confirm they were wrong.

### Hai–Walsh, and a defect found in SageMath

The integral points of 179 elliptic curves were first listed with SageMath's `integral_points()`. An independent audit found that this function substitutes an unjustified lattice bound when its reduction inequality fails. This is a known defect (Sage issues #10152, #27015; open PR #43044), and it can lose points: we reproduced 12 omissions on 11 curves.

We therefore re-certified all 179 curves with a separately derived elliptic-logarithm certificate that avoids the defect. The solution list is unchanged. The patch and details are in `hai-walsh/recertification-and-sage-fix/` and in [athanor-software-patches](https://github.com/iwasborninbali/athanor-software-patches).

## Provenance and credit

These results come from a programme on long-stalled published questions. AI research agents worked under the direction of the author of record (Aleksei Kudriashov, ORCID 0009-0006-8885-5338), who takes responsibility for the content:
- OpenAI GPT-6.1 "Sol" cores ran the searches, proofs and independent audits;
- Anthropic Claude orchestrated them.

Every result was checked by a separate session that did not run the solver's code. The checks are in each folder: certificates, stdlib checkers and audit reports. Downloaded third-party papers are not redistributed here.

We claim priority only as far as the dated literature searches recorded in each folder go. Corrections are welcome as issues or pull requests, from people and AI agents alike.

## License

Code: MIT. Data, certificates and text: CC BY 4.0. Third-party inputs (e.g. the Costas array catalogue) keep their original terms and are credited where used.
