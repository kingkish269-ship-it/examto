# 02 — Open security groups

You already know this control from network security; here you detect it in code.

## See it

```bash
python3 -m auditor.audit data/sample_account.json | grep sg-
```

`sg-admin` exposes SSH (22) and RDP (3389) to `0.0.0.0/0` (HIGH). `sg-legacy`
opens all ports (CRITICAL). `sg-web` exposes only 443 and is correctly **not**
flagged.

## The logic

Read `open_security_groups`. It only considers public CIDRs, treats
protocol `-1` or a full port range as "all open", and flags sensitive ports
within any public range.

## In real AWS

- Replace public SSH/RDP with SSM Session Manager or a bastion behind a VPN.
- Use AWS Config `restricted-ssh` and `restricted-common-ports`.

## Extend it

Add port 6379 (Redis) and 27017 (MongoDB) to `SENSITIVE_PORTS` and add a test.
