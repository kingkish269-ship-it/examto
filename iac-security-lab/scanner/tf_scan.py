"""Scan a Terraform plan (``terraform show -json``) for insecure resources.

Works on the parsed plan dict so you can practise the logic offline. The same
rule ideas are what Checkov and tfsec implement; see tools/checkov_guide.md to
run the real scanner locally.
"""

from __future__ import annotations

import json

PUBLIC_CIDRS = {"0.0.0.0/0", "::/0"}
SENSITIVE_PORTS = {22, 3389, 3306, 5432}


def _finding(rule: str, severity: str, address: str, message: str) -> dict:
    return {"rule": rule, "severity": severity, "resource": address, "message": message}


def _iter_resources(module: dict):
    for res in module.get("resources", []):
        yield res
    for child in module.get("child_modules", []):
        yield from _iter_resources(child)


def _address(res: dict) -> str:
    return res.get("address") or f"{res.get('type')}.{res.get('name')}"


def scan_plan(plan: dict) -> list[dict]:
    root = plan.get("planned_values", {}).get("root_module", {})
    findings: list[dict] = []
    for res in _iter_resources(root):
        rtype = res.get("type")
        values = res.get("values", {})
        addr = _address(res)

        if rtype == "aws_s3_bucket" and values.get("acl") in {"public-read", "public-read-write"}:
            findings.append(_finding("s3-public-acl", "CRITICAL", addr,
                                     f"S3 bucket ACL is {values['acl']}."))

        if rtype == "aws_s3_bucket_public_access_block":
            flags = ["block_public_acls", "block_public_policy",
                     "ignore_public_acls", "restrict_public_buckets"]
            if any(values.get(f) is False for f in flags):
                findings.append(_finding("s3-weak-public-block", "HIGH", addr,
                                         "Public access block has a disabled control."))

        if rtype == "aws_security_group":
            for rule in values.get("ingress", []):
                cidrs = set(rule.get("cidr_blocks", []))
                if not (cidrs & PUBLIC_CIDRS):
                    continue
                frm, to = rule.get("from_port"), rule.get("to_port")
                if frm == 0 and to == 0 or rule.get("protocol") == "-1":
                    findings.append(_finding("sg-all-open", "CRITICAL", addr,
                                             "Ingress allows all ports from the internet."))
                elif isinstance(frm, int) and isinstance(to, int):
                    if any(frm <= p <= to for p in SENSITIVE_PORTS):
                        findings.append(_finding("sg-sensitive-open", "HIGH", addr,
                                                 "Sensitive port open to the internet."))

        if rtype == "aws_db_instance":
            if values.get("publicly_accessible"):
                findings.append(_finding("rds-public", "CRITICAL", addr,
                                         "RDS instance is publicly accessible."))
            if values.get("storage_encrypted") is False:
                findings.append(_finding("rds-unencrypted", "HIGH", addr,
                                         "RDS storage is not encrypted."))

        if rtype == "aws_ebs_volume" and values.get("encrypted") is False:
            findings.append(_finding("ebs-unencrypted", "MEDIUM", addr,
                                     "EBS volume is not encrypted."))

        if rtype in {"aws_iam_policy", "aws_iam_role_policy"}:
            findings.extend(_scan_iam(values.get("policy"), addr))

    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(findings, key=lambda f: order.get(f["severity"], 9))


def _scan_iam(policy_doc, addr: str) -> list[dict]:
    if not policy_doc:
        return []
    if isinstance(policy_doc, str):
        try:
            policy_doc = json.loads(policy_doc)
        except json.JSONDecodeError:
            return []
    out = []
    statements = policy_doc.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    for stmt in statements:
        if stmt.get("Effect") != "Allow":
            continue
        actions = stmt.get("Action", [])
        resources = stmt.get("Resource", [])
        actions = [actions] if isinstance(actions, str) else actions
        resources = [resources] if isinstance(resources, str) else resources
        if "*" in actions and "*" in resources:
            out.append(_finding("iam-admin-wildcard", "HIGH", addr,
                                "IAM policy allows Action:* on Resource:*."))
    return out
