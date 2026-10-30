"""CLI: run all detection rules over an event log and print alerts.

    python3 run_detections.py
    python3 run_detections.py --events data/events.json

Exits non-zero when any HIGH or CRITICAL alert fires (useful for automated
monitoring checks).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from detections import run_all

ROOT = Path(__file__).resolve().parent


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Run detection rules over an event log.")
    p.add_argument("--events", type=Path, default=ROOT / "data" / "events.json")
    args = p.parse_args(argv)

    events = json.loads(args.events.read_text(encoding="utf-8"))
    alerts = run_all(events)

    if not alerts:
        print("No alerts. Event log looks clean.")
        return 0

    print(f"{'SEVERITY':9}{'RULE':24}{'ENTITY':18}EVIDENCE")
    for a in alerts:
        print(f"{a['severity']:9}{a['rule']:24}{a['entity']:18}{a['evidence']}")

    high = [a for a in alerts if a["severity"] in ("CRITICAL", "HIGH")]
    print(f"\n{len(alerts)} alert(s), {len(high)} high/critical.")
    return 1 if high else 0


if __name__ == "__main__":
    raise SystemExit(main())
