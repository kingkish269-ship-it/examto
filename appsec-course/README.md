# Application Security Course — theory + hands-on, from beginner

One folder, start to finish. Each module is a single page with **easy theory
first**, then a **step-by-step lab** you do in the terminal, then a check. Work
them in order. By the end you will have attacked and fixed every major web
vulnerability and understood the DevSecOps pipeline around it — real,
demonstrable AppSec experience.

No prior AppSec needed. You run everything in your Codespace (a real cloud Linux
machine). Nothing here touches real systems.

## One-time setup

```bash
cd /workspaces/examto && git pull

# The web-app labs need Python + Flask (done automatically in a Codespace).
# If a lab says "flask not found", run its setup once:
cd appsec-lab && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cd ..
cd ctf-lab   && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cd ..
```

## How to use each module

1. Read the **Theory** (5 minutes, plain English).
2. Do the **Lab** steps exactly (copy the commands).
3. Do the **Verify** step to confirm it worked.
4. Read **Key takeaways** — this is what you say in an interview.

## The modules (do them in order)

### Foundations
- [00 — How web apps work](00-how-web-apps-work.md)

### OWASP Top 10 (web)
- [01 — Broken Access Control (IDOR)](01-broken-access-control.md)
- [02 — SQL Injection](02-sql-injection.md)
- [03 — Command Injection](03-command-injection.md)
- [04 — Cross-Site Scripting (XSS)](04-xss.md)
- [05 — SSRF](05-ssrf.md)
- [06 — Authentication & JWT](06-auth-and-jwt.md)
- [07 — Cryptographic Failures & Secrets](07-crypto-and-secrets.md)
- [08 — Insecure Deserialization](08-insecure-deserialization.md)
- [09 — Security Misconfiguration](09-security-misconfiguration.md)

### Modern & API
- [10 — API Security](10-api-security.md)
- [11 — AI / LLM Security](11-llm-security.md)

### Process
- [12 — Threat Modeling](12-threat-modeling.md)
- [13 — Secure Code Review](13-secure-code-review.md)

### DevSecOps pipeline
- [14 — SAST (static analysis)](14-sast.md)
- [15 — DAST (dynamic analysis)](15-dast.md)
- [16 — Dependency Scanning (SCA)](16-dependency-scanning.md)
- [17 — Secret Scanning](17-secret-scanning.md)
- [18 — CI/CD Pipeline Security](18-cicd-security.md)

### Cloud-native
- [19 — Container Security](19-container-security.md)
- [20 — Kubernetes Security](20-kubernetes-security.md)
- [21 — IaC Security](21-iac-security.md)
- [22 — Supply Chain Security](22-supply-chain.md)

## When you finish

You will have done, not just read, every topic. Pair this with the guided web
lab (`python3 webapp/app.py`) and the deep labs (`appsec-lab/`, `ctf-lab/`,
`devsecops-lab/`, etc.). Then rebuild one exploit+fix from memory and you can
talk through it in an interview. Career next steps: `FINISH_ON_YOUR_OWN.md`.
