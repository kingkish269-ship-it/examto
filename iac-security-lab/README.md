# IaC Security Lab — Terraform scanning

Catch cloud misconfigurations **before** they are deployed, by scanning the
Terraform plan. You get a working Python scanner plus paired insecure/secure
Terraform to study, and a guide for running the real tool (Checkov) locally.

Pure standard library for the scanner. No cloud account needed.

## Run it

```bash
cd iac-security-lab
python3 -c "import json; from scanner.tf_scan import scan_plan; \
print(json.dumps(scan_plan(json.load(open('terraform/sample_plan_insecure.json'))), indent=2))"
python3 -m unittest discover -v    # 3 tests
```

The scanner reads the JSON that `terraform show -json tfplan` produces, so it
works on real plans too.

## What it flags

| Rule | Severity | Resource |
|---|---|---|
| `s3-public-acl` | CRITICAL | `aws_s3_bucket` public ACL |
| `s3-weak-public-block` | HIGH | disabled public-access-block control |
| `sg-all-open` | CRITICAL | security group all ports to internet |
| `sg-sensitive-open` | HIGH | SSH/RDP/DB port to internet |
| `rds-public` | CRITICAL | publicly accessible RDS |
| `rds-unencrypted` | HIGH | RDS without storage encryption |
| `ebs-unencrypted` | MEDIUM | unencrypted EBS volume |
| `iam-admin-wildcard` | HIGH | IAM `Action:* Resource:*` |

## Study the pairs

- `terraform/insecure/main.tf` — every issue, commented with its severity.
- `terraform/secure/main.tf` — the fixed version.

Read both, then confirm the scanner flags the first and passes the second
(the `sample_plan_*.json` files are their plan outputs).

## Run the real tool

See `tools/checkov_guide.md` to scan the same Terraform with Checkov and
compare its findings to your scanner's.

## Extend it

Add a rule for `aws_s3_bucket` without logging, or a security group egress
rule, with a sample resource and a test.
