#!/usr/bin/env python3
"""Web lab — Hackversity-style guided rooms with a live terminal.

Each module is a room with six sections:
  1. Mission brief   2. Theory   3. Worked example
  4. Knowledge check (several graded questions)
  5. Investigation (step-by-step + hints, you use the terminal)
  6. Capture the flag (submit the answer)

Left: the room (sections + content + a progress sidebar).
Right: a real bash terminal (your Codespace is the machine).

Run:  bash webapp/start.sh      (installs deps, then starts this)
Then open the forwarded port 5000. Keep the port PRIVATE.
"""

from __future__ import annotations

import hashlib
import json
import os
import pty
import select
import signal
import subprocess
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

try:
    from flask_sock import Sock
    _HAS_SOCK = True
except Exception:  # noqa: BLE001
    _HAS_SOCK = False

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MODULES_DIR = HERE / "modules"
PROGRESS = HERE / ".web_progress.json"

app = Flask(__name__)
sock = Sock(app) if _HAS_SOCK else None

SECTIONS = ["brief", "theory", "worked_example", "knowledge_check",
            "investigation", "capture"]
SECTION_LABELS = {
    "brief": "Mission brief", "theory": "Theory", "worked_example": "Worked example",
    "knowledge_check": "Knowledge check", "investigation": "Investigation",
    "capture": "Capture the flag",
}


def _modules() -> list[dict]:
    mods = []
    for p in sorted(MODULES_DIR.glob("*.json")):
        mods.append(json.loads(p.read_text(encoding="utf-8")))
    mods.sort(key=lambda m: m.get("order", 999))
    return mods


def _module(mid: str) -> dict | None:
    return next((m for m in _modules() if m["id"] == mid), None)


def _progress() -> dict:
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {}


def _save_progress(p: dict) -> None:
    PROGRESS.write_text(json.dumps(p, indent=2), encoding="utf-8")


def _h(answer: str) -> str:
    return hashlib.sha256(answer.strip().lower().encode()).hexdigest()


def _mod_progress(mid: str) -> dict:
    return _progress().get(mid, {"sections": [], "kc": [], "captured": False})


def _pct(mid: str, m: dict) -> int:
    mp = _mod_progress(mid)
    total = len(SECTIONS)
    done = len(set(mp.get("sections", [])) & set(SECTIONS))
    return int(done / total * 100)


