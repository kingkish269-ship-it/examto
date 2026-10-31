# The Complete Roadmap — from beginner to job-ready AppSec / DevSecOps

This is the single ordered path. It ties together three things you already have:

1. **This repo** — 23 guided rooms, the `learn-python` track, and `tools-lab` (the real tools).
2. **PortSwigger Web Security Academy** — free, the best place to learn the *full variation tree* of each web vulnerability. <https://portswigger.net/web-security>
3. **Reps + proof** — TryHackMe / HackTheBox for volume, a real CI/CD pipeline you build yourself, and a public writeups repo.

> **Who this is for:** you are experienced in cloud / network / endpoint / data
> security (SC-100, AWS Security, Zscaler ZTCA) but new to *application* security
> and weak at Python. This roadmap is tuned for exactly that: it moves fast through
> foundations and leans into AppSec depth + proof, which is where your gap is.

**Honest expectation.** The repo alone makes you *conversant*. Repo + PortSwigger +
a real pipeline project + reps makes you a *credible, hireable AppSec/DevSecOps
candidate*. The senior ~₹70L level also wants 1-3 years doing this on the job —
this roadmap shortens the ramp, it doesn't replace it.

**Assumed pace:** ~10 hours/week. Total ≈ **16 weeks (~4 months)**. Go faster or
slower; the *order* matters more than the calendar.

---

## How to use each room alongside PortSwigger

For every web-vuln room, do it in this loop:

1. **Learn it here** — read the room's Theory (What it is / How it works / In the
   real world / How to prevent), then do the Investigation (exploit → fix → verify).
2. **Go deep on PortSwigger** — do the matching topic's labs. The repo teaches *one*
   clean path; PortSwigger teaches the variations (blind, stored, bypasses) that
   interviews and real work actually test.
3. **Prove it** — write a 5-line note (the vuln, how you exploited it, the fix) into
   your `writeups/` repo. These become your interview talking points.

---

## Phase 0 — Setup & orientation  (½ day)

- [ ] Open the repo in a GitHub Codespace (Code → Codespaces → Create on main).
- [ ] Read `COMPLETE_GUIDE.pdf` (or `docs/COMPLETE_GUIDE.md`).
- [ ] Run `git pull && bash webapp/start.sh`, open port 5000, click through the
      **Intro** room so you know how the 6 sections and the terminal work.
- [ ] Create a **public** repo called `appsec-writeups` for your notes.
- [ ] Create a free PortSwigger account.

**Exit criteria:** the web lab runs, the terminal connects, you have a writeups repo.

---

## Phase 1 — Foundations + Python start  (Weeks 1-2)

