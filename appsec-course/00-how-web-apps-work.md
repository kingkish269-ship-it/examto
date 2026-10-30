# 00 — How web apps work (the foundation)

## Theory

A web app has four parts:
- **Client** — the browser (or `curl`, or a mobile app) that sends requests.
- **Server** — your application code that receives them.
- **Database** — where data is stored.
- **Other services** the server calls (APIs, files, the cloud).

A request has four things: a **method** (GET to read, POST to send), a **path**
(`/login`), **headers** (including cookies and `Authorization`), and a **body**.
The server reads these, maybe talks to the database or a file, and sends back a
**response**: a **status code** (200 OK, 401 not logged in, 403 forbidden, 404
not found, 500 error) plus headers and a body.

**The one idea behind almost every web vulnerability:**
> Untrusted input from the client reaches a dangerous operation without the
> right check in between.

Two words you'll use forever:
- **Source** — where untrusted input enters (URL, form field, header, cookie).
- **Sink** — the dangerous thing it reaches (a database query, a shell command,
  the HTML page, the file system).

And the **golden rule**: *never trust input from the client* — even if your own
app produced it. The attacker controls the whole request. All real checks happen
on the server.

Analogy: the client is a stranger handing you a note. You never run whatever the
note says — you check it first. "Checking it" is what security is.

## Lab

```bash
# Look at a real request/response and its headers:
curl -s -D - https://example.com -o /dev/null
```

You'll see the status line (e.g. `HTTP/2 200`) and headers. Notice there's no
`Content-Security-Policy` by default — you'll learn why that matters in module 09.

Now start the lab app you'll attack in later modules:

```bash
cd /workspaces/examto/appsec-lab
source .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
python3 run_server.py
```

Leave it running. In a **second terminal**:

```bash
curl -s http://127.0.0.1:5000/health
curl -s "http://127.0.0.1:5000/greet?name=Kiro"
```

## Verify

You saw: a status code + headers from a real site, and the lab app answering on
`127.0.0.1:5000`. You now have a target for the next modules.

## Key takeaways

- Request = method + path + headers + body; response = status + headers + body.
- Every vuln = untrusted **source** reaching a dangerous **sink** unchecked.
- Never trust the client. Enforce on the server.
