# Room: Threat Modeling — STRIDE

**Topic:** threat modeling · **Difficulty:** intro

## The story

A team is about to build a login feature. Before a line of code is written, the
security engineer runs a **threat model** — finding design flaws early, when
they are cheapest to fix. Your job is to think like that engineer.

## Theory (2 minutes)

Threat modeling asks, for each part of a system: *what could go wrong?* The most
common framework is **STRIDE** — six categories of threat:

| Letter | Threat | Plain meaning |
|---|---|---|
| **S** | Spoofing | Pretending to be someone else |
| **T** | Tampering | Changing data you shouldn't |
| **R** | Repudiation | Doing something with no trace |
| **I** | Information disclosure | Leaking data |
| **D** | Denial of service | Taking it offline |
| **E** | Elevation of privilege | Gaining rights you shouldn't have |

You map each data flow and entry point to these, then decide a control for each
real risk. (A full template is in `../../appsec-lab/threat-modeling/TEMPLATE.md`.)

## What you will actually do

Think about this specific flaw in the login design:

> The session token is just `base64("username:role")`. An attacker can craft
> their own token that says `admin:admin` and the server trusts it.

The attacker is **pretending to be an admin** without real credentials.

## Your task

Which single STRIDE category does this flaw belong to? Submit the category name
(one word).

```bash
python3 rooms.py submit tm <category>
```
