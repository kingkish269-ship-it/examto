# Security Engineering Career Lab

Hands-on labs for building the practical skills behind senior cloud, product, and
DevSecOps security roles. Everything uses free, open-source tooling. No paid
service, cloud account, or subscription is required to start.

## Labs

### 1. Python Security Lab — [`python-security-lab/`](python-security-lab/README.md)

The programming foundation for security automation: parsing tool output, calling
APIs, writing reports, and auditing cloud configuration. Standard library only.

- Start: [`python-security-lab/README.md`](python-security-lab/README.md)
- Cheatsheet: [`python-security-lab/CHEATSHEET.md`](python-security-lab/CHEATSHEET.md)
- Roadmap: [`python-security-lab/CAREER_ROADMAP.md`](python-security-lab/CAREER_ROADMAP.md)

```bash
cd python-security-lab
python3 run_demo.py
python3 -m unittest discover -v
```

### 2. Application Security Lab — [`appsec-lab/`](appsec-lab/README.md)

A deliberately vulnerable Flask app with ten OWASP-mapped vulnerabilities, each
paired with a fix and a test that proves the attack works and the fix stops it.
Includes free SAST/DAST/secret-scanning guides and a threat-modeling template.

- Start: [`appsec-lab/README.md`](appsec-lab/README.md)
- Plan: [`appsec-lab/PLAN.md`](appsec-lab/PLAN.md)

```bash
cd appsec-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

> The app in `appsec-lab/vulnerable_app/` is intentionally insecure and for local
> training only. Never deploy it or expose it to a network.

## Continuous integration

`.github/workflows/ci.yml` runs each lab's tests on every pull request, skipping
any lab not present on the branch.
