# Threat model: <system or feature name>

> Reusable STRIDE template. Copy this file and fill each section. Threat modeling
> finds design flaws before code exists, which is cheaper than finding them in
> testing or production.

## 1. Scope

- What system or feature is in scope?
- What is explicitly out of scope?

## 2. Assets

What is worth protecting? (credentials, personal data, money, availability,
signing keys, audit integrity.)

## 3. Actors

- Legitimate: (anonymous user, authenticated user, admin, service account.)
- Adversarial: (external attacker, malicious user, compromised dependency,
  malicious insider.)

## 4. Data-flow diagram

Describe or sketch the flow: entry points, processes, data stores, external
services, and the **trust boundaries** they cross.

```
[Client] --HTTPS--> [App server] --query--> [Database]
                        |
                        +--outbound--> [Third-party API]
```

## 5. STRIDE analysis

For each element and data flow, ask the six questions:

| Threat | Question | Applies here? | Mitigation |
|---|---|---|---|
| **S**poofing | Can an attacker pretend to be someone else? | | |
| **T**ampering | Can data be modified in transit or at rest? | | |
| **R**epudiation | Can an actor deny an action with no trace? | | |
| **I**nformation disclosure | Can data leak to the wrong party? | | |
| **D**enial of service | Can availability be degraded? | | |
| **E**levation of privilege | Can an actor gain rights they should not have? | | |

## 6. Prioritised risks

List the top risks by impact and likelihood, highest first.

## 7. Mitigations and owners

| Risk | Mitigation | Control type | Owner | Status |
|---|---|---|---|---|

## 8. Residual risk

What remains after mitigations, and who accepts it?
