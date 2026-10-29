# 03 — IAM wildcards and encryption

## IAM least privilege

```bash
python3 -m auditor.audit data/sample_account.json | grep iam
```

`break-glass-admin` grants `Action:* Resource:*` (HIGH). `ci-deployer` grants
`Action:*` on a specific bucket (MEDIUM). `read-only-metrics` is fine.

Read `wildcard_iam`. It distinguishes full admin from action-only wildcards
because the blast radius differs.

### In real AWS
Use IAM Access Analyzer, scope policies to specific actions and resources, and
prefer permission boundaries for CI roles.

## Encryption at rest

`unencrypted_storage` and `public_and_unencrypted_rds` flag unencrypted EBS,
unencrypted RDS, and publicly accessible RDS. This is the same key-management
discipline you apply with KMS, expressed as a check.

## Extend it

Add a check for IAM users or access keys older than 90 days, with sample data
and a test.
