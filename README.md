# Security Engineering Career Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/kingkish269-ship-it/examto)

**Run it entirely in your browser — no local setup.** Click the badge above to
open a Codespace; it auto-installs everything. Then either:

- **Clickable GUI (easiest for beginners):** `python3 dashboard.py` → open the
  forwarded port 5000 → read each task and press **Run check**.
- **Terminal coach:** `python3 coach.py`.

Hands-on labs for building the practical skills behind senior cloud, product, and
DevSecOps security roles. Everything uses free, open-source tooling. No paid
service, cloud account, or subscription is required to start.

> **Want the whole plan in one place?** Follow [`FINISH_ON_YOUR_OWN.md`](FINISH_ON_YOUR_OWN.md)
> — a complete, self-grading, start-to-finish playbook (no help needed).
>
> **Want the TryHackMe/Hackversity split — theory on the left, a terminal on the
> right, in your browser?** Run the web lab:
> ```bash
> python3 webapp/app.py      # open the forwarded port 5000
> ```
> Clickable modules (AppSec, SAST, DAST, threat modeling, CI/CD), each with
> theory + objectives + a flag box, and a live terminal beside it. Text-only
> version: `cd rooms && python3 rooms.py`.
>
> **New here? Run the self-guided coach — it grades you, no help needed:**
> ```bash
> python3 coach.py        # shows your next task; `check` grades it
> ```
> Or read [`GUIDE.md`](GUIDE.md) for full instructions (setup, how to use the
> coach, every lab, troubleshooting), or [`START_HERE.md`](START_HERE.md) for the
> sequenced program at a glance.

Built for an engineer already strong in endpoint, network, cloud, and data
security who wants demonstrable automation, application security, and DevSecOps
skill. Each lab's core logic is tested so you can prove it works.

## Labs

| # | Lab | What you build | Runtime |
|---|---|---|---|
| 1 | [`python-security-lab/`](python-security-lab/README.md) | Security automation fundamentals in Python | stdlib |
| 2 | [`appsec-lab/`](appsec-lab/README.md) | Vulnerable app + 10 OWASP attacks, fixes, and proofs | Flask |
| 3 | [`cloud-security-lab/`](cloud-security-lab/README.md) | Cloud exposure auditor (S3/SG/IAM/RDS/CloudTrail) | stdlib |
| 4 | [`iac-security-lab/`](iac-security-lab/README.md) | Terraform plan security scanner | stdlib |
| 5 | [`container-k8s-lab/`](container-k8s-lab/README.md) | Dockerfile + Kubernetes validators, Kyverno policies | stdlib |
| 6 | [`supply-chain-lab/`](supply-chain-lab/README.md) | SBOM analyzer; signing & provenance guides | stdlib |
| 7 | [`devsecops-lab/`](devsecops-lab/README.md) | CI/CD policy gate that blocks releases | stdlib |
| 8 | [`ctf-lab/`](ctf-lab/README.md) | Gamified capture-the-flag challenges (8, easy→hard) | Flask |
| 9 | [`llm-security-lab/`](llm-security-lab/README.md) | AI/LLM security — OWASP LLM Top 10, attack + defend | stdlib |
| 10 | [`detection-lab/`](detection-lab/README.md) | Detection engineering / SOC — rules over logs | stdlib |

## Suggested order

1. **Python** (lab 1) — the automation foundation.
2. **Application security** (lab 2) — attack, fix, prove.
3. **Cloud** (lab 3) — turn your AWS knowledge into checks.
4. **IaC → containers/K8s → supply chain** (labs 4–6) — shift security left.
5. **CTF** (lab 8) — prove your AppSec skill by capturing flags under your own steam.
5. **DevSecOps** (lab 7) — assemble it all into a release gate.

The full career plan is in
[`python-security-lab/CAREER_ROADMAP.md`](python-security-lab/CAREER_ROADMAP.md);
the eight-week AppSec schedule is in [`appsec-lab/PLAN.md`](appsec-lab/PLAN.md).

**New to Python?** Read [`PYTHON_FOR_YOUR_DOMAIN.md`](PYTHON_FOR_YOUR_DOMAIN.md)
— a complete, read-and-follow guide to the exact Python a security engineer
needs (no lab required), with an 8-week plan and resources. For **step-by-step lessons that test you**, use [`learn-python/`](learn-python/).

## Quick start

```bash
# stdlib labs (1, 3, 4, 5, 6, 7) need only Python 3.10+
cd cloud-security-lab && python3 -m unittest discover -v

# the AppSec lab (2) needs Flask:
cd appsec-lab && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pytest tests/ -v
```

## Safety

`appsec-lab/vulnerable_app/` is intentionally insecure, for local training only
(same category as OWASP Juice Shop / DVWA). It binds to `127.0.0.1`. Never deploy
it. The insecure Terraform, Dockerfiles, and manifests in other labs are study
material — do not apply them.

## Continuous integration

`.github/workflows/ci.yml` runs every lab's tests on each pull request, with
read-only permissions, skipping any lab not present on the branch.
