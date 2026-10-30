# Room: SAST — find the bug without running the code

**Topic:** SAST (static analysis) · **Difficulty:** intro

## The story

Your pipeline needs to catch dangerous code **before** it ships. Static
Application Security Testing (SAST) reads source code and flags risky patterns —
no need to run the program. Tools like **Bandit** (Python) and **Semgrep**
(many languages) do this at scale. Here you run a tiny version yourself.

## Theory (1 minute)

SAST looks for a **source** (untrusted input) reaching a dangerous **sink**
(a risky function). A classic sink is `subprocess.run(..., shell=True)` with
input concatenated in — that is **command injection**: an attacker adds `; rm -rf /`
and the shell runs it.

## What you will actually do (in your terminal)

```bash
cd rooms/sast
python3 scan.py vulnerable_example.py
```

Read the output. The scanner tells you which vulnerability class it found on the
`shell=True` line. (Open `vulnerable_example.py` to see the flawed code.)

## Your task

What vulnerability class does the scanner report? Submit it (two words).

```bash
python3 rooms.py submit sast <vulnerability class>
```

## Going further (real tools, when ready)

`pip install bandit semgrep`, then `bandit -r .` or
`semgrep --config auto .`. The idea is identical; the real tools carry hundreds
of rules. See `../../appsec-lab/SETUP.md`.
