# 02 — SQL Injection

**OWASP A03:2021 — Injection.**

## Where

`GET /api/search?username=...` builds a SQL string by concatenation.

## Exploit

```bash
curl -s "http://127.0.0.1:5000/api/search?username=x' OR '1'='1"
# returns every user instead of one
```

The input closes the quote and adds `OR '1'='1'`, which is always true. Richer
payloads can use `UNION SELECT` to read other tables, or stacked queries to
modify data.

## Source → Sink → Impact → Control

- **Source:** the `username` query parameter.
- **Sink:** `conn.execute(string)` — the string is the query.
- **Impact:** read or modify any data in the database, bypass authentication,
  sometimes achieve remote code execution depending on the engine.
- **Control:** parameterised queries. The query text and the data travel
  separately, so input can never change the query's structure.

## The fix

```python
rows = conn.execute(
    "SELECT username, role FROM users WHERE username = ?", (username,)
).fetchall()
```

Never build SQL by string concatenation. Use parameters (or a well-configured
ORM). Input validation is a useful second layer but is not a substitute.

## Detect with free tools

```bash
semgrep --config auto vulnerable_app/        # flags the string-built query
# Optional dynamic confirmation against the LOCAL lab only:
sqlmap -u "http://127.0.0.1:5000/api/search?username=alice" --batch
```

## Verify

```bash
pytest tests/test_exploits.py::test_sql_injection_bypass -v
pytest tests/test_fixes.py::test_sql_injection_blocked -v
```
