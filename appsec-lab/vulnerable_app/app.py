"""Deliberately vulnerable Flask application for Application Security training.

WARNING
-------
This application contains intentional security vulnerabilities. It exists only
to be attacked and fixed inside a local lab. Never deploy it, never expose it to
a network, and never run it with real data. It binds to 127.0.0.1 by design.

How it works
------------
Every vulnerable route has two code paths controlled by one flag:

    app.config["SECURE"]  ->  False = vulnerable behaviour
                              True  = fixed, secure behaviour

Reading both branches side by side is the core learning exercise. The test
suite (tests/) proves each attack succeeds when SECURE is False and is blocked
when SECURE is True.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import ipaddress
import os
import pickle
import secrets
import socket
import sqlite3
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from flask import Flask, Response, g, jsonify, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

# A hardcoded secret committed to source control. This is itself a finding
# (A02 / secret sprawl) and is used to show why secrets must come from the
# environment, never from code.
HARDCODED_SECRET = "s3cr3t-signing-key-do-not-commit"  # noqa: S105 (intentional)

SERVER_SECRET = "server-side-metadata-token-9f83"


def _db(app: Flask) -> sqlite3.Connection:
    if "db" not in app.extensions:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _seed(conn, app.config["SECURE"])
        app.extensions["db"] = conn
    return app.extensions["db"]


def _seed(conn: sqlite3.Connection, secure: bool) -> None:
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            balance INTEGER
        );
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY,
            owner TEXT,
            body TEXT
        );
        """
    )

    def hash_password(raw: str) -> str:
        if secure:
            # A02 fix: salted, slow, adaptive hash.
            return generate_password_hash(raw)
        # A02 vulnerability: fast, unsalted MD5.
        return hashlib.md5(raw.encode()).hexdigest()  # noqa: S324 (intentional)

    users = [
        (1, "alice", hash_password("password123"), "user", 500),
        (2, "bob", hash_password("password123"), "user", 1200),
        (3, "admin", hash_password("admin-super-secret"), "admin", 999999),
    ]
    conn.executemany(
        "INSERT INTO users (id, username, password_hash, role, balance) VALUES (?,?,?,?,?)",
        users,
    )
    conn.executemany(
        "INSERT INTO notes (owner, body) VALUES (?,?)",
        [("alice", "Alice private note"), ("bob", "Bob private note")],
    )
    conn.commit()


def _issue_session(app: Flask, username: str, role: str) -> str:
    if app.config["SECURE"]:
        # A07 fix: random, server-side session identifier.
        token = secrets.token_urlsafe(32)
        app.extensions.setdefault("sessions", {})[token] = {"username": username, "role": role}
        return token
    # A07 vulnerability: guessable/forgeable token derived only from the username.
    return base64.b64encode(f"{username}:{role}".encode()).decode()


def _resolve_session(app: Flask, token: str) -> dict | None:
    if not token:
        return None
    if app.config["SECURE"]:
        return app.extensions.get("sessions", {}).get(token)
    try:
        username, role = base64.b64decode(token.encode()).decode().split(":", 1)
        return {"username": username, "role": role}
    except Exception:
        return None


