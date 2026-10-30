# Web Lab — theory left, terminal right (in your browser)

A two-pane web page, TryHackMe / Hackversity style, running in your Codespace:

- **Left:** clickable modules; each shows LEARN + OBJECTIVES + briefing + a flag box.
- **Right:** a real **bash terminal** on your Codespace (the machine).
- Submitting a flag is graded and shared with `rooms.py`.

## Run it

In your Codespace (dependencies are installed automatically by the dev container):

```bash
cd /workspaces/examto
python3 webapp/app.py
```

Then open the **port 5000** popup → **Open in Browser**. You'll get the split
page: pick a module on the left, do the objective commands in the terminal on
the right, and submit the flag.

If you run it outside the Codespace, install the deps first:
```bash
pip install -r webapp/requirements.txt
```

## Safety

The right pane is a real shell on your own Codespace — keep the forwarded port
**Private** (the default). Never make it public; it is for you only.

## How it fits

- The **modules** are the same rooms as `rooms/` (intro, threat modeling, SAST,
  DAST, AppSec, CI/CD) — this is just the graphical, two-pane way to do them.
- The deep labs behind them are `appsec-lab/`, `ctf-lab/`, `devsecops-lab/`, etc.
- Prefer the terminal only? `cd rooms && python3 rooms.py` does the same, text-only.
