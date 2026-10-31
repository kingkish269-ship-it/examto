# examto — The Complete Step-by-Step Guide

A readable mirror of **COMPLETE_GUIDE.pdf** (at the repo root). Same content, in Markdown, so you can read it on GitHub without downloading the PDF. To regenerate the PDF after editing content, run:

```bash
pip install fpdf2
python3 docs/make_pdf.py
```

> **The one rule:** you never pay for anything and you never wait for anyone. If a step asks you to buy a VM or sign up for a paid tier, you are off the path — come back here.

---

## 1. One-time setup (~3 minutes)

Runs in your browser; nothing is installed on your own computer.

1. Open the repo: `github.com/kingkish269-ship-it/examto`.
2. Green **Code** button → **Codespaces** tab → **Create codespace on main**.
3. Wait for the build. The `.devcontainer` auto-installs Python and lab deps the first time.
4. When the editor loads you have a full Linux machine in your browser. **This Codespace is the lab machine** you attack and scan.

**Free hours:** GitHub gives personal accounts a monthly pool of free Codespaces hours — plenty if you **stop** the Codespace after each session (see §9). You are not charged on the free tier.

## 2. Start the web lab

Every return visit: reopen the Codespace (github.com → repo → Code → Codespaces → click the existing one), then in the editor terminal:

```bash
git pull
bash webapp/start.sh
```

`start.sh` installs the small web deps (flask, flask-sock) if missing, then launches the server on **port 5000**.

1. Click **Open in Browser** on the port-forwarded popup (or the globe icon on port 5000 in the **Ports** tab).
2. The lab opens: room list on the left, room content in the middle, **live terminal on the right**.
3. The terminal connects automatically — no `Ctrl+\`` or VS Code steps needed.

> **If the terminal says `[terminal closed]`:** flask-sock didn’t install. Press `Ctrl+C` in the editor terminal and re-run `bash webapp/start.sh`.

## 3. How a room works — the 6 sections

Work them top to bottom. Left pane = content; right pane = terminal where you do the work.

| Section | What you do |
|---|---|
| 1. Brief | Two-line "why this matters". |
| 2. Theory | Four parts — What it is, How it works, In the real world (real breaches), How to prevent it. The part you study. |
| 3. Worked example | A fully worked command/response so you see what "good" looks like. |
| 4. Knowledge check | Multiple-choice / short answers, graded instantly. Get them right to pass. |
| 5. Investigation | A complete hands-on lab: exploit the flaw, apply the fix, then re-test to confirm it's closed. |
| 6. Capture | Enter the flag / one-word answer you derived. Graded against a hash (never stored in plaintext). |

A room is complete when all six sections are done. Progress saves locally in the Codespace.

> **Finish the whole room, not one command.** The Capture answer usually only makes sense after you've done the full investigation.

## 4. The full room order

Do them in order; each track builds on the previous.

| # | Room | Track | Core idea |
|---|---|---|---|
| 1 | Intro to AppSec | Foundations | Source-and-sink model; the golden rule |
| 2 | Broken Access Control | Foundations | #1 OWASP risk; IDOR; server-side checks |
| 3 | SQL Injection | Web Exploits | UNION/boolean injection; parameterized queries |
| 4 | Command Injection | Web Exploits | Shell metacharacters; avoid `shell=True` |
| 5 | Cross-Site Scripting | Web Exploits | Reflected/stored XSS; output encoding; CSP |
| 6 | SSRF | Web Exploits | Server-side request forgery; cloud metadata |
| 7 | Broken Authentication | Web Exploits | Sessions, JWT `alg=none`, token forging |
| 8 | Crypto Failures | Web Exploits | Weak hashing, secrets, transport security |
| 9 | Security Misconfiguration | Web Exploits | Headers, defaults, verbose errors |
| 10 | Insecure Deserialization | Web Exploits | pickle/yaml RCE; safe parsing |
| 11 | API Security | AppSec | BOLA/BFLA; OWASP API Top 10 |
| 12 | AI / LLM Security | AppSec | Prompt injection; OWASP LLM Top 10 |
| 13 | Threat Modeling | AppSec | STRIDE; data-flow diagrams |
| 14 | Secure Code Review | AppSec | Spotting vulnerable patterns by hand |
| 15 | SAST | DevSecOps | Static analysis with Bandit / Semgrep |
| 16 | DAST | DevSecOps | Dynamic scanning of a running app |
| 17 | Dependency Scanning (SCA) | DevSecOps | pip-audit; known-CVE components |
| 18 | Secret Scanning | DevSecOps | gitleaks; committed-credential detection |
| 19 | CI/CD Pipeline Security | DevSecOps | Build-time gates; failing on findings |
| 20 | IaC Security | DevSecOps | Checkov on Terraform; misconfig rules |
| 21 | Container Security | DevSecOps | Non-root; image hygiene |
| 22 | Kubernetes Security | DevSecOps | securityContext; privileged pods |
| 23 | Supply Chain Security | DevSecOps | SBOM; provenance; dependency risk |

