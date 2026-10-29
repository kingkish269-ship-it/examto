"""Analyse a CycloneDX SBOM for known-vulnerable and unpinned components.

Parses a CycloneDX JSON SBOM (the format Syft produces) and compares each
component against a local advisory list. Also flags components with no version
(unpinned), which cannot be assessed. Pure standard library.
"""

from __future__ import annotations


def _finding(kind: str, severity: str, component: str, message: str) -> dict:
    return {"kind": kind, "severity": severity, "component": component, "message": message}


def load_components(sbom: dict) -> list[dict]:
    return sbom.get("components", [])


def analyze(sbom: dict, advisories: list[dict]) -> list[dict]:
    findings: list[dict] = []
    index: dict[str, list[dict]] = {}
    for adv in advisories:
        index.setdefault(adv["name"], []).append(adv)

    for comp in load_components(sbom):
        name = comp.get("name", "<unknown>")
        version = comp.get("version")

        if not version:
            findings.append(_finding("unpinned", "MEDIUM", name,
                                     "Component has no version; cannot assess risk. Pin it."))
            continue

        for adv in index.get(name, []):
            if version in adv.get("affected", []):
                findings.append(_finding(
                    "vulnerable", adv.get("severity", "HIGH"), f"{name}@{version}",
                    f"{adv.get('id', 'ADVISORY')}: {adv.get('summary', 'known vulnerability')}. "
                    f"Fixed in {adv.get('fixed', 'a later version')}.",
                ))

    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(findings, key=lambda f: order.get(f["severity"], 9))


def summary(findings: list[dict]) -> dict:
    out = {"total": len(findings), "vulnerable": 0, "unpinned": 0}
    for f in findings:
        if f["kind"] == "vulnerable":
            out["vulnerable"] += 1
        elif f["kind"] == "unpinned":
            out["unpinned"] += 1
    return out
