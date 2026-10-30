# 03 — Command Injection — OWASP A03 (Injection)

## Theory

Same idea as SQL injection, but the sink is the **operating system shell**. The
server builds a shell command with your input and runs it. Shell metacharacters
like `;`, `|`, `&&` let you add your own command.

Example the server runs:
```
ping -c1 <your input>
```
Send `localhost; echo INJECTED` and the shell runs *two* commands — the ping,
then your `echo`. A real attacker runs `; cat /etc/passwd` or opens a reverse
shell. This often means full server takeover (RCE).

**The fix:** don't use a shell. Pass an **argument list** so input can't be
interpreted as commands, and validate the input:
```python
subprocess.run(["ping", "-c1", host])      # no shell=True
```

## Lab

App running. Second terminal:

```bash
# Normal:
curl -s "http://127.0.0.1:5000/diag?host=localhost"

# Injected second command (the %3B is a URL-encoded ';'):
curl -s "http://127.0.0.1:5000/diag?host=localhost%3B%20echo%20INJECTED"
```

The output contains `INJECTED` — your second command ran.

Fix — restart secure:
```bash
# Ctrl+C, then:
LAB_SECURE=1 python3 run_server.py
```
Re-run the injected command: it's rejected (`invalid host`).

## Verify

- Insecure: `INJECTED` appears in the output.
- Secure: the injected input is rejected.

## Key takeaways

- Command injection = user input reaching a shell; often full RCE.
- Fix = argument list with `shell=False` + input allowlist.
- Red flag in code review: `subprocess.run(..., shell=True)` with a variable.
