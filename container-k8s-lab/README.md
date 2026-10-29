# Container & Kubernetes Security Lab

Harden containers and Kubernetes workloads, and validate them automatically. You
get two Python validators (Dockerfile and Kubernetes manifest), paired
insecure/secure manifests, and ready-to-use Kyverno admission policies.

Validators are pure standard library. No cluster or Docker needed to run them.

## Run it

```bash
cd container-k8s-lab
python3 -m unittest discover -v    # 5 tests
```

Audit a manifest you parsed yourself:

```python
from validator.k8s_audit import audit_manifest
import json
# audit_manifest takes a parsed dict; load YAML with PyYAML if you want a CLI.
```

Lint a Dockerfile:

```python
from validator.dockerfile_lint import lint
print(lint(open("manifests/insecure/Dockerfile").read()))
```

## What the validators flag

**Kubernetes (`k8s_audit.py`)** — aligned with the Pod Security Standards
`restricted` profile:

| Rule | Severity |
|---|---|
| `privileged` | CRITICAL |
| `host-network` / `host-pid` / `host-ipc` | HIGH |
| `allow-priv-esc` (not false) | HIGH |
| `run-as-root` (runAsNonRoot not true) | HIGH |
| `writable-rootfs` | MEDIUM |
| `caps-not-dropped` (no drop: [ALL]) | MEDIUM |
| `mutable-image-tag` (latest / untagged) | MEDIUM |
| `no-resource-limits` | LOW |

**Dockerfile (`dockerfile_lint.py`)** — untagged base image, pipe-to-shell,
`ADD` misuse, missing `--no-install-recommends`, and running as root.

## Study the pairs

- `manifests/insecure/` vs `manifests/secure/` — Deployment and Dockerfile.
- Read both, then map each validator finding to the exact line.

## Enforce in a cluster

`policies/` contains Kyverno policies that **block** insecure workloads at
admission time — the real control behind the validator checks:

- `kyverno-disallow-privileged.yaml`
- `kyverno-require-nonroot.yaml`
- `kyverno-require-resource-limits.yaml`

Apply them to a local `kind` cluster (see `tools/README.md`) and watch the
insecure Deployment get rejected.

## Extend it

Add a check that `hostPath` volumes are disallowed, with a test.
