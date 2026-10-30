# Room: Server-Side Request Forgery (SSRF, OWASP A10)

**Topic:** OWASP Top 10 · **Difficulty:** core · **ties to your cloud/network skills**

## Story
You make the server fetch a URL you choose — including internal ones.

## Theory (2 min)
A "fetch this URL" feature with no validation lets an attacker reach internal
services and, in the cloud, the **metadata endpoint** `169.254.169.254` (a
**link-local** address) to steal instance credentials. The fix: allowlist the
scheme (http/https), resolve the hostname, and **reject private, loopback, and
link-local IP ranges** — exactly the network segmentation thinking you already
know, applied in code.

## What you'll do
Read `appsec-lab/exercises/04_ssrf.md`; use SSRF to read a local file, then read
the IP-range-blocking fix.

## Going further
`appsec-lab/` SSRF exploit + fix + tests.
