# 17 — Secret Scanning

## Theory

A committed API key, token, or password leaks to everyone with repo access and
lives **forever in git history** — deleting it from the latest commit is not
enough. Secret scanning finds these in code and history. Free tools: **Gitleaks**
and **TruffleHog**. Run them in CI so a leaked secret **fails the build** before
it merges. Anything ever committed must be **rotated**.

## Lab

```bash
cd /workspaces/examto/appsec-lab

# Quick manual pass (what a scanner automates):
grep -rnE "s3cr3t|api[_-]?key|password\s*=" vulnerable_app/

# The real tool (if installed):
gitleaks detect --source . --no-git -v
```

Both find the intentional hardcoded secret in `vulnerable_app/app.py`. If
`gitleaks` isn't installed, the `run_gitleaks.sh` script in `tools/` shows the
exact command and expected finding.

## Verify

The scan (or grep) flags the hardcoded secret in the source.

## Key takeaways

- Secrets in code leak to everyone and persist in git history.
- Gitleaks / TruffleHog in CI; fail the build on a hit.
- Rotate any secret that was ever committed — removal isn't enough.
