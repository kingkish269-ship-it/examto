# 09 — Cryptographic Failures and Secret Management

**OWASP A02:2021 — Cryptographic Failures.**

## Where

- Password storage in `_seed` / `login` (`vulnerable_app/app.py`).
- A hardcoded `HARDCODED_SECRET` committed in source.

## Flaw 1: weak password storage

Vulnerable mode stores passwords as unsalted MD5. MD5 is fast and unsalted, so:

- identical passwords produce identical hashes (no salt), and
- attackers crack them with rainbow tables or GPUs almost instantly.

Confirm the missing salt:

```bash
pytest tests/test_exploits.py::test_weak_password_hash_is_unsalted -v
# alice and bob share a password -> identical hash
```

## Flaw 2: hardcoded secret

```python
HARDCODED_SECRET = "s3cr3t-signing-key-do-not-commit"
```

A secret in source control leaks to everyone with repo access and lives forever
in git history.

## Source → Sink → Impact → Control

- **Impact:** mass credential compromise; a leaked signing key lets attackers
  forge tokens.
- **Controls:**
  - Store passwords with a slow, salted, adaptive hash (bcrypt, scrypt,
    argon2, or PBKDF2).
  - Keep secrets in environment variables or a secrets manager / vault, never
    in code. Rotate anything that was ever committed.

## The fixes

```python
from werkzeug.security import generate_password_hash, check_password_hash
password_hash = generate_password_hash(raw)          # salted + slow
ok = check_password_hash(stored_hash, submitted)

# secret from the environment, not the source:
app.config["SECRET_KEY"] = os.environ["LAB_SECRET_KEY"]
```

## Detect with free tools

```bash
semgrep --config auto vulnerable_app/   # flags md5 for passwords
gitleaks detect --source . --no-git -v  # finds the hardcoded secret
```

## Connect to your background

This is the same key-management discipline you apply in the cloud (KMS, Key
Vault, rotation), expressed at the application layer.