def create_app(secure: bool = False) -> Flask:
    """Build the lab app. secure=False is vulnerable; secure=True is fixed."""
    app = Flask(__name__)
    app.config["SECURE"] = secure
    app.config["SECRET_KEY"] = os.environ.get("LAB_SECRET_KEY", HARDCODED_SECRET)
    app.config["LOGIN_ATTEMPTS"] = {}
    app.extensions = {}

    files_dir = Path(tempfile.mkdtemp(prefix="appsec_files_"))
    (files_dir / "welcome.txt").write_text("Public welcome file.\n", encoding="utf-8")
    secret_outside = files_dir.parent / "lab_secret_outside.txt"
    secret_outside.write_text("TOP-SECRET-OUTSIDE-WEBROOT\n", encoding="utf-8")
    app.config["FILES_DIR"] = files_dir

    marker = Path(tempfile.gettempdir()) / f"appsec_pwned_{secrets.token_hex(4)}"
    app.config["PWN_MARKER"] = marker

    _db(app)

    def current_user() -> dict | None:
        return _resolve_session(app, request.headers.get("X-Session", ""))

    # ---- A01: Broken Access Control (IDOR) -------------------------------
    @app.get("/api/account/<int:account_id>")
    def account(account_id: int):
        user = current_user()
        if user is None:
            return jsonify(error="login required"), 401
        row = _db(app).execute(
            "SELECT id, username, role, balance FROM users WHERE id = ?", (account_id,)
        ).fetchone()
        if row is None:
            return jsonify(error="not found"), 404
        if app.config["SECURE"]:
            # A01 fix: enforce ownership. Users may only read their own account.
            if row["username"] != user["username"] and user["role"] != "admin":
                return jsonify(error="forbidden"), 403
        # A01 vulnerability: no ownership check; any id is returned.
        return jsonify(dict(row))

    # ---- A03: SQL Injection ----------------------------------------------
    @app.get("/api/search")
    def search():
        username = request.args.get("username", "")
        conn = _db(app)
        if app.config["SECURE"]:
            # A03 fix: parameterised query.
            rows = conn.execute(
                "SELECT username, role FROM users WHERE username = ?", (username,)
            ).fetchall()
        else:
            # A03 vulnerability: string concatenation allows injection.
            query = "SELECT username, role FROM users WHERE username = '" + username + "'"
            rows = conn.execute(query).fetchall()
        return jsonify([dict(r) for r in rows])

    # ---- A03: Reflected Cross-Site Scripting ------------------------------
    @app.get("/greet")
    def greet():
        name = request.args.get("name", "guest")
        if app.config["SECURE"]:
            # A03 fix: contextual output encoding.
            body = f"<h1>Hello {escape(name)}</h1>"
        else:
            # A03 vulnerability: untrusted input reflected into HTML unescaped.
            body = f"<h1>Hello {name}</h1>"
        return Response(body, mimetype="text/html")

    # ---- SSRF (A10) -------------------------------------------------------
    @app.get("/fetch")
    def fetch():
        url = request.args.get("url", "")
        if app.config["SECURE"]:
            blocked = _ssrf_reason(url)
            if blocked:
                return jsonify(error=blocked), 400
        else:
            # A10 vulnerability: no scheme/host validation. file:// and internal
            # addresses are reachable.
            pass
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:  # noqa: S310
                return Response(resp.read()[:2048], mimetype="text/plain")
        except Exception as exc:  # noqa: BLE001
            return jsonify(error=str(exc)), 502

    # ---- Path Traversal ---------------------------------------------------
    @app.get("/download")
    def download():
        name = request.args.get("file", "welcome.txt")
        base = app.config["FILES_DIR"]
        if app.config["SECURE"]:
            # Fix: resolve and confine to the base directory.
            target = (base / name).resolve()
            if not str(target).startswith(str(base.resolve()) + os.sep):
                return jsonify(error="forbidden"), 403
        else:
            # Vulnerability: user-controlled path joined directly.
            target = Path(os.path.join(str(base), name))
        try:
            return Response(target.read_text(encoding="utf-8"), mimetype="text/plain")
        except Exception as exc:  # noqa: BLE001
            return jsonify(error=str(exc)), 404

    # ---- OS Command Injection --------------------------------------------
    @app.get("/diag")
    def diag():
        host = request.args.get("host", "localhost")
        if app.config["SECURE"]:
            # Fix: no shell, strict allowlist of characters.
            if not all(c.isalnum() or c in ".-" for c in host):
                return jsonify(error="invalid host"), 400
            proc = subprocess.run(
                ["echo", "diagnostic for", host],
                capture_output=True, text=True, timeout=5,
            )
        else:
            # Vulnerability: user input concatenated into a shell command.
            proc = subprocess.run(
                "echo diagnostic for " + host,
                shell=True, capture_output=True, text=True, timeout=5,
            )
        return jsonify(output=proc.stdout.strip())

    # ---- Insecure Deserialization ----------------------------------------
    @app.post("/prefs")
    def prefs():
        blob = request.get_data()
        if app.config["SECURE"]:
            # Fix: never unpickle untrusted data; use a safe format.
            import json
            try:
                data = json.loads(blob.decode() or "{}")
            except Exception:
                return jsonify(error="invalid json"), 400
            return jsonify(ok=True, theme=data.get("theme", "light"))
        # Vulnerability: untrusted input deserialized with pickle -> RCE.
        try:
            data = pickle.loads(base64.b64decode(blob))  # noqa: S301
        except Exception as exc:  # noqa: BLE001
            return jsonify(error=str(exc)), 400
        return jsonify(ok=True, theme=str(data))

    # ---- A02: Cryptographic / password storage ---------------------------
    @app.post("/login")
    def login():
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        attempts = app.config["LOGIN_ATTEMPTS"]

        if app.config["SECURE"]:
            # A07 fix: throttle brute force.
            if attempts.get(username, 0) >= 5:
                return jsonify(error="account temporarily locked"), 429

        row = _db(app).execute(
            "SELECT username, role, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        ok = False
        if row is not None:
            if app.config["SECURE"]:
                ok = check_password_hash(row["password_hash"], password)
            else:
                ok = row["password_hash"] == hashlib.md5(password.encode()).hexdigest()  # noqa: S324

        if not ok:
            attempts[username] = attempts.get(username, 0) + 1
            return jsonify(error="invalid credentials"), 401

        attempts[username] = 0
        token = _issue_session(app, row["username"], row["role"])
        return jsonify(session=token, role=row["role"])

    # ---- A05: Security Misconfiguration / headers / errors ----------------
    @app.after_request
    def harden(resp: Response) -> Response:
        if app.config["SECURE"]:
            resp.headers["X-Content-Type-Options"] = "nosniff"
            resp.headers["X-Frame-Options"] = "DENY"
            resp.headers["Content-Security-Policy"] = "default-src 'none'"
            resp.headers["Referrer-Policy"] = "no-referrer"
            resp.headers.pop("Server", None)
        return resp

    @app.errorhandler(500)
    def on_error(exc):  # noqa: ANN001
        if app.config["SECURE"]:
            # Fix: generic error, no internals leaked.
            return jsonify(error="internal server error"), 500
        # Vulnerability: leak the exception detail to the client.
        return jsonify(error=repr(exc)), 500

    @app.get("/health")
    def health():
        return jsonify(status="ok", secure=app.config["SECURE"])

    return app


def _ssrf_reason(url: str) -> str | None:
    """Return a rejection reason for an unsafe URL, or None if allowed."""
    parts = urllib.parse.urlparse(url)
    if parts.scheme not in {"http", "https"}:
        return "only http/https allowed"
    host = parts.hostname or ""
    try:
        infos = socket.getaddrinfo(host, None)
    except Exception:
        return "host did not resolve"
    for info in infos:
        addr = ipaddress.ip_address(info[4][0])
        if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
            return "target resolves to an internal address"
    return None


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit("Use run_server.py; do not run app.py directly.")
