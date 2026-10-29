# Running Checkov (free IaC scanner)

Checkov is a free, open-source static analysis tool for Terraform, CloudFormation,
Kubernetes, and more. Use it alongside the lab's own scanner.

## Install

```bash
pip install checkov
```

## Scan the lab Terraform

```bash
cd iac-security-lab
checkov -d terraform/insecure      # expect many failures
checkov -d terraform/secure        # expect passes
```

## Scan a real plan

```bash
terraform init
terraform plan -out tfplan.binary
terraform show -json tfplan.binary > tfplan.json
checkov -f tfplan.json
```

## Use it in CI

Checkov returns a non-zero exit code when checks fail, so it gates a pipeline
the same way the lab scanner does. You can suppress a specific check inline with
a `# checkov:skip=CKV_AWS_XX:reason` comment — treat each skip as an accepted
risk that needs a reason, exactly like the allowlist in the DevSecOps gate.

## Compare

Run both the lab scanner and Checkov on `terraform/insecure`. The lab scanner
teaches the detection logic; Checkov adds hundreds of maintained rules. In a
real job you run Checkov (or tfsec) and understand *why* each rule exists —
which is what building the lab scanner gives you.

Docs: https://www.checkov.io/
