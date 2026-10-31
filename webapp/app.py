#!/usr/bin/env python3
"""Web lab — theory on the left, a live terminal on the right.

A TryHackMe / Hackversity-style two-pane page you run inside your Codespace:
  * left  = clickable modules, each showing LEARN + OBJECTIVES + the task,
  * right = a real bash terminal (your Codespace is the machine),
  * a flag box to submit answers (graded, shared with rooms.py).

Run it:
    python3 webapp/app.py
then open the forwarded port 5000 in your browser.

Keep the forwarded port PRIVATE (the default). The terminal is a real shell on
your own Codespace — do not expose it publicly.
"""

from __future__ import annotations

import hashlib
import json
import os
import pty
import select
import signal
import struct
import subprocess
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

try:
    from flask_sock import Sock
    _HAS_SOCK = True
except Exception:  # noqa: BLE001
    _HAS_SOCK = False

REPO = Path(__file__).resolve().parents[1]
ROOMS_DIR = REPO / "rooms"
PROGRESS = ROOMS_DIR / ".rooms_progress.json"

app = Flask(__name__)
sock = Sock(app) if _HAS_SOCK else None


def _rooms() -> list[dict]:
    path = ROOMS_DIR / "rooms.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def _done() -> set[str]:
    if PROGRESS.exists():
        return set(json.loads(PROGRESS.read_text()).get("done", []))
    return set()


def _save(done: set[str]) -> None:
    PROGRESS.write_text(json.dumps({"done": sorted(done)}))


def _h(answer: str) -> str:
    return hashlib.sha256(answer.strip().lower().encode()).hexdigest()


