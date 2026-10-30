# CTF Lab — capture the flags

A gamified, hands-on hacking lab in the style of TryHackMe / Hack The Box, but
fully local and free. You get a deliberately vulnerable target app; you exploit
each weakness yourself to capture a `FLAG{...}`, then submit it to score points.
Difficulty rises from easy to hard.

> **Safety and ethics:** the target is intentionally vulnerable. Run it only on
> `127.0.0.1`. Never deploy it to the public internet — a vulnerable box left
> exposed will be found and abused. Only ever attack systems you own or are
> authorised to test.

## Setup

```bash
cd ctf-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Play

Open two terminals.

**Terminal 1 — start the target:**

```bash
python target/run_target.py        # http://127.0.0.1:5000
```

**Terminal 2 — work the challenges:**

```bash
python ctf.py list                 # see all challenges and your score
python ctf.py show idor            # read the objective
python ctf.py hint idor            # reveal one hint at a time
# ... exploit the target with curl / browser / Burp ...
python ctf.py submit idor 'FLAG{...}'
python ctf.py score
```

Treat the target as a black box over HTTP. (Reading `target/app.py` spoils the
flags.)

## Challenges

| ID | Tier | Pts | Skill |
|---|---|---|---|
| `idor` | easy | 100 | Broken object-level authorization |
| `sqli` | easy | 100 | SQL injection (UNION) |
| `traversal` | easy | 100 | Path traversal |
| `xss` | easy | 75 | Reflected XSS (admin-bot) |
| `session` | medium | 150 | Forgeable session token |
| `ssrf` | medium | 150 | SSRF to cloud metadata |
| `cmdi` | medium | 125 | OS command injection |
| `jwt` | hard | 200 | JWT `alg:none` forgery |

1000 points total.

## Example: first blood on `idor`

```bash
python ctf.py show idor
curl -s http://127.0.0.1:5000/api/account/3    # no ownership check
# copy the FLAG{...} from secret_note
python ctf.py submit idor 'FLAG{...}'
```

## If you get stuck

Use hints first (`python ctf.py hint <id>`). Full solutions are in
[`walkthroughs/`](walkthroughs/) — spoilers, open only after you have tried.

## How it works

- Flags are validated against **salted SHA-256 hashes** in `challenges.json`, so
  the answer key holds no plaintext flags.
- Your progress is saved in `progress.json` (git-ignored).
- `tests/` proves every challenge is solvable and that captured flags match the
  key — run `pytest tests/ -v`.

## Want to host it like TryHackMe / Hackversity?

See [`HOSTING.md`](HOSTING.md) for free and low-cost ways to put this (and a real
CTF platform) online for a small group.

## Extend it

Add a challenge: add its flag to `target/flags.py`, add the vulnerable endpoint
to `target/app.py`, add a definition and hints to
`tools/generate_answer_key.py`, run it to refresh `challenges.json`, and add a
solve test. The test proves your new challenge is actually solvable.