## 5. The Python track (in parallel)

A self-contained track that teaches the Python an AppSec engineer needs and tests you after each lesson. Runs in the terminal; no web lab required.

```bash
cd /workspaces/examto/learn-python
cat README.md          # the plan and lesson list
python3 check.py       # runs tests for each lesson you've done
```

- 14 lessons, variables → calling HTTP APIs, including a Microsoft Graph / Intune-style lesson that matches your background.
- Each lesson has an exercise file you edit; `check.py` grades it and tells you what's failing.
- Aim for one lesson + one or two rooms per day.

## 6. Using the real free tools

The rooms teach logic with offline stand-ins (zero setup). To run the **real** industry tools against the lab code:

```bash
cd /workspaces/examto/tools-lab
cat README.md          # what each tool is and when to use it
bash install.sh        # installs the real tools into a local venv
bash run_real_tools.sh # runs them all and prints findings
```

| Tool | Type | Catches in this repo |
|---|---|---|
| Bandit | SAST (Python) | pickle, `subprocess shell=True`, md5, raw SQL, urlopen |
| Semgrep | SAST (rules) | Multiple injection / crypto patterns |
| pip-audit | SCA | Known CVEs in pinned dependencies |
| Checkov | IaC | Terraform misconfigs (public DB, open SG, …) |
| sqlmap | DAST | Confirms the SQL injection in the lab app |
| gitleaks | Secrets | Committed credentials / tokens |

> **Semgrep in a fresh Codespace** needs a writable home for settings. If it complains: `export SEMGREP_SETTINGS_FILE=$PWD/.semgrep.yml`. `run_real_tools.sh` already handles this.

## 7. Suggested weekly rhythm (~4–5 weeks)

| Week | Rooms | Python | Tools |
|---|---|---|---|
| 1 | 1–2 + 3–5 | Lessons 1–4 | Bandit intro |
| 2 | 6–10 | Lessons 5–8 | sqlmap, Semgrep |
| 3 | 11–14 | Lessons 9–11 | Code review with Bandit |
| 4 | 15–19 | Lessons 12–14 | pip-audit, gitleaks |
| 5 | 20–23 | Review | Checkov |

## 8. Prove it (build evidence as you go)

- Keep a short notes file per room: the vuln, how you exploited it, the fix.
- Screenshot real tool output (Bandit/Checkov/sqlmap) — portfolio material.
- Push a `writeups/` folder to this repo. A public writeups repo is a strong signal.
- Map each room to job-description language: "Broken Access Control", "SAST in CI", "IaC scanning", "SBOM".

## 9. Stop the Codespace when done (saves free hours)

Codespaces bill per **running** hour, so stop it at the end of each session.

1. In the editor press `F1` (or `Ctrl+Shift+P`).
2. Type **Codespaces: Stop Current Codespace**, Enter.
3. Or at `github.com/codespaces`, `...` next to the codespace → **Stop codespace**.

> **Stopping is not deleting.** It keeps all files and progress and just powers the machine down. Only **Delete** when you're completely finished with the course.

## 10. Quick command reference

```bash
# start / resume the web lab
git pull && bash webapp/start.sh      # then open port 5000

# python track
cd learn-python && python3 check.py

# real security tools against the lab
cd tools-lab && bash install.sh && bash run_real_tools.sh

# stop a stuck server
Ctrl+C in the editor terminal

# stop the codespace (saves hours):  F1 -> Codespaces: Stop
```

## 11. Job-readiness checklist

- [ ] Finished all 23 rooms (every section, every capture).
- [ ] Finished the learn-python track — `check.py` passes all lessons.
- [ ] Ran every real tool in `tools-lab` and can explain each finding.
- [ ] Can explain Broken Access Control, SQLi, XSS, SSRF and the fix for each from memory.
- [ ] Can describe a DevSecOps pipeline: SAST + SCA + secret scan + IaC scan with a gate that fails the build.
- [ ] Have a public writeups repo and 3–4 screenshots of real tool output.
- [ ] Can tie your SC-100 / AWS Security / Zscaler ZTCA background to application and pipeline security in one sentence.

> **Your edge:** most AppSec candidates come from dev and are weak on cloud/network/endpoint. You are the opposite, and now have the application + pipeline skills to match — exactly what platform-security and DevSecOps teams struggle to hire.
