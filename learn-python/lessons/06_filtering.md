# Module 2 · Lesson 6 — Filtering with a loop + `if`

## Learn
A **loop** visits each item; an **`if`** keeps only the ones you want:
```python
result = []
for f in findings:
    if f["severity"] == "HIGH":
        result.append(f)
```
`==` means "is equal to" (two equals signs). This "loop + if + append" is the
heart of every security tool: *show me only the HIGH findings*.

## Do
In `exercises/ex06.py`, keep only findings whose severity equals `"HIGH"`.
Replace `BLANK` with `"HIGH"`.

## Test
```bash
python3 check.py 6
```
