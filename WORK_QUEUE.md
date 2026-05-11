# Work Queue — Twin Prime Project

_Last updated: 2026-05-10._

This queue is the operational task list for future ChatGPT/GitHub runs. Use `RUN_PROTOCOL.md` as the execution protocol and `PROJECT_STATE.md` as the source of truth for current state.

## P0 — Conjecture-facing mechanism track

### Track 7BI — multiset-labelled affine-C3

- [ ] **7BI.47 — Multiset-Labelled Affine-C3 State Space and Entropy Functional**
  - Define the multiset-labelled shifted factorization state.
  - Define the entropy functional that retains prime-absorption history.
  - Include collision/recoverability caveats.
- [ ] **7BI.48 — Prime-Absorption Collision and Recoverability Lemma**
  - Determine when rough-window prime labels are recoverable from the shifted factorization multiset.
  - Identify collision configurations and whether they are negligible.
- [ ] **7BI.49 — Rough-Cell Entropy Accumulation Toy Theorem**
  - Prove or refute a toy entropy accumulation lemma under affine dilation.
  - Test against parity-adversary models.
- [ ] **7BI.50 — mAffine-C3 to Structured ARDO Reduction**
  - Formalize the bridge from multiset-labelled affine-C3 to `ARDO_3^str`.

### Track 7BJ — positivity bridge

- [ ] **7BJ.1 — Chen-Type Positivity Bridge Architecture**
  - State the exact bridge from Chen-type lower bound plus parity upgrade to twin-prime positivity.
- [ ] **7BJ.2 — Prime vs Rough-Semiprime Signed Main-Term Separation**
  - Identify the signed main-term control needed to separate primes from rough semiprimes.
- [ ] **7BJ.3 — Structured Parity Upgrade Target Lemma**
  - Define the parity upgrade needed after the Chen-type bridge.

### Track 7BK — structured ARDO

- [ ] **7BK.1 — Structured ARDO Coefficient Class v2**
  - Replace arbitrary TV-dual coefficients by the actual cell-routed structured coefficients when possible.
- [ ] **7BK.2 — Structured ARDO Stress Test**
  - Test major arcs, bilinear energy, and diagonal obstructions under structured coefficients.

## P1 — Manuscript preservation track

- [ ] **7BH.11 — Manuscript Draft v1.0 Consolidated Markdown**
  - Combine 7BH manuscript sections into one coherent draft.
  - Preserve TODO markers for citations and proof-port checks.
- [ ] **7BH.12 — Citation and Proof-Port Cleanup**
  - Verify exact statements needed for `PASC_{5/8}^{adm}` and `SS-RFBDH_3^{adm}`.

## P2 — Repository automation

- [ ] Add a script to rebuild a chronological note index.
- [ ] Add a script to concatenate selected note packets into an archive.
- [ ] Add a GitHub Actions workflow for link/TODO checks.
- [ ] Add issue templates for technical notes and proof-port audits.

## Stop conditions for a run

Stop a run early if:

- the next step requires an external citation check unavailable from the repo;
- the next notes would only restate known barriers;
- a new obstruction invalidates the current track;
- a coherent packet of 5–10 notes and ledger updates has been produced.
