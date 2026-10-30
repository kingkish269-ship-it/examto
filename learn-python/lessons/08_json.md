# Module 2 · Lesson 8 — Read JSON

## Learn
**JSON** is the text format almost every security tool uses for output. The
`json` module turns a JSON file into Python lists/dicts:
```python
import json
with open("findings.json") as file:
    data = json.load(file)        # now loop over it like any list/dict
```
`with open(...) as file:` opens the file and closes it automatically.

## Do
In `exercises/ex08.py`, finish `load_findings(path)` so it returns the file's
data. Replace `BLANK` with `json`.

## Test
```bash
python3 check.py 8
```
(It reads `exercises/findings.json` — open that to see what JSON looks like.)
