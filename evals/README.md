# HGT evals — simple hill-climbing eval

**What is measured (the criterion, before any code):** the attractor's one job is to
drive every ledger row to a green-gated PR. So the fitness the run hill-climbs is
`implemented_frac` — the fraction of ledger rows in state `implemented`. That state
is only ever set by the Commit node *after* both gates pass (unit suite + real-
terminal forge check), so the score bakes in quality as a precondition: the harness
cannot score by lowering the bar, and `acknowledged` (gave up / human handoff)
drains the queue but earns nothing — "do less" cannot score.

**The hill-climb property:** a healthy run only climbs. Two invariants (the ratchet):
1. `implemented_frac` is non-decreasing across successive ledger snapshots;
2. no row un-completes (`implemented` → `new`/`acknowledged`).

Any violation is a regression / Goodhart tripwire and fails the eval.

## Run it

```sh
python3 evals/hillclimb.py --self-test     # the eval proves it detects regressions
python3 evals/hillclimb.py --fixture       # demo curve over a bundled 4-snapshot run
python3 evals/fitness.py <ledger.tsv>      # score one ledger state
python3 evals/hillclimb.py s0.tsv s1.tsv…  # evaluate a REAL run's snapshot series
```

## Evaluating a real run

Snapshot the ledger as the run progresses (e.g. `cp $LEDGER_FILE snaps/$(date +%s).tsv`
after each loop, or from git history of the ledger file:
`git log -p --follow -- <ledger>` → materialize each version), then feed the ordered
snapshots to `hillclimb.py`. Exit 0 = the run climbed monotonically; exit 1 = it
regressed somewhere, with the offending step named.

## Honest limits

This eval scores the ATTRACTOR's convergence behavior — progress, monotonicity, and
queue integrity. It does **not** re-judge the quality of an individual transfer
beyond what the gates enforced (that judgment lives in the gates themselves and in
PR review). Keep it that way: one high-signal criterion beats ten noisy ones.
