# Evaluating HGT — three loops, honestly scoped

Reviewer feedback (from the author of the reality-check / DTU / evaluation
bundles) identified two real gaps, both conceded:

1. **The pipeline authors the acceptance artifacts it is graded against.**
   `PlanTransfer` writes the forge probe ("the probe is the spec",
   `pipelines/hgt.dot`) and `Implement` writes the unit tests — the same flow
   that must pass them. Gate *execution* is deterministic and node contexts are
   fresh (`truncate` fidelity), and the orchestrator "re-verifies gates
   independently" — but that is independent *execution* of self-authored
   criteria. Deterministic ≠ independent.
2. **`evals/hillclimb.py` is near-tautological as a technique signal.** Ledger
   rows only move forward; within-run monotonicity is close to guaranteed. It
   cannot say HGT-v2 beats HGT-v1.

## Loop 0 — what exists: the run monitor (inner)

`evals/fitness.py` + `hillclimb.py` — a ratchet over ledger snapshots. Honest
scope: run health + Goodhart tripwires (stall, un-complete, give-up-everything
scores 0). Not an objective function for the technique.

## Loop 1 — outer verification: grader independence

Adapted from [amplifier-bundle-reality-check](https://github.com/microsoft/amplifier-bundle-reality-check)
(intent-analyzer derives acceptance from *intent*, DTU-deployed validators
execute it, gap report follows), exploiting HGT's 1:1 advantage: the ground
truth is the **donor app itself**. A blind verifier — never reading `.ai/` or
the builder's tests/probe — observes the donor capability via forge, derives
its own checks, validates the host(s) in a DTU, and emits
`verified | rejected(findings)`. Rejected rows reopen once, then acknowledge
with findings. Ledger gains terminal state `verified`; the eval's protected
scalar becomes `verified_frac`.

## Loop 2 — the technique objective function: frozen answer key

Freeze a host at the commit *before* a real capability landed in it; donor = a
repo where the capability exists; run HGT; grade with the real commit's tests
(behavioral subset) against HGT's output. The number comes from outside the
loop. Climb by comparing HGT-v1 vs HGT-v2 on the identical frozen task, K≥3
repeats. For a whole-app-scale worked example (openai/codex TS→Rust, verified
from git history) and the contamination / test-coupling threat analysis, see
the sibling doc: `amplifier-bundle-genemigration/docs/EVALUATION.md`.

## Roadmap

1. Blind-verifier stage (closes Loop 1).
2. Frozen answer-key pilot via `amplifier-evaluation` + DTU (closes Loop 2).
3. Only then tune the technique, with Loop 2 as arbiter.
