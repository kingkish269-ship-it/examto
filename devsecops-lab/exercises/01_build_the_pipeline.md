# 01 — Build the pipeline

Goal: a pipeline that scans, then decides.

## Stages, in order

1. **Secret scan (Gitleaks)** — cheapest, highest signal. Fail fast on leaked
   credentials.
2. **SAST (Semgrep)** — find code-level bugs (injection, SSRF, weak crypto).
3. **Dependency / container scan (Trivy)** — known CVEs in dependencies and
   base images.
4. **SBOM (Syft)** — record what you shipped.
5. **Gate** — aggregate all findings and apply one policy to pass or fail.

## Run the gate locally

```bash
cd devsecops-lab
python3 -m gate.run_gate \
  --semgrep samples/semgrep_sample.json \
  --trivy samples/trivy_sample.json \
  --gitleaks samples/gitleaks_sample.json \
  --fail-on HIGH
```

The output lists every blocking finding and returns exit code 1, which stops a
real pipeline.

## Then

Copy `pipeline/github-actions-devsecops.yml` into a project and adapt it. Read
each step and explain what it protects against and why the gate runs last.
