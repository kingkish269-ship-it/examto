# 01 — Triage the alerts

## Generate alerts

```bash
cd detection-lab
python3 run_detections.py
```

You get five alerts, sorted by severity. Triage them like a SOC analyst:

| Alert | First question | Likely action |
|---|---|---|
| `privilege-escalation` (CRITICAL) | Did `mallory` legitimately grant admin? | Contain the account; this is the highest risk. |
| `brute-force-login` (HIGH) | One IP, many failures — password spray? | Block the IP; check for a later success. |
| `web-sqli-attempt` (HIGH) | Did the injection return data (status 200, large body)? | Check the app/DB; block the source. |
| `impossible-travel` (HIGH) | Two countries for `bob` in minutes | Possible credential theft; force re-auth / MFA. |
| `web-path-traversal` (MEDIUM) | Did `../etc/passwd` succeed? | Check the file endpoint; patch traversal. |

## Correlate

Notice the brute-force IP (`203.0.113.9`) and the SQLi/traversal IP
(`198.51.100.7`) are different actors. Correlation — linking events to one
actor or one incident — is the step that turns raw alerts into an investigation.

## Map each alert to its events

Open `data/events.json` and find the events behind each alert. Confirm the
evidence string in the alert matches what you see.

## Why it matters

Detection without triage is noise. Being able to explain *what you would do
next* for each alert is exactly what SOC interviews test.
