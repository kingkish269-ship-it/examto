# Start here — your security engineering program

This repo is a complete, self-paced program to build the skills for senior
cloud, product, and DevSecOps security roles. Everything is free and runs
locally. You do not need to install anything beyond Python to begin.

If you only read one file, read this one.

## The rule that makes it work

For every lab: **run it, read the small amount of code that matters, explain the
security decision in your own words, change one thing, and re-run.** You are not
memorising syntax — you are learning to understand, review, and modify security
code. That is the actual job.

## The program (in order)

Work top to bottom. Each lab builds on the mindset of the previous one. Times
assume 4–6 focused hours a week.

| Step | Lab | Weeks | You can explain / do afterwards |
|---|---|---|---|
| 1 | `python-security-lab/` | 2 | Parse tool output, call APIs, write reports in Python |
| 2 | `appsec-lab/` | 3 | Exploit and fix the OWASP Top 10; review code for them |
| 3 | `ctf-lab/` | 1 | Prove step 2 by capturing flags unaided |
| 4 | `cloud-security-lab/` | 1 | Turn cloud knowledge into automated checks |
| 5 | `iac-security-lab/` | 1 | Catch misconfig in Terraform before deploy |
| 6 | `container-k8s-lab/` | 1 | Harden Docker and Kubernetes; write admission policy |
| 7 | `supply-chain-lab/` | 1 | SBOMs, vulnerable dependencies, signing, provenance |
| 8 | `devsecops-lab/` | 1 | Assemble it all into a release-blocking pipeline |

Total: roughly 11 weeks part-time. The full career context is in
[`python-security-lab/CAREER_ROADMAP.md`](python-security-lab/CAREER_ROADMAP.md).

## What to do each week

1. Open that lab's `README.md`.
2. Run its demo or tests (commands are in each README).
3. Work its `exercises/` (or drills/challenges) one at a time.
4. Use the checklist below to mark progress.
5. When stuck, read the lab's `tools/`, `walkthroughs/`, or ask Kiro to walk you
   through it live.

## How to use Kiro to drive this

You do not have to do this alone or set anything up by hand. In chat you can say:

- "start `appsec-lab` exercise 1" — Kiro runs it and explains it.
- "start the CTF" — Kiro runs the target and coaches you to the first flag.
- "change the cloud auditor to also flag public RDS snapshots" — Kiro edits,
  tests, and shows the diff.

## Progress checklist

Copy this into `PROGRESS.md` (git-ignored) or just tick here as you go.

- [ ] 1. python-security-lab — 8 drills pass, I can explain each
- [ ] 2. appsec-lab — exploited and fixed all 10 vulns
- [ ] 3. ctf-lab — captured all 8 flags (1000/1000)
- [ ] 4. cloud-security-lab — ran the auditor, added one new check
- [ ] 5. iac-security-lab — scanned a plan, read the insecure/secure diff
- [ ] 6. container-k8s-lab — hardened a Dockerfile and a Deployment
- [ ] 7. supply-chain-lab — analysed an SBOM, understand signing + SLSA
- [ ] 8. devsecops-lab — built a gate that blocks a release

## When you finish

You will have eight runnable, tested projects in a public repo — that is your
portfolio. Then: rewrite your CV around "cloud + product security" leading with
these projects and your certifications, and target vendor pre-sales / solutions
engineering, cloud/product security engineer, or DevSecOps roles.

## Safety and ethics (applies to the whole repo)

Several labs contain intentionally vulnerable code (`appsec-lab/`, `ctf-lab/`,
and the insecure samples in other labs). Run them only locally, never deploy
them, and only ever attack systems you own or are explicitly authorised to test.
