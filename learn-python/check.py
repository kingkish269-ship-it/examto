#!/usr/bin/env python3
"""Step-by-step learning checker.

    python3 check.py            show progress and your next lesson
    python3 check.py 1          check lesson 1 (after you edit exercises/ex01.py)
    python3 check.py test 1     test a whole MODULE (runs all its lessons, scores you)

Feedback is specific: what your code returned, what was expected, and a hint.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EX = ROOT / "exercises"
PROGRESS = ROOT / ".progress.json"

MODULES = {
    1: ("Core syntax (Tier 1)", [1, 2, 3]),
    2: ("Data & parsing (Tier 2)", [4, 5, 6, 7, 8, 9]),
    3: ("Automation (Tier 3)", [10, 11, 12]),
    4: ("Command-line tools (Tier 4)", [13]),
}
TITLES = {
    1: "Variables and f-strings", 2: "String methods (.split)",
    3: "Numbers and booleans", 4: "Lists and 'in'", 5: "Dictionaries and .get",
    6: "Filtering with loops + if", 7: "Sets (remove duplicates)",
    8: "Read JSON", 9: "Regex (extract an IP)", 10: "Write a function",
    11: "Read a file", 12: "Error handling (try/except)", 13: "Build a CLI (argparse)",
}
TOTAL = len(TITLES)


def _load(num: int):
    path = EX / f"ex{num:02d}.py"
    spec = importlib.util.spec_from_file_location(f"ex{num:02d}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _cmp(got, expected) -> tuple[bool, str]:
    if got == expected:
        return True, "Correct!"
    return False, f"your code returned\n    {got!r}\nexpected\n    {expected!r}"


# Each entry: a function(mod) -> (ok, message)
def _t(num, mod):
    if num == 1:
        return _cmp(mod.alert_message("10.0.0.5", 22), "Connection from 10.0.0.5 on port 22")
    if num == 2:
        a = mod.get_username("FAILED login user=admin")
        b = mod.get_username("x y user=root")
        return _cmp([a, b], ["admin", "root"])
    if num == 3:
        return _cmp([mod.is_well_known(22), mod.is_well_known(8080)], [True, False])
    if num == 4:
        return _cmp([mod.is_risky(22), mod.is_risky(80), mod.is_risky(3389)], [True, False, True])
    if num == 5:
        return _cmp([mod.get_severity({"severity": "HIGH"}), mod.get_severity({})], ["HIGH", "UNKNOWN"])
    if num == 6:
        out = mod.high_findings([{"severity": "HIGH"}, {"severity": "LOW"}, {"severity": "HIGH"}])
        return _cmp(out, [{"severity": "HIGH"}, {"severity": "HIGH"}])
    if num == 7:
        return _cmp(mod.unique_ips(["1.1.1.1", "1.1.1.1", "2.2.2.2"]), ["1.1.1.1", "2.2.2.2"])
    if num == 8:
        data = mod.load_findings(str(EX / "findings.json"))
        return _cmp(data, json.loads((EX / "findings.json").read_text()))
    if num == 9:
        return _cmp(mod.extract_ip("login from 203.0.113.9 ok"), "203.0.113.9")
    if num == 10:
        return _cmp([mod.is_sensitive(22), mod.is_sensitive(3306), mod.is_sensitive(80)],
                    [True, True, False])
    if num == 11:
        return _cmp(mod.count_alerts(str(EX / "alerts.txt")), 3)
    if num == 12:
        return _cmp([mod.safe_int("5"), mod.safe_int("abc", -1)], [5, -1])
    if num == 13:
        args = mod.build_parser().parse_args(["f.json"])
        return _cmp([args.file, args.severity], ["f.json", "HIGH"])
    return False, "no test"


def _run_one(num: int, quiet: bool = False) -> bool:
    try:
        mod = _load(num)
        ok, msg = _t(num, mod)
    except FileNotFoundError:
        print(f"No lesson {num}.")
        return False
    except NameError as e:
        if not quiet:
            print(f"Lesson {num} ({TITLES[num]}): you still have a BLANK to fill in.")
            print(f"  Edit exercises/ex{num:02d}.py, replace every BLANK, then run again. ({e})")
        return False
    except NotImplementedError:
        if not quiet:
            print(f"Lesson {num} ({TITLES[num]}): write your code where it says, then run again.")
        return False
    except Exception as e:  # noqa: BLE001
        if not quiet:
            print(f"Lesson {num} ({TITLES[num]}): your code raised an error: {e!r}")
        return False
    if ok:
        _mark(num)
        if not quiet:
            print(f"Lesson {num} ({TITLES[num]}): Correct! Well done.")
        return True
    if not quiet:
        print(f"Lesson {num} ({TITLES[num]}): Not yet — {msg}")
        print("  Hint: re-read the lesson; it is one small change.")
    return False


def _mark(num: int) -> None:
    d = _done()
    d.add(num)
    PROGRESS.write_text(json.dumps({"done": sorted(d)}))


def _done() -> set[int]:
    if PROGRESS.exists():
        return set(json.loads(PROGRESS.read_text()).get("done", []))
    return set()


def test_module(m: int) -> int:
    if m not in MODULES:
        print(f"Modules are 1 to {len(MODULES)}.")
        return 2
    name, lessons = MODULES[m]
    print(f"Testing Module {m}: {name}\n")
    passed = sum(1 for n in lessons if _run_one(n))
    total = len(lessons)
    print(f"\nModule {m}: {passed}/{total} lessons passed.")
    if passed == total:
        print(f"MODULE {m} PASSED. On to the next module.")
        return 0
    print("Finish the lessons above, then test the module again.")
    return 1


def status() -> int:
    d = _done()
    print("Learn Python for Security — step by step\n")
    for m, (name, lessons) in MODULES.items():
        done_here = sum(1 for n in lessons if n in d)
        print(f"Module {m}: {name}  ({done_here}/{len(lessons)})")
        for n in lessons:
            mark = "[x]" if n in d else "[ ]"
            print(f"   {mark} Lesson {n}: {TITLES[n]}")
    nxt = next((n for n in TITLES if n not in d), None)
    bar = "#" * len(d) + "." * (TOTAL - len(d))
    print(f"\n[{bar}] {len(d)}/{TOTAL} lessons")
    if nxt:
        print(f"\nNext: read lessons/{nxt:02d}_*.md, edit exercises/ex{nxt:02d}.py, "
              f"then run: python3 check.py {nxt}")
    else:
        print("\nAll lessons done. You have the Python a security engineer uses most.")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        return status()
    if argv[0] == "test":
        return test_module(int(argv[1])) if len(argv) > 1 and argv[1].isdigit() else status()
    if argv[0].isdigit():
        return 0 if _run_one(int(argv[0])) else 1
    print("Usage: python3 check.py [ <lesson-number> | test <module-number> ]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
