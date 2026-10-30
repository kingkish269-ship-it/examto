# Python for Security — your complete guide

Written for you: strong in endpoint, network, cloud, and data security; basic
Python; heading into AppSec, DevSecOps, SAST and DAST. This is a guide to read
and follow, not a lab. Goal: be **confident** writing and reading the Python
your work needs — not become a software engineer.

---

> **Want step-by-step lessons with a test after each module?** Do the
> hands-on track in [`learn-python/`](learn-python/) — it teaches each tier in
> small steps and grades you (`python3 check.py` to start).

## 0. Mindset and your finish line

You are **not** learning "all of Python." You are learning Python as a tool to
automate security work and read other people's code. That is a much smaller,
reachable target.

**You are ready when you can:**

- read a 100–200 line security script and explain what it does,
- parse JSON/YAML/CSV from any tool and pull out what you need,
- call a REST API (auth, pagination, errors) and act on the response,
- write a small CLI tool that takes input and returns a clear result,
- recognise insecure patterns in Python code (injection, secrets, bad crypto).

Nobody memorises syntax. Professionals look things up constantly. Your job is to
understand the *shape* of a solution and adapt a known pattern.

---

## 1. Exactly what to learn (and what to skip)

Learn these five tiers in order. Each builds on the last.

### Tier 1 — Core syntax (the alphabet)
- Variables, and the main types: `str`, `int`, `float`, `bool`, `None`
- String f-strings and common methods: `.split()`, `.strip()`, `.lower()`,
  `.startswith()`, `.replace()`, `in`
- Comparisons and logic: `==`, `!=`, `<`, `>`, `and`, `or`, `not`

### Tier 2 — Data and parsing (this is 70% of the job)
- `list` (ordered), `dict` (key/value), `set` (unique), `tuple` (fixed)
- Indexing and slicing: `items[0]`, `items[-1]`, `items[1:3]`
- `dict.get(key, default)` — safe access to messy data
- Loops: `for`, `while`; list/dict comprehensions
- `if / elif / else`
- **Data formats: JSON (`json`), YAML (`pyyaml`), CSV (`csv`)** — the daily bread
- **Regular expressions (`re`)** — parse logs, payloads, indicators

### Tier 3 — Automation and APIs (where you become useful)
- Functions: `def`, parameters, defaults, `return`
- Modules and imports; the standard library
- **Virtual environments (`venv`) and `pip`** — isolate and install packages
- Files: `with open(path) as f:` read/write
- **`requests`** — HTTP GET/POST, headers, bearer/API-key auth, JSON bodies,
  query params, pagination, timeouts, status codes, retries
- Errors: `try` / `except`, raising, and `logging`
- `subprocess` — run other tools safely (argument list, never `shell=True` on
  untrusted input)
- Dates/times: `datetime`, epoch timestamps, timezones (log correlation)

### Tier 4 — Packaging your work
- `argparse` — turn a script into a real command-line tool
- `pytest` basics — assertions, a few tests, mocking an API response
- Reading **classes** (you must read them; you rarely need to design them)
- `requirements.txt` and pinning versions

### Tier 5 — Security-specific libraries (pick as needed)
- `hashlib`, `hmac`, `secrets`, `base64` — hashing, tokens, encoding
- `requests` + `urllib.parse` — web testing and SSRF reasoning
- `boto3` — AWS automation (you already know the cloud concepts)
- Microsoft Graph via `requests` (or the SDK) — Entra/Defender/Sentinel
- `PyJWT` — inspect/forge JWTs (auth testing)
- `beautifulsoup4` — parse HTML responses
- `bandit` — Python SAST; `semgrep` — multi-language SAST (rules are YAML)
- `scapy` (optional) — packet crafting, ties to your network background

### Skip for now (do not waste time)
LeetCode / data-structures-and-algorithms, async/`await`, metaclasses, writing
decorators, web frameworks (Django/Flask) beyond reading, GUI apps, data science
/ pandas, threading internals, design patterns. Add any of these only if a real
task demands it.

---

## 2. The core topics, each with a security example

Short, readable examples. Type them out, change a value, see what happens.

### Strings and f-strings
```python
ip, port = "10.0.0.5", 22
print(f"Connection from {ip} on port {port}")
line = "2026-01-01 FAILED login user=admin ip=10.0.0.5"
print(line.split())                 # list of words
print("FAILED" in line)             # True
```

