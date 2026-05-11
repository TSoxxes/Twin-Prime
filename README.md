# Twin Prime Project

This repository is the working space for the **Twin Prime / Beyond the Parity Barrier** research program developed through the ChatGPT project thread.

The project is currently split into two complementary tracks:

1. **Manuscript preservation track**: preserve the conditional two-gate theorem developed in the 7BG/7BH notes.
2. **Conjecture-facing mechanism track**: pursue new parity-breaking mechanisms, especially the 7BI affine/multiset-labelled convolution-entropy route and the Chen-type positivity bridge.

## Current frontier

The manuscript-stage conditional theorem is:

\[
\mathrm{PASC}_{5/8}^{\mathrm{adm}}
+
\mathrm{SS\text{-}RFBDH}^{\mathrm{adm}}_3
+
\mathrm{ARDO}_3(\eta)
+
\mathrm{AvSAT}_{\mathrm{crit}}(\eta)
\Longrightarrow
\mathrm{WFBV}^{\mathrm{dual}}_\lambda(2/3+\eta')
\]

for every \(0<\eta'<\eta\).

The conjecture-facing route now prioritizes:

- C3 / affine convolution-entropy decrement;
- multiset-labelled shifted factorization states;
- structured ARDO rather than arbitrary TV-dual ARDO;
- Chen-type positivity bridge plus parity upgrade.

## Repository layout

```text
PROJECT_STATE.md       # live project status and next step
WORK_QUEUE.md          # prioritized task queue
RUN_PROTOCOL.md        # how future ChatGPT/GitHub runs should proceed
NOTE_TEMPLATE.md       # standard note template
notes/                 # technical notes and combined continuations
ledgers/               # continuation and decision ledgers
gates/                 # definitions of external gates and hypotheses
manuscript/            # manuscript drafts and assembly plans
.github/ISSUE_TEMPLATE # issue templates for task tracking
```

## Current recommended next step

Start from the latest 7BI continuation and draft:

\[
\boxed{\text{Technical Note 7BI.47 — Multiset-Labelled Affine-C3 State Space and Entropy Functional.}}
\]

Use `RUN_PROTOCOL.md` for future work sessions.
