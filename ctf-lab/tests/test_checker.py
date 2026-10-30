"""Test the flag checker, scoreboard, and hint logic (no Flask needed)."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import ctf  # noqa: E402


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    # Redirect progress to a temp file so tests never touch real progress.json.
    monkeypatch.setattr(ctf, "PROGRESS", tmp_path / "progress.json")
    importlib.reload  # no-op reference; PROGRESS patched above is what matters
    return ctf


def test_flag_hash_is_stable_and_salted(isolated):
    h1 = ctf.flag_hash("salt-a", "FLAG{x}")
    h2 = ctf.flag_hash("salt-b", "FLAG{x}")
    assert h1 == ctf.flag_hash("salt-a", "FLAG{x}")
    assert h1 != h2  # different salt -> different hash


def test_submit_correct_then_scored(isolated):
    challenges = ctf.load_challenges()
    c = challenges[0]
    # Reconstruct a correct submission by brute-free means: the answer key stores
    # only the hash, so we validate the checker with a known salt/flag pair.
    salt, flag = "t-salt", "FLAG{known}"
    c_test = {"id": "demo", "title": "demo", "tier": "easy", "points": 10,
              "target": "x", "objective": "y", "hints": ["h1", "h2"],
              "salt": salt, "flag_sha256": ctf.flag_hash(salt, flag)}
    progress = {"solved": [], "hints_used": {}}

    assert ctf.cmd_submit([c_test], progress, "demo", flag) == 0
    assert "demo" in progress["solved"]
    # wrong flag returns non-zero and does not double-add
    assert ctf.cmd_submit([c_test], progress, "demo", "FLAG{wrong}") == 1


def test_hints_reveal_in_order(isolated):
    c_test = {"id": "demo", "title": "d", "tier": "easy", "points": 10, "target": "x",
              "objective": "y", "hints": ["first", "second"], "salt": "s", "flag_sha256": "x"}
    progress = {"solved": [], "hints_used": {}}
    assert ctf.cmd_hint([c_test], progress, "demo") == 0
    assert progress["hints_used"]["demo"] == 1
    assert ctf.cmd_hint([c_test], progress, "demo") == 0
    assert progress["hints_used"]["demo"] == 2
    # no more hints -> still returns 0, does not exceed count
    assert ctf.cmd_hint([c_test], progress, "demo") == 0
    assert progress["hints_used"]["demo"] == 2


def test_unknown_challenge(isolated):
    assert ctf.cmd_show(ctf.load_challenges(), {"solved": [], "hints_used": {}}, "nope") == 2


def test_answer_key_loads_and_is_sorted(isolated):
    challenges = ctf.load_challenges()
    assert len(challenges) == 8
    tiers = [ctf.TIER_ORDER[c["tier"]] for c in challenges]
    assert tiers == sorted(tiers)
