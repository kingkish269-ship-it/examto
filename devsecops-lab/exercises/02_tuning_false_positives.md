# 02 — Tuning: a fair gate, not a noisy one

A gate that fails on everything gets ignored or disabled. The skill is making it
block what matters and allow the rest with a reason.

## Levers in the gate

- `--fail-on` — the lowest severity that blocks. Start at `HIGH`, not `LOW`.
- `--max-allowed` — tolerate a small number of blocking findings while you burn
  down a backlog.
- `--allow <id>` — ignore a specific finding id (an accepted risk or a confirmed
  false positive). Every allow should have a reason recorded, like a risk
  acceptance.

## Try it

```bash
# Blocks: a critical CVE is present.
python3 -m gate.run_gate --trivy samples/trivy_sample.json --fail-on HIGH; echo $?

# Accept that one CVE explicitly -> gate passes.
python3 -m gate.run_gate --trivy samples/trivy_sample.json --fail-on HIGH \
  --allow CVE-2023-0001; echo $?
```

## The principle

Treat every allowlist entry as a tracked, time-boxed risk acceptance with an
owner — not a permanent silence. This is exactly the exception-handling
discipline a security architect is expected to own.

## Extend it

Add an `--allow-file` option that reads ids and reasons from a JSON file, and a
test that proves an allowlisted critical finding no longer blocks.
