"""Prove each fix BLOCKS the attack in the secure app.

Same attacks as test_exploits.py, now expected to fail or be rejected.
"""

import base64
import os
import pickle


def _login(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def test_idor_blocked(secure):
    client, _ = secure
    token = _login(client, "alice", "password123").get_json()["session"]
    resp = client.get("/api/account/3", headers={"X-Session": token})
    assert resp.status_code == 403


def test_sql_injection_blocked(secure):
    client, _ = secure
    resp = client.get("/api/search", query_string={"username": "x' OR '1'='1"})
    assert resp.get_json() == []


def test_xss_encoded(secure):
    client, _ = secure
    resp = client.get("/greet", query_string={"name": "<script>alert(1)</script>"})
    body = resp.get_data(as_text=True)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body


def test_ssrf_file_scheme_blocked(secure, tmp_path):
    client, _ = secure
    secret = tmp_path / "secret.txt"
    secret.write_text("INTERNAL-ONLY")
    resp = client.get("/fetch", query_string={"url": secret.as_uri()})
    assert resp.status_code == 400


def test_ssrf_internal_ip_blocked(secure):
    client, _ = secure
    resp = client.get("/fetch", query_string={"url": "http://127.0.0.1:80/"})
    assert resp.status_code == 400


def test_path_traversal_blocked(secure):
    client, app = secure
    outside = app.config["FILES_DIR"].parent / "lab_secret_outside.txt"
    resp = client.get("/download", query_string={"file": "../" + outside.name})
    assert resp.status_code == 403


def test_command_injection_blocked(secure):
    client, _ = secure
    resp = client.get("/diag", query_string={"host": "localhost; echo INJECTED"})
    assert resp.status_code == 400


def test_deserialization_safe(secure):
    client, app = secure
    marker = app.config["PWN_MARKER"]
    if marker.exists():
        marker.unlink()

    class Exploit:
        def __reduce__(self):
            return (os.system, (f"touch {marker}",))

    payload = base64.b64encode(pickle.dumps(Exploit()))
    resp = client.post("/prefs", data=payload)
    assert resp.status_code == 400
    assert not marker.exists()


def test_password_hash_salted(secure):
    client, app = secure
    rows = app.extensions["db"].execute(
        "SELECT username, password_hash FROM users WHERE username IN ('alice','bob')"
    ).fetchall()
    hashes = {r["username"]: r["password_hash"] for r in rows}
    assert hashes["alice"] != hashes["bob"]  # salted


def test_rate_limited(secure):
    client, _ = secure
    for _ in range(5):
        _login(client, "alice", "wrong")
    resp = _login(client, "alice", "wrong")
    assert resp.status_code == 429


def test_security_headers_present(secure):
    client, _ = secure
    resp = client.get("/health")
    assert resp.headers["Content-Security-Policy"] == "default-src 'none'"
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
