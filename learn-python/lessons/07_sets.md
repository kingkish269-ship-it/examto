# Module 2 · Lesson 7 — Sets (remove duplicates)

## Learn
A **set** keeps only unique values. Wrapping a list in `set(...)` drops
duplicates; `sorted(...)` turns it back into a sorted list:
```python
set(["a", "a", "b"])          # {"a", "b"}
sorted(set(["a", "a", "b"]))  # ["a", "b"]
```
Useful for "unique source IPs", "unique usernames", etc.

## Do
In `exercises/ex07.py`, make `unique_ips(ips)` return a sorted list of the unique
IPs. Replace `BLANK` with `set`.

## Test
```bash
python3 check.py 7
```
