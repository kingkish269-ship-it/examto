# Module 1 · Lesson 2 — String methods

## Learn
Strings have built-in tools. The most useful for security is **`.split()`**,
which breaks text into a list of pieces:
```python
"FAILED login user=admin".split()        # ["FAILED", "login", "user=admin"]
"user=admin".split("=")                   # ["user", "admin"]
```
`list[-1]` gets the **last** item; `list[0]` the first, `list[1]` the second.
You parse logs this way constantly.

## Do
In `exercises/ex02.py`, make `get_username(line)` return just the username
(`"admin"`). The code already splits twice — replace `BLANK` with the index `1`
to take the part after `=`.

## Test
```bash
python3 check.py 2
```
