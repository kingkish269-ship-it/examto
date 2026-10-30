# Room: Broken Access Control (OWASP A01)

**Topic:** OWASP Top 10 · **Difficulty:** core

## Story
The #1 web risk. The app lets you reach data or actions you shouldn't.

## Theory (2 min)
**IDOR** (Insecure Direct Object Reference / BOLA in APIs): an object is returned
by id with no ownership check. Change `/account/1` to `/account/2` and read
someone else's data. The fix is a **server-side** check: the requester must own
the object (or be an admin). Hiding the id in the UI is not a control — the
attacker controls the request.

## What you'll do
In `appsec-lab`, read `exercises/01_broken_access_control.md`, then exploit the
IDOR against the running app and see admin data returned for a normal user.

## Going further
Full attack + fix + test in `appsec-lab/`; capture the flag in the `appsec` room.
