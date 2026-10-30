# Module 3 · Lesson 12 — Error handling (try / except)

## Learn
Real data is messy. **`try` / `except`** lets your script keep going instead of
crashing:
```python
try:
    n = int(value)        # might fail if value is "abc"
except ValueError:
    n = 0                 # fallback when it is not a number
```
Catch only the error you expect (`ValueError`), not everything.

## Do
In `exercises/ex12.py`, make `safe_int(value, default)` return the number, or the
`default` when the value is not a valid number. Replace `BLANK` with `default`.

## Test
```bash
python3 check.py 12
```
Then test the module: `python3 check.py test 3`
