# Room: Infrastructure-as-Code Security

**Topic:** DevSecOps / cloud-native · **Difficulty:** core · **ties to your cloud skills**

## Story
Catch cloud misconfiguration in the Terraform, before `apply` ever runs.

## Theory (2 min)
IaC security scans Terraform/CloudFormation for the same issues you fix in the
console — public S3, security groups open to `0.0.0.0/0`, unencrypted/public
databases, IAM `Action:* Resource:*` — but **before deployment**. Tools:
Checkov, tfsec. In CI, a HIGH/CRITICAL finding fails the build. This is your
cloud expertise shifted "left" into code.

## What you'll do
Run `iac-security-lab/scan.py terraform/sample_plan_insecure.json` and read the
findings; compare the insecure vs secure `.tf` pair.

## Going further
`iac-security-lab/` (scanner + Checkov guide).
