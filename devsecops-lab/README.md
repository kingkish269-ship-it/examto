# DevSecOps Lab — pipeline and policy gate

Assemble the security tools from the other labs into a CI/CD pipeline that can
**block a release**. The core is a Python gate that normalises findings from
Semgrep, Trivy, and Gitleaks, applies a policy, and returns a pipeline exit code.

Pure standard library. No external tool needed to run the gate or its tests.

## Run it

```bash
cd devsecops-lab
python3 -m gate.run_gate \
  --semgrep samples/semgrep_sample.json \
  --trivy samples/trivy_sample.json \
  --gitleaks samples/gitleaks_sample.json \
  --fail-on HIGH
echo "exit code: $?"          # 1 -> the pipeline would stop
python3 -m unittest discover -v   # 7 tests
```

## What the gate does

1. **Normalises** each tool's JSON into one finding shape
   (`tool`, `id`, `severity`, `location`).
2. **Applies policy**: `--fail-on` severity, `--max-allowed` tolerance, and an
   `--allow` list for accepted risks / false positives.
3. **Returns an exit code** so the pipeline passes or fails deterministically.

This is the piece most engineers miss: running scanners is easy; turning noisy
output into a fair, tunable release decision is the real DevSecOps skill.

## The reference pipeline

`pipeline/github-actions-devsecops.yml` is a complete reference workflow:
secret scan → SAST → dependency/container scan → SBOM → gate. It is a sample to
copy into a project's `.github/workflows/`; it is intentionally **not** placed
in this repo's live `.github/` so it does not require the external tools here.

## Exercises

- `exercises/01_build_the_pipeline.md` — assemble the stages.
- `exercises/02_tuning_false_positives.md` — make gates fair, not noisy.

## How this connects the other labs

| Stage | Tool | Lab |
|---|---|---|
| Secret scan | Gitleaks | appsec-lab |
| SAST | Semgrep | appsec-lab |
| Dependency / container scan | Trivy / Grype | container-k8s-lab, supply-chain-lab |
| IaC scan | Checkov | iac-security-lab |
| SBOM + signing | Syft + Cosign | supply-chain-lab |
| Release decision | this gate | devsecops-lab |
