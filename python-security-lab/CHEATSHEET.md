# Python Security Cheatsheet

Use this file while solving drills. Professional engineers look up syntax.

## Read JSON

```python
import json

with open("data/findings.json", encoding="utf-8") as file:
    findings = json.load(file)
```

## Dictionaries

```python
finding["severity"]              # key must exist
finding.get("severity")          # returns None when absent
finding.get("severity", "LOW")   # supplies a default
```

## Nested dictionaries

```python
port = rule.get("network", {}).get("port")
```

## Lists

```python
results = []
results.append(item)

for item in items:
    print(item)
```

## Filter a list

```python
high = [item for item in items if item.get("severity") == "HIGH"]
```

A normal loop is often easier to debug:

```python
high = []
for item in items:
    if item.get("severity") == "HIGH":
        high.append(item)
```

## Count values

```python
counts = {}
for item in items:
    key = item.get("severity", "UNKNOWN")
    counts[key] = counts.get(key, 0) + 1
```

## Functions

```python
def is_critical(finding):
    return finding.get("severity") == "CRITICAL"
```

## Errors

```python
try:
    result = operation()
except TimeoutError as error:
    print(f"Temporary failure: {error}")
```

Catch only errors you understand. Do not use a bare `except:`.

## CSV

```python
import csv

with open("report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "severity"])
    writer.writeheader()
    writer.writerows(rows)
```

## Command-line arguments

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("--severity", default="HIGH")
args = parser.parse_args()
```

## Sort

```python
ordered = sorted(items, key=lambda item: item.get("severity", ""))
```

## Sets for fast membership checks

```python
allowed = {"HIGH", "CRITICAL"}
if severity in allowed:
    ...
```

## Run tests

```bash
python3 -m unittest tests.test_01_parse_findings -v
```

A failed test is feedback about one behavior, not a judgement about your ability.
