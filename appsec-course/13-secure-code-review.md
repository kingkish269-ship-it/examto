# 13 — Secure Code Review

## Theory

Reading code to find vulnerabilities is the daily work of an AppSec engineer and
a favourite interview exercise. You don't read every line — you hunt for
**sources** (untrusted input) reaching **sinks** (dangerous calls) without a
control. Train your eye on the recurring "sins":

```python
cursor.execute("... " + user_input)     # SQL injection
subprocess.run(cmd, shell=True)          # command injection
requests.get(url, verify=False)          # TLS verification disabled
password = "hardcoded-secret"            # secret in code
pickle.loads(untrusted)                  # RCE via deserialization
open("/files/" + name)                   # path traversal
f"<h1>{name}</h1>"  (unescaped)          # XSS
```

For each finding, write: the **finding**, the **impact**, the **fix**, and a
reference. That's a review comment.

## Lab

```bash
cd /workspaces/examto/appsec-lab

# Hunt for the dangerous sinks in the app, the way a reviewer scans a PR:
grep -nE "shell=True|verify=False|pickle.loads|hashlib.md5|\" \+ |' \+ " vulnerable_app/app.py
```

Open `vulnerable_app/app.py` and read each hit in context. The app is written so
the **vulnerable** and **fixed** version of every route sit side by side (search
for the OWASP tags `A01`, `A03`, etc.). For each vulnerable branch, say out loud:
the source, the sink, the impact, and the fix.

## Verify

You located every dangerous sink and can explain, for each, why it's unsafe and
what the fix is.

## Key takeaways

- Review = trace untrusted input to a dangerous sink.
- Know the sin patterns on sight; `grep` is a fine first pass before SAST.
- Deliver findings as: finding → impact → fix → reference.
