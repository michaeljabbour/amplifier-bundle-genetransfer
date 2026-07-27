# HGT — Horizontal Gene-Transfer (awareness)

This session can run **HGT**: transfer a capability from a donor repo into one or
more host repos, re-expressed through each host's own seams (never copying donor
code), gated by the host unit suite **and** a real-terminal forge check, one PR per
capability per host.

**Ways in**
- **`/hgt` mode** — orchestrator posture for a transfer run.
- **`hgt-orchestrator` agent** — `delegate(agent="hgt:hgt-orchestrator", …)` to drive
  the loop (self-delegated workers in git worktrees; the proven engine).
- **`hgt-expert` agent** — questions about the archetype, the graph, or how to
  instantiate for a given source/host/scope.
- **The graph:** `hgt:pipelines/hgt.dot`; **the ledger tool:** `hgt:pipelines/ledger.py`.

**When to reach for it:** "port these capabilities from repo X into repo(s) Y",
cross-ecosystem capability transfer, keeping two client implementations at parity.
It **re-expresses**; it never grafts foreign code. Read `PRINCIPLES.md` before a run.
