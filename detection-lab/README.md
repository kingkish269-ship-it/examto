# Detection Engineering Lab (blue team / SOC)

Hands-on lab for the defensive side: write detection rules over security logs
and prove they catch attacks without drowning you in false positives. This is
the core skill of SOC analysts and detection engineers — consistently in demand.

Pure standard library.

## Run it

```bash
cd detection-lab
python3 run_detections.py        # alerts from the sample event log
python3 -m unittest discover -v  # 8 tests
```

## The detections (read `detections.py`)

| Rule | Severity | Catches |
|---|---|---|
| `brute-force-login` | HIGH | many failed logins from one IP in a window |
| `web-sqli-attempt` | HIGH | SQL-injection patterns in HTTP requests |
| `web-path-traversal` | MEDIUM | `../` / `/etc/passwd` in request paths |
| `privilege-escalation` | CRITICAL | admin granted by a non-admin actor |
| `impossible-travel` | HIGH | one user, two countries, impossibly fast |

Each rule returns alerts with a severity, the entity (IP or user), and the
evidence — the shape a real SIEM alert takes.

## How detection engineering works

1. **Know the attack** — you already do (the offensive labs here).
2. **Find the signal in logs** — what event(s) betray it?
3. **Write a rule** — precise enough to catch the attack, loose enough to
   survive normal variation.
4. **Tune** — reduce false positives (benign events must not alert) and false
   negatives (the attack must alert). The tests here encode exactly that:
   every rule fires on the attack and stays quiet on benign traffic.

In production these rules are written as **Sigma** (vendor-neutral) or directly
as SIEM queries — Splunk SPL, Microsoft Sentinel KQL, Elastic. The logic is the
same; this lab teaches the logic in Python you can read and test.

## The data

`data/events.json` mixes benign activity with five attacks. Open it and match
each alert from `run_detections.py` back to the events that triggered it.

## Exercises

- `exercises/01_triage_the_alerts.md`
- `exercises/02_write_a_rule.md`

## Extend it

Add a rule for repeated HTTP 401/403 bursts (credential stuffing against an API)
or for logins outside business hours, with a test that it fires on an attack
sample and not on benign traffic.
