#!/usr/bin/env bash
# One command to run the web lab WITH a working in-page terminal.
# Installs the terminal backend if missing, then starts the server.
#
#   bash webapp/start.sh
#
# Then open the forwarded port 5000 in your browser. The terminal on the right
# connects automatically — no Ctrl+`, no VS Code needed.
set -e
cd "$(dirname "$0")/.."

echo "Ensuring the web lab dependencies are installed..."
python3 -m pip install --quiet flask flask-sock simple-websocket 2>/dev/null \
  || pip install --quiet flask flask-sock simple-websocket

echo
echo "Starting the web lab. Open the forwarded port 5000 in your browser."
echo "The terminal on the right will connect automatically."
echo
python3 webapp/app.py
