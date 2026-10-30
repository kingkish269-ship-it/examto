#!/usr/bin/env python3
"""Rooms — a TryHackMe / Hackversity-style guided track.

Left side (theory + task + flag box) = this tool.
Right side (the machine)             = your terminal / Codespace.

    python3 rooms.py                 # list rooms and your progress
    python3 rooms.py show tm         # read a room's briefing + task
    python3 rooms.py submit tm <answer>   # submit the flag/answer, get graded

Each room teaches a topic, then asks you to DO something in the terminal and
capture a flag or answer. Flags are checked against hashes, so this file holds
no plaintext answers.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROOMS = json.loads((ROOT / "rooms.json").read_text(encoding="utf-8"))
PROGRESS = ROOT / ".rooms_progress.json"


def _h(answer: str) -> str:
    return hashlib.sha256(answer.strip().lower().encode()).hexdigest()


def _get(rid: str) -> dict | None:
    return next((r for r in ROOMS if r["id"] == rid), None)


def _done() -> set[str]:
    if PROGRESS.exists():
        return set(json.loads(PROGRESS.read_text()).get("done", []))
    return set()


def _save(done: set[str]) -> None:
    PROGRESS.write_text(json.dumps({"done": sorted(done)}))


def cmd_list() -> int:
    done = _done()
    print("Rooms — Application Security to DevSecOps\n")
    for r in ROOMS:
        mark = "[x]" if r["id"] in done else "[ ]"
        print(f"  {mark} {r['id']:6} {r['title']:34} ({r['topic']})")
    print(f"\n  {len(done)}/{len(ROOMS)} rooms completed")
    nxt = next((r for r in ROOMS if r["id"] not in done), None)
    if nxt:
        print(f"\nNext: python3 rooms.py show {nxt['id']}")
    else:
        print("\nAll rooms complete. You can talk through every topic from real work.")
    return 0


def cmd_show(rid: str) -> int:
    r = _get(rid)
    if not r:
        print(f"No room '{rid}'. Run: python3 rooms.py")
        return 2
    done = r["id"] in _done()
    print(f"=== {r['title']}  [{r['topic']}] ===   {'[COMPLETED]' if done else ''}\n")
    print("New here? You can't break anything. Read the theory, do the objectives")
    print("in order, and use the free hint if you get stuck.\n")
    print("LEARN")
    print(f"  {r['summary']}")
    print(f"  Full briefing: rooms/{r['dir']}/README.md\n")
    print("OBJECTIVES  (tick these off as you go — they are your notes)")
    for i, obj in enumerate(r["objectives"], 1):
        print(f"  [ ] {i}. {obj}")
    print(f"\nTASK\n  {r['task']}")
    print(f"\nSUBMIT\n  python3 rooms.py submit {rid} <your answer>")
    if r.get("hint"):
        print(f"\nHINT (free)\n  {r['hint']}")
    return 0


def cmd_submit(rid: str, answer: str) -> int:
    r = _get(rid)
    if not r:
        print(f"No room '{rid}'.")
        return 2
    if _h(answer) == r["answer_sha256"]:
        done = _done()
        done.add(rid)
        _save(done)
        print(f"Correct! Room '{r['title']}' complete.")
        nxt = next((x for x in ROOMS if x["id"] not in done), None)
        print(f"Next: python3 rooms.py show {nxt['id']}" if nxt else "All rooms done!")
        return 0
    print("Not correct. Re-read the briefing and try the task again.")
    print(f"  Hint: {r.get('hint', 'work the terminal task in the briefing')}")
    return 1


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        return cmd_list()
    if argv[0] == "show" and len(argv) > 1:
        return cmd_show(argv[1])
    if argv[0] == "submit" and len(argv) > 2:
        return cmd_submit(argv[1], " ".join(argv[2:]))
    print("Usage: python3 rooms.py | show <id> | submit <id> <answer>")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
