# 01 — Public storage and open security groups (IaC)

Catch these in the Terraform plan, before `terraform apply` ever runs.

## See it

```bash
cd iac-security-lab
python3 -c "import json; from scanner.tf_scan import scan_plan; \
[print(f['severity'], f['rule'], f['resource']) for f in \
scan_plan(json.load(open('terraform/sample_plan_insecure.json')))]"
```

`aws_s3_bucket.data` is flagged `s3-public-acl` (CRITICAL) and
`aws_security_group.admin` is flagged `sg-sensitive-open` (HIGH).

## Read the pair

Open `terraform/insecure/main.tf` and `terraform/secure/main.tf` side by side.
The secure bucket drops the public ACL and adds an
`aws_s3_bucket_public_access_block`; the secure security group restricts the
source CIDR to a private range.

## The logic

In `scanner/tf_scan.py`, `scan_plan` walks `planned_values.root_module.resources`
(and child modules). A public ACL on `aws_s3_bucket`, or a public CIDR on a
sensitive port in `aws_security_group`, becomes a finding.

## In a real pipeline

Run `terraform show -json tfplan > plan.json` and scan `plan.json`, or run
Checkov (see `tools/checkov_guide.md`). Fail the pipeline on CRITICAL/HIGH.

## Extend it

Add a rule that flags an `aws_s3_bucket` without a matching
`aws_s3_bucket_public_access_block` anywhere in the plan, and add a test.
