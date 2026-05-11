# Run Protocol — Twin Prime Project

Use this protocol whenever the user asks to continue the Twin Prime / Beyond the Parity Barrier project.

## Source of truth

1. Read `PROJECT_STATE.md` first.
2. Read `WORK_QUEUE.md` second.
3. Use the latest continuation ledger and the latest combined note packet as the mathematical starting point.
4. Prefer conjecture-facing progress over manuscript polish unless the active queue item says otherwise.

## Standard run procedure

When asked to continue:

1. Identify the latest completed note and the next queued task.
2. Draft 5–10 logical technical notes unless a stop condition is reached earlier.
3. Save each note as Markdown under the appropriate folder, e.g. `notes/7BI/`.
4. Produce one combined continuation file for the run.
5. Update `PROJECT_STATE.md`.
6. Update `WORK_QUEUE.md`.
7. Update the continuation ledger under `ledgers/`.
8. If using GitHub issues, close or comment on completed issues and create follow-up issues for the next tasks.

## Standard technical-note structure

Each note should include:

- Status
- Purpose
- Setup
- Main verdict or theorem target
- Proof sketch, audit, or obstruction analysis
- Consequences for the project map
- Next-step pointer

Use `NOTE_TEMPLATE.md` when drafting new notes.

## Stop conditions

Stop early if:

- the next step requires an external source/citation not available in the repo or uploaded files;
- additional notes would only restate an already documented barrier;
- the active track is invalidated by a new obstruction;
- a coherent packet of 5–10 notes and a ledger update has been completed;
- the user explicitly interrupts with a new instruction.

## Update discipline

Every run should leave the repo resumable. At minimum, update:

- latest completed note;
- latest combined packet;
- unresolved dependencies;
- next recommended step;
- work queue checkboxes or issue statuses.

## Current default priority

Unless the user says otherwise, prioritize:

\[
\boxed{\text{Technical Note 7BI.47 — Multiset-Labelled Affine-C3 State Space and Entropy Functional.}}
\]
