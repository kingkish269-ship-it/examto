# Learn Python for Security — step by step, with tests

This is the hands-on companion to [`../PYTHON_FOR_YOUR_DOMAIN.md`](../PYTHON_FOR_YOUR_DOMAIN.md).
It teaches the Python a security engineer needs, **one small step at a time**,
and **tests you after each module**. You write the code (fill one blank per
lesson); the checker grades you with specific feedback. Every example is
security data.

Made for a newcomer: no prior Python needed beyond "I've seen it once." No
internet, no extra tools — just Python 3.

## The loop for every lesson

1. **Read** the lesson in `lessons/` (1–2 minutes, plain English).
2. **Edit** the matching file in `exercises/` — replace the `BLANK`
   (lesson 10 asks you to write one line yourself).
3. **Test** it:
   ```bash
   python3 check.py 1
   ```
   You get `Correct!`, or a specific hint showing what your code returned vs what
   was expected.

After each module, run the **module test**:
```bash
python3 check.py test 1
```
It runs every lesson in that module and tells you `MODULE 1 PASSED` when you've
got them all.

See where you are any time:
```bash
python3 check.py
```

## The modules (mapped to the guide's tiers)

**Module 1 — Core syntax (Tier 1)**
1. Variables and f-strings
2. String methods (`.split`)
3. Numbers and booleans

**Module 2 — Data & parsing (Tier 2)** *(this is most of the real job)*
4. Lists and `in`
5. Dictionaries and `.get`
6. Filtering with a loop + `if`
7. Sets (remove duplicates)
8. Read JSON
9. Regex (extract an IP)

**Module 3 — Automation (Tier 3)**
10. Write a function yourself
11. Read a file
12. Error handling (`try`/`except`)

**Module 4 — Command-line tools (Tier 4)**
13. Build a CLI with `argparse`

**Module 5 — Real-world automation (Graph / Intune)**
14. Apply Intune tags via Microsoft Graph — a real interview task (get a token,
    then PATCH a device configuration). Tested offline with a fake session.

## How to progress

Do the lessons in order. Finish a module, run its test, and only move on when it
says PASSED. That is how you know you actually learned it — not just read it.

## When you finish

You'll have written (and been tested on) the Python that the rest of this repo —
and AppSec/DevSecOps work — uses most. Next: the `../PYTHON_FOR_YOUR_DOMAIN.md`
confidence checklist, then the security labs. Keep the guide as your reference.
