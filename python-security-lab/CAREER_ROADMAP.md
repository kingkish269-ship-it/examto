# Cloud, DevSecOps, and Application Security Roadmap

## Target profile

Build toward roles such as:

- Senior Cloud Security Engineer
- Cloud Security Architect
- DevSecOps Security Engineer or Architect
- Platform Security Engineer
- Product Security Engineer with a cloud focus
- Product Security Architect

The positioning is cloud and product security, not junior software development or pure penetration testing. Existing endpoint, network, Zero Trust, cloud, and data-security knowledge remains the foundation.

## Python boundary

Do not attempt to learn all of Python. The required finish line is the ability to read and modify a 100–200-line security script, call APIs, process JSON/YAML, handle failures, test security rules, and produce reports.

### Required Python

- Lists, dictionaries, sets, loops, conditions, and functions
- Modules, virtual environments, packages, and basic type hints
- JSON, YAML, CSV, files, timestamps, and regular expressions
- REST APIs, headers, authentication, pagination, timeouts, and rate limits
- Exceptions, retries, logging, environment variables, and CLI arguments
- `requests`, `boto3`, and selected Microsoft Graph/Azure SDK use
- `pytest`, fixtures, assertions, and mocked API responses
- Secure handling of input, paths, commands, credentials, TLS, and SQL

### Not required initially

- LeetCode or competitive programming
- Advanced algorithms
- Web-framework expertise
- Metaclasses or advanced decorators
- Complex concurrency or asynchronous programming
- GUI or machine-learning development

## Supporting engineering skills

### Git

Practice branches, commits, pull requests, diffs, conflicts, `.gitignore`, secret prevention, and safe reversions.

### Linux

Practice permissions, processes, environment variables, pipes, `curl`, `jq`, logs, SSH fundamentals, and small Bash commands.

### Configuration and query languages

- YAML for pipelines, Kubernetes, and security rules
- Terraform/HCL for cloud resources and controls
- Basic SQL for queries, permissions, and injection prevention
- Basic Rego after gaining confidence with Kyverno

## Application security

### Foundation

Understand clients, servers, databases, HTTP, headers, cookies, sessions, JWT, TLS, CORS, REST APIs, proxies, microservices, message queues, file uploads, authentication, and authorization.

### Vulnerability practice

Reproduce and remediate:

- Broken access control
- Authentication and session failures
- SQL, command, and template injection
- Cross-site scripting
- Server-side request forgery
- Path traversal and unsafe file upload
- Insecure deserialization
- Security misconfiguration
- Vulnerable dependencies
- Cryptographic failures
- Missing security logging

For each issue, identify the untrusted input, dangerous operation, business impact, correct control, and verification test.

### API security

Practice object-level and function-level authorization, token handling, rate limiting, mass assignment, excessive data exposure, resource exhaustion, API inventory, versioning, and third-party API trust.

### Secure code review

Begin with Python. Then learn to read security-sensitive Java/Spring and JavaScript/Node code. Focus on controllers, authorization, database access, deserialization, file handling, secrets, and outbound HTTP calls. Writing complete Java or JavaScript applications is not required initially.

### Threat modeling

Practice data-flow diagrams, trust boundaries, assets, entry points, STRIDE, abuse cases, security requirements, mitigations, and residual risk. Model login, checkout, password reset, file upload, public APIs, and cloud data pipelines.

## DevSecOps and secure SDLC

Understand the security activity at every stage:

| Stage | Security activity |
|---|---|
| Requirements | Security and privacy requirements |
| Design | Threat modeling and architecture review |
| Coding | Secure patterns and secret prevention |
| Pull request | Review, SAST, and policy checks |
| Build | Dependency and container scanning |
| Test | DAST and API security validation |
| Release | SBOM, signing, provenance, and approvals |
| Deployment | IaC and Kubernetes policies |
| Runtime | Detection, vulnerability management, and response |

### Pipeline tools

- Gitleaks or TruffleHog for secrets
- Semgrep and CodeQL for SAST
- Trivy, Grype, or OWASP Dependency-Check for dependencies and containers
- OWASP ZAP for DAST
- Checkov and Trivy for infrastructure-as-code
- Syft for SBOM generation
- Cosign for artifact signing and verification
- GitHub Actions first, then enough GitLab CI and Jenkins to review them

