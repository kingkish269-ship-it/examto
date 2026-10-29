"""Security checks over a cloud inventory snapshot.

Each check takes the parsed inventory dict and returns a list of findings.
A finding is a plain dict so it is easy to print, serialise, and test.

The checks are written against a provider-neutral JSON shape (see
data/sample_account.json) so you can practise the logic without a real cloud
account. The ideas map directly to AWS Config, Security Hub, and Prowler rules.
"""

from __future__ import annotations

PUBLIC_CIDRS = {"0.0.0.0/0", "::/0"}
SENSITIVE_PORTS = {22: "SSH", 3389: "RDP", 3306: "MySQL", 5432: "PostgreSQL"}


def _finding(check: str, severity: str, resource: str, message: str, remediation: str) -> dict:
    return {
        "check": check,
        "severity": severity,
        "resource": resource,
        "message": message,
        "remediation": remediation,
    }


def public_s3_buckets(inv: dict) -> list[dict]:
    findings = []
    for bucket in inv.get("s3_buckets", []):
        name = bucket.get("name", "<unknown>")
        if bucket.get("public") or not bucket.get("public_access_block", True):
            findings.append(_finding(
                "s3-public-access", "CRITICAL", f"s3://{name}",
                "Bucket is public or missing Block Public Access.",
                "Enable Block Public Access and remove public ACLs/policies.",
            ))
        if not bucket.get("encryption", True):
            findings.append(_finding(
                "s3-unencrypted", "MEDIUM", f"s3://{name}",
                "Bucket has no default encryption.",
                "Enable default SSE-KMS or SSE-S3 encryption.",
            ))
    return findings


def open_security_groups(inv: dict) -> list[dict]:
    findings = []
    for sg in inv.get("security_groups", []):
        sgid = sg.get("id", "<unknown>")
        for rule in sg.get("ingress", []):
            if rule.get("cidr") not in PUBLIC_CIDRS:
                continue
            proto = rule.get("protocol")
            frm, to = rule.get("from_port"), rule.get("to_port")
            if proto == "-1" or (frm in (None, 0) and to in (None, 65535)):
                findings.append(_finding(
                    "sg-all-open", "CRITICAL", sgid,
                    "Security group allows all ports from the internet.",
                    "Restrict ingress to required ports and known source ranges.",
                ))
                continue
            for port, label in SENSITIVE_PORTS.items():
                if isinstance(frm, int) and isinstance(to, int) and frm <= port <= to:
                    findings.append(_finding(
                        "sg-sensitive-port", "HIGH", sgid,
                        f"{label} (port {port}) is open to the internet.",
                        "Limit to a bastion, VPN, or specific CIDR; prefer SSM.",
                    ))
    return findings


def wildcard_iam(inv: dict) -> list[dict]:
    findings = []
    for policy in inv.get("iam_policies", []):
        name = policy.get("name", "<unknown>")
        for stmt in policy.get("document", {}).get("Statement", []):
            if stmt.get("Effect") != "Allow":
                continue
            actions = stmt.get("Action", [])
            resources = stmt.get("Resource", [])
            actions = [actions] if isinstance(actions, str) else actions
            resources = [resources] if isinstance(resources, str) else resources
            if "*" in actions and "*" in resources:
                findings.append(_finding(
                    "iam-admin-wildcard", "HIGH", name,
                    "Policy grants Action:* on Resource:* (full admin).",
                    "Scope actions and resources to least privilege.",
                ))
            elif "*" in actions:
                findings.append(_finding(
                    "iam-action-wildcard", "MEDIUM", name,
                    "Policy grants Action:* on specific resources.",
                    "Replace Action:* with the specific actions required.",
                ))
    return findings


def unencrypted_storage(inv: dict) -> list[dict]:
    findings = []
    for vol in inv.get("ebs_volumes", []):
        if not vol.get("encrypted", True):
            findings.append(_finding(
                "ebs-unencrypted", "MEDIUM", vol.get("id", "<unknown>"),
                "EBS volume is not encrypted at rest.",
                "Enable EBS encryption by default; re-create from encrypted snapshot.",
            ))
    return findings


def public_and_unencrypted_rds(inv: dict) -> list[dict]:
    findings = []
    for db in inv.get("rds_instances", []):
        dbid = db.get("id", "<unknown>")
        if db.get("publicly_accessible"):
            findings.append(_finding(
                "rds-public", "CRITICAL", dbid,
                "RDS instance is publicly accessible.",
                "Set PubliclyAccessible=false; place in private subnets.",
            ))
        if not db.get("storage_encrypted", True):
            findings.append(_finding(
                "rds-unencrypted", "HIGH", dbid,
                "RDS storage is not encrypted.",
                "Enable storage encryption (KMS); restore into an encrypted instance.",
            ))
    return findings


def missing_cloudtrail(inv: dict) -> list[dict]:
    trail = inv.get("cloudtrail", {})
    if not trail.get("enabled", False):
        return [_finding(
            "cloudtrail-disabled", "HIGH", "account",
            "CloudTrail is not enabled for the account.",
            "Enable a multi-region CloudTrail with log file validation.",
        )]
    return []


ALL_CHECKS = [
    public_s3_buckets,
    open_security_groups,
    wildcard_iam,
    unencrypted_storage,
    public_and_unencrypted_rds,
    missing_cloudtrail,
]


def run_all(inv: dict) -> list[dict]:
    findings: list[dict] = []
    for check in ALL_CHECKS:
        findings.extend(check(inv))
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(findings, key=lambda f: order.get(f["severity"], 9))
