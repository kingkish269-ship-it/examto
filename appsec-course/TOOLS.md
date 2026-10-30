# Free & open-source tools for each module

Every tool here is free or open source. Use them to practise beyond the labs.
Run offensive tools **only** against this repo's labs or targets you are
authorised to test.

## Cross-cutting practice targets (free, deliberately vulnerable)
- **PortSwigger Web Security Academy** — free, the best structured web-vuln labs.
- **OWASP Juice Shop** — modern vulnerable app (Node).
- **OWASP WebGoat**, **DVWA**, **bWAPP** — classic vulnerable apps.
- **OWASP crAPI** — vulnerable API.
- **TryHackMe** free rooms, **picoCTF**, **VulnHub**, **Hack The Box** free tier.

## Per module

| # | Module | Free / open-source tools |
|---|---|---|
| 00 | How web apps work | curl, HTTPie, browser DevTools, **Burp Suite Community**, **OWASP ZAP**, mitmproxy |
| 01 | Broken Access Control (IDOR) | Burp Community (Repeater/Intruder) + **Autorize** extension, OWASP ZAP |
| 02 | SQL Injection | **sqlmap**, Burp, ZAP |
| 03 | Command Injection | **Commix**, Burp, ZAP |
| 04 | XSS | **Dalfox**, **XSStrike**, Burp, ZAP; Google **XSS Game** |
| 05 | SSRF | **SSRFmap**, **interactsh**, Gopherus, Burp |
| 06 | Auth & JWT | **jwt_tool**, jwt.io, **John the Ripper** / **Hashcat**, **Hydra** |
| 07 | Crypto & secrets | **gitleaks**, **TruffleHog**, **Hashcat**/**John**, **CyberChef** |
| 08 | Insecure Deserialization | **ysoserial** (Java), **ysoserial.net** (.NET), **phpggc** (PHP) |
| 09 | Security Misconfiguration | **Nikto**, **testssl.sh**, **Nuclei**, Mozilla Observatory, securityheaders.com |
| 10 | API Security | OWASP ZAP, Postman, **kiterunner**, **Arjun**, OWASP crAPI |
| 11 | AI / LLM Security | **garak**, **PyRIT**, **promptfoo**, Lakera **Gandalf** (free) |
| 12 | Threat Modeling | **OWASP Threat Dragon**, Microsoft Threat Modeling Tool, **pytm**, draw.io |
| 13 | Secure Code Review | **Semgrep**, **Bandit**, ripgrep, VS Code |
| 14 | SAST | **Semgrep**, **Bandit** (Python), **CodeQL** (free for OSS), **gosec**, **SonarQube Community** |
| 15 | DAST | **OWASP ZAP**, **Nikto**, **Nuclei**, **Wapiti**, w3af |
| 16 | Dependency Scanning (SCA) | **Trivy**, **Grype**, **OWASP Dependency-Check**, **OSV-Scanner**, **pip-audit**, `npm audit` |
| 17 | Secret Scanning | **gitleaks**, **TruffleHog**, **detect-secrets**, **git-secrets** |
| 18 | CI/CD Security | **Semgrep**/**Trivy**/**gitleaks** in CI, **OpenSSF Scorecard**, **poutine**, **Checkov** |
| 19 | Container Security | **Trivy**, **Grype**, **hadolint** (Dockerfile), **Dockle**, Docker Bench |
| 20 | Kubernetes Security | **kube-bench**, **kubescape**, **Trivy (k8s)**, **Polaris**, **Kyverno**, **OPA/Gatekeeper**, kind/minikube |
| 21 | IaC Security | **Checkov**, **tfsec**, **Terrascan**, **KICS**, Trivy config |
| 22 | Supply Chain | **Syft** (SBOM), **Grype**, **Cosign/Sigstore**, **OSV-Scanner**, **OpenSSF Scorecard**, **in-toto**, SLSA |

## Quick install in your Codespace (the pip-installable ones)

```bash
pip install semgrep bandit pip-audit checkov sqlmap
# Trivy / Grype / gitleaks / hadolint / syft / cosign / nuclei are single
# binaries — download from each project's GitHub releases, or:
curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

(Inspect any install script before piping to a shell — that is itself a
supply-chain lesson, module 22.)

## The one tool to start with

If you install only one thing: **OWASP ZAP** (DAST) plus **Semgrep** (SAST).
Between them they cover most of the pipeline, and both are free and widely used
in real jobs.
