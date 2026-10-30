# Room: Injection — SQL & Command (OWASP A03)

**Topic:** OWASP Top 10 · **Difficulty:** core

## Story
Untrusted input becomes part of a command the server runs.

## Theory (2 min)
**SQL injection:** input concatenated into a query lets an attacker change the
query (`' OR '1'='1`, `UNION SELECT ...`). **Command injection:**
`subprocess.run(cmd, shell=True)` with user input lets `; rm -rf /` run.

The fix for SQLi is **parameterized queries** (the data travels separately from
the query, so it can't change the query's structure). The fix for command
injection is no shell — pass an argument list and validate input.

## What you'll do
In `appsec-lab`, read `02_sql_injection.md` and `06_command_injection.md`, run
the exploits, and read the parameterized fix.

## Going further
`appsec-lab/` has both, with tests proving the fix blocks the attack.
