# Finish on your own — the complete plan

One document, start to end. Every step tells you what to do and **grades you
itself**, so you never need to ask anyone. Work top to bottom at your own pace.

Rule of thumb: do a step, run its check, and only move on when it passes.

---

## Setup (once)

1. Open your Codespace (github.com/codespaces → your `examto` space), or create
   one (repo → **Code → Codespaces → Create**).
2. In the terminal, get the latest content:
   ```bash
   cd /workspaces/examto
   git pull
   ```
3. When you stop for the day: **F1 → Stop Current Codespace** (saves your free
   hours; your progress is kept).

You need nothing installed — the Codespace sets itself up.

---

## Phase 1 — Python (2–4 weeks)

**Read the map** once: [`PYTHON_FOR_YOUR_DOMAIN.md`](PYTHON_FOR_YOUR_DOMAIN.md)
(what to learn, what to skip, resources).

**Then do the step-by-step track that tests you:**

```bash
cd /workspaces/examto/learn-python
python3 check.py                 # shows your next lesson
```

For each lesson (1 to 14):
1. Read `lessons/<NN>_*.md`.
2. Edit `exercises/ex<NN>.py` — replace the `BLANK` (lesson 10 you write a line).
3. Grade it: `python3 check.py <NN>`.

After each module, run the module test and only continue when it says PASSED:
```bash
python3 check.py test 1     # Core syntax
python3 check.py test 2     # Data & parsing   (most important)
python3 check.py test 3     # Automation
python3 check.py test 4     # CLI tools
python3 check.py test 5     # Real-world: Intune / Microsoft Graph
```

**Done with Phase 1 when:** `python3 check.py` shows 14/14, and you can tick most
of the confidence checklist at the end of `PYTHON_FOR_YOUR_DOMAIN.md`.

> Lesson 14 is the real interview task — applying Intune tags via the Graph API.
> That same token-then-request pattern covers the other Graph/Intune tasks too
> (listing devices, setting a device category); the lesson lists them.

---

## Phase 2 — Application Security (3–4 weeks)

In the Codespace the setup is automatic. Use the GUI or the terminal.

1. Read first: `appsec-lab/exercises/00_how_web_apps_work.md`.
2. Work the exercises in order: `01_broken_access_control.md` → `02_sql_injection.md`
   → `03_xss.md` → `04_ssrf.md` → `05_path_traversal.md` → `06_command_injection.md`
   → `07_insecure_deserialization.md` → `08_auth_session.md`
   → `09_crypto_and_secrets.md` → `10_security_misconfiguration.md`.
3. Prove the whole lab passes:
   ```bash
   cd /workspaces/examto/appsec-lab
   pytest tests/ -v
   ```

**Then capture flags (this is where it clicks):**
```bash
cd /workspaces/examto/ctf-lab
python3 target/run_target.py          # terminal 1: the target
# terminal 2 (click + in the terminal panel):
python3 ctf.py list
python3 ctf.py show idor
python3 ctf.py submit idor 'FLAG{...}'
```

**Done with Phase 2 when:** appsec tests pass and `python3 ctf.py list` shows
8/8 solved.

---

## Phase 3 — DevSecOps, SAST & DAST (2–3 weeks)

Each lab self-checks with its own tests.

```bash
cd /workspaces/examto/iac-security-lab      && python3 scan.py terraform/sample_plan_insecure.json
cd /workspaces/examto/container-k8s-lab     && python3 -m unittest discover
cd /workspaces/examto/supply-chain-lab      && python3 scan.py
cd /workspaces/examto/devsecops-lab         && python3 -m gate.run_gate \
    --semgrep samples/semgrep_sample.json --trivy samples/trivy_sample.json \
    --gitleaks samples/gitleaks_sample.json --fail-on HIGH
```

Read each lab's `README.md` and `exercises/` first. For the real free tools
(Semgrep, Trivy, Checkov, ZAP, Gitleaks), see:
`appsec-lab/SETUP.md`, `iac-security-lab/tools/checkov_guide.md`,
`container-k8s-lab/tools/README.md`.

**Done with Phase 3 when:** you can explain what each tool checks and why the
pipeline gate blocks a release.

---

## Phase 4 — Cloud, AI/LLM, and Detection (2–3 weeks)

```bash
cd /workspaces/examto/cloud-security-lab    && python3 -m auditor.audit data/sample_account.json --fail-on HIGH
cd /workspaces/examto/llm-security-lab       && python3 demo.py
cd /workspaces/examto/detection-lab          && python3 run_detections.py
```

Read each lab's README + exercises. These map to real roles: cloud security
engineer, AI security, and SOC / detection engineering.

**Done with Phase 4 when:** each lab's `python3 -m unittest discover` passes and
you can describe each finding/alert.

---

## The one-command driver (optional, covers the labs)

Instead of running labs by hand, the coach sequences and grades them:
```bash
cd /workspaces/examto
python3 coach.py            # next task
python3 coach.py check      # grade it, advance
```
Or the clickable GUI:
```bash
python3 dashboard.py        # open forwarded port 5000
```

---

## How you know you are ready (job-ready checklist)

- [ ] `learn-python`: 14/14 lessons passed.
- [ ] Python confidence checklist (in `PYTHON_FOR_YOUR_DOMAIN.md`) mostly ticked.
- [ ] You wrote the Intune/Graph tagging function and understand the pattern.
- [ ] AppSec: all 10 vulns exploited and fixed; CTF 8/8 flags.
- [ ] DevSecOps: you can build/explain a pipeline gate.
- [ ] Cloud / IaC / container / supply-chain: each lab passes and you can explain it.
- [ ] You can talk through any of these in an interview from your own repo.

When most are ticked: update your CV around "cloud + product security + DevSecOps,"
lead with this repo and your certifications, and start applying. The career plan
is in `python-security-lab/CAREER_ROADMAP.md`.

---

## If you get stuck

- Re-read the lesson/exercise; the checker's message says exactly what was wrong.
- `python3 coach.py` or `python3 check.py` always shows your next step.
- `git pull` to get any new content.
- Nothing here needs the internet or another person — it is built to be finished
  solo.
