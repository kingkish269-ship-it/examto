# Eight-week Application Security plan

Assumes 4–6 focused hours per week. You already understand endpoint, network,
cloud, and data security, so this plan spends no time on general security
theory. It builds the application-layer and secure-code-review muscle that
product and DevSecOps interviews test.

Each week ends with something you can explain in an interview and, where useful,
commit to this repository.

## Week 1 — How web apps work and break

Goal: a clear mental model of request flow and trust boundaries.

- Read `exercises/00_how_web_apps_work.md`.
- Run the app, hit `/health`, `/greet`, `/api/search` with a browser and `curl`.
- Watch requests and responses in your browser's dev tools.
- Deliverable: draw the data-flow diagram for the login request (client, server,
  database, session) and mark the trust boundary.

## Week 2 — Injection: SQL, command, XSS

Goal: recognise untrusted input reaching a dangerous sink.

- Exercises 02 (SQL), 03 (XSS), 06 (command injection).
- Exploit each with the provided `curl` commands.
- Read the `if SECURE` branch for each route and explain the fix.
- Tool: `semgrep --config auto vulnerable_app/` and map findings to the routes.
- Deliverable: in your own words, the four questions for every injection bug —
  where does input enter, what sink receives it, what is the impact, where is
  the correct control.

## Week 3 — Broken access control and SSRF

Goal: authorization logic and server-side request validation.

- Exercises 01 (IDOR), 04 (SSRF), 05 (path traversal).
- Exploit the IDOR as `alice` reading `admin`.
- Use SSRF to read a local file; then read the SSRF fix and the private-IP block.
- Tie SSRF to your cloud knowledge: the classic target is the cloud metadata
  endpoint (`169.254.169.254`). Explain why the fix blocks link-local ranges.
- Deliverable: a short note on why access control must be server-side.

## Week 4 — Authentication, sessions, cryptography

Goal: credential storage, session integrity, brute-force resistance.

- Exercises 08 (auth/session) and 09 (crypto/secrets).
- Forge the insecure session token; see why the random server-side token
  cannot be forged.
- Compare MD5 storage with the salted hash; run Gitleaks to find the hardcoded
  secret in `app.py`.
- Deliverable: explain salting, slow hashing, and why secrets belong in the
  environment or a vault, not in code.

## Week 5 — Security misconfiguration and secure headers

Goal: the cheap, high-value hardening layer.

- Exercise 10 (misconfiguration).
- Compare response headers in vulnerable vs secure mode.
- Tool: run an OWASP ZAP baseline scan (`tools/run_zap_baseline.sh`) and a
  Nikto scan; map each alert to a header or setting.
- Deliverable: a checklist of the headers you now add by default.

## Week 6 — API security

Goal: the OWASP API Top 10 mindset.

- Re-examine `/api/account/<id>` and `/api/search` as API endpoints.
- Study broken object-level authorization (BOLA/IDOR), excessive data exposure,
  and lack of rate limiting using this app.
- Optional: stand up OWASP crAPI (free, Docker) for a richer API target.
- Deliverable: list which OWASP API risks this lab demonstrates and which it does not.

## Week 7 — Threat modeling

Goal: find design flaws before code exists.

- Read `threat-modeling/TEMPLATE.md` and the worked example.
- Threat-model the login and file-download features of this app with STRIDE.
- Threat-model one system from your own experience (a cloud data pipeline or a
  Zero Trust access flow) to connect it to your strengths.
- Deliverable: one completed threat model in the template format.

## Week 8 — Secure code review and a pipeline

Goal: do the job end to end and leave evidence.

- Review `vulnerable_app/app.py` as if it were a pull request. Write review
  comments: finding, impact, fix, reference.
- Confirm the CI workflow (`.github/workflows/ci.yml`) runs the tests and the
  SAST step on every pull request.
- Deliverable: a one-page secure-code-review report plus a green pipeline.

## After the plan

- Rebuild one fix from memory and re-run its test.
- Add one new vulnerable route and its paired fix and tests.
- Position yourself as cloud + product security, not a beginner. Your infra
  background plus demonstrable AppSec review is the differentiator.
