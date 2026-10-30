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

## The curriculum (25 modules, in order)

A complete Application Security + DevSecOps path, focused on what an
endpoint/cloud/network/data background does not already cover — aimed at senior
AppSec / Product Security / DevSecOps roles.

**Foundations:** `intro`, `http`
**OWASP Top 10 (web):** `access`, `inject`, `xss`, `ssrf`, `authn`, `crypto`,
`deser`, `misconfig`
**Hands-on milestone:** `appsec` (capture a real flag)
**Modern & API:** `api`, `llm`
**Process:** `tm` (threat modeling), `review` (secure code review)
**DevSecOps pipeline:** `sast`, `dast`, `sca`, `secrets`, `cicd`
**Cloud-native:** `iac`, `containers`, `k8s`, `supplychain`
**Career:** `interview` (landing the ₹70+ LPA role)

Each module's briefing is in its folder; the deep, full versions are the labs
(`appsec-lab/`, `ctf-lab/`, `devsecops-lab/`, `iac-security-lab/`,
`container-k8s-lab/`, `supply-chain-lab/`, `llm-security-lab/`). Do them in the
order above — that is the learning path.

## Why this gets you job-ready

Interviewers ask you to *do* these things, not recite them. Finishing these
rooms means you have actually threat-modeled a flaw, run SAST and DAST, exploited
a vuln, and gated a pipeline — from a public repo you can show and talk through.
