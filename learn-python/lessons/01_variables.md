# Module 1 · Lesson 1 — Variables and f-strings

## Learn
A **variable** is a name for a value:
```python
ip = "10.0.0.5"
port = 22
```
An **f-string** builds text with values inside it. Put `f` before the quotes and
wrap each variable in `{ }`:
```python
f"Connection from {ip} on port {port}"   # "Connection from 10.0.0.5 on port 22"
```
Security engineers build strings like this all day: alerts, log lines, reports.

## Do
Open `exercises/ex01.py`. Make `alert_message(ip, port)` return
`Connection from 10.0.0.5 on port 22`. Replace the two `BLANK`s with `ip` and `port`.

## Test
```bash
python3 check.py 1
```
