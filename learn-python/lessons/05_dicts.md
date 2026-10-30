# Module 2 · Lesson 5 — Dictionaries and `.get`

## Learn
A **dictionary** stores values by name (a key). Tool output is almost always
dictionaries:
```python
finding = {"id": "F1", "severity": "HIGH"}
finding["severity"]                 # "HIGH"
```
`finding["owner"]` would **crash** if the key is missing. Safer:
```python
finding.get("severity", "UNKNOWN")  # value, or "UNKNOWN" if missing
```
Always use `.get(key, default)` with messy real-world data.

## Do
In `exercises/ex05.py`, return the finding's severity, or `"UNKNOWN"` if it is
missing. Replace `BLANK` with `"UNKNOWN"` (keep the quotes).

## Test
```bash
python3 check.py 5
```
