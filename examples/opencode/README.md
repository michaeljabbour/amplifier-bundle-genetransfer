# Example instance — opencode → newtui (Python) + newtui-rust (Rust)

HGT **instance #1**: transfer capabilities from the SST **opencode** agent (a
TypeScript/Bun monorepo) into the two amplifier terminal clients.

## The three knobs

- **source:** `/Users/michaeljabbour/dev/opencode` (read-only; TypeScript)
- **hosts:**
  - Host A — `/Users/michaeljabbour/dev/amplifier-app-newtui` · `kind=python` ·
    owns the backend (kernel/model/commands) **and** the `serve` stdio protocol.
  - Host B — `/Users/michaeljabbour/dev/amplifier-app-newtui-rust` · `kind=rust` ·
    a **pure protocol client** of Host A's `amplifier-newtui serve` (codex-tui /
    codex-core split) — renders protocol state, owns no session/agent logic.
- **scope:** "Transfer opencode capabilities absent from BOTH clients; skip
  cloud/hosted/plugin-system/desktop features and anything already present."

Because Host B is a *client* of Host A, `target` maps to layer:
`a` (backend, Host A only — Rust gets it over the protocol) · `ab` (pure client UX,
both) · `split` (Host A backend/protocol first, then client in both).

## Env vars for a run

```sh
export DONOR_PATH=/Users/michaeljabbour/dev/opencode
export HOST_A_PATH=/Users/michaeljabbour/dev/amplifier-app-newtui   HOST_A_KIND=python
export HOST_B_PATH=/Users/michaeljabbour/dev/amplifier-app-newtui-rust HOST_B_KIND=rust
export FORGE_TOOL=/Users/michaeljabbour/.claude/skills/amplifier-skill-forge/tools/forge.py
export LEDGER_FILE=pipelines/hgt-ledger.tsv
export SCOPE="opencode caps absent from both clients; skip hosted/plugin/desktop"
```

## Candidate capabilities (after the gap-check prunes already-haves)

codemode-execute (split) · question-tool (split) · apply-patch-tool (a) · lsp-tool
(a) · prompt-stash (ab) · prompt-frecency-history (ab) · model-variant-cycle (split) ·
session-tags (split) · stats-dashboard (a) · sanitized-export-import (a).

**Skip** (out of scope / philosophy): cloud workspaces, ACP, Slack, Electron,
enterprise console, hosted stats, GitHub-Action bot, hosted share links, the ~30-hook
plugin system, bundled provider adapters, embedded SDK. **Verify-then-skip** (already
in newtui): sessions/fork/subagents/plan/permissions/providers/routing/MCP/skills/
notifications/themes/tool-invoke/reset.

> The full triage table + a ready-to-paste orchestrator launch prompt live in the
> newtui repo at `pipelines/OPENCODE.md` and `pipelines/opencode-run-prompt.md`
> (the first place this instance was drafted, before HGT was extracted here).
