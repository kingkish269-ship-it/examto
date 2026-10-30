# 12 — Threat Modeling (STRIDE)

## Theory

Threat modeling finds design flaws **before** code exists — the cheapest place
to fix them. You look at a feature and ask, for each part: *what could go wrong?*

The common framework is **STRIDE**, six categories:

| Letter | Threat | Plain meaning |
|---|---|---|
| S | Spoofing | pretending to be someone else |
| T | Tampering | changing data you shouldn't |
| R | Repudiation | acting with no trace |
| I | Information disclosure | leaking data |
| D | Denial of service | taking it offline |
| E | Elevation of privilege | gaining rights you shouldn't have |

You draw the data flow, mark **trust boundaries** (where data crosses from
less-trusted to more-trusted — the client→server line is the big one), map each
flow to STRIDE, and pick a control for each real risk.

## Lab

```bash
cd /workspaces/examto/appsec-lab/threat-modeling
cat TEMPLATE.md            # the reusable template
cat example_login_and_download.md   # a worked example on this app
```

Now do one yourself: copy the template and fill it in for the **login** feature.
```bash
cp TEMPLATE.md /tmp/my_threat_model.md
# edit /tmp/my_threat_model.md: assets, actors, data-flow, STRIDE table, mitigations
```

Quick check of your STRIDE understanding: a forgeable `admin:admin` session
token (module 06) is which category? (Answer: **Spoofing** — the attacker
pretends to be someone they're not.)

## Verify

You produced one completed threat model in the template format and can name the
STRIDE category of a real flaw.

## Key takeaways

- Threat model at design time; it's cheaper than fixing in production.
- STRIDE = 6 questions to ask about every data flow and trust boundary.
- At architect level this matters more than memorising payloads.
