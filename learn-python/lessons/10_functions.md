# Module 3 · Lesson 10 — Write a function yourself

## Learn
A **function** is reusable logic. You define it with `def`, take inputs in `( )`,
and hand back an answer with `return`:
```python
def is_risky(port):
    return port in [22, 23, 3389]
```
This lesson has **no BLANK** — you write the one line. You already did almost
exactly this in lesson 4.

## Do
In `exercises/ex10.py`, delete the `raise NotImplementedError(...)` line and
write a `return` so `is_sensitive(port)` is `True` when `port` is in
`SENSITIVE_PORTS`. One good answer:
```python
return port in SENSITIVE_PORTS
```
Try it before peeking.

## Test
```bash
python3 check.py 10
```
