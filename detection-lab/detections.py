"""Detection rules over security event logs (blue-team / SOC engineering).

Each rule scans a list of event dicts and returns alerts. This is the logic a
detection engineer writes and tunes; in production the same ideas are expressed
as Sigma rules or SIEM queries (Splunk SPL, KQL). Pure standard library.

Event shapes (see data/events.json):
  auth: {ts, type:"auth", action:"login_failed"|"login_success", user, src_ip, country}
  http: {ts, type:"http", method, path, status, src_ip}
  iam:  {ts, type:"iam", action, actor, target}
"""

from __future__ import annotations

import re

SQLI_PATTERNS = [r"' or '?1'?='?1", r"union\s+select", r"--", r";\s*drop\s+table", r"sleep\("]
TRAVERSAL_PATTERNS = [r"\.\./", r"%2e%2e%2f", r"/etc/passwd"]
KNOWN_ADMINS = {"root", "secops"}


def _alert(rule: str, severity: str, entity: str, evidence: str) -> dict:
    return {"rule": rule, "severity": severity, "entity": entity, "evidence": evidence}


def detect_brute_force(events, threshold: int = 5, window: int = 120) -> list[dict]:
    """Many failed logins from one source IP in a short window."""
    fails = [e for e in events if e.get("type") == "auth" and e.get("action") == "login_failed"]
    by_ip: dict[str, list[int]] = {}
    for e in fails:
        by_ip.setdefault(e["src_ip"], []).append(e["ts"])
    alerts = []
    for ip, times in by_ip.items():
        times.sort()
        for i in range(len(times)):
            window_hits = [t for t in times if times[i] <= t < times[i] + window]
            if len(window_hits) >= threshold:
                alerts.append(_alert("brute-force-login", "HIGH", ip,
                                     f"{len(window_hits)} failed logins within {window}s"))
                break
    return alerts


def detect_sqli(events) -> list[dict]:
    alerts = []
    for e in events:
        if e.get("type") != "http":
            continue
        path = e.get("path", "").lower()
        if any(re.search(p, path) for p in SQLI_PATTERNS):
            alerts.append(_alert("web-sqli-attempt", "HIGH", e.get("src_ip", "?"),
                                 f"{e.get('method')} {e.get('path')}"))
    return alerts


def detect_path_traversal(events) -> list[dict]:
    alerts = []
    for e in events:
        if e.get("type") != "http":
            continue
        path = e.get("path", "").lower()
        if any(re.search(p, path) for p in TRAVERSAL_PATTERNS):
            alerts.append(_alert("web-path-traversal", "MEDIUM", e.get("src_ip", "?"),
                                 f"{e.get('method')} {e.get('path')}"))
    return alerts


def detect_unauthorized_admin_grant(events) -> list[dict]:
    alerts = []
    for e in events:
        if e.get("type") == "iam" and e.get("action") == "add_admin":
            if e.get("actor") not in KNOWN_ADMINS:
                alerts.append(_alert("privilege-escalation", "CRITICAL", e.get("actor", "?"),
                                     f"{e.get('actor')} granted admin to {e.get('target')}"))
    return alerts


def detect_impossible_travel(events, window: int = 3600) -> list[dict]:
    """Same user logs in from two countries within an impossible timeframe."""
    logins = [e for e in events if e.get("type") == "auth" and e.get("action") == "login_success"]
    by_user: dict[str, list[dict]] = {}
    for e in logins:
        by_user.setdefault(e["user"], []).append(e)
    alerts = []
    for user, evs in by_user.items():
        evs.sort(key=lambda e: e["ts"])
        for a, b in zip(evs, evs[1:]):
            if a.get("country") != b.get("country") and (b["ts"] - a["ts"]) < window:
                alerts.append(_alert("impossible-travel", "HIGH", user,
                                     f"{a['country']} -> {b['country']} in {b['ts'] - a['ts']}s"))
                break
    return alerts


ALL_RULES = [
    detect_brute_force, detect_sqli, detect_path_traversal,
    detect_unauthorized_admin_grant, detect_impossible_travel,
]


def run_all(events) -> list[dict]:
    alerts: list[dict] = []
    for rule in ALL_RULES:
        alerts.extend(rule(events))
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(alerts, key=lambda a: order.get(a["severity"], 9))
