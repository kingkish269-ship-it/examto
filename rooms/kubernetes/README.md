# Room: Kubernetes Security

**Topic:** cloud-native security · **Difficulty:** advanced · **high demand**

## Story
Kubernetes runs modern apps; its defaults are not secure.

## Theory (2 min)
Harden workloads to the Pod Security Standards "restricted" profile: no
privileged containers, `runAsNonRoot: true`, `allowPrivilegeEscalation: false`,
read-only root filesystem, drop all capabilities, set resource limits, no host
namespaces. Enforce at **admission** with Kyverno/OPA so insecure pods are
rejected, not just detected. Add RBAC least-privilege and NetworkPolicies.

## What you'll do
Compare `container-k8s-lab/manifests/insecure` vs `secure` Deployments; run the
manifest validator; read the Kyverno policies in `policies/`.

## Going further
`container-k8s-lab/` (validator + Kyverno + kube-bench guide).
