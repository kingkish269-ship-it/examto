# Room: Container Security

**Topic:** cloud-native security · **Difficulty:** core

## Story
Containers package your app — and its vulnerabilities — for deployment.

## Theory (2 min)
Harden images: pin the base image by digest (not `latest`), run as a **non-root**
user, use a minimal/distroless base, set a read-only root filesystem, drop Linux
capabilities, and don't pipe downloads into a shell at build time. Scan images
with Trivy/Grype for CVEs. A container running as root is a key finding.

## What you'll do
Read `container-k8s-lab/manifests/insecure/Dockerfile` vs `secure/Dockerfile`,
and run the Dockerfile linter in that lab.

## Going further
`container-k8s-lab/` (Dockerfile linter + Trivy guide).
