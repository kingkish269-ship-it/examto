"""Run the CTF target locally for you to attack.

    python target/run_target.py      # http://127.0.0.1:5000

Intentionally vulnerable. Bind to localhost only; never deploy.
"""

import os
import sys

# Make `python3 target/run_target.py` work from the ctf-lab root: ensure the
# repo-relative parent (which contains the `target` package) is importable,
# not just this script's own directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from target.app import create_target_app  # noqa: E402

BANNER = r"""
============================================================
  CTF LAB TARGET - intentionally vulnerable, local only
  URL: http://127.0.0.1:5000   Health: /health
  Capture flags, then: python ctf.py submit <id> <flag>
============================================================
"""


def main() -> None:
    app = create_target_app()
    print(BANNER)
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
