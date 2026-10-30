# 21 — Infrastructure-as-Code (IaC) Security

## Theory

Cloud today is built with **Terraform/CloudFormation**, not clicks. IaC security
scans that code for the same misconfigurations you'd otherwise catch in the
console — **before** deployment:
- public S3 buckets,
- security groups open to `0.0.0.0/0`,
- public or unencrypted databases,
- IAM policies with `Action:* Resource:*`.

Free tools: **Checkov**, **tfsec**. In CI, a HIGH/CRITICAL finding fails the
build, so the bad infra never gets applied. This is your cloud expertise shifted
"left" into code review.

## Lab

```bash
cd /workspaces/examto/iac-security-lab

# Scan an insecure Terraform plan:
python3 scan.py terraform/sample_plan_insecure.json
echo "exit code: $?"

# Compare the insecure vs secure Terraform:
cat terraform/insecure/main.tf
cat terraform/secure/main.tf

# The secure plan passes:
python3 scan.py terraform/sample_plan_secure.json
echo "exit code: $?"
```

Real tool (verified — via `tools-lab/`):
```bash
checkov -d /workspaces/examto/iac-security-lab/terraform/insecure --compact
```
Checkov reports ~31 failed checks on our insecure Terraform (SSH/RDP open to the
internet, RDS unencrypted, public S3, …); the secure folder passes.

## Verify

- Insecure plan: findings printed (public S3, open SG, public/unencrypted RDS,
  IAM wildcard) and exit code `1`.
- Secure plan: no findings, exit code `0`.

## Key takeaways

- Catch cloud misconfig in the Terraform, before `apply`.
- Checkov / tfsec; fail CI on HIGH/CRITICAL.
- Your cloud security knowledge, applied as code review.
