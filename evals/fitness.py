#!/usr/bin/env python3
"""Fitness function for the HGT attractor — the scalars the run monitor tracks.

WHAT IS BEING MEASURED: the attractor drives every ledger row to a green-gated PR
(`implemented`), and Loop 1 (the blind verifier, pipelines/verify.dot) then drives
it to `verified` — independently confirmed against the donor's real behavior.
`implemented` bakes in the builder's own gates; `verified` bakes in an INDEPENDENT
rubric. `acknowledged` (gave up / failed verification twice) earns nothing.

Scalars:
  implemented_frac  rows the builder landed (intermediate once Loop 1 is in play)
  verified_frac     rows independently confirmed — Loop 1's protected scalar
  landed_frac       implemented + verified — the legacy protected scalar
  score             == landed_frac (headline)

Ledger row: <slug>\t<target>\t<state>  state in {new, implemented, verified, acknowledged}

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
    ver = sum(1 for r in rows if r[2] == "verified")
    ack = sum(1 for r in rows if r[2] == "acknowledged")
    new = sum(1 for r in rows if r[2] == "new")
    return {
        "total": total,
        "implemented": impl,
        "verified": ver,
        "acknowledged": ack,
        "new": new,
        "implemented_frac": round(impl / denom, 4),
        "verified_frac": round(ver / denom, 4),  # Loop-1 PROTECTED scalar
        "landed_frac": round((impl + ver) / denom, 4),  # legacy PROTECTED scalar
        "resolved_frac": round((impl + ver + ack) / denom, 4),
        "score": round((impl + ver) / denom, 4),
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
