#!/usr/bin/env python3
"""A TryHackMe-style browser GUI for the security-lab program.

Left side: the task — lesson, the commands to run, hints, and (for the CTF) a
flag-submission box that grades you. You run the actual lab work in a terminal.
It shares progress with coach.py.

    python3 dashboard.py        # then open the forwarded port 5000 in a browser

Recommended layout in a Codespace: open this in the Simple Browser and drag the
tab to the left; move the Terminal panel to the right. Instructions on the left,
terminal on the right — just like TryHackMe.
"""

from __future__ import annotations

import hashlib
import json

from flask import Flask, jsonify, render_template_string, request

from coach import (ROOT, _interpreter, _run, _verify_ctf, current_step,
                   load_curriculum, load_done, save_done)

app = Flask(__name__)

CTF_DIR = ROOT / "ctf-lab"


# ----- CTF helpers (read the challenge key, grade flags, track progress) -----
def _ctf_challenges() -> list[dict]:
    path = CTF_DIR / "challenges.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def _ctf_progress() -> dict:
    path = CTF_DIR / "progress.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"solved": [], "hints_used": {}}


def _ctf_save(progress: dict) -> None:
    (CTF_DIR / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")


def _flag_ok(challenge: dict, flag: str) -> bool:
    digest = hashlib.sha256(f"{challenge['salt']}:{flag.strip()}".encode()).hexdigest()
    return digest == challenge["flag_sha256"]


PAGE = """
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Labs</title>
<style>
  :root{color-scheme:dark}
  *{box-sizing:border-box}
  body{font-family:system-ui,sans-serif;margin:0;background:#0d1117;color:#e6edf3;font-size:15px}
  header{padding:16px 20px;background:#161b22;border-bottom:1px solid #30363d;position:sticky;top:0}
  h1{margin:0 0 8px;font-size:17px}
  .bar{height:10px;background:#30363d;border-radius:6px;overflow:hidden}
  .bar>div{height:100%;background:#2ea043;transition:width .3s}
  .sub{color:#8b949e;font-size:12px;margin-top:6px}
  main{padding:18px 20px;max-width:760px;margin:0 auto}
  .task{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:18px}
  .nav{display:flex;gap:8px;margin:14px 0}
  .nav button{flex:0 0 auto}
  .badge{font-size:11px;padding:2px 8px;border-radius:20px;background:#21262d;color:#8b949e;margin-right:6px}
  .status{font-weight:600}.ok{color:#2ea043}.now{color:#2f81f7}.todo{color:#8b949e}
  h2{font-size:18px;margin:10px 0}
  .teach{color:#adbac7;line-height:1.5}
  .label{color:#8b949e;font-size:12px;text-transform:uppercase;letter-spacing:.04em;margin-top:16px}
  pre{background:#010409;border:1px solid #30363d;border-radius:6px;padding:12px;overflow-x:auto;font-size:13px}
  button{background:#2ea043;color:#fff;border:0;padding:9px 15px;border-radius:6px;font-size:14px;cursor:pointer}
  button.ghost{background:#21262d;color:#c9d1d9;border:1px solid #30363d}
  button:disabled{background:#30363d;cursor:wait}
  input[type=text]{background:#010409;border:1px solid #30363d;color:#e6edf3;border-radius:6px;padding:9px;width:100%;font-size:14px}
  .result{margin-top:10px;white-space:pre-wrap;font-size:13px}
  .pass{color:#2ea043}.fail{color:#f85149}
  .chal{border-top:1px solid #30363d;padding:10px 0}
  .chal .row{display:flex;align-items:center;gap:8px}
  .hint{color:#d29922;font-size:13px;margin-top:6px}
  .flagbox{display:flex;gap:8px;margin-top:8px}
  a{color:#2f81f7}
</style></head><body>
<header>
  <h1>Security Labs</h1>
  <div class="bar"><div style="width:{{pct}}%"></div></div>
  <div class="sub">{{done}}/{{total}} tasks complete &middot; run lab work in a terminal, submit here &middot;
   <a href="https://github.com/kingkish269-ship-it/examto/blob/main/GUIDE.md">help</a></div>
</header>
<main>
{% if step %}
  <div class="task">
    <div><span class="badge">{{step.lab}}</span><span class="status now">Task {{index}} of {{total}}</span></div>
    <h2>{{step.title}}</h2>
    <p class="teach">{{step.teach}}</p>

    <div class="label">Do this in a terminal</div>
    <pre>{{step.do}}</pre>

    {% if is_ctf %}
      <div class="label">Capture flags ({{ctf_solved}}/{{ctf_total}} solved)</div>
      {% for c in challenges %}
        <div class="chal">
          <div class="row">
            <span class="badge">{{c.tier}}</span>
            <b>{{c.id}}</b> — {{c.title}}
            <span class="status {{'ok' if c.solved else 'todo'}}" style="margin-left:auto">
              {{'✓ captured' if c.solved else c.points ~ ' pts'}}</span>
          </div>
          <button class="ghost" onclick="hint('{{c.id}}')" style="margin-top:6px">Show hint</button>
          <div class="hint" id="hint-{{c.id}}" data-hints='{{c.hints_json}}' data-i="0"></div>
          <div class="flagbox">
            <input type="text" id="flag-{{c.id}}" placeholder="FLAG{...}">
            <button onclick="submitFlag('{{c.id}}')">Submit</button>
          </div>
          <div class="result" id="res-{{c.id}}"></div>
        </div>
      {% endfor %}
    {% else %}
      <button onclick="runCheck()" style="margin-top:14px">Run check</button>
      <div class="result" id="result"></div>
    {% endif %}
  </div>
{% else %}
  <div class="task"><h2>All tasks complete 🎉</h2>
  <p class="teach">You finished every lab. That is your portfolio.</p></div>
{% endif %}
</main>
<script>
async function runCheck(){
  const b=document.querySelector('main button'),r=document.getElementById('result');
  b.disabled=true;r.textContent='Running check...';r.className='result';
  const d=await (await fetch('/api/check',{method:'POST'})).json();
  if(d.passed){r.className='result pass';r.textContent='PASS. '+(d.next?'Next: '+d.next:'Done!');setTimeout(()=>location.reload(),900);}
  else{r.className='result fail';r.textContent='Not yet.\\n\\n'+d.detail;b.disabled=false;}
}
async function submitFlag(id){
  const flag=document.getElementById('flag-'+id).value,res=document.getElementById('res-'+id);
  res.textContent='Checking...';res.className='result';
  const d=await (await fetch('/api/ctf/submit',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id,flag})})).json();
  if(d.ok){res.className='result pass';res.textContent='Correct! '+d.solved+'/'+d.total+' captured.';setTimeout(()=>location.reload(),900);}
  else{res.className='result fail';res.textContent='Not correct. Try a hint.';}
}
function hint(id){
  const el=document.getElementById('hint-'+id);const hints=JSON.parse(el.dataset.hints||'[]');
  let i=parseInt(el.dataset.i||'0');if(i>=hints.length){el.textContent='No more hints.';return;}
  el.textContent='Hint '+(i+1)+': '+hints[i];el.dataset.i=i+1;
}
</script></body></html>
"""


@app.get("/")
def index():
    curriculum = load_curriculum()
    done = load_done()
    step = current_step(curriculum, done)
    total = len(curriculum)
    pct = int(len(done) / total * 100) if total else 0
    index_no = (curriculum.index(step) + 1) if step else total

    is_ctf = bool(step and step.get("verify", {}).get("type") == "ctf")
    challenges, ctf_solved, ctf_total = [], 0, 0
    if is_ctf:
        solved = set(_ctf_progress().get("solved", []))
        ctf_total = len(_ctf_challenges())
        ctf_solved = len(solved)
        for c in _ctf_challenges():
            challenges.append({**c, "solved": c["id"] in solved,
                               "hints_json": json.dumps(c.get("hints", []))})

    return render_template_string(
        PAGE, step=step, index=index_no, total=total, done=len(done), pct=pct,
        is_ctf=is_ctf, challenges=challenges, ctf_solved=ctf_solved, ctf_total=ctf_total)


@app.post("/api/check")
def api_check():
    curriculum = load_curriculum()
    done = load_done()
    step = current_step(curriculum, done)
    if step is None:
        return jsonify(passed=True, next=None)
    v = step["verify"]
    if v.get("type") == "ctf":
        ok, detail = _verify_ctf(v)
    else:
        cmd = v["cmd"].replace("{py}", _interpreter(step["lab"]))
        code, output = _run(cmd, ROOT / v["cwd"])
        needle = v.get("contains")
        ok = needle in output if needle else code == 0
        detail = output[-1500:]
    if ok:
        done.add(step["id"])
        save_done(done)
        nxt = current_step(curriculum, done)
        return jsonify(passed=True, next=(nxt["title"] if nxt else None))
    hint = ""
    if v.get("setup"):
        hint = f"First time in this lab? Run:\n  cd {step['lab']} && {v['setup']}\n\n"
    return jsonify(passed=False, detail=hint + detail)


@app.post("/api/ctf/submit")
def api_ctf_submit():
    data = request.get_json(force=True)
    cid, flag = data.get("id"), data.get("flag", "")
    challenge = next((c for c in _ctf_challenges() if c["id"] == cid), None)
    if challenge is None:
        return jsonify(ok=False, error="unknown challenge"), 404
    progress = _ctf_progress()
    solved = progress.setdefault("solved", [])
    ok = _flag_ok(challenge, flag)
    if ok and cid not in solved:
        solved.append(cid)
        _ctf_save(progress)
    # If enough flags are now captured, auto-complete the current coach task.
    curriculum, done = load_curriculum(), load_done()
    step = current_step(curriculum, done)
    if step and step.get("verify", {}).get("type") == "ctf":
        passed, _ = _verify_ctf(step["verify"])
        if passed:
            done.add(step["id"])
            save_done(done)
    return jsonify(ok=ok, solved=len(solved), total=len(_ctf_challenges()))


if __name__ == "__main__":
    print("Open the forwarded port 5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False)
