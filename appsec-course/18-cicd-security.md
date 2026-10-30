# 18 — CI/CD Pipeline Security

## Theory

DevSecOps means security runs **inside the pipeline**, automatically, on every
change. A typical pipeline: secret scan → SAST → dependency/container scan →
build → tests → a **gate**. The gate collects all findings, applies a policy
(e.g. "fail on any CRITICAL or HIGH"), and returns an **exit code**: `0` lets
the build continue, **non-zero stops it**. That exit code is how CI blocks a bad
release.

The real skill isn't running scanners — it's turning noisy output into a **fair,
tunable release decision** (with an allowlist for accepted risks, so the gate
blocks what matters and doesn't cry wolf).

Pipeline files also hold secrets, so: least-privilege permissions, never dump the
environment, and review changes to them.

## Lab

```bash
cd /workspaces/examto/devsecops-lab
python3 -m gate.run_gate \
  --semgrep samples/semgrep_sample.json \
  --trivy samples/trivy_sample.json \
  --gitleaks samples/gitleaks_sample.json \
  --fail-on HIGH
echo "exit code: $?"
```

The samples include a CRITICAL vuln and a leaked secret, so the gate prints
`FAIL` and returns exit code `1` — a real pipeline would stop here. Now try an
accepted-risk allowlist:
```bash
python3 -m gate.run_gate --trivy samples/trivy_sample.json --fail-on HIGH --allow CVE-2023-0001
echo "exit code: $?"
```

Read the reference pipeline: `cat pipeline/github-actions-devsecops.yml`.

## Verify

- The gate returns exit code `1` (blocks) on the samples.
- Allowlisting the finding changes the decision — a tunable gate.

## Key takeaways

- The gate's exit code is how CI blocks an insecure release.
- Make gates fair: start at HIGH, allowlist accepted risks with a reason.
- Treat pipeline files as sensitive; least privilege, never dump env.
