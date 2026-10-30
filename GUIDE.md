# Guide — what to start and how to use everything

This is the one document that explains how to use this repository end to end.
It is written to be followed on your own, without help.

- New to it all? Follow this guide top to bottom.
- Want the shortest path? Jump to [The 4-command loop](#the-4-command-loop).

---

## 1. What this repository is

Ten hands-on security labs that take you from "I can run a script" to
demonstrable skill in the areas employers hire for: security automation,
application security, cloud, infrastructure-as-code, containers/Kubernetes,
software supply chain, DevSecOps pipelines, offensive CTF practice, AI/LLM
security, and blue-team detection engineering.

Everything is free and runs on your own machine. Most labs need only Python; two
need a quick virtual environment.

## 2. Prerequisites (one time)

1. **Python 3.10 or newer.**
   ```bash
   python3 --version
   ```
   If that fails, install Python from python.org (Windows/macOS) or your package
   manager (Linux), then re-check.

2. **The repository on your machine.**
   ```bash
   git clone https://github.com/kingkish269-ship-it/examto.git
   cd examto
   ```

That is all you need to begin. Two labs (`appsec-lab`, `ctf-lab`) also use
Flask; the guide tells you exactly when and how to set that up.

### Option: run in your browser with GitHub Codespaces (no install)

If you don't want to install anything locally, open the repo in a **GitHub
Codespace** — a full Linux dev machine in your browser with Python and git
already there.

1. On the repo page, click **Code → Codespaces → Create codespace on main**
   (or click the **Open in GitHub Codespaces** badge in the README).
2. Wait for it to finish setting up. A dev container
   (`.devcontainer/`) runs automatically and installs everything — including
   the virtual environments for the Flask labs — so there is nothing to set up
   by hand. When it's ready, in the terminal:
   ```bash
   python3 coach.py        # start the program immediately
   ```
3. The Flask labs are already set up (the dev container did it). To play the
   CTF, start the target, then open the **forwarded port** popup Codespaces
   shows, or use `curl` inside the same terminal.

Good to know:

- A personal **Free** account includes about **120 core-hours per month**
  (roughly 60 hours on a 2-core machine). Plenty for working through the labs;
  stop the codespace when you're done so it doesn't burn hours idle.
- Codespaces is for **doing the labs**, not for **hosting** a lab platform for
  others. A codespace sleeps when idle and is tied to your session — for an
  always-on shared CTF use Oracle Always Free + CTFd (see
  [`ctf-lab/HOSTING.md`](ctf-lab/HOSTING.md)).
- If you expose the intentionally vulnerable apps via a forwarded port, keep the
  port **private** (the default), never public.

## 3. The 4-command loop

The coach runs the whole program for you and grades you automatically. From the
repo root:

```bash
python3 coach.py          # shows your next task and your progress
python3 coach.py task     # full details for that task + the exact command
#   ... you do the task ...
python3 coach.py check    # grades it PASS/FAIL and moves you to the next one
```

Useful extras:

```bash
python3 coach.py list     # every task and whether it is done
python3 coach.py reset    # start over
```

Your progress is saved locally, so you can stop any time and resume later. There
are 14 tasks across all 10 labs; finishing them means you have worked through
the whole program.

## 4. How a lab works (the method that makes it stick)

Every lab follows the same shape, so once you learn one you know them all:

- `README.md` — what the lab teaches and the commands to run.
- an engine (Python) — the security logic, kept small and readable.
- `tests/` — proof it works, and your instant feedback when you change things.
- `exercises/` — short guided tasks (some labs use `drills/` or `challenges`).
- often a CLI (`scan.py`, `audit`, `run_*.py`) you can run in one line.

For each lab: **run it, read the few lines that matter, explain the security
decision in your own words, change one thing, re-run.** You are learning to
understand and modify security code — not to memorise syntax.

## 5. The labs, in order

Work them in this order; each builds on the mindset of the last.

1. **python-security-lab** — the automation basics (stdlib).
2. **appsec-lab** — exploit and fix the OWASP Top 10 (needs Flask).
3. **ctf-lab** — capture flags to prove step 2 (needs Flask).
4. **cloud-security-lab** — turn cloud knowledge into automated checks (stdlib).
5. **iac-security-lab** — catch misconfig in Terraform before deploy (stdlib).
6. **container-k8s-lab** — harden Docker/Kubernetes; write admission policy (stdlib).
7. **supply-chain-lab** — SBOMs, vulnerable deps, signing, provenance (stdlib).
8. **devsecops-lab** — assemble it into a release-blocking pipeline (stdlib).
9. **llm-security-lab** — AI/LLM security, OWASP LLM Top 10 (stdlib).
10. **detection-lab** — blue-team detection rules over logs (stdlib).

The coach already encodes this order.

## 6. The two Flask labs (setup when you reach them)

`appsec-lab` and `ctf-lab` run a small web app, so they need Flask in a virtual
environment. Do this once per lab:

```bash
cd appsec-lab            # or: cd ctf-lab
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest tests/ -v
```

The coach detects these virtual environments automatically and will remind you
with the exact command if they are missing.

### Playing the CTF

```bash
cd ctf-lab
source .venv/bin/activate
python target/run_target.py      # terminal 1: the vulnerable target (localhost)
# terminal 2:
python ctf.py list               # pick a challenge
python ctf.py show idor
python ctf.py hint idor          # one hint at a time if stuck
python ctf.py submit idor 'FLAG{...}'   # capture it
```

## 7. Running a lab without the coach

Each lab stands alone. Examples:

```bash
# stdlib labs — no setup:
cd cloud-security-lab && python3 -m auditor.audit data/sample_account.json --fail-on HIGH
cd iac-security-lab   && python3 scan.py terraform/sample_plan_insecure.json
cd supply-chain-lab   && python3 scan.py
cd devsecops-lab      && python3 -m gate.run_gate --semgrep samples/semgrep_sample.json --trivy samples/trivy_sample.json --gitleaks samples/gitleaks_sample.json --fail-on HIGH
cd llm-security-lab   && python3 demo.py
cd detection-lab      && python3 run_detections.py

# run any lab's tests:
cd <lab> && python3 -m unittest discover -v     # stdlib labs
cd appsec-lab && pytest tests/ -v               # Flask labs (venv active)
```

## 8. The free real tools (optional, when you want them)

The labs teach the detection logic in readable Python; in a real job you also
run the mature free tools. Install guides are inside the labs:

- `appsec-lab/SETUP.md` — Semgrep, Gitleaks, OWASP ZAP, sqlmap, Nikto.
- `iac-security-lab/tools/checkov_guide.md` — Checkov.
- `container-k8s-lab/tools/README.md` — kind, Trivy, Kyverno, kube-bench.
- `supply-chain-lab/exercises/` — Syft, Grype, Cosign, SLSA.
- `ctf-lab/HOSTING.md` — free ways to host a CTF (Oracle Always Free + CTFd).

## 9. Safety and ethics (read once)

Several labs contain intentionally vulnerable code (`appsec-lab`, `ctf-lab`, and
insecure samples elsewhere). Rules:

1. Run them only locally; never deploy them or expose them to a network.
2. Only ever attack systems you own or are explicitly authorised to test.
3. The "secrets" and flags in these labs are fake and for learning only.

## 10. Troubleshooting

- **`python3: command not found`** — use `python` instead, or install Python.
- **`ModuleNotFoundError: flask`** — you are in a Flask lab without its venv.
  Do the setup in section 6.
- **A coach check fails right after cloning a Flask lab** — run that lab's venv
  setup first; the coach prints the exact command.
- **`unittest` says "Ran 0 tests"** — run it from inside the lab folder.
- **Windows activation** — use `.venv\Scripts\activate` instead of `source`.
- **Reset your progress** — `python3 coach.py reset`.

## 11. When you finish

You will have ten runnable, tested projects in a public repo — that is your
portfolio. Next steps:

- Rewrite your CV around "cloud + product security," leading with these projects
  and your certifications.
- Target roles: cloud/product security engineer, application security engineer,
  DevSecOps engineer, vendor solutions/sales engineering, SOC/detection engineer.
- The full career plan is in
  [`python-security-lab/CAREER_ROADMAP.md`](python-security-lab/CAREER_ROADMAP.md).

## 12. Quick reference

| I want to… | Command |
|---|---|
| See my next task | `python3 coach.py` |
| Read the task | `python3 coach.py task` |
| Get graded | `python3 coach.py check` |
| See all tasks | `python3 coach.py list` |
| Start over | `python3 coach.py reset` |
| Run one lab's tests | `cd <lab> && python3 -m unittest discover -v` |
| Set up a Flask lab | `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
