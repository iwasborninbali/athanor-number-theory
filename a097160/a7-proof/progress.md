# Progress

- 2026-11-10 23:43 UTC: Read Reble's complete note. Its method uses rational progressions and multiplicativity; integer windows alone are insufficient.
- Initial search (started 23:40 UTC): current OEIS still lists six terms. Screened targeted searches, the 27 citing titles in the scout's OpenAlex export, and recent 2024/2025 and October 2026 residue papers. No exact resolution located. Live OpenAlex/source retrieval is in progress.
- A simpler complete exclusion is available via the standard Weil bound, reducing the target to primes at most 600625. Derived coefficient B_8=769 and zero correction C_8=1024. Piloting the same argument for a(6) with cutoff 108900, B_7=321, C_7=448.
- Files are confined to this folder; no installs, paid calls, other agents, or external messages. Initial free disk: 16 GiB. One computational process at a time.
- 2026-11-10 23:44–23:49 UTC: Both complete finite lists generated, with zero failures: 10028 primes for a(6), 48537 for a(7). Independent stdlib checker passed (about 0.9 s). Verified the analytic tail margins 2522 and 3626 using integer arithmetic. Corrupt-certificate rejection tests passed. The all-primes target is proved via Weil plus finite witnesses; SAT/DRAT is unnecessary and was not used. Report, hashes and search record written.
