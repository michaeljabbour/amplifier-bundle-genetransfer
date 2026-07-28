# HGT Design Decisions

Why the graph and bundle are shaped this way. Grounded in an attractor-engine review.

## 1. Params reach tool_command via ENV VARS / run_pipeline, never mounted config.params
The loop-pipeline engine substitutes a mounted orchestrator's `session.orchestrator.
config.params` into **prompts only** — they live as a nested dict, not flat context
keys, so they never reach `tool_command`. A graph that did `cd $host_path` under that
launch path would get an empty shell var and `cd` to `$HOME`, misrouting silently.
**Decision:** `hgt.dot` reads params as UPPERCASE shell env vars with `${VAR:?msg}`
fail-loud guards at the loop head. This works under (a) `run_pipeline` (seeds flat
context keys that reach both prompts and tool_command) and (b) plain env-export before
`amplifier run`. `bundles/hgt-interactive.yaml` (run_pipeline) is the recommended
engine path; `bundles/hgt-pipeline.yaml` requires exported env vars.

## 2. `... && printf pass || printf fail` is load-bearing — never simplify it
Routing is EXACT-string match on the last non-empty **stdout** line. On a non-zero
exit the tool node FAILs *and leaves `tool.last_line` stale* — and condition edges are
still evaluated, so a stale `pass` could route a crashed gate to Commit. Every gate
node forces exit 0 with an explicit `|| printf fail`. Diagnostics go to files/stderr.

## 3. Two retry budgets, orthogonal (no double-count)
Our `.ai/hgt_retries` counter bounds the Implement→Validate→AnalyzeFailure **fix
loop** at 3. The engine's `default_max_retry=3` bounds **in-node** re-execution and
fires only on RETRY outcomes / transient exceptions (flaky LLM calls on box nodes) —
a gate printing `fail` at exit 0 is a SUCCESS outcome and is never engine-retried.
Different failures; kept both deliberately.

## 4. `truncate` fidelity → file-based handoff is required
Every LLM node runs in a fresh session (goal + run id only). State passes between
nodes through `.ai/hgt_*` files, not conversation. `default_thread_id` is dead weight
under `truncate` and is omitted.

## 5. Gate == CI, dispatched by host kind
`UnitValidate` runs the host's exact CI commands per `kind` (python: ruff+format+
pyright+pytest; rust: cargo test+clippy; `new:<lang>`: a scaffolded `./ci/gate.sh`).
This is what lets feature+tests+CI be co-built as one slice without a green-locally/
red-in-CI tax. A new host's CI lands with its first capability.

## 6. Ledger is a stdlib CLI, not a tool module
Per the tool-leverage-patterns DRY rule, the deterministic ledger's one home is
`pipelines/ledger.py`; the `.dot` and the orchestrator shell out to it. No L3 tool
module is shipped — none is needed until an agent must call the ledger directly.

## 7. `hgt-orchestrator` declares an inline orchestrator
Spawn merges an agent's `session:` onto the parent. Without an explicit non-pipeline
orchestrator, an `hgt-orchestrator` spawned as a pipeline node would inherit
loop-pipeline and recurse. It declares `loop-streaming` inline.

## 8. Extension path for >2 hosts (deferred until a 2nd instance needs it)
The gate/branch/commit dispatch is inlined for 1–2 hosts keyed by `kind`. A third host
kind or an N-host run lifts the dispatch into `pipelines/hgt_gates.sh` + `hgt_forge.sh`
(kind → gate/boot), keeping the `.dot` a pure orchestrator. Not built yet — until a
real second consumer exists, that indirection is ceremony.

## 9. Session durability requires the logging hook (DTU reality-check finding)
A self-contained bundle that omits `hooks-logging` produces runs whose sessions
exist only in memory: the CLI's end-of-run finalizer looks the session up in the
store (`session_store.py`), finds no directory (the logging hook is what creates
it), raises `Session '<id>' not found`, and never writes transcript/metadata —
no resume, no events.jsonl, no observability. Proven by A/B in a DTU (anchors
persisted; hgt did not; same cwd, same prompt). `hooks-logging` is therefore part
of hgt-core, config mirroring foundation `behaviors/logging.yaml`.

## 10. Loop 1 — the blind verifier is a separate GRAPH, not a node in the build loop
Independence is about who writes the rubric, so the verifier lives in its own
pipeline (`verify.dot`) with its own queue (`ledger.py earliest-implemented`), its
own artifacts namespace (`.ai/verify_*`), and explicit read-prohibitions on every
builder artifact. `verified` is the terminal ledger state; a verification failure
reopens the row once (implemented → new, findings attached — verifier→builder flow
is the allowed direction) and then acknowledges. The run monitor grows a
`--verifier` mode whose protected scalar is `verified_frac` and which tolerates the
now-legal reopen dip while still rejecting any row that leaves `verified`.
