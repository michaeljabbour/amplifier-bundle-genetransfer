# amplifier-bundle-genetransfer

**HGT — the Horizontal Gene-Transfer attractor.** A self-contained Amplifier bundle
that packages a reusable, parameterized *capability-transfer* pipeline: it moves a
capability from a donor repo (any language) into **one or more host repos**,
re-expressed through each host's own seams — **never** by copying donor code — gated
by the host's unit suite **and** a real-terminal [forge](https://github.com/michaeljabbour/amplifier-skill-forge)
check, one PR per capability per host.

Where the earlier `gene-transfer` was *vertical* (one donor → one host, same
ecosystem), **HGT is horizontal**: across a species boundary (a foreign codebase),
into multiple hosts. `opencode → {newtui-py, newtui-rust}` is instance #1
(`examples/opencode/`).

## The three knobs

| Knob | What |
|---|---|
| **source(s)** | Donor repo(s), read-only, any language. You transfer the capability, not the code. |
| **host(s)** | Target repo(s), each `path:kind` (`python` / `rust` / `new:<lang>`). A host may be a **new/empty repo** — transfer #1 scaffolds its CI. |
| **scope** | Free-text: which capabilities transfer, what's excluded. Applied as a **gap-check first**. |

## What makes it a distinct type

- **Forge-woven QA at three points, not one final gate:** observe the real donor in
  forge, author the forge probe *before* the code (acceptance-first), then validate
  by booting the real host app(s). The terminal is the acceptance oracle.
- **Feature + tests + CI co-built as one vertical slice.** The local gate *is* the CI
  gate (per host kind) → no green-locally/red-in-CI tax. New host ⇒ CI ships with
  capability #1.
- **Cross-ecosystem + multi-host, first-class.** Donor language is irrelevant;
  heterogeneous hosts land the same capability in different layers via the ledger
  `target` (`a` / `ab` / `split`).

## Install & run

```sh
amplifier bundle add git+https://github.com/microsoft/amplifier-bundle-genetransfer@main
amplifier bundle use hgt          # /hgt mode + hgt-orchestrator/hgt-expert agents
```

Two launch paths:
- **Orchestrator-as-engine (recommended, proven):** activate `/hgt` or delegate to
  `hgt-orchestrator` — it gap-checks, seeds the ledger, and runs a max-parallel wave
  of self-delegated workers in git worktrees. This is how the campaigns actually ran.
- **run_pipeline engine:** use `bundles/hgt-interactive.yaml` (provides `run_pipeline`)
  and pass params (`DONOR_PATH`, `HOST_A_PATH`, `HOST_A_KIND`, …). See
  `context/hgt-runbook.md`.

## Layout

| Path | What |
|---|---|
| `bundle.md` · `behaviors/hgt-core.yaml` | Root bundle + composable capability set |
| `bundles/` | `hgt-pipeline` (headless) · `hgt-interactive` (run_pipeline) launchers |
| `agents/` | `hgt-orchestrator` (execute) · `hgt-expert` (explain/plan) |
| `modes/hgt.md` | `/hgt` orchestrator posture |
| `context/` | `hgt-awareness.md` (thin) · `hgt-runbook.md` (method) |
| `pipelines/` | `hgt.dot` (the attractor graph) · `ledger.py` (stdlib ledger) |
| `examples/opencode/` | Worked instance |
| `PRINCIPLES.md` · `docs/DESIGN_DECISIONS.md` | Non-negotiables · why it's shaped this way |

## Principles (full list in `PRINCIPLES.md`)

Re-express, never graft · the terminal is the acceptance oracle · gate == CI · never a
protected branch · obey the host · bounded & never stalled · gap-check first.
