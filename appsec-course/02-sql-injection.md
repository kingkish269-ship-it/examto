# 02 — SQL Injection — OWASP A03 (Injection)

## Theory

The server builds a database query by gluing your input into a text string. If
you send input with SQL syntax in it, you change the query itself.

Example the server runs:
```
SELECT * FROM users WHERE username = '<your input>'
```
If you send `x' OR '1'='1`, the query becomes:
```
SELECT * FROM users WHERE username = 'x' OR '1'='1'
```
`'1'='1'` is always true, so it returns **every** user. Attackers also use
`UNION SELECT` to read other tables, or bypass logins.

Analogy: you're filling in a form, but you write extra instructions in the blank
and the clerk follows them.

**The fix: parameterized queries.** The query text and your data travel
separately, so your input can never change the query's structure:
```python
conn.execute("SELECT * FROM users WHERE username = ?", (username,))
```

## Lab

App running (module 00). Second terminal. We use `-G --data-urlencode` so curl
encodes the spaces and quotes correctly:

```bash
# Normal search — one user:
curl -s -G "http://127.0.0.1:5000/api/search" --data-urlencode "username=alice"

# Injection — returns EVERY user:
curl -s -G "http://127.0.0.1:5000/api/search" --data-urlencode "username=x' OR '1'='1"
```

Now the fix — restart in secure mode:

```bash
# Ctrl+C the server first, then:
LAB_SECURE=1 python3 run_server.py
```

Re-run the injection command. It now returns `[]` — the input is treated as
data, not SQL.

## Verify

- Insecure: the injection returns all users.
- Secure: the same input returns nothing.

Optional real tool (local only): `pip install sqlmap` then
`sqlmap -u "http://127.0.0.1:5000/api/search?username=alice" --batch`.

## Key takeaways

- SQLi = input changing a query because it was concatenated in.
- Fix = **parameterized queries** (never string-concatenate SQL).
- Input validation is a helpful second layer, not the fix.
