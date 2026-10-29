"""Lint a Dockerfile's text for common security problems."""

from __future__ import annotations


def _finding(rule: str, severity: str, line_no: int, message: str) -> dict:
    return {"rule": rule, "severity": severity, "line": line_no, "message": message}


def lint(dockerfile_text: str) -> list[dict]:
    findings: list[dict] = []
    has_user_nonroot = False
    last_user_root = False

    for i, raw in enumerate(dockerfile_text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        upper = line.upper()

        if upper.startswith("FROM"):
            image = line.split()[1] if len(line.split()) > 1 else ""
            if ("@sha256:" not in image) and (":" not in image.split("/")[-1] or image.endswith(":latest")):
                findings.append(_finding("base-image-untagged", "MEDIUM", i,
                                         "Base image is 'latest' or untagged; pin a version or digest."))

        if upper.startswith("USER"):
            user = line.split()[1] if len(line.split()) > 1 else ""
            if user in {"root", "0"}:
                last_user_root = True
            else:
                has_user_nonroot = True
                last_user_root = False

        if upper.startswith("ADD ") and "http" not in line:
            findings.append(_finding("prefer-copy", "LOW", i,
                                     "Use COPY instead of ADD unless you need its extra behaviour."))

        if ("curl" in line or "wget" in line) and ("| sh" in line or "| bash" in line):
            findings.append(_finding("pipe-to-shell", "HIGH", i,
                                     "Piping a download straight into a shell is unsafe."))

        if "--no-install-recommends" not in line and "apt-get install" in line:
            findings.append(_finding("apt-recommends", "LOW", i,
                                     "Add --no-install-recommends to reduce image surface."))

    if not has_user_nonroot or last_user_root:
        findings.append(_finding("runs-as-root", "HIGH", 0,
                                 "No non-root USER set; container defaults to root."))

    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(findings, key=lambda f: order.get(f["severity"], 9))