A useful pipeline checks source, tests, secrets, code, dependencies, containers, IaC, SBOM, signatures, and policy before release. Learn to tune false positives and make risk-based gates rather than blocking every finding.

## Containers, Kubernetes, and supply chain

### Docker

Practice multi-stage builds, non-root users, minimal images, pinned versions, read-only filesystems, limited capabilities, secret handling, health checks, and image scanning.

### Kubernetes

Practice Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, service accounts, RBAC, NetworkPolicy, security contexts, resource limits, Pod Security Standards, audit logging, and admission control.

Write Kyverno policies that reject privileged/root containers, host networking, host-path mounts, mutable image tags, unapproved registries, missing limits, and unsigned images.

### Supply chain

Understand dependency pinning, SBOMs, signatures, provenance, protected branches, restricted workflow permissions, and SLSA concepts.

## Cloud automation projects

### Project 1: Cloud Exposure Auditor

Build a Python CLI that examines sample and read-only AWS data for public storage, exposed security groups, wildcard IAM, inactive access keys, missing logging, unencrypted storage/databases, and public databases. Produce JSON/CSV findings, evidence, remediation, and CI-friendly exit codes.

### Project 2: Secure CI/CD Pipeline

Use a small vulnerable application. Add tests, Gitleaks, Semgrep, dependency scanning, a container build, Trivy, SBOM generation, signing, and risk-based release gates.

### Project 3: Application Security Assessment

Produce an architecture diagram, threat model, OWASP/API findings, risk ratings, fixed code, verification tests, and an executive summary.

### Project 4: Kubernetes Security Guardrails

Build a hardened deployment with RBAC, NetworkPolicy, security contexts, image scanning, Kyverno policy, and signed-image verification.

## Six-month sequence

Assume 8–10 focused hours each week.

### Month 1: Python, Git, and Linux

Complete the eight drills and expand the security-group audit into Project 1. Be able to explain every function and add a security rule with assistance.

### Month 2: Application security

Practice HTTP, authorization, OWASP vulnerabilities, API security, secure code review, fixes, tests, and threat modeling. Complete Project 3's first version.

### Month 3: DevSecOps

Create Project 2 with GitHub Actions, secret scanning, SAST, SCA, container scanning, DAST, and meaningful gates.

### Month 4: Containers, Kubernetes, and Terraform

Harden Docker and Kubernetes workloads, scan Terraform, and implement Project 4 guardrails.

### Month 5: Supply chain and architecture

Add SBOMs, signing, provenance, architecture reviews, exception handling, and risk acceptance. Connect the four projects into an end-to-end secure delivery story.

### Month 6: Interview readiness

Practice a Python automation walkthrough, secure-code-review exercise, threat model, CI/CD design, Kubernetes review, cloud incident scenario, and stakeholder communication. Apply while interview preparation continues.

## Weekly shadow-coding method

Kiro handles file editing and test execution. The learner must still understand decisions because interviews and production reviews cannot be delegated.

1. Observe a working example and its output.
2. Identify input, decision, output, and failure condition.
3. Request one security-rule change.
4. Review the diff and tests.
5. Diagnose one intentionally introduced defect.
6. Explain the final behavior as if speaking to an engineering team.
7. Revisit the pattern one week later.

## Readiness criteria

A candidate is ready to pursue senior cloud/product-security interviews when they can:

- Explain and modify security automation without memorizing syntax
- Review cloud and application architecture for trust-boundary failures
- Identify and remediate common web/API vulnerabilities
- Design risk-based CI/CD controls
- Review Docker, Kubernetes, and Terraform security
- Explain SBOM, signing, and provenance
- Distinguish false positives from exploitable findings
- Present technical risk clearly to engineers and leadership
- Demonstrate the four projects and explain every important decision

## Priorities to avoid

Until the portfolio is complete, avoid collecting more certifications, studying multiple programming languages, starting LeetCode, attempting every security tool at once, or depending on generated code that cannot be explained.
