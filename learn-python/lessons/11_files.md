# Module 3 · Lesson 11 — Read a file

## Learn
Open a file, read its lines, work with them:
```python
with open("alerts.txt") as file:
    lines = file.readlines()      # a list of lines
```
`line.strip()` removes spaces/newlines; `len(a_list)` counts items. A
comprehension can keep only non-empty lines:
```python
[line for line in lines if line.strip()]
```

## Do
In `exercises/ex11.py`, make `count_alerts(path)` return the number of non-empty
lines. Replace `BLANK` with `len`.

## Test
```bash
python3 check.py 11
```
