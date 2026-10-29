# Free container & Kubernetes security tools

All free and open source. The lab validators teach the detection logic; these
tools are what you run in a real job.

## Local cluster (free)

```bash
# kind runs Kubernetes in Docker.
kind create cluster --name appsec
```

## Trivy — image and config scanning

```bash
trivy image python:3.11-slim         # scan an image for CVEs
trivy config manifests/insecure/     # scan manifests for misconfig
```

## kube-bench — CIS Kubernetes benchmark

Runs the CIS checks against a cluster. Use the official job manifest from the
kube-bench repo.

## Kyverno — policy as code (admission control)

```bash
# Install Kyverno, then apply the lab policies:
kubectl apply -f policies/
# Try to deploy the insecure workload -> it is rejected:
kubectl apply -f manifests/insecure/deployment.yaml
# The secure workload is admitted:
kubectl apply -f manifests/secure/deployment.yaml
```

## Docker hardening checks

- Scan images with Trivy or Grype.
- Use minimal/distrolesss base images, pin by digest, run as non-root,
  set a read-only root filesystem, and drop all capabilities.

Docs: kind https://kind.sigs.k8s.io/ · Trivy https://trivy.dev/ ·
Kyverno https://kyverno.io/ · kube-bench https://github.com/aquasecurity/kube-bench