| Do in the repo | Do on PortSwigger | Python track |
|---|---|---|
| Rooms **1 Intro**, **2 Broken Access Control** | [Access control vulnerabilities](https://portswigger.net/web-security/access-control) | `learn-python` lessons 1-6 (`python3 check.py`) |

- [ ] Finish rooms 1-2 completely (every section + capture).
- [ ] Do the PortSwigger access-control **apprentice** labs (all) and 2-3 practitioner.
- [ ] `learn-python` lessons 1-6 passing in `check.py`.
- [ ] Writeup: IDOR — what it is, the request you changed, the server-side fix.

**Exit criteria:** you can explain, from memory, why access control must be checked
server-side per request, and you've solved real IDOR labs beyond this repo.

---

## Phase 2 — Core web exploits  (Weeks 3-6)

This is the heart of AppSec. Do not rush it.

| Repo rooms | PortSwigger topics | Python |
|---|---|---|
| **3 SQLi** | [SQL injection](https://portswigger.net/web-security/sql-injection) | lessons 7-9 |
| **4 Command Injection** | [OS command injection](https://portswigger.net/web-security/os-command-injection) | |
| **5 XSS** | [Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) | lessons 10-11 |
| **6 SSRF** | [SSRF](https://portswigger.net/web-security/ssrf) | |
| **7 Broken Auth** | [Authentication](https://portswigger.net/web-security/authentication) + [JWT attacks](https://portswigger.net/web-security/jwt) | |
| **8 Crypto Failures** | [Information disclosure](https://portswigger.net/web-security/information-disclosure) | |
| **9 Misconfiguration** | (headers / info disclosure) | |
| **10 Insecure Deserialization** | [Insecure deserialization](https://portswigger.net/web-security/deserialization) | |

- [ ] All 8 rooms finished (capture every CTF flag: run `ctf-lab` as the rooms show).
- [ ] PortSwigger: **all apprentice** labs for SQLi, command injection, XSS, SSRF,
      auth; plus the deserialization apprentice labs. Reach for practitioner where
      you can.
- [ ] Use the real tool at least once: `sqlmap` against the lab (room 3 / `tools-lab`).
- [ ] `learn-python` lessons 7-11 passing.
- [ ] One writeup per vuln class (8 total).

**Exit criteria:** you can take any of these 8 vulns, exploit a fresh lab, explain
*why* it works, and state the correct fix without looking it up.

---

## Phase 3 — Application security practice  (Weeks 7-8)

| Repo rooms | PortSwigger | Python |
|---|---|---|
| **11 API Security** | [API testing](https://portswigger.net/web-security/api-testing) | lessons 12-14 |
| **12 AI / LLM Security** | [Web LLM attacks](https://portswigger.net/web-security/llm-attacks) | |
| **13 Threat Modeling** | — (use the repo's STRIDE template) | |
| **14 Secure Code Review** | — (review real open-source PRs) | |

- [ ] Rooms 11-14 finished.
- [ ] PortSwigger API and LLM apprentice labs.
- [ ] **Threat-model a real app**: pick any small open-source web app, draw its data
      flow, fill the STRIDE table from room 13, list mitigations. Put it in writeups.
- [ ] **Code review drill**: find a real CVE in an open-source project, read the
      vulnerable commit and the fix commit, and write up the sink → source path.
- [ ] `learn-python` lessons 12-14 passing (including the Graph/Intune API lesson —
      this ties directly to your background).

**Exit criteria:** you can threat-model a system and read code to find a planted
bug, not just run a tool.

---

## Phase 4 — DevSecOps (your strongest hiring angle)  (Weeks 9-11)

Your infra/cloud background makes this the fastest ROI. Lean in.

| Repo rooms | Real deliverable |
|---|---|
| **15 SAST**, **16 DAST**, **17 SCA**, **18 Secret Scanning** | Run every real tool via `tools-lab` and read the findings |
| **19 Container**, **20 Kubernetes** | Compare insecure vs hardened manifests; understand each control |
| **21 IaC**, **22 Supply Chain**, **23 CI/CD** *(do CI/CD last)* | **Build a real pipeline (below)** |

- [ ] Rooms 15-23 finished.
- [ ] Run the real tools in `tools-lab`: Bandit, Semgrep, Checkov, pip-audit,
      gitleaks — and be able to explain every finding.
- [ ] **Capstone — build a real security pipeline.** Take one of your own GitHub
      repos (or fork a vulnerable sample) and wire a GitHub Actions workflow that
      runs **Semgrep + pip-audit + gitleaks + Checkov** and **fails the build** on
      high-severity findings. Tune out the false positives. Screenshot the passing
      and failing runs. *This single artifact is worth more than a certificate.*

**Exit criteria:** a working, public CI/CD pipeline with security gates that you
built and can walk someone through line by line.

---

## Phase 5 — Volume & proof  (Weeks 12-14)

Experience = reps on messy targets you've never seen.

- [ ] **TryHackMe** or **HackTheBox** web track — grind at least 15-20 machines/labs.
      Repeat the Phase-2 vuln classes on targets nobody walked you through.
- [ ] **Bug bounty (start safe):** pick a program with a *Vulnerability Disclosure
      Program (VDP)* scope on HackerOne/Bugcrowd and spend time hunting. Goal is
      reps and one real submission, not income yet.
- [ ] Grow `appsec-writeups` to ~15-20 solid writeups with screenshots of real tool
      output. This *is* your portfolio.

**Exit criteria:** you can approach an unfamiliar app and work through it
methodically, and you have public proof of it.

---

## Phase 6 — Job readiness & applying  (Weeks 15-16)

- [ ] **Resume positioning:** lead with "cloud + application security" — pair your
      SC-100 / AWS Security / Zscaler background with "built and secured a DevSecOps
      pipeline," "exploited and remediated the OWASP Top 10," and your writeups link.
- [ ] **Interview prep:** for each topic, be ready to (a) explain the vuln, (b) show
      the fix, (c) describe how you'd catch it in CI. Rehearse out loud.
- [ ] **Mock interview:** rebuild one exploit + fix from memory and narrate it as if
      to an interviewer.
- [ ] Review `FINISH_ON_YOUR_OWN.md` and the `rooms/interview` material in this repo.
- [ ] Start applying to remote AppSec / DevSecOps / Product Security / Cloud Security
      Engineer roles. Apply while you finish Phase 5 reps — don't wait for "perfect."

**Exit criteria (you are "complete" / ready to apply when all are true):**

- [ ] All 23 rooms finished (every section, every capture).
- [ ] `learn-python` — `check.py` passes all 14 lessons.
- [ ] PortSwigger: all apprentice labs for the core vuln classes done.
- [ ] A working, public CI/CD security pipeline you built.
- [ ] 15+ writeups with real tool-output screenshots in a public repo.
- [ ] You can explain Broken Access Control, SQLi, XSS, SSRF, auth and their fixes
      from memory, and describe a full DevSecOps gate.
- [ ] You can tie your cloud/network/endpoint background to app + pipeline security
      in one sentence.

---

## After you land the role (ongoing)

- Keep a running list of CVEs/breaches and reason about how you'd have caught each.
- Go deeper on one specialty: cloud-native security, LLM/AI security, or supply
  chain — all are rising and pay well.
- Contribute security fixes to open source; it compounds your portfolio.
- Revisit the ₹70L target: that level comes from *level + employer + track record*.
  This roadmap gets you in the door and growing toward it.

---

### Quick reference — room order

`1 intro → 2 access → 3 sqli → 4 cmdi → 5 xss → 6 ssrf → 7 auth → 8 crypto →`
`9 misconfig → 10 deser → 11 api → 12 llm → 13 tm → 14 review → 15 sast →`
`16 dast → 17 sca → 18 secrets → 19 containers → 20 k8s → 21 iac →`
`22 supplychain → 23 cicd`

Start today with Phase 0, then Room 1. One room + its PortSwigger topic + one
writeup at a time. That loop, repeated, is the whole journey.
