# 02 — Pod security and admission control

## Audit a manifest

The validator works on a parsed manifest dict. Try it on a privileged pod:

```bash
cd container-k8s-lab
python3 - <<'PY'
from validator.k8s_audit import audit_manifest
pod = {"kind": "Pod", "spec": {"containers": [
    {"name": "app", "image": "app:latest", "securityContext": {"privileged": True}}
]}}
for f in audit_manifest(pod):
    print(f["severity"], f["rule"], "->", f["container"])
PY
```

The test file
`tests/test_validator.py` shows an insecure and a secure Deployment; run it:

```bash
python3 -m unittest discover -v
```

The insecure Deployment is flagged `privileged` (CRITICAL), `host-network`
(HIGH), `run-as-root` (HIGH), and `mutable-image-tag`. The secure one passes.

## Read the pair

Compare `manifests/insecure/deployment.yaml` and `manifests/secure/deployment.yaml`.
The secure pod sets `runAsNonRoot`, `allowPrivilegeEscalation: false`,
`readOnlyRootFilesystem: true`, drops all capabilities, pins the image by digest,
and sets resource limits — the Pod Security Standards "restricted" profile.

## Enforce it, don't just detect it

Detection tells you after the fact; **admission control** blocks it at deploy.
Apply the Kyverno policies:

```bash
# on a local kind cluster with Kyverno installed:
kubectl apply -f policies/
kubectl apply -f manifests/insecure/deployment.yaml   # rejected
kubectl apply -f manifests/secure/deployment.yaml     # admitted
```

See `tools/README.md` for the free `kind` + Kyverno + Trivy setup.

## Extend it

Add a Kyverno policy (and a validator rule + test) that disallows `hostPath`
volumes.