### Lists and membership
```python
risky = [22, 23, 3389]
print(22 in risky)                  # True
open_ports = [22, 80, 443]
print([p for p in open_ports if p in risky])   # [22]
```

### Dictionaries (how tool output looks)
```python
finding = {"id": "F1", "severity": "HIGH", "resource": "s3://logs"}
print(finding["severity"])          # HIGH
print(finding.get("owner", "unknown"))   # safe: no crash if missing
```

### Loops + conditions (filtering)
```python
findings = [{"severity": "HIGH"}, {"severity": "LOW"}, {"severity": "HIGH"}]
high = [f for f in findings if f["severity"] == "HIGH"]
print(len(high))                    # 2
```

### Functions
```python
SENSITIVE = {22, 3389, 3306}
def is_sensitive(port):
    return port in SENSITIVE
print(is_sensitive(3306))           # True
```

### JSON (the format everything speaks)
```python
import json
with open("findings.json") as f:
    data = json.load(f)             # -> Python list/dict
counts = {}
for f_ in data:
    sev = f_.get("severity", "UNKNOWN")
    counts[sev] = counts.get(sev, 0) + 1
print(counts)                       # {"HIGH": 2, "LOW": 1}
```

### Regex (parsing logs and payloads)
```python
import re
log = "Failed password for admin from 203.0.113.9 port 51734"
m = re.search(r"from (\d+\.\d+\.\d+\.\d+)", log)
print(m.group(1))                   # 203.0.113.9
```

### HTTP / APIs with requests
```python
import requests
r = requests.get(
    "https://api.example.com/v1/alerts",
    headers={"Authorization": "Bearer TOKEN"},
    params={"severity": "high"},
    timeout=10,
)
r.raise_for_status()                # raise on HTTP error
for alert in r.json().get("items", []):
    print(alert["id"], alert["title"])
```

### Errors and logging
```python
import logging
logging.basicConfig(level=logging.INFO)
try:
    r = requests.get("https://api.example.com", timeout=5)
    r.raise_for_status()
except requests.RequestException as e:
    logging.error("API call failed: %s", e)
```

### Running a tool safely (subprocess)
```python
import subprocess
# GOOD: argument list, no shell
out = subprocess.run(["nmap", "-sV", "10.0.0.5"], capture_output=True, text=True)
print(out.stdout)
# BAD (command injection): subprocess.run("nmap " + user_input, shell=True)
```

### A real CLI tool (argparse)
```python
import argparse, json
p = argparse.ArgumentParser(description="Show HIGH findings")
p.add_argument("file")
p.add_argument("--min", default="HIGH")
args = p.parse_args()
data = json.load(open(args.file))
for f in data:
    if f.get("severity") == args.min:
        print(f["id"], f.get("title"))
```

### Reading a class (you mostly read, not write)
```python
class Scanner:
    def __init__(self, target):
        self.target = target        # stored on the object
    def run(self):
        return f"scanning {self.target}"
s = Scanner("10.0.0.5")
print(s.run())                      # scanning 10.0.0.5
```

### Secure-coding sins to recognise (AppSec review)
```python
cursor.execute("SELECT * FROM users WHERE id = " + uid)   # SQL injection
subprocess.run(cmd, shell=True)                           # command injection
requests.get(url, verify=False)                           # TLS turned off
password = "hardcoded-secret"                             # secret in code
pickle.loads(untrusted_bytes)                             # RCE via deserialisation
open("/files/" + name)                                    # path traversal
```

---

## 3. How Python shows up in your target roles

### Application Security
- Write quick **proof-of-concept scripts** with `requests` to test an endpoint
  (auth bypass, IDOR, SSRF).
- **Read code** in Python, and learn to *read* (not write) JavaScript/Java to
  spot the sins above.
- Inspect/forge **JWTs** with `PyJWT`; decode `base64`; compute hashes.

### DevSecOps
- **Glue scripts** that run in CI: call an API, parse a tool's JSON, decide
  pass/fail, exit non-zero to block a build.
- Parse **SAST/DAST/SCA output** (Semgrep, Trivy, ZAP, Gitleaks are all JSON).
- Automate cloud posture checks with `boto3` / Graph — your cloud strength plus
  a little Python is a strong combination.

### SAST (static analysis)
- Run **`bandit`** (Python) and **`semgrep`** (many languages).
- Understand the idea of **source → sink** (untrusted input reaching a dangerous
  call). Writing Semgrep rules is YAML pattern-matching, not heavy Python.

