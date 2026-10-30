# Room: Secure Code Review

**Topic:** AppSec skill · **Difficulty:** core · **interview favourite**

## Story
Reading code for bugs is the day-to-day of an AppSec engineer.

## Theory (2 min)
Train your eye for the recurring "sins". When you see these, you flag them:
```
cursor.execute("... " + user_input)      # SQL injection
subprocess.run(cmd, shell=True)           # command injection
requests.get(url, verify=False)           # TLS disabled
password = "hardcoded-secret"             # secret in code
pickle.loads(untrusted)                   # RCE
open("/files/" + name)                    # path traversal
```
For each: find the **source** (untrusted input), the **sink** (dangerous call),
the impact, and the fix.

## What you'll do
Open `appsec-lab/vulnerable_app/app.py` and review it like a pull request: find
each insecure branch and name the vulnerability and its fix.

## Going further
`appsec-lab/` is written to be read this way (vulnerable + fixed side by side).
