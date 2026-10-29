"""Reference solution for Drill 8."""

PUBLIC_CIDRS = {"0.0.0.0/0", "::/0"}
RISKY_PORTS = {
    22: ("HIGH", "SSH is open to the internet"),
    3389: ("HIGH", "RDP is open to the internet"),
    3306: ("CRITICAL", "MySQL is open to the internet"),
    5432: ("CRITICAL", "PostgreSQL is open to the internet"),
}


def audit_security_groups(groups: list[dict]) -> list[dict]:
    findings = []

    for group in groups:
        for rule in group.get("rules", []):
            if rule.get("cidr") not in PUBLIC_CIDRS:
                continue

            if rule.get("protocol") == "-1":
                findings.append(
                    {
                        "group_id": group.get("group_id"),
                        "group_name": group.get("name"),
                        "severity": "CRITICAL",
                        "port": "ALL",
                        "reason": "All traffic is open to the internet",
                    }
                )
                continue

            from_port = rule.get("from_port")
            to_port = rule.get("to_port")
            if not isinstance(from_port, int) or not isinstance(to_port, int):
                continue

            for port, (severity, reason) in RISKY_PORTS.items():
                if from_port <= port <= to_port:
                    findings.append(
                        {
                            "group_id": group.get("group_id"),
                            "group_name": group.get("name"),
                            "severity": severity,
                            "port": port,
                            "reason": reason,
                        }
                    )

    return findings
