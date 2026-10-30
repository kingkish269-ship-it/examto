# 02 — RDS, IAM, and gating the pipeline (IaC)

## Public and unencrypted databases

The insecure plan has an `aws_db_instance` that is `publicly_accessible = true`
and `storage_encrypted = false` — flagged `rds-public` (CRITICAL) and
`rds-unencrypted` (HIGH). The secure plan flips both.

```bash
python3 -c "import json; from scanner.tf_scan import scan_plan; \
print([f['rule'] for f in scan_plan(json.load(open('terraform/sample_plan_insecure.json')))])"
```

## IAM admin wildcard

The insecure `aws_iam_policy` embeds a policy document granting
`Action:* Resource:*`. `_scan_iam` parses the embedded JSON and flags
`iam-admin-wildcard` (HIGH). This is the IaC equivalent of the cloud lab's IAM
check — the same risk, caught earlier.

## Make it a gate

A scanner is only useful if it can stop a bad deploy. The scanner sorts findings
by severity; wire it so any CRITICAL/HIGH fails the job:

```bash
python3 - <<'PY'
import json, sys
from scanner.tf_scan import scan_plan
f = scan_plan(json.load(open("terraform/sample_plan_insecure.json")))
block = [x for x in f if x["severity"] in ("CRITICAL", "HIGH")]
print(f"{len(block)} blocking findings")
sys.exit(1 if block else 0)
PY
echo "exit: $?"
```

Confirm the secure plan exits 0.

## Extend it

Add an `--allow` list (accepted risks by rule+resource) like the DevSecOps gate,
so a reviewed exception does not block the pipeline, and add a test.
