# Cloud Security Lab — Exposure Auditor

A working cloud posture auditor you build and extend in Python. It reads a cloud
inventory snapshot (JSON) and reports misconfigurations with severity and
remediation, and it exits non-zero so it can gate a pipeline. This is the
portfolio project that turns your AWS Security Specialty knowledge into
executable checks.

Pure standard library. No cloud account, no paid tool.

## Run it

```bash
cd cloud-security-lab
python3 -m auditor.audit data/sample_account.json                 # table
python3 -m auditor.audit data/sample_account.json --format json   # JSON
python3 -m auditor.audit data/sample_account.json --format csv --out report.csv
python3 -m auditor.audit data/sample_account.json --fail-on HIGH  # exit 1 if HIGH+
python3 -m unittest discover -v                                   # 8 tests
```

## What it checks

| Check | Severity | Maps to |
|---|---|---|
| Public S3 bucket / no Block Public Access | CRITICAL | S3 Block Public Access |
| S3 without default encryption | MEDIUM | SSE-KMS/SSE-S3 |
| Security group all ports open to internet | CRITICAL | SG ingress |
| SSH/RDP/DB port open to internet | HIGH | SG ingress |
| IAM `Action:* Resource:*` | HIGH | least privilege |
| IAM `Action:*` on specific resource | MEDIUM | least privilege |
| Unencrypted EBS volume | MEDIUM | EBS encryption |
| Public RDS / unencrypted RDS | CRITICAL/HIGH | RDS config |
| CloudTrail disabled | HIGH | account logging |

## How to use it as a learning project

1. Read `auditor/checks.py`. Each check is a small function — read one, run the
   matching test, and explain what it flags.
2. Work through `exercises/`.
3. **Extend it** (this is the interview-worthy part): add a check for a control
   you know, such as "S3 bucket without versioning" or "IAM user without MFA".
   Add sample data and a test, then re-run.
4. Point it at real read-only data later: export with the AWS CLI
   (`aws ec2 describe-security-groups`, `aws s3api ...`) and adapt the inventory
   shape, or compare your rules against Prowler's.

## Files

- `auditor/checks.py` — the security checks
- `auditor/audit.py` — CLI, report formats, and the pipeline exit code
- `data/sample_account.json` — a sample inventory with intentional problems
- `tests/test_checks.py` — proves each check fires correctly
- `exercises/` — guided walkthroughs
