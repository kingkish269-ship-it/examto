#!/usr/bin/env bash
# Runs automatically when the Codespace is created. Sets up the two Flask labs'
# virtual environments so everything works immediately. The stdlib labs need no
# setup. Safe to re-run.
set -e

echo "Setting up the security labs..."

# Flask powers the clickable GUI dashboard (dashboard.py).
python3 -m pip install --quiet flask || pip install --quiet flask || true

for lab in appsec-lab ctf-lab; do
  if [ -f "$lab/requirements.txt" ]; then
    echo "  - $lab: creating virtualenv and installing dependencies"
    python3 -m venv "$lab/.venv"
    "$lab/.venv/bin/pip" install --quiet --upgrade pip
    "$lab/.venv/bin/pip" install --quiet -r "$lab/requirements.txt"
  fi
done

cat <<'DONE'

Setup complete.

Start here — pick ONE:

  CLICKABLE GUI (easiest):
    python3 dashboard.py      # then open the forwarded port 5000 in your browser

  OR the terminal coach:
    python3 coach.py          # shows your next task
    python3 coach.py check    # grades it and moves you on

Full instructions: GUIDE.md
DONE
