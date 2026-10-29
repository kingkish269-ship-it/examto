"""Run the lab app locally so you can attack it with a browser or curl.

Safety:
  * Binds to 127.0.0.1 only. Do not change this to 0.0.0.0.
  * Vulnerable by default so you can practise the attacks.
  * Set LAB_SECURE=1 to run the fixed version and confirm the attacks fail.

Usage:
    python run_server.py            # vulnerable mode on http://127.0.0.1:5000
    LAB_SECURE=1 python run_server.py   # secure mode
"""

import os

from vulnerable_app import create_app

BANNER = r"""
============================================================
  APPSEC LAB - INTENTIONALLY VULNERABLE APPLICATION
  For local training only. Never deploy. Never expose.
  Mode: {mode}
  URL : http://127.0.0.1:5000
============================================================
"""


def main() -> None:
    secure = os.environ.get("LAB_SECURE") == "1"
    app = create_app(secure=secure)
    print(BANNER.format(mode="SECURE (fixed)" if secure else "VULNERABLE"))
    # debug=False so we never expose the Werkzeug debugger/PIN.
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
