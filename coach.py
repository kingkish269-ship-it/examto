#!/usr/bin/env python3
"""Self-guided coach for the security labs.

Runs the whole program for you without anyone's help. It tells you the next
task, runs the check itself, and grades you with instant PASS/FAIL. Progress is
saved locally, so you can stop and resume any time.

    python3 coach.py              # show progress and the next task
    python3 coach.py task         # show the current task in detail
    python3 coach.py check        # grade the current task; advance on PASS
    python3 coach.py list         # all tasks and their status
    python3 coach.py reset        # start over

No internet, no account, no interaction with anyone required.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CURRICULUM = ROOT / "curriculum.json"
PROGRESS = ROOT / ".coach_progress.json"


def load_curriculum() -> list[dict]:
    return json.loads(CURRICULUM.read_text(encoding="utf-8"))


def load_done() -> set[str]:
    if PROGRESS.exists():
        return set(json.loads(PROGRESS.read_text(encoding="utf-8")).get("done", []))
    return set()


def save_done(done: set[str]) -> None:
    PROGRESS.write_text(json.dumps({"done": sorted(done)}, indent=2), encoding="utf-8")


def _interpreter(lab: str) -> str:
    """Prefer a lab's virtualenv python if it exists, else system python3."""
    venv = ROOT / lab / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else "python3"


def current_step(curriculum: list[dict], done: set[str]) -> dict | None:
    for step in curriculum:
        if step["id"] not in done:
            return step
    return None


def _progress_bar(done: set[str], total: int) -> str:
    n = len(done)
    filled = int((n / total) * 20) if total else 0
    return f"[{'#' * filled}{'.' * (20 - filled)}] {n}/{total}"


def cmd_status(curriculum, done) -> int:
    print("Security Labs — self-guided coach")
    print(_progress_bar(done, len(curriculum)))
    step = current_step(curriculum, done)
    if step is None:
        print("\nAll tasks complete. You have worked through every lab. Well done.")
        return 0
    print(f"\nNext: [{step['lab']}] {step['title']}")
    print("Run 'python3 coach.py task' for details, then do it and run "
          "'python3 coach.py check'.")
    return 0


def cmd_list(curriculum, done) -> int:
    for step in curriculum:
        mark = "[x]" if step["id"] in done else "[ ]"
        print(f"{mark} {step['lab']:22} {step['title']}")
    print("\n" + _progress_bar(done, len(curriculum)))
    return 0


def cmd_task(curriculum, done) -> int:
    step = current_step(curriculum, done)
    if step is None:
        print("All tasks complete.")
        return 0
    print(f"[{step['lab']}] {step['title']}\n")
    print("Why it matters:")
    print(f"  {step['teach']}\n")
    print("Do this:")
    print(f"  {step['do']}\n")
    v = step["verify"]
    if v.get("setup"):
        print("First-time setup for this lab (run inside the lab folder):")
        print(f"  {v['setup']}\n")
    print("When done: python3 coach.py check")
    return 0


def _run(cmd: str, cwd: Path, timeout: int = 180) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                              text=True, timeout=timeout)
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return 1, "(timed out)"
    except Exception as exc:  # noqa: BLE001
        return 1, f"(error running check: {exc})"


def _verify_ctf(v: dict) -> tuple[bool, str]:
    prog = ROOT / "ctf-lab" / "progress.json"
    if not prog.exists():
        return False, "No CTF progress yet. Start the target and capture a flag."
    solved = json.loads(prog.read_text(encoding="utf-8")).get("solved", [])
    need = v.get("min_solved", 1)
    ok = len(solved) >= need
    return ok, f"Flags captured: {len(solved)}/{need} required."


def cmd_check(curriculum, done) -> int:
    step = current_step(curriculum, done)
    if step is None:
        print("All tasks complete — nothing to check.")
        return 0
    v = step["verify"]
    print(f"Checking: [{step['lab']}] {step['title']} ...")

    if v.get("type") == "ctf":
        ok, detail = _verify_ctf(v)
    else:
        cmd = v["cmd"].replace("{py}", _interpreter(step["lab"]))
        code, output = _run(cmd, ROOT / v["cwd"])
        needle = v.get("contains")
        ok = needle in output if needle else code == 0
        detail = _tail(output)

    if ok:
        done.add(step["id"])
        save_done(done)
        print("PASS. Nice work.\n")
        nxt = current_step(curriculum, done)
        if nxt:
            print(f"Next: [{nxt['lab']}] {nxt['title']}  (python3 coach.py task)")
        else:
            print("That was the last task. You completed the whole program.")
        return 0

    print("Not passing yet.\n")
    if v.get("setup"):
        print("If this is your first time in this lab, do the setup first:")
        print(f"  cd {step['lab']} && {v['setup']}\n")
    print("What the check saw:")
    print(detail)
    print("\nFix it and run 'python3 coach.py check' again.")
    return 1


def _tail(text: str, lines: int = 12) -> str:
    rows = text.strip().splitlines()
    return "\n".join("  " + r for r in rows[-lines:]) if rows else "  (no output)"


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    command = argv[0] if argv else "status"
    curriculum = load_curriculum()
    done = load_done()

    if command == "reset":
        if PROGRESS.exists():
            PROGRESS.unlink()
        print("Progress reset.")
        return 0
    dispatch = {
        "status": cmd_status, "list": cmd_list,
        "task": cmd_task, "check": cmd_check,
    }
    handler = dispatch.get(command)
    if handler is None:
        print(__doc__)
        return 2
    return handler(curriculum, done)


if __name__ == "__main__":
    raise SystemExit(main())
