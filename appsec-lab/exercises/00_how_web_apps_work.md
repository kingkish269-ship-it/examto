# 00 — How web apps work and where they break

Before attacking anything, build the mental model. You review cloud and network
flows already; this is the same thinking applied to an HTTP request.

## The request lifecycle

1. **Client** (browser, mobile app, `curl`) sends an HTTP request: method, path,
   headers, and an optional body.
2. **Server** routes the request to a handler. The handler reads inputs from the
   path, query string, headers, cookies, and body.
3. The handler may reach **sinks**: a database, the file system, another HTTP
   service, a shell, or a deserializer.
4. The server builds a response: status code, headers, and body.
5. The browser renders the body and runs any returned JavaScript.

## The one idea behind almost every web vulnerability

> Untrusted input reaches a dangerous operation (a "sink") without the right
> validation, encoding, or authorization in between.

For every bug in this lab, answer four questions:

1. **Source** — where does untrusted input enter?
2. **Sink** — what dangerous operation receives it?
3. **Impact** — what does an attacker gain?
4. **Control** — where is the correct fix, and why there?

## Trust boundaries

A trust boundary is any line where data crosses from less-trusted to
more-trusted. The client-to-server boundary is the big one: never trust data
from the client, even if your own JavaScript produced it. Access-control checks,
input validation, and output encoding all belong on the server side of that line.

## Try it

```bash
python run_server.py
curl "http://127.0.0.1:5000/health"
curl "http://127.0.0.1:5000/greet?name=Kiro"
curl "http://127.0.0.1:5000/api/search?username=alice"
```

Now open the same URLs in a browser with dev tools open and watch the request
and response headers. Notice there are no security headers in vulnerable mode —
you will fix that in exercise 10.