PAGE = """
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Web Lab</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css">
<style>
  :root{color-scheme:dark}
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;font-family:system-ui,sans-serif;background:#0d1117;color:#e6edf3}
  #grid{display:grid;grid-template-columns:minmax(320px,44%) 1fr;height:100vh}
  #left{overflow-y:auto;border-right:1px solid #30363d;padding:0 0 40px}
  #right{display:flex;flex-direction:column;min-width:0}
  header{padding:12px 16px;background:#161b22;border-bottom:1px solid #30363d;position:sticky;top:0;z-index:2}
  h1{font-size:15px;margin:0}
  .mods{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
  .mods button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:16px;padding:4px 10px;font-size:12px;cursor:pointer}
  .mods button.active{background:#2f81f7;border-color:#2f81f7;color:#fff}
  .mods button.done{border-color:#2ea043}
  .body{padding:16px}
  h2{font-size:18px;margin:4px 0 10px}
  .summary{color:#adbac7;line-height:1.5;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px}
  .label{color:#8b949e;font-size:12px;text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px}
  ol{margin:0;padding-left:20px;line-height:1.6}
  .md{line-height:1.55} .md pre{background:#010409;border:1px solid #30363d;border-radius:6px;padding:10px;overflow-x:auto}
  .md code{background:#010409;padding:1px 4px;border-radius:4px}
  .task{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px;margin-top:8px}
  .flagbox{display:flex;gap:8px;margin-top:10px}
  input[type=text]{flex:1;background:#010409;border:1px solid #30363d;color:#e6edf3;border-radius:6px;padding:9px}
  button.go{background:#2ea043;color:#fff;border:0;border-radius:6px;padding:9px 14px;cursor:pointer}
  .result{margin-top:8px;font-size:13px}.pass{color:#2ea043}.fail{color:#f85149}
  #termwrap{flex:1;min-height:0;background:#000;padding:6px}
  #terminal{width:100%;height:100%}
  .termbar{padding:8px 12px;background:#161b22;border-bottom:1px solid #30363d;font-size:12px;color:#8b949e}
</style></head>
<body>
<div id="grid">
  <div id="left">
    <header>
      <h1>Security Web Lab</h1>
      <div class="mods" id="mods"></div>
    </header>
    <div class="body" id="content">Loading…</div>
  </div>
  <div id="right">
    <div class="termbar">Terminal — your Codespace machine. (If it doesn't connect, use the VS Code terminal with Ctrl+` and run the commands there.)</div>
    <div id="termwrap"><div id="terminal"></div></div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
let rooms=[], current=null;
async function load(){
  rooms = await (await fetch('/api/rooms')).json();
  renderMods();
  if(rooms.length) select(rooms[0].id);
}
function renderMods(){
  const m=document.getElementById('mods'); m.innerHTML='';
  rooms.forEach(r=>{
    const b=document.createElement('button');
    b.textContent=r.title.split(' — ')[0];
    b.className=(r.id===current?'active ':'')+(r.done?'done':'');
    b.onclick=()=>select(r.id); m.appendChild(b);
  });
}
async function select(id){
  current=id; renderMods();
  const r=await (await fetch('/api/room/'+id)).json();
  document.getElementById('content').innerHTML=`
    <h2>${r.title} ${r.done?'✓':''}</h2>
    <div class="summary">${r.summary}</div>
    <div class="label">Objectives</div>
    <ol>${r.objectives.map(o=>'<li>'+o+'</li>').join('')}</ol>
    <div class="label">Briefing</div>
    <div class="md" id="md"></div>
    <div class="label">Task</div>
    <div class="task">${r.task}
      <div class="flagbox">
        <input type="text" id="ans" placeholder="type your answer / FLAG{...}">
        <button class="go" onclick="submit('${id}')">Submit</button>
      </div>
      <div class="result" id="res"></div>
      <div style="color:#8b949e;font-size:12px;margin-top:6px">Hint: ${r.hint||''}</div>
    </div>`;
  document.getElementById('md').innerHTML = marked.parse(r.readme||'');
}
async function submit(id){
  const ans=document.getElementById('ans').value, res=document.getElementById('res');
  const d=await (await fetch('/api/submit',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id,answer:ans})})).json();
  if(d.ok){res.className='result pass';res.textContent='Correct! Room complete.';
    const r=rooms.find(x=>x.id===id); if(r)r.done=true; renderMods();}
  else{res.className='result fail';res.textContent='Not correct — re-read the briefing and try again.';}
}
// ---- terminal ----
const TERM_ENABLED = {{ 'true' if term_enabled else 'false' }};
function help(msg){
  return '<div style="padding:14px;color:#adbac7;font-size:13px;line-height:1.7">'
    + '<b style="color:#f0883e">'+msg+'</b><br><br>'
    + 'Easiest fix — use the built-in VS Code terminal instead:<br>'
    + 'press <b>Ctrl+`</b> (or Terminal menu), and run the objective commands there.<br><br>'
    + 'To enable this in-page terminal: in a terminal run<br>'
    + '<code>pip install flask-sock simple-websocket</code><br>'
    + 'then restart <code>python3 webapp/app.py</code> and reload this page.</div>';
}
function initTerm(){
  const host=document.getElementById('terminal');
  if(!TERM_ENABLED){ host.innerHTML=help("The in-page terminal backend (flask-sock) isn't installed."); return; }
  if(typeof Terminal==='undefined'){ host.innerHTML=help("The terminal display library didn't load (no internet for the CDN?)."); return; }
  const term=new Terminal({fontSize:13,theme:{background:'#000000'}});
  const fit=new FitAddon.FitAddon(); term.loadAddon(fit);
  term.open(host); fit.fit();
  const proto=location.protocol==='https:'?'wss':'ws';
  let opened=false;
  const ws=new WebSocket(proto+'://'+location.host+'/ws/term');
  ws.onopen=()=>{ opened=true; term.onData(d=>ws.send(d)); term.write('connected. type commands here.\\r\\n'); };
  ws.onmessage=e=>term.write(e.data);
  ws.onclose=()=>{ if(!opened){ host.innerHTML=help("Couldn't connect to the terminal backend."); }
                   else { term.write('\\r\\n[session ended — reload the page to restart]\\r\\n'); } };
  window.addEventListener('resize',()=>fit.fit());
}
load(); initTerm();
</script></body></html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, term_enabled=_HAS_SOCK)


@app.get("/api/rooms")
def api_rooms():
    done = _done()
    return jsonify([{"id": r["id"], "title": r["title"], "done": r["id"] in done}
                    for r in _rooms()])


@app.get("/api/room/<rid>")
def api_room(rid):
    r = next((x for x in _rooms() if x["id"] == rid), None)
    if not r:
        return jsonify(error="not found"), 404
    readme = ""
    rp = ROOMS_DIR / r["dir"] / "README.md"
    if rp.exists():
        readme = rp.read_text(encoding="utf-8")
    return jsonify({**{k: r[k] for k in ("id", "title", "summary", "objectives", "task", "hint")},
                    "readme": readme, "done": rid in _done()})


@app.post("/api/submit")
def api_submit():
    data = request.get_json(force=True)
    r = next((x for x in _rooms() if x["id"] == data.get("id")), None)
    if not r:
        return jsonify(ok=False, error="unknown room"), 404
    ok = _h(data.get("answer", "")) == r["answer_sha256"]
    if ok:
        done = _done()
        done.add(r["id"])
        _save(done)
    return jsonify(ok=ok)


if _HAS_SOCK:
    @sock.route("/ws/term")
    def ws_term(ws):
        master, slave = pty.openpty()
        proc = subprocess.Popen(
            ["bash"], preexec_fn=os.setsid,
            stdin=slave, stdout=slave, stderr=slave, cwd=str(REPO),
            env={**os.environ, "TERM": "xterm-256color", "PS1": "lab$ "},
        )
        os.close(slave)

        def reader():
            try:
                while True:
                    r, _, _ = select.select([master], [], [], 0.2)
                    if master in r:
                        data = os.read(master, 4096)
                        if not data:
                            break
                        ws.send(data.decode(errors="ignore"))
                    if proc.poll() is not None:
                        break
            except Exception:  # noqa: BLE001
                pass

        t = threading.Thread(target=reader, daemon=True)
        t.start()
        try:
            while True:
                msg = ws.receive()
                if msg is None:
                    break
                os.write(master, msg.encode())
        except Exception:  # noqa: BLE001
            pass
        finally:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:  # noqa: BLE001
                pass


if __name__ == "__main__":
    if not _HAS_SOCK:
        print("Note: flask-sock not installed; terminal pane disabled.")
        print("Install it:  pip install flask-sock simple-websocket")
    print("Open the forwarded port 5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
