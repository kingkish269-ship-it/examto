# Room: Authentication, Sessions & JWT (OWASP A07)

**Topic:** OWASP Top 10 · **Difficulty:** core

## Story
If identity can be forged, everything else fails.

## Theory (2 min)
Weak session tokens (guessable, or encoding `username:role`) can be forged — mint
your own `admin` token. Fix: **random, server-side** session ids that carry no
attacker-controllable meaning. **JWTs** are signed tokens; a classic flaw is
accepting the header's `alg: none` (no signature) — always pin the algorithm and
verify the signature. Add brute-force throttling and MFA.

## What you'll do
Read `appsec-lab/exercises/08_auth_session.md`; forge the insecure token. In
`ctf-lab`, the `jwt` challenge is an `alg:none` forgery.

## Going further
`appsec-lab/` auth lab and `ctf-lab/` JWT challenge.