PAGE = r"""
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Web Lab</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css">
<style>
 :root{color-scheme:dark} *{box-sizing:border-box}
 html,body{margin:0;height:100%;font-family:system-ui,sans-serif;background:#0b0f14;color:#e6edf3;font-size:14px}
 #grid{display:grid;grid-template-columns:200px minmax(360px,1fr) 1fr;height:100vh}
 /* section rail */
 #rail{background:#0d1117;border-right:1px solid #222b33;overflow-y:auto;padding:10px}
 #rail h3{font-size:11px;color:#6e7781;text-transform:uppercase;letter-spacing:.06em;margin:6px 6px 10px}
 .sec{display:flex;align-items:center;gap:8px;padding:8px 8px;border-radius:7px;cursor:pointer;color:#adbac7}
 .sec:hover{background:#161b22}.sec.active{background:#162436;color:#fff}
 .dot{width:16px;height:16px;border-radius:50%;border:1.5px solid #3b434b;flex:0 0 auto;font-size:10px;text-align:center;line-height:14px}
 .sec.done .dot{background:#2ea043;border-color:#2ea043;color:#fff}
 .bar{height:6px;background:#222b33;border-radius:4px;margin:10px 6px}.bar>div{height:100%;background:#2ea043;border-radius:4px}
 /* middle */
 #mid{overflow-y:auto}
 header{padding:10px 16px;background:#0d1117;border-bottom:1px solid #222b33;position:sticky;top:0;z-index:2}
 .mods{display:flex;flex-wrap:wrap;gap:6px}
 .mods button{background:#161b22;color:#adbac7;border:1px solid #30363d;border-radius:16px;padding:3px 9px;font-size:12px;cursor:pointer}
 .mods button.active{background:#2f81f7;border-color:#2f81f7;color:#fff}.mods button.done{border-color:#2ea043}
 .content{padding:18px 22px;max-width:760px}
 h1{font-size:20px;margin:0 0 4px}.meta{color:#6e7781;font-size:12px;margin-bottom:14px}
 h2{font-size:17px;margin:2px 0 10px}
 .card{background:#0d1117;border:1px solid #222b33;border-radius:10px;padding:14px;margin:10px 0;line-height:1.6}
 pre{background:#010409;border:1px solid #222b33;border-radius:8px;padding:12px;overflow-x:auto;font-size:12.5px}
 code{background:#010409;padding:1px 5px;border-radius:4px}
 .md h3{margin:14px 0 6px}
 button.go{background:#2ea043;color:#fff;border:0;border-radius:7px;padding:9px 16px;font-size:14px;cursor:pointer}
 button.ghost{background:#161b22;color:#c9d1d9;border:1px solid #30363d;border-radius:7px;padding:8px 12px;cursor:pointer}
 input[type=text]{background:#010409;border:1px solid #30363d;color:#e6edf3;border-radius:7px;padding:9px;width:100%}
 .q{border-top:1px solid #222b33;padding:12px 0}
 .choice{display:block;background:#010409;border:1px solid #30363d;border-radius:7px;padding:9px;margin:6px 0;cursor:pointer}
 .choice:hover{border-color:#2f81f7}.choice.sel{border-color:#2f81f7;background:#122033}
 .ok{color:#2ea043}.bad{color:#f85149}.result{margin-top:8px;font-size:13px}
 .step{display:flex;gap:10px;padding:8px 0;border-top:1px solid #1c242b}
 .step b{color:#2f81f7}
 .next{margin-top:16px;display:flex;gap:10px}
 /* right terminal */
 #right{display:flex;flex-direction:column;min-width:0;border-left:1px solid #222b33}
 .termbar{padding:7px 12px;background:#0d1117;border-bottom:1px solid #222b33;font-size:12px;color:#6e7781}
 #termwrap{flex:1;min-height:0;background:#000;padding:6px}#terminal{width:100%;height:100%}
 a{color:#2f81f7}
</style></head><body>
<div id="grid">
  <div id="rail">
    <h3>Room</h3>
    <div id="sections"></div>
    <div class="bar"><div id="fill" style="width:0%"></div></div>
    <div id="pcttext" style="color:#6e7781;font-size:12px;margin:0 6px">0%</div>
  </div>
  <div id="mid">
    <header><div class="mods" id="mods"></div></header>
    <div class="content" id="content">Loading…</div>
  </div>
  <div id="right">
    <div class="termbar">Terminal — your machine. The Investigation section's commands run here.</div>
    <div id="termwrap"><div id="terminal"></div></div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
const SECTIONS=["brief","theory","worked_example","knowledge_check","investigation","capture"];
const LABELS={brief:"Mission brief",theory:"Theory",worked_example:"Worked example",
 knowledge_check:"Knowledge check",investigation:"Investigation",capture:"Capture the flag"};
let mods=[], cur=null, curMod=null, sec="brief";

async function boot(){ mods=await (await fetch('/api/modules')).json(); renderMods(); if(mods.length) select(mods[0].id); }
function renderMods(){ const m=document.getElementById('mods'); m.innerHTML='';
 mods.forEach(r=>{const b=document.createElement('button'); b.textContent=r.title;
  b.className=(r.id===cur?'active ':'')+(r.done?'done':''); b.onclick=()=>select(r.id); m.appendChild(b);});}
async function select(id){ cur=id; curMod=await (await fetch('/api/module/'+id)).json(); sec="brief"; renderMods(); renderRail(); renderSection(); }
function renderRail(){ const el=document.getElementById('sections'); el.innerHTML='';
 SECTIONS.forEach(s=>{const d=document.createElement('div'); const done=curMod.progress.sections.includes(s);
  d.className='sec'+(s===sec?' active':'')+(done?' done':'');
  d.innerHTML='<span class="dot">'+(done?'✓':'')+'</span> '+LABELS[s]; d.onclick=()=>{sec=s;renderRail();renderSection();}; el.appendChild(d);});
 const total=SECTIONS.length, done=SECTIONS.filter(s=>curMod.progress.sections.includes(s)).length;
 const pct=Math.round(done/total*100); document.getElementById('fill').style.width=pct+'%'; document.getElementById('pcttext').textContent=pct+'% complete';}
function md(t){return marked.parse(t||'');}
function markDone(s){ fetch('/api/section',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({module:cur,section:s})})
  .then(()=>{ if(!curMod.progress.sections.includes(s))curMod.progress.sections.push(s); renderRail(); renderMods();}); }
function navButtons(nextMsg){ const i=SECTIONS.indexOf(sec);
  let h='<div class="next">'; if(i>0)h+='<button class="ghost" onclick="sec=SECTIONS['+(i-1)+'];renderRail();renderSection()">← Back</button>';
  if(i<SECTIONS.length-1)h+='<button class="go" onclick="markDone(\''+sec+'\');sec=SECTIONS['+(i+1)+'];renderRail();renderSection()">'+(nextMsg||'Mark complete & continue')+' →</button>';
  h+='</div>'; return h; }
function renderSection(){ const c=document.getElementById('content'); const m=curMod;
 let h='<h1>'+m.title+'</h1><div class="meta">'+m.track+' · '+m.difficulty+' · ~'+m.estimate+'</div>';
 h+='<h2>'+LABELS[sec]+'</h2>';
 if(sec==='brief'){ h+='<div class="card md">'+md(m.brief)+'</div>'+navButtons(); }
 else if(sec==='theory'){ h+='<div class="card md">'+md(m.theory)+'</div>'+navButtons(); }
 else if(sec==='worked_example'){ h+='<div class="card md">'+md(m.worked_example)+'</div>'+navButtons(); }
 else if(sec==='knowledge_check'){
   h+='<div class="card">Short checkpoints. Wrong answers cost nothing — retry freely.';
   m.knowledge_check.forEach((q,idx)=>{ const done=m.progress.kc.includes(idx);
     h+='<div class="q"><div><b>Q'+(idx+1)+'.</b> '+q.q+(done?' <span class="ok">✓</span>':'')+'</div>';
     if(q.type==='choice'){ q.choices.forEach(ch=>{ h+='<label class="choice"><input type="radio" name="kc'+idx+'" value="'+encodeURIComponent(ch)+'"> '+ch+'</label>'; }); }
     else { h+='<input type="text" id="kc'+idx+'" placeholder="type the command / answer">'; }
     h+='<button class="ghost" style="margin-top:6px" onclick="submitKc('+idx+',\''+q.type+'\')">Submit answer</button><div class="result" id="kcr'+idx+'"></div></div>'; });
   h+='</div>'+navButtons('Continue');
 }
 else if(sec==='investigation'){
   h+='<div class="card md">'+md(m.investigation.intro)+'</div>';
   h+='<div class="card"><b>Steps</b> (run these in the terminal on the right):';
   m.investigation.steps.forEach((s,i)=>{ h+='<div class="step"><b>'+(i+1)+'</b><div class="md">'+md(s)+'</div></div>'; });
   h+='</div>';
   h+='<div class="card"><b>Need help?</b> Hints get more specific. None gives the flag.<div id="hints"></div>';
   h+='<button class="ghost" id="hintbtn" onclick="revealHint()">Reveal next hint</button></div>';
   h+=navButtons('Continue');
 }
 else if(sec==='capture'){
   h+='<div class="card">'+md(m.capture.task)+'<div style="display:flex;gap:8px;margin-top:10px">'+
      '<input type="text" id="flag" placeholder="'+(m.capture.placeholder||'answer / FLAG{...}')+'">'+
      '<button class="go" onclick="submitFlag()">Submit flag</button></div>'+
      '<div class="result" id="flagr"></div>'+
      '<div style="color:#6e7781;font-size:12px;margin-top:6px">Hint: '+(m.capture.hint||'')+'</div></div>';
 }
 c.innerHTML=h; c.parentElement.scrollTop=0;
 window._hintI=0;
}
async function submitKc(idx,type){ let val='';
 if(type==='choice'){ const sel=document.querySelector('input[name=kc'+idx+']:checked'); if(!sel){return;} val=decodeURIComponent(sel.value);}
 else { val=document.getElementById('kc'+idx).value; }
 const d=await (await fetch('/api/kc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({module:cur,idx,answer:val})})).json();
 const r=document.getElementById('kcr'+idx);
 if(d.ok){ r.className='result ok'; r.textContent='Correct ✓'; if(!curMod.progress.kc.includes(idx))curMod.progress.kc.push(idx); renderSection(); }
 else { r.className='result bad'; r.textContent='Not quite — try again.'; }
}
function revealHint(){ const h=curMod.investigation.hints||[]; const box=document.getElementById('hints');
 if(window._hintI>=h.length){ box.innerHTML+='<div style="color:#6e7781">No more hints.</div>'; return;}
 box.innerHTML+='<div style="color:#d29922;margin:6px 0">Hint '+(window._hintI+1)+': '+h[window._hintI]+'</div>'; window._hintI++; }
async function submitFlag(){ const val=document.getElementById('flag').value;
 const d=await (await fetch('/api/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({module:cur,answer:val})})).json();
 const r=document.getElementById('flagr');
 if(d.ok){ r.className='result ok'; r.textContent='Correct! Room complete 🎉';
   ['capture','investigation'].forEach(s=>{if(!curMod.progress.sections.includes(s))curMod.progress.sections.push(s);}); renderRail(); renderMods(); }
 else { r.className='result bad'; r.textContent='Not correct — re-read the Investigation and try again.'; }
}
// terminal
const TERM_ENABLED = {{ 'true' if term_enabled else 'false' }};
function help(msg){return '<div style="padding:14px;color:#adbac7;font-size:13px;line-height:1.7"><b style="color:#f0883e">'+msg+'</b><br><br>Run <code>bash webapp/start.sh</code> to enable it, then reload.<br>Or use the VS Code terminal.</div>';}
function initTerm(){ const host=document.getElementById('terminal');
 if(!TERM_ENABLED){host.innerHTML=help("Terminal backend (flask-sock) not installed.");return;}
 if(typeof Terminal==='undefined'){host.innerHTML=help("Terminal library didn't load.");return;}
 const term=new Terminal({fontSize:13,theme:{background:'#000'}}); const fit=new FitAddon.FitAddon(); term.loadAddon(fit);
 term.open(host); fit.fit(); const proto=location.protocol==='https:'?'wss':'ws'; let opened=false;
 const ws=new WebSocket(proto+'://'+location.host+'/ws/term');
 ws.onopen=()=>{opened=true;term.onData(d=>ws.send(d));}; ws.onmessage=e=>term.write(e.data);
 ws.onclose=()=>{ if(!opened)host.innerHTML=help("Couldn't connect to the terminal backend."); else term.write('\r\n[session ended — reload]\r\n'); };
 window.addEventListener('resize',()=>fit.fit());
}
boot(); initTerm();
</script></body></html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, term_enabled=_HAS_SOCK)


@app.get("/api/modules")
def api_modules():
    out = []
    for m in _modules():
        mp = _mod_progress(m["id"])
        done = mp.get("captured") or (len(set(mp.get("sections", [])) & set(SECTIONS)) == len(SECTIONS))
        out.append({"id": m["id"], "title": m["title"], "done": bool(done)})
    return jsonify(out)


@app.get("/api/module/<mid>")
def api_module(mid):
    m = _module(mid)
    if not m:
        return jsonify(error="not found"), 404
    public = {k: m.get(k) for k in ("id", "title", "track", "difficulty", "estimate",
                                    "brief", "theory", "worked_example")}
    public["knowledge_check"] = [{"q": q["q"], "type": q["type"],
                                  "choices": q.get("choices", [])} for q in m.get("knowledge_check", [])]
    inv = m.get("investigation", {})
    public["investigation"] = {"intro": inv.get("intro", ""), "steps": inv.get("steps", []),
                               "hints": inv.get("hints", [])}
    cap = m.get("capture", {})
    public["capture"] = {"task": cap.get("task", ""), "hint": cap.get("hint", ""),
                         "placeholder": cap.get("placeholder", "")}
    public["progress"] = _mod_progress(mid)
    return jsonify(public)


@app.post("/api/section")
def api_section():
    d = request.get_json(force=True)
    p = _progress()
    mp = p.setdefault(d["module"], {"sections": [], "kc": [], "captured": False})
    if d["section"] not in mp["sections"]:
        mp["sections"].append(d["section"])
    _save_progress(p)
    return jsonify(ok=True)


@app.post("/api/kc")
def api_kc():
    d = request.get_json(force=True)
    m = _module(d["module"])
    if not m:
        return jsonify(ok=False), 404
    idx = int(d["idx"])
    q = m["knowledge_check"][idx]
    ok = _h(d.get("answer", "")) == q["answer_sha256"]
    if ok:
        p = _progress()
        mp = p.setdefault(d["module"], {"sections": [], "kc": [], "captured": False})
        if idx not in mp["kc"]:
            mp["kc"].append(idx)
        # mark knowledge_check section done when all questions solved
        if len(mp["kc"]) >= len(m["knowledge_check"]) and "knowledge_check" not in mp["sections"]:
            mp["sections"].append("knowledge_check")
        _save_progress(p)
    return jsonify(ok=ok)


@app.post("/api/capture")
def api_capture():
    d = request.get_json(force=True)
    m = _module(d["module"])
    if not m:
        return jsonify(ok=False), 404
    ok = _h(d.get("answer", "")) == m["capture"]["answer_sha256"]
    if ok:
        p = _progress()
        mp = p.setdefault(d["module"], {"sections": [], "kc": [], "captured": False})
        mp["captured"] = True
        for s in ("capture", "investigation"):
            if s not in mp["sections"]:
                mp["sections"].append(s)
        _save_progress(p)
    return jsonify(ok=ok)


if _HAS_SOCK:
    @sock.route("/ws/term")
    def ws_term(ws):
        master, slave = pty.openpty()
        proc = subprocess.Popen(["bash"], preexec_fn=os.setsid, stdin=slave, stdout=slave,
                                stderr=slave, cwd=str(REPO),
                                env={**os.environ, "TERM": "xterm-256color"})
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

        threading.Thread(target=reader, daemon=True).start()
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
        print("flask-sock not installed; terminal disabled. Run webapp/start.sh.")
    print("Open the forwarded port 5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
