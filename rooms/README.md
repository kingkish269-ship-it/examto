# Rooms — learn AppSec → DevSecOps like TryHackMe / Hackversity

Guided rooms with a briefing, a hands-on task, and a **flag/answer to capture** —
the same learn-by-doing style as TryHackMe or Hackversity, but free and running
in your own Codespace.

## The layout (same as Hackversity)

- **Left side — theory, task, flag box:** this tool (`rooms.py`) + each room's
  `README.md` briefing.
- **Right side — the machine:** your **terminal** (your Codespace *is* the cloud
  Linux box). You run real commands to complete each task.

> Honest note: the one thing a free setup can't give you is a private, hosted
> **Kali VM per user** — that is what Hackversity charges for. You don't need it
> for AppSec/DevSecOps/SAST/DAST; your Codespace terminal is a real cloud Linux
> machine with everything these rooms use.

## How to play

```bash
cd rooms
python3 rooms.py                 # list rooms + your progress
python3 rooms.py show tm         # read a room's briefing and task
# ...do the task in your terminal (the briefing gives the commands)...
python3 rooms.py submit tm <answer>   # capture the flag / answer
```

Tip for the split-screen feel: keep one terminal for `rooms.py` and open a
second terminal (the **+** in the terminal panel) to run the task commands —
briefing on one side, machine on the other.

## The rooms (your requested topics)

| Room | Topic | You will |
|---|---|---|
| `tm` | Threat modeling (STRIDE) | classify a real design flaw |
| `sast` | SAST | run a scanner and name the bug it finds |
| `dast` | DAST | attack a running app and identify the flaw |
| `appsec` | Application security | exploit an IDOR and capture a real flag |
| `cicd` | DevSecOps / CI-CD | run a release gate and read its exit code |

Each room's briefing is in its folder (`threat-modeling/`, `sast/`, `dast/`,
`appsec/`, `cicd/`). The deeper, full versions of each topic are the labs:
`appsec-lab/`, `ctf-lab/`, `devsecops-lab/`, and the threat-modeling template in
`appsec-lab/threat-modeling/`.

## Why this gets you job-ready

Interviewers ask you to *do* these things, not recite them. Finishing these
rooms means you have actually threat-modeled a flaw, run SAST and DAST, exploited
a vuln, and gated a pipeline — from a public repo you can show and talk through.
