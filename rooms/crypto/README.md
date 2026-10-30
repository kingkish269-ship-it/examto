# Room: Cryptographic Failures & Secrets (OWASP A02)

**Topic:** OWASP Top 10 · **Difficulty:** core · **ties to your data-security skills**

## Story
Weak crypto and leaked secrets turn one breach into a catastrophe.

## Theory (2 min)
Passwords must use a **salted, slow** hash (bcrypt, scrypt, argon2, PBKDF2) —
never MD5/SHA1 (fast, often unsalted). Data must be encrypted in transit (TLS)
and at rest. **Secrets** (API keys, tokens) belong in environment variables or a
**vault / secrets manager**, never in source code — and anything ever committed
must be rotated.

## What you'll do
Read `appsec-lab/exercises/09_crypto_and_secrets.md`; see why MD5 password hashes
are unsafe, and find the hardcoded secret with Gitleaks (the `secrets` room).

## Going further
`appsec-lab/` crypto lab; this is the app-layer version of your KMS/DLP work.
