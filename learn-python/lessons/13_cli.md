# Module 4 · Lesson 13 — Build a command-line tool (argparse)

## Learn
`argparse` turns a script into a real tool that takes arguments:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file")                  # required: python tool.py data.json
parser.add_argument("--severity", default="HIGH")   # optional: --severity LOW
args = parser.parse_args()
args.file        # "data.json"
args.severity    # "HIGH" unless the user passed --severity
```
This is how every security CLI tool reads its options.

## Do
In `exercises/ex13.py`, finish `build_parser()` so `--severity` defaults to
`"HIGH"`. Replace `BLANK` with `"HIGH"`.

## Test
```bash
python3 check.py 13
```
Then `python3 check.py test 4`, and `python3 check.py` to see you finished.
