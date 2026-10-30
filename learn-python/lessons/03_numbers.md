# Module 1 · Lesson 3 — Numbers and booleans

## Learn
Python compares numbers with `<  >  <=  >=  ==  !=`. A comparison is already a
**boolean** (`True` / `False`), so you can return it directly:
```python
port < 1024        # True for 22, False for 8080
```
Ports below 1024 are the "well-known" ports (22, 80, 443...).

## Do
In `exercises/ex03.py`, make `is_well_known(port)` return `True` when the port
is below 1024. Replace `BLANK` with `1024`.

## Test
```bash
python3 check.py 3
```
When this passes, test the whole module: `python3 check.py test 1`
