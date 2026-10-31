# Web Lab — Hackversity-style guided rooms with a live terminal

A three-pane web page running in your Codespace:

- **Left rail:** the room's six sections with progress ticks.
- **Middle:** the current section's content.
- **Right:** a real **bash terminal** on your Codespace (the machine).

Each module is a full room with six sections (exactly like Hackversity):
1. **Mission brief** — the scenario and what to find.
2. **Theory** — the concept, plain English.
3. **Worked example** — the technique run once on another machine.
4. **Knowledge check** — several graded questions (wrong answers cost nothing).
5. **Investigation** — step-by-step, with hints; you run the commands in the terminal.
6. **Capture the flag** — submit the flag you recovered.

Content lives in `modules/*.json` (one file per room). Progress is saved in
`.web_progress.json` (git-ignored). Capture flags for the exploit rooms are the
real `ctf-lab` flags, so you genuinely capture them from the running target.

## Run it (one command)

```bash
cd /workspaces/examto
bash webapp/start.sh
```

This installs the terminal backend if needed, then starts the server. Open the
**port 5000** popup → **Open in Browser**. The page loads with the modules on
the left and a terminal on the right that **connects automatically** — no
Ctrl+`, no VS Code. Pick a module, run the commands in the right-hand terminal,
and submit the flag on the left.

(You're viewing a plain browser tab, so VS Code shortcuts like Ctrl+` do not
apply here — the terminal in the page is your terminal.)

## Terminal shows "[terminal closed]"?

The in-page terminal needs `flask-sock`. Install it once and restart:

```bash
pip install flask-sock simple-websocket
python3 webapp/app.py      # then reload the browser tab
```

Either way you can always use the **VS Code integrated terminal** (press
**Ctrl+`**) for the objective commands — the left panel still guides you.

## Safety

The right pane is a real shell on your own Codespace — keep the forwarded port
**Private** (the default). Never make it public; it is for you only.

## How it fits

- The **modules** are the same rooms as `rooms/` (intro, threat modeling, SAST,
  DAST, AppSec, CI/CD) — this is just the graphical, two-pane way to do them.
- The deep labs behind them are `appsec-lab/`, `ctf-lab/`, `devsecops-lab/`, etc.
- Prefer the terminal only? `cd rooms && python3 rooms.py` does the same, text-only.
