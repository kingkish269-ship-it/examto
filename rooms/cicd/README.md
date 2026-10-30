# Room: CI/CD Security — the release gate

**Topic:** DevSecOps / CI/CD security · **Difficulty:** intro

## The story

Security tools are only useful if a bad build actually gets stopped. In a
DevSecOps pipeline, a **gate** collects findings from the scanners and decides:
ship, or block. Your job is to see the gate block a release.

## Theory (1 minute)

The pipeline runs secret scanning, SAST, dependency/container scanning, then a
**gate** that applies a policy (for example: "fail on any CRITICAL or HIGH").
The gate returns an **exit code** — `0` lets the pipeline continue, non-zero
stops it. That exit code is how CI knows to fail the build.

## What you will actually do (in your terminal)

```bash
cd devsecops-lab
python3 -m gate.run_gate \
  --semgrep samples/semgrep_sample.json \
  --trivy samples/trivy_sample.json \
  --gitleaks samples/gitleaks_sample.json \
  --fail-on HIGH
echo "exit code: $?"
```

The samples contain a CRITICAL vulnerability and a leaked secret, so the gate
prints FAIL and returns a blocking exit code.

## Your task

What exit code does the gate return when it blocks the release? Submit the number.

```bash
python3 rooms.py submit cicd <number>
```

## Going further

Read `devsecops-lab/pipeline/github-actions-devsecops.yml` — the full reference
pipeline this gate plugs into.
