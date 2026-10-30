"""A tiny SAST (static analysis) scanner for the SAST room.

It reads a Python file without running it and flags a dangerous pattern — the
same idea as Bandit or Semgrep, in miniature.

    python3 scan.py vulnerable_example.py
"""

import sys
from pathlib import Path


def scan(path: str):
    findings = []
    for i, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if "subprocess" in line and "shell=True" in line:
            findings.append((i, "command injection",
                             "subprocess with shell=True on non-literal input"))
    return findings


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "vulnerable_example.py"
    results = scan(str(Path(__file__).resolve().parent / target))
    if not results:
        print("No findings.")
    for line, vuln, why in results:
        print(f"Line {line}: {vuln.upper()} — {why}")
    print("\nThe vulnerability class above is your answer for this room.")
