import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from validator.dockerfile_lint import lint  # noqa: E402
from validator.k8s_audit import audit_manifest  # noqa: E402

INSECURE_POD = {
    "kind": "Deployment",
    "spec": {"template": {"spec": {
        "hostNetwork": True,
        "containers": [{
            "name": "app",
            "image": "myapp:latest",
            "securityContext": {"privileged": True},
        }],
    }}},
}

SECURE_POD = {
    "kind": "Deployment",
    "spec": {"template": {"spec": {
        "securityContext": {"runAsNonRoot": True},
        "containers": [{
            "name": "app",
            "image": "myapp@sha256:abc123",
            "securityContext": {
                "privileged": False,
                "allowPrivilegeEscalation": False,
                "runAsNonRoot": True,
                "readOnlyRootFilesystem": True,
                "capabilities": {"drop": ["ALL"]},
            },
            "resources": {"limits": {"cpu": "500m", "memory": "256Mi"}},
        }],
    }}},
}


class K8sAuditTests(unittest.TestCase):
    def test_insecure_pod_flags_critical(self):
        rules = {f["rule"] for f in audit_manifest(INSECURE_POD)}
        self.assertIn("privileged", rules)
        self.assertIn("host-network", rules)
        self.assertIn("run-as-root", rules)
        self.assertIn("mutable-image-tag", rules)

    def test_secure_pod_is_clean(self):
        self.assertEqual(audit_manifest(SECURE_POD), [])

    def test_privileged_is_critical(self):
        findings = audit_manifest(INSECURE_POD)
        self.assertEqual(findings[0]["severity"], "CRITICAL")


class DockerfileLintTests(unittest.TestCase):
    def test_insecure_dockerfile(self):
        text = "FROM ubuntu:latest\nRUN curl http://x | sh\nCMD [\"/app\"]\n"
        rules = {f["rule"] for f in lint(text)}
        self.assertIn("base-image-untagged", rules)
        self.assertIn("pipe-to-shell", rules)
        self.assertIn("runs-as-root", rules)

    def test_secure_dockerfile(self):
        text = (
            "FROM python:3.11-slim@sha256:deadbeef\n"
            "RUN pip install --no-cache-dir flask\n"
            "USER 1000\n"
            "CMD [\"python\", \"app.py\"]\n"
        )
        self.assertEqual(lint(text), [])


if __name__ == "__main__":
    unittest.main()
