# Security Engineering Career Lab

Hands-on labs for building the practical skills behind senior cloud, product, and
DevSecOps security roles. Everything uses free, open-source tooling. No paid
service, cloud account, or subscription is required to start.

> **New here? Read [`START_HERE.md`](START_HERE.md)** — it sequences all eight
> labs into one program with a week-by-week plan and a progress checklist.

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