### DAST (dynamic analysis)
- Script **`requests`** to drive an app; automate **OWASP ZAP** via its API;
  parse results and feed them into the pipeline gate.

The pattern under all four: **call something, parse the result, make a decision,
report it.** That is exactly Tiers 2–3 above.

---

## 4. Your 8-week plan (about 1 hour a day, 5 days a week)

You do not need a lab. Learn the concept, then immediately write a 5–15 line
script about security data you already understand.

- **Week 1 — Core + strings.** Tier 1. Write scripts that parse a log line into
  fields and build alert messages.
- **Week 2 — Lists, dicts, loops.** Tier 2 (no files yet). Filter a list of
  findings; count ports; find duplicates with a `set`.
- **Week 3 — Files + JSON + CSV.** Load a JSON findings file, summarise it,
  write a CSV report. This alone makes you useful.
- **Week 4 — Regex + functions + errors.** Extract IPs/hashes/URLs from text;
  wrap logic in functions; handle missing data gracefully.
- **Week 5 — HTTP and APIs.** `requests`: GET/POST, auth headers, pagination,
  timeouts. Pull data from any API you have access to and summarise it.
- **Week 6 — venv, pip, argparse, subprocess.** Turn week 3–5 scripts into real
  command-line tools; run an external scanner and parse its output.
- **Week 7 — Security libraries + reading code.** `hashlib`/`base64`/`PyJWT`;
  run `bandit`/`semgrep` and read their findings; read a medium Python script
  and explain it.
- **Week 8 — Apply it to AppSec/DevSecOps.** Write a tiny script that reads a
  SAST tool's JSON and exits non-zero if any HIGH finding exists (a pipeline
  gate). Read a vulnerable code sample and name the bug and fix.

Repeat anything that felt shaky. Depth beats speed.

---

## 5. How to practice without a "lab"

Pick tasks from your own world and script them. Ten-to-twenty lines each:

- Parse an auth log and list IPs with more than 5 failed logins.
- Read a firewall/security-group export (JSON) and flag any rule open to
  `0.0.0.0/0`.
- Call a cloud or EDR API and print the 10 newest alerts.
- Take a list of hashes and check them against a local allowlist file.
- Diff two JSON config exports and print what changed.
- Decode and inspect a JWT from a request.

Each one practises Tiers 2–3 and produces something you could actually use.

---

## 6. Free and trusted resources (ranked for you)

1. **Automate the Boring Stuff with Python** — Al Sweigart, free online at
   automatetheboringstuff.com. Best practical start; do chapters on strings,
   lists, dicts, files, regex, and web/APIs.
2. **The official Python Tutorial** — docs.python.org/3/tutorial — accurate and
   concise; use as reference.
3. **Real Python** — realpython.com — focused tutorials (requests, venv,
   argparse, json).
4. **Black Hat Python** (Justin Seitz) and **Violent Python** (TJ O'Connor) —
   books that teach Python *through* security scripting; great once you have
   Tiers 1–2.
5. **Python for DevOps** (O'Reilly) — automation mindset for DevSecOps.
6. **Semgrep docs** — semgrep.dev/docs — for SAST rule-writing when you get there.

Use **one** primary source (Automate the Boring Stuff) plus the official docs.
Jumping between many courses is why syntax doesn't stick.

Content was rephrased/condensed for licensing compliance; see each source for
the authoritative text.

---

## 7. Confidence checklist

Tick these off over the 8 weeks. When most are ticked, you are "confident enough"
for AppSec/DevSecOps interviews and work:

- [ ] I can slice lists and read nested dicts without guessing.
- [ ] I can load JSON and summarise it (counts, filters).
- [ ] I can parse a log line with `split()` and with a regex.
- [ ] I can call an authenticated API, page through results, handle errors.
- [ ] I can write a function with parameters and a return value.
- [ ] I can make a script a CLI tool with `argparse`.
- [ ] I can create a venv, `pip install`, and pin `requirements.txt`.
- [ ] I can run an external tool with `subprocess` safely.
- [ ] I can read a class and explain what it does.
- [ ] I can spot SQL/command injection, hardcoded secrets, and `verify=False`.
- [ ] I can write a 10-line pipeline gate that fails on HIGH findings.

---

## 8. Then what

Once Tiers 1–3 feel comfortable, move into the AppSec and DevSecOps material.
Keep this guide as your Python reference and only deepen a topic when a real
task needs it. You do not circle back to "learn more Python" in the abstract —
you learn the next piece when a problem in front of you calls for it.
