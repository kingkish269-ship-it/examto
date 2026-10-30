# 07 — Cryptographic Failures & Secrets — OWASP A02

## Theory

Two everyday failures turn one mistake into a disaster:

**Weak password storage.** Passwords stored with fast, unsalted hashes (MD5,
SHA1) are cracked almost instantly, and identical passwords produce identical
hashes. Fix: a **salted, slow** hash — bcrypt, scrypt, argon2, or PBKDF2.

**Hardcoded secrets.** API keys/tokens in source code leak to everyone with repo
access and live forever in git history. Fix: keep secrets in **environment
variables or a vault/secrets manager**, and rotate anything ever committed.

This is the app-layer version of the key management you already do in the cloud
(KMS/Key Vault) and data security (DLP).

## Lab

```bash
cd /workspaces/examto/appsec-lab
source .venv/bin/activate 2>/dev/null

# 1) Prove the password hashes are unsalted (two users, same password, same hash):
python3 -m pytest tests/test_exploits.py::test_weak_password_hash_is_unsalted -q

# 2) Find the hardcoded secret sitting in the source:
grep -n "s3cr3t" vulnerable_app/app.py
```

The test passes (it asserts the two hashes are identical = unsalted). The grep
prints the secret committed in the code.

## Verify

- The unsalted-hash test passes (proving the weakness).
- `grep` shows a hardcoded secret in `app.py`.

Real tool: `gitleaks detect --source . --no-git -v` (see module 17).

## Key takeaways

- Passwords: salted, slow hash (bcrypt/scrypt/argon2/PBKDF2) — never MD5/SHA1.
- Secrets: env vars or a vault, never in code; rotate if ever committed.
- Encrypt in transit (TLS) and at rest.
