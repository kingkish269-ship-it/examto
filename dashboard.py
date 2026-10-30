#!/usr/bin/env python3
"""A clickable browser GUI for the security-lab program.

Run it, open the forwarded port, and work through the labs by pointing and
clicking: read each task, copy the command, press "Run check", and watch it
grade you with a green PASS. It reuses the same engine as coach.py, so your
progress is shared between the GUI and the command line.

    python3 dashboard.py        # then open the forwarded port (5000) in a browser
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template_string

from coach import (ROOT, _interpreter, _run, _verify_ctf, current_step,
                   load_curriculum, load_done, save_done)

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Labs</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: system-ui, sans-serif; margin: 0; background:#0d1117; color:#e6edf3; }
  header { padding: 20px 24px; background:#161b22; border-bottom:1px solid #30363d; }
  h1 { margin:0 0 10px; font-size:20px; }
  .bar { height:12px; background:#30363d; border-radius:6px; overflow:hidden; }
  .bar > div { height:100%; background:#2ea043; width:0%; transition:width .3s; }
  .sub { color:#8b949e; font-size:13px; margin-top:6px; }
  main { padding: 20px 24px; max-width: 860px; margin:0 auto; }
  .card { background:#161b22; border:1px solid #30363d; border-radius:10px; padding:16px; margin:12px 0; }
  .card.done { opacity:.6; }
  .card.current { border-color:#2f81f7; box-shadow:0 0 0 1px #2f81f7; }
  .row { display:flex; align-items:center; gap:10px; }
  .badge { font-size:11px; padding:2px 8px; border-radius:20px; background:#21262d; color:#8b949e; }
  .status { margin-left:auto; font-weight:600; }
  .status.ok { color:#2ea043; } .status.todo { color:#8b949e; } .status.now { color:#2f81f7; }
  h3 { margin:6px 0; font-size:16px; }
  .teach { color:#adbac7; font-size:14px; }
  code, pre { background:#0d1117; border:1px solid #30363d; border-radius:6px; }
  pre { padding:10px; overflow-x:auto; font-size:13px; }
  button { background:#2ea043; color:#fff; border:0; padding:10px 16px; border-radius:6px;
           font-size:14px; cursor:pointer; margin-top:10px; }
  button:disabled { background:#30363d; cursor:wait; }
  .result { margin-top:10px; font-size:13px; white-space:pre-wrap; }
  .result.pass { color:#2ea043; } .result.fail { color:#f85149; }
  a { color:#2f81f7; }
</style>
</head>
<body>
<header>
  <h1>Security Labs — your progress</h1>
  <div class="bar"><div id="fill" style="width:{{ pct }}%"></div></div>
  <div class="sub">{{ done }}/{{ total }} tasks complete. Do the command shown, then press
  <b>Run check</b>. Full help in <a href="https://github.com/kingkish269-ship-it/examto/blob/main/GUIDE.md">GUIDE.md</a>.</div>
</header>
<main>
{% for s in steps %}
  <div class="card {{ s.cls }}" id="card-{{ s.id }}">
    <div class="row">
      <span class="badge">{{ s.lab }}</span>
      <span class="status {{ s.scls }}">{{ s.label }}</span>
    </div>
    <h3>{{ loop.index }}. {{ s.title }}</h3>
    {% if s.cls == 'current' %}
      <p class="teach">{{ s.teach }}</p>
      <div class="teach">Do this (open a terminal, paste it):</div>
      <pre>{{ s.do }}</pre>
      <button onclick="runCheck()">Run check</button>
      <div class="result" id="result"></div>
    {% endif %}
  </div>
{% endfor %}
{% if done == total %}
  <div class="card"><h3>All tasks complete 🎉</h3>
  <p class="teach">You worked through every lab. That is your portfolio.</p></div>
{% endif %}
</main>
<script>
async function runCheck(){
  const btn = document.querySelector('button'); const res = document.getElementById('result');
  btn.disabled = true; res.textContent = 'Running check...'; res.className = 'result';
  try{
    const r = await fetch('/api/check', {method:'POST'}); const d = await r.json();
    if(d.passed){ res.className='result pass'; res.textContent = 'PASS. '+ (d.next ? 'Next: '+d.next : 'Program complete!');
      setTimeout(()=>location.reload(), 900); }
    else { res.className='result fail'; res.textContent = 'Not passing yet.\\n\\n'+d.detail; btn.disabled=false; }
  }catch(e){ res.className='result fail'; res.textContent='Error: '+e; btn.disabled=false; }
}
</script>
</body>
</html>
"""


def _state():
    curriculum = load_curriculum()
    done = load_done()
    steps = []
    cur = current_step(curriculum, done)
    cur_id = cur["id"] if cur else None
    for s in curriculum:
        if s["id"] in done:
            cls, scls, label = "done", "ok", "✓ done"
        elif s["id"] == cur_id:
            cls, scls, label = "current", "now", "▶ current"
        else:
            cls, scls, label = "upcoming", "todo", "locked"
        steps.append({**s, "cls": cls, "scls": scls, "label": label,
                      "teach": s["teach"], "do": s["do"]})
    total = len(curriculum)
    pct = int(len(done) / total * 100) if total else 0
    return curriculum, done, steps, total, pct


@app.get("/")
def index():
    _c, done, steps, total, pct = _state()
    return render_template_string(PAGE, steps=steps, done=len(done), total=total, pct=pct)


@app.post("/api/check")
def api_check():
    curriculum = load_curriculum()
    done = load_done()
    step = current_step(curriculum, done)
    if step is None:
        return jsonify(passed=True, detail="All done", next=None)
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
        hint = f"First time in this lab? Run its setup first:\n  cd {step['lab']} && {v['setup']}\n\n"
    return jsonify(passed=False, detail=hint + detail)


if __name__ == "__main__":
    print("Open the forwarded port 5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False)
