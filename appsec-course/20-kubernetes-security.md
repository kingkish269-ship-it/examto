# 20 — Kubernetes Security

## Theory

Kubernetes runs modern apps, and its defaults are **not** secure. Harden
workloads to the Pod Security Standards **"restricted"** profile:
- no `privileged` containers,
- `runAsNonRoot: true`,
- `allowPrivilegeEscalation: false`,
- read-only root filesystem,
- drop all capabilities,
- set CPU/memory limits,
- no host namespaces (`hostNetwork/hostPID/hostIPC`).

Then **enforce at admission** with **Kyverno** or **OPA Gatekeeper** so insecure
pods are *rejected*, not merely detected. Add **RBAC** least-privilege and
**NetworkPolicies** (your network-segmentation skills, in the cluster).

## Lab

```bash
cd /workspaces/examto/container-k8s-lab

# Compare insecure vs hardened Deployments:
cat manifests/insecure/deployment.yaml
cat manifests/secure/deployment.yaml

# Run the manifest validator (tests show insecure vs secure):
python3 -m unittest discover -v

# See the admission policies that would BLOCK bad pods in a real cluster:
ls policies/ && cat policies/kyverno-require-nonroot.yaml
```

The validator flags `privileged`, `host-network`, `run-as-root`, and
`mutable-image-tag` on the insecure Deployment; the secure one passes.

## Verify

The unittest run passes, confirming the validator flags the insecure pod and
clears the hardened one. You can read the Kyverno policies that enforce this.

## Key takeaways

- Apply the Pod Security "restricted" profile to every workload.
- Enforce with Kyverno/OPA at admission — detection isn't enough.
- RBAC least-privilege + NetworkPolicies complete it.
