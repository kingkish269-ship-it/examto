"""Audit a Kubernetes workload manifest (as a parsed dict) for insecure settings.

Takes an already-parsed manifest dict so the engine needs no YAML dependency.
The CLI (audit_cli) loads YAML only if PyYAML is installed. The checks mirror
the Pod Security Standards 'restricted' profile and common Kyverno policies.
"""

from __future__ import annotations


def _finding(rule: str, severity: str, target: str, message: str) -> dict:
    return {"rule": rule, "severity": severity, "container": target, "message": message}


def _pod_spec(manifest: dict) -> dict:
    kind = manifest.get("kind")
    if kind == "Pod":
        return manifest.get("spec", {})
    # Deployment, StatefulSet, DaemonSet, Job, etc.
    return manifest.get("spec", {}).get("template", {}).get("spec", {})


def audit_manifest(manifest: dict) -> list[dict]:
    spec = _pod_spec(manifest)
    findings: list[dict] = []

    if spec.get("hostNetwork"):
        findings.append(_finding("host-network", "HIGH", "pod", "hostNetwork is enabled."))
    if spec.get("hostPID"):
        findings.append(_finding("host-pid", "HIGH", "pod", "hostPID is enabled."))
    if spec.get("hostIPC"):
        findings.append(_finding("host-ipc", "HIGH", "pod", "hostIPC is enabled."))

    pod_sc = spec.get("securityContext", {})
    containers = spec.get("containers", [])
    for c in containers:
        name = c.get("name", "<unnamed>")
        sc = c.get("securityContext", {})

        if sc.get("privileged"):
            findings.append(_finding("privileged", "CRITICAL", name, "Container runs privileged."))

        if sc.get("allowPrivilegeEscalation") is not False:
            findings.append(_finding("allow-priv-esc", "HIGH", name,
                                     "allowPrivilegeEscalation is not set to false."))

        run_as_non_root = sc.get("runAsNonRoot", pod_sc.get("runAsNonRoot"))
        if run_as_non_root is not True:
            findings.append(_finding("run-as-root", "HIGH", name,
                                     "runAsNonRoot is not true; container may run as root."))

        if sc.get("readOnlyRootFilesystem") is not True:
            findings.append(_finding("writable-rootfs", "MEDIUM", name,
                                     "readOnlyRootFilesystem is not true."))

        caps = sc.get("capabilities", {})
        if "ALL" not in [str(x).upper() for x in caps.get("drop", [])]:
            findings.append(_finding("caps-not-dropped", "MEDIUM", name,
                                     "Linux capabilities are not dropped (drop: [ALL])."))

        image = c.get("image", "")
        if (":" not in image) or image.endswith(":latest"):
            findings.append(_finding("mutable-image-tag", "MEDIUM", name,
                                     "Image uses 'latest' or no tag; pin to a digest or version."))

        limits = c.get("resources", {}).get("limits", {})
        if not limits.get("cpu") or not limits.get("memory"):
            findings.append(_finding("no-resource-limits", "LOW", name,
                                     "Container is missing CPU/memory limits."))

    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(findings, key=lambda f: order.get(f["severity"], 9))
