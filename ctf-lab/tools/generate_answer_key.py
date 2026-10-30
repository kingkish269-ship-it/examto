"""Regenerate challenges.json from the challenge definitions and target flags.

Run this if you change a flag or add a challenge:
    python tools/generate_answer_key.py

It writes salted SHA-256 hashes (not plaintext flags) into challenges.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ctf import flag_hash  # noqa: E402
from target.flags import FLAGS  # noqa: E402

# Public metadata (objective + hints). No plaintext flags here.
DEFS = [
    {"id": "idor", "tier": "easy", "points": 100,
     "title": "Read the admin's account",
     "target": "GET /api/account/<id>",
     "objective": "The app returns any account by id with no ownership check. "
                  "Read the admin account and capture the note it hides.",
     "hints": ["Accounts are numbered. Try ids other than your own.",
               "The admin is id 3.",
               "curl http://127.0.0.1:5000/api/account/3"]},
    {"id": "sqli", "tier": "easy", "points": 100,
     "title": "Leak the secrets table",
     "target": "GET /api/search?username=",
     "objective": "The search query is built by string concatenation. Use a "
                  "UNION to read the hidden secrets table.",
     "hints": ["Break out of the quoted string with a single quote.",
               "The query selects two columns; your UNION must match.",
               "username=' UNION SELECT flag, label FROM secrets-- -"]},
    {"id": "traversal", "tier": "easy", "points": 100,
     "title": "Escape the web root",
     "target": "GET /download?file=",
     "objective": "The download endpoint joins your filename without "
                  "confinement. Read the flag file outside the served folder.",
     "hints": ["The served folder has a parent directory.",
               "Use ../ to climb up one level.",
               "file=../ctf_flag.txt"]},
    {"id": "xss", "tier": "easy", "points": 75,
     "title": "Pop the admin bot",
     "target": "GET /greet?name=",
     "objective": "Your name is reflected into HTML unescaped. Land a script "
                  "payload; a simulated admin bot executes it and leaks its "
                  "cookie in a response header.",
     "hints": ["The value is placed straight into the page.",
               "A <script> tag or an onerror handler triggers the bot.",
               "name=<script>x</script> then read the X-Admin-Cookie header"]},
    {"id": "session", "tier": "medium", "points": 150,
     "title": "Forge an admin session",
     "target": "GET /ctf/admin  (header X-Session)",
     "objective": "The session token is not random — it encodes the username "
                  "and role. Forge an admin token and reach /ctf/admin.",
     "hints": ["Log in as a normal user and look at the token format.",
               "It is base64url of 'username:role'.",
               "base64url('admin:admin') in the X-Session header"]},
    {"id": "ssrf", "tier": "medium", "points": 150,
     "title": "Reach the metadata service",
     "target": "GET /fetch?url=",
     "objective": "The fetch endpoint will request internal addresses. Reach "
                  "the cloud metadata service and read the role credentials.",
     "hints": ["The classic internal target is the link-local metadata IP.",
               "169.254.169.254 serves instance metadata.",
               "url=http://169.254.169.254/latest/meta-data/iam/security-credentials/role"]},
    {"id": "cmdi", "tier": "medium", "points": 125,
     "title": "Run a second command",
     "target": "GET /diag?host=",
     "objective": "The diagnostic runs a shell command built from your input. "
                  "Inject a second command to read the flag from the "
                  "environment variable CTF_FLAG.",
     "hints": ["The host value lands inside a shell command.",
               "A semicolon separates commands.",
               "host=x; printenv CTF_FLAG"]},
    {"id": "jwt", "tier": "hard", "points": 200,
     "title": "alg:none forgery",
     "target": "GET /ctf/jwt-admin  (Authorization: Bearer <jwt>)",
     "objective": "The JWT verifier trusts the token's own 'alg' header. Forge "
                  "an unsigned admin token and access the endpoint.",
     "hints": ["A JWT is three base64url parts: header.payload.signature.",
               "Set the header alg to 'none' and leave the signature empty.",
               "header {\"alg\":\"none\"}, payload {\"user\":\"admin\"}, then "
               "base64url(header)+'.'+base64url(payload)+'.'"]},
]


def main() -> None:
    out = []
    for d in DEFS:
        flag = FLAGS[d["id"]]
        salt = f"ctf-{d['id']}-salt"
        entry = dict(d)
        entry["salt"] = salt
        entry["flag_sha256"] = flag_hash(salt, flag)
        out.append(entry)
    (ROOT / "challenges.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(out)} challenges to challenges.json")


if __name__ == "__main__":
    main()
