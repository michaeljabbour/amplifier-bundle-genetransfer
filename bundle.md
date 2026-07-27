---
bundle:
  name: hgt
  version: 0.1.0
  description: >
    HGT (Horizontal Gene-Transfer) — a parameterized capability-transfer attractor.
    Ports a capability from a donor repo (any language) into one or more host repos,
    re-expressed through each host's own seams — never copying donor code — gated by
    the host unit suite AND a real-terminal forge check, one PR per capability per host.

# Self-contained: every source is a full git+https URL; only the bundle's own
# `hgt:` namespace is used. No `- bundle: foundation`, no bare `foundation:` refs.
includes:
  - bundle: hgt:behaviors/hgt-core

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main
---

# HGT — Horizontal Gene-Transfer

A reusable **attractor archetype** for moving a capability across a *species
boundary* (a foreign codebase, any language) into **one or more host repos**,
expressed in each host's own machinery — never by grafting foreign code.

- **The graph:** `hgt:pipelines/hgt.dot` — one capability per loop, gated by the
  host unit suite + a real-terminal forge check before any PR.
- **The tool:** `hgt:pipelines/ledger.py` — stdlib transfer-state ledger.
- **The posture:** `/hgt` mode + the `hgt-orchestrator` agent drive the proven
  orchestrator-as-engine loop (self-delegated workers in git worktrees).

See `README.md` for the three knobs (source / hosts / scope), the forge-woven QA
model, and how to instantiate. `PRINCIPLES.md` carries the non-negotiables.
