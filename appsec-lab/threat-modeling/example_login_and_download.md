# Threat model: lab login and file download

A worked example using the lab app, in the `TEMPLATE.md` format.

## 1. Scope

In scope: `POST /login`, session handling, and `GET /download`.
Out of scope: the deployment platform and TLS termination.

## 2. Assets

- User credentials and password hashes.
- Session tokens (identity).
- Files served by `/download`, and any file the process can read.

## 3. Actors

- Legitimate: anonymous visitor, authenticated user, admin.
- Adversarial: external attacker with no account; an authenticated user trying
  to reach other users' data or server files.

## 4. Data-flow diagram

```
[Client] --POST /login--> [App] --lookup--> [Users table]
[Client] --GET /download?file--> [App] --read--> [File system]
```

Trust boundary: the client-to-app HTTP boundary. All input from the client is
untrusted.

## 5. STRIDE analysis

| Threat | Applies here? | Mitigation |
|---|---|---|
| Spoofing | Yes — forgeable session token lets an attacker impersonate admin (exercise 08). | Random server-side session id. |
| Tampering | Yes — `../` in the file name changes which file is read (exercise 05). | Canonicalise and confine to the base directory. |
| Repudiation | Partial — no audit log of logins or downloads. | Log authN events and file access server-side. |
| Information disclosure | Yes — path traversal and verbose errors leak data (exercises 05, 10). | Path confinement; generic errors. |
| Denial of service | Yes — no brute-force throttle on login (exercise 08). | Rate-limit and lock accounts. |
| Elevation of privilege | Yes — weak hashing plus forgeable tokens enable account takeover (exercises 08, 09). | Salted slow hashing; unforgeable sessions; authorization checks. |

## 6. Prioritised risks

1. Account takeover via forgeable session token (high impact, easy).
2. Arbitrary file read via path traversal (high impact, easy).
3. Offline credential cracking via unsalted MD5 (high impact if DB leaks).
4. Brute-force login (medium).
5. Information leak via verbose errors (medium).

## 7. Mitigations and owners

| Risk | Mitigation | Control type | Owner | Status |
|---|---|---|---|---|
| Forgeable token | Random server-side session id | Preventive | app team | fixed in secure mode |
| Path traversal | Resolve + confine path | Preventive | app team | fixed in secure mode |
| Weak hashing | Salted slow hash | Preventive | app team | fixed in secure mode |
| Brute force | Rate limit / lockout | Preventive | app team | fixed in secure mode |
| Verbose errors | Generic error + server-side logging | Preventive/Detective | app team | fixed in secure mode |

## 8. Residual risk

Even fixed, the app has no MFA and no central audit pipeline. For a real system
those would be tracked as accepted or planned, with a named owner.
