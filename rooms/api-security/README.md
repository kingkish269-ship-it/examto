# Room: API Security (OWASP API Top 10)

**Topic:** API security · **Difficulty:** core · **high demand**

## Story
Modern apps are APIs. They have their own Top 10.

## Theory (2 min)
The headline API risk is **BOLA** (Broken Object Level Authorization) — the API
version of IDOR, and OWASP API #1. Others: broken authentication, broken
**function-level** authorization, excessive data exposure (returning more fields
than the client needs), mass assignment, and lack of rate limiting. The fixes:
authorize **every object and function** on the server, return only needed fields,
and rate-limit.

## What you'll do
Re-examine `appsec-lab`'s `/api/account/<id>` and `/api/search` as API endpoints;
identify BOLA and excessive data exposure. Optional: stand up OWASP crAPI.

## Going further
`appsec-lab/` + the OWASP API Security Top 10.
