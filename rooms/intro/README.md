# Room: Intro to Application Security

**Topic:** application security basics · **Difficulty:** absolute beginner

> This room assumes you know nothing about AppSec. You cannot break anything.
> Read the theory, do the objectives one at a time, and use the hint if stuck.

## The story

You're moving from infrastructure security (endpoint, network, cloud) into
**application security** — finding and fixing the flaws in the software itself.
Before any tools or exploits, you need one mental model. This room gives it to
you.

## Theory (3 minutes)

A web app has four parts: a **client** (browser), a **server** (your code), a
**database**, and often other services it calls.

A request flows: the client sends input → the server reads it → the server may
pass it to a **sink** (a database query, the file system, a shell, an HTML
page) → a response goes back.

**The one idea behind almost every web vulnerability:**

> Untrusted input reaches a dangerous operation without the right check,
> encoding, or authorization in between.

Two words you'll use constantly:
- **Source** — where untrusted input enters (a form field, URL, header, cookie).
- **Sink** — the dangerous operation it reaches (SQL query, shell command, HTML).

And the golden rule of AppSec:

> **Never trust input from the client — even if your own app produced it.**
> The attacker fully controls the request. All real checks happen on the server.

That rule is the answer to this room.

## Objectives

1. Read the theory above.
2. Understand the client → server → sink flow.
3. Learn the terms **source** and **sink**.
4. Learn the golden rule: do we trust data from the client?
5. Answer the task below.

## Task

The golden rule says you should ___ trust data coming from the client.
Should you trust it? Answer **true** or **false**.

```bash
python3 rooms.py submit intro <true-or-false>
```

## What's next

After this, the rooms get hands-on: you'll run a scanner (SAST), attack a live
app (DAST), exploit a real flaw and capture a flag (AppSec), model threats, and
gate a pipeline (CI/CD). The deep versions are the `appsec-lab/` and `ctf-lab/`.
