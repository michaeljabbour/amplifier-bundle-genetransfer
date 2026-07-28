#!/usr/bin/env python3
"""Fitness function for the HGT attractor — the scalar the run hill-climbs.

WHAT IS BEING MEASURED (the criterion, not the code): the attractor's whole job is
to drive every ledger row to a GREEN-GATED pr (state=implemented). A row reaches
`implemented` ONLY after both gates pass (the Commit node marks it), so
`implemented_frac` already bakes in "gate passed" as a precondition — you cannot
score by lowering quality. Fitness is deliberately conservative: `implemented_frac`
is the PROTECTED scalar the harness climbs and it must never decrease across a
healthy run (a monotone ratchet). `acknowledged` (gave-up / human handoff) drains
the queue but does NOT raise fitness — so "do less" scores nothing.

Ledger row: <slug>\t<target>\t<state>   state in {new, implemented, acknowledged}

Usage:
    python3 evals/fitness.py <ledger.tsv>
"""
from __future__ import annotations

import sys
from pathlib import Path


def read_rows(path: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def fitness(rows: list[tuple[str, str, str]]) -> dict:
    total = len(rows)
    denom = total or 1
    impl = sum(1 for r in rows if r[2] == "implemented")
    ack = sum(1 for r in rows if r[2] == "acknowledged")
    new = sum(1 for r in rows if r[2] == "new")
    return {
        "total": total,
        "implemented": impl,
        "acknowledged": ack,
        "new": new,
        "implemented_frac": round(impl / denom, 4),  # PROTECTED — climb this
        "resolved_frac": round((impl + ack) / denom, 4),  # queue drained
        "score": round(impl / denom, 4),  # headline fitness
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: fitness.py <ledger.tsv>", file=sys.stderr)
        return 2
    for k, v in fitness(read_rows(argv[1])).items():
        print(f"{k}\t{v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
