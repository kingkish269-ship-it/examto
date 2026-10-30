# Room: Secret Scanning

**Topic:** DevSecOps · **Difficulty:** core

## Story
A committed API key lives forever in git history and leaks to everyone with repo
access.

## Theory (2 min)
Secret scanning finds credentials, tokens, and keys in code and git history.
Free tools: **Gitleaks** and **TruffleHog**. Run them in CI so a leaked secret
fails the build before it merges. Anything ever committed must be **rotated** —
removing it from the latest commit is not enough; it is in history.

## What you'll do
In `appsec-lab`, run `tools/run_gitleaks.sh` (or read it) — it finds the
intentional hardcoded secret in `vulnerable_app/app.py`.

## Going further
`appsec-lab/SETUP.md` (Gitleaks) and the `crypto` room (secret management).
