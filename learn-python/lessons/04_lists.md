# Module 2 · Lesson 4 — Lists and `in`

## Learn
A **list** holds many values in order: `[22, 23, 3389]`. The word **`in`** checks
membership and gives back `True`/`False`:
```python
22 in [22, 23, 3389]      # True
80 in [22, 23, 3389]      # False
```
Because `port in a_list` is already a boolean, just return it.

## Do
In `exercises/ex04.py`, make `is_risky(port)` return whether the port is in
`RISKY_PORTS`. Replace `BLANK` with `RISKY_PORTS`.

## Test
```bash
python3 check.py 4
```
