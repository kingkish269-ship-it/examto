# Module 2 · Lesson 9 — Regex (find patterns in text)

## Learn
A **regular expression** finds patterns in text. `re.search(pattern, text)`
returns a match; `.group(1)` gives the part in the first `( )`:
```python
import re
m = re.search(r"(\d+\.\d+\.\d+\.\d+)", "login from 203.0.113.9 ok")
m.group(1)        # "203.0.113.9"
```
`\d+` means "one or more digits". This is how you pull IPs, hashes, and URLs out
of logs.

## Do
In `exercises/ex09.py`, make `extract_ip(text)` return the first IP. Replace
`BLANK` with `1`.

## Test
```bash
python3 check.py 9
```
Then test the module: `python3 check.py test 2`
