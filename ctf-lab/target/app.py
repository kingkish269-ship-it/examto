"""CTF target application.

A deliberately vulnerable Flask app whose vulnerabilities each hide a FLAG.
You capture a flag by exploiting the matching weakness over HTTP, then submit
it with ``python ctf.py submit <id> <flag>``.

WARNING: intentionally insecure. Run locally only (127.0.0.1). Never deploy.

Play fair: interact with this app over HTTP as a black box. Reading this source
reveals the flags and spoils the challenges.
"""

from __future__ import annotations

import base64
import json
import sqlite3

from flask import Flask, Response, jsonify, request

from .flags import FLAGS, INTERNAL_METADATA


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, secret_note TEXT);
        CREATE TABLE secrets (flag TEXT, label TEXT);
        """
    )
    conn.executemany(
        "INSERT INTO users (id, username, role, secret_note) VALUES (?,?,?,?)",
        [
            (1, "alice", "user", "nothing here"),
            (2, "bob", "user", "nothing here"),
            (3, "admin", "admin", FLAGS["idor"]),
        ],
    )
    conn.execute("INSERT INTO secrets (flag, label) VALUES (?, ?)", (FLAGS["sqli"], "vault"))
    conn.commit()
    return conn


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def create_target_app() -> Flask:
    app = Flask(__name__)
    conn = _db()

    # 1) IDOR (easy): no ownership check; reading admin (id 3) leaks the flag.
    @app.get("/api/account/<int:account_id>")
    def account(account_id: int):
        row = conn.execute(
            "SELECT id, username, role, secret_note FROM users WHERE id = ?", (account_id,)
        ).fetchone()
        if row is None:
            return jsonify(error="not found"), 404
        return jsonify(dict(row))

    # 2) SQL injection (easy): string-built query; UNION leaks the secrets table.
    @app.get("/api/search")
    def search():
        username = request.args.get("username", "")
        query = "SELECT username, role FROM users WHERE username = '" + username + "'"
        try:
            rows = conn.execute(query).fetchall()
        except sqlite3.Error as exc:
            return jsonify(error=str(exc)), 400
        return jsonify([dict(r) for r in rows])

    # 3) Path traversal (easy): the flag file sits outside the served folder.
    @app.get("/download")
    def download():
        import os
        from pathlib import Path
        base = Path(app.config["_FILES_DIR"])
        name = request.args.get("file", "welcome.txt")
        target = Path(os.path.join(str(base), name))  # no confinement
        try:
            return Response(target.read_text(encoding="utf-8"), mimetype="text/plain")
        except Exception:
            return jsonify(error="not found"), 404

    # 4) Reflected XSS (easy): a simulated admin bot "runs" a script payload.
    @app.get("/greet")
    def greet():
        name = request.args.get("name", "guest")
        body = f"<h1>Hello {name}</h1>"  # unescaped reflection
        resp = Response(body, mimetype="text/html")
        lowered = name.lower()
        if "<script" in lowered or "onerror=" in lowered or "onload=" in lowered:
            # The admin bot executed your payload and leaked its cookie.
            resp.headers["X-Admin-Cookie"] = FLAGS["xss"]
        return resp

    # 5) Broken auth (medium): session token is just base64("user:role").
    @app.get("/ctf/admin")
    def admin_area():
        token = request.headers.get("X-Session", "")
        try:
            username, role = _b64url_decode(token).decode().split(":", 1)
        except Exception:
            return jsonify(error="invalid session"), 401
        if role == "admin":
            return jsonify(flag=FLAGS["session"])
        return jsonify(error="forbidden"), 403

    # 6) SSRF (medium): fetches any URL; internal metadata host leaks a flag.
    @app.get("/fetch")
    def fetch():
        from urllib.parse import urlparse
        url = request.args.get("url", "")
        parsed = urlparse(url)
        if parsed.hostname in {"169.254.169.254", "metadata", "metadata.internal"}:
            data = INTERNAL_METADATA.get(parsed.path)
            if data:
                return Response(data, mimetype="text/plain")
            return jsonify(error="no such metadata path"), 404
        return jsonify(error="only demo internal fetches are wired up"), 400

    # 7) OS command injection (medium): user input into a shell string.
    @app.get("/diag")
    def diag():
        import subprocess
        host = request.args.get("host", "localhost")
        flag = FLAGS["cmdi"]
        # The flag is "on the box"; a shell metacharacter can read it.
        cmd = f"echo pinging {host}; true"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              env={"CTF_FLAG": flag}, timeout=5)
        out = proc.stdout
        if "printenv CTF_FLAG" in host or "echo $CTF_FLAG" in host:
            out += "\n" + flag
        return jsonify(output=out.strip())

    # 8) JWT alg:none (hard): verification trusts the header's algorithm.
    @app.get("/ctf/jwt-admin")
    def jwt_admin():
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify(error="missing bearer token"), 401
        token = auth[len("Bearer "):]
        try:
            header_b64, payload_b64, _sig = token.split(".")
            header = json.loads(_b64url_decode(header_b64))
            payload = json.loads(_b64url_decode(payload_b64))
        except Exception:
            return jsonify(error="malformed token"), 400
        # Vulnerability: accept alg:none without verifying a signature.
        if str(header.get("alg", "")).lower() == "none" and payload.get("user") == "admin":
            return jsonify(flag=FLAGS["jwt"])
        return jsonify(error="not an admin token"), 403

    @app.get("/health")
    def health():
        return jsonify(status="ok", challenges=len(FLAGS))

    # Set up the traversal flag file outside the served directory.
    import tempfile
    from pathlib import Path
    files_dir = Path(tempfile.mkdtemp(prefix="ctf_web_"))
    (files_dir / "welcome.txt").write_text("public welcome\n", encoding="utf-8")
    (files_dir.parent / "ctf_flag.txt").write_text(FLAGS["traversal"] + "\n", encoding="utf-8")
    app.config["_FILES_DIR"] = str(files_dir)
    app.config["_FLAG_PARENT"] = str(files_dir.parent)

    return app
