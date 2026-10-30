"""CTF command-line: list challenges, read objectives, take hints, submit flags.

Flags are checked against salted SHA-256 hashes in challenges.json, so the
answer key does not contain plaintext flags. Progress is saved to progress.json.

    python ctf.py list
    python ctf.py show idor
    python ctf.py hint idor          # reveal the next hint
    python ctf.py submit idor 'FLAG{...}'
    python ctf.py score
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHALLENGES = ROOT / "challenges.json"
PROGRESS = ROOT / "progress.json"

TIER_ORDER = {"easy": 0, "medium": 1, "hard": 2}


def flag_hash(salt: str, flag: str) -> str:
    return hashlib.sha256(f"{salt}:{flag.strip()}".encode()).hexdigest()


def load_challenges() -> list[dict]:
    data = json.loads(CHALLENGES.read_text(encoding="utf-8"))
    return sorted(data, key=lambda c: (TIER_ORDER.get(c["tier"], 9), c["id"]))


def load_progress() -> dict:
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {"solved": [], "hints_used": {}}


def save_progress(progress: dict) -> None:
    PROGRESS.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def _get(challenges: list[dict], cid: str) -> dict | None:
    return next((c for c in challenges if c["id"] == cid), None)


def cmd_list(challenges, progress) -> int:
    solved = set(progress["solved"])
    print(f"{'STATUS':8}{'ID':12}{'TIER':8}{'PTS':5}TITLE")
    for c in challenges:
        status = "[x]" if c["id"] in solved else "[ ]"
        print(f"{status:8}{c['id']:12}{c['tier']:8}{c['points']:<5}{c['title']}")
    total = sum(c["points"] for c in challenges if c["id"] in solved)
    cap = sum(c["points"] for c in challenges)
    print(f"\nScore: {total}/{cap}  Solved: {len(solved)}/{len(challenges)}")
    return 0


def cmd_show(challenges, progress, cid) -> int:
    c = _get(challenges, cid)
    if not c:
        print(f"No challenge '{cid}'.", file=sys.stderr)
        return 2
    print(f"{c['title']}  [{c['tier']}, {c['points']} pts]")
    print(f"\nTarget : {c['target']}")
    print(f"Objective:\n  {c['objective']}")
    print(f"\nHints available: {len(c['hints'])}  (reveal with: python ctf.py hint {cid})")
    return 0


def cmd_hint(challenges, progress, cid) -> int:
    c = _get(challenges, cid)
    if not c:
        print(f"No challenge '{cid}'.", file=sys.stderr)
        return 2
    used = progress["hints_used"].get(cid, 0)
    if used >= len(c["hints"]):
        print("No more hints. See walkthroughs/ if you are truly stuck.")
        return 0
    print(f"Hint {used + 1}/{len(c['hints'])}: {c['hints'][used]}")
    progress["hints_used"][cid] = used + 1
    save_progress(progress)
    return 0


def cmd_submit(challenges, progress, cid, flag) -> int:
    c = _get(challenges, cid)
    if not c:
        print(f"No challenge '{cid}'.", file=sys.stderr)
        return 2
    if flag_hash(c["salt"], flag) == c["flag_sha256"]:
        if cid not in progress["solved"]:
            progress["solved"].append(cid)
            save_progress(progress)
        print(f"Correct! '{c['title']}' solved (+{c['points']} pts).")
        return 0
    print("Incorrect flag. Keep going — try a hint: python ctf.py hint " + cid)
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CTF lab runner")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    sub.add_parser("score")
    for name in ("show", "hint"):
        sp = sub.add_parser(name)
        sp.add_argument("id")
    sp = sub.add_parser("submit")
    sp.add_argument("id")
    sp.add_argument("flag")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    challenges = load_challenges()
    progress = load_progress()
    if args.command in ("list", "score"):
        return cmd_list(challenges, progress)
    if args.command == "show":
        return cmd_show(challenges, progress, args.id)
    if args.command == "hint":
        return cmd_hint(challenges, progress, args.id)
    if args.command == "submit":
        return cmd_submit(challenges, progress, args.id, args.flag)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
