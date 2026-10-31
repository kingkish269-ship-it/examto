#!/usr/bin/env python3
"""
Generate COMPLETE_GUIDE.pdf at the repo root.

This is a self-contained generator. The guide content lives in the CONTENT
list below as simple structured blocks, so it is easy to edit and regenerate:

    pip install fpdf2
    python3 docs/make_pdf.py

Everything is ASCII-only on purpose so the default PDF font (latin-1) never
chokes on em-dashes, emoji, or smart quotes.
"""
import os
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Colors / layout
# ---------------------------------------------------------------------------
INK = (30, 34, 40)
MUTED = (90, 98, 110)
ACCENT = (36, 99, 235)      # blue
ACCENT_DK = (23, 64, 153)
RULE = (210, 215, 222)
CODE_BG = (244, 246, 249)
TBL_HEAD = (36, 99, 235)
TBL_ALT = (242, 245, 250)

MARGIN = 18


class Guide(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(8)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "examto  -  Application Security Learning Lab", align="L")
        self.cell(0, 6, "Complete Guide", align="R")
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(MARGIN, 15, self.w - MARGIN, 15)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "github.com/kingkish269-ship-it/examto", align="L")
        self.cell(0, 6, "Page %d" % self.page_no(), align="R")


def ascii_only(s):
    return (s.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2014", "-").replace("\u2013", "-")
             .replace("\u2026", "...").encode("ascii", "ignore").decode())


def new_pdf():
    pdf = Guide(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(MARGIN, 18, MARGIN)
    return pdf


def cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, pdf.w, 70, "F")
    pdf.set_xy(MARGIN, 24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 30)
    pdf.cell(0, 14, "examto", ln=1)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "", 15)
    pdf.cell(0, 10, "Application Security Learning Lab", ln=1)

    pdf.set_xy(MARGIN, 86)
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "The Complete Step-by-Step Guide", ln=1)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 7, ascii_only(
        "Everything you need to finish every room on your own. Free, runs "
        "entirely in GitHub Codespaces, no interaction with anyone required."))
    pdf.ln(6)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*INK)
    facts = [
        "23 hands-on rooms across 4 tracks (foundations, web exploits, AppSec, DevSecOps)",
        "6 sections per room: Brief, Theory, Worked example, Knowledge check, Investigation, Capture",
        "Live terminal on the right - the Codespace is your machine",
        "Real free tools: Bandit, Semgrep, Checkov, pip-audit, sqlmap, gitleaks",
        "A separate learn-python track that tests you lesson by lesson",
    ]
    for f in facts:
        pdf.set_x(MARGIN)
        pdf.set_text_color(*ACCENT)
        pdf.cell(6, 7, ">")
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 7, ascii_only(f))
    pdf.ln(10)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6, ascii_only(
        "Built for your path: from infrastructure/cloud/endpoint security into "
        "remote Application Security and DevSecOps roles. Keep this PDF handy; "
        "it is your map."))


# ---------------------------------------------------------------------------
# Rendering engine for CONTENT blocks
# ---------------------------------------------------------------------------
def h1(pdf, text):
    if pdf.get_y() > pdf.h - 60:
        pdf.add_page()
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*ACCENT_DK)
    pdf.multi_cell(0, 9, ascii_only(text))
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.5)
    y = pdf.get_y() + 1
    pdf.line(MARGIN, y, MARGIN + 40, y)
    pdf.ln(4)


def h2(pdf, text):
    if pdf.get_y() > pdf.h - 45:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 7, ascii_only(text))
    pdf.ln(1)


def para(pdf, text):
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.6, ascii_only(text))
    pdf.ln(1.5)


def bullet(pdf, items):
    pdf.set_font("Helvetica", "", 10.5)
    for it in items:
        pdf.set_x(MARGIN + 2)
        pdf.set_text_color(*ACCENT)
        pdf.cell(5, 5.6, "-")
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 5.6, ascii_only(it))
    pdf.ln(1.5)


def steps(pdf, items):
    pdf.set_font("Helvetica", "", 10.5)
    for i, it in enumerate(items, 1):
        pdf.set_x(MARGIN + 1)
        pdf.set_text_color(*ACCENT_DK)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(7, 5.6, "%d." % i)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 5.6, ascii_only(it))
    pdf.ln(1.5)


def code(pdf, lines):
    pdf.ln(1)
    pdf.set_font("Courier", "", 9.5)
    line_h = 5.0
    pad = 2.5
    height = line_h * len(lines) + pad * 2
    if pdf.get_y() + height > pdf.h - 16:
        pdf.add_page()
    x0, y0 = MARGIN, pdf.get_y()
    pdf.set_fill_color(*CODE_BG)
    pdf.set_draw_color(*RULE)
    pdf.rect(x0, y0, pdf.w - 2 * MARGIN, height, "DF")
    pdf.set_xy(x0 + 3, y0 + pad)
    pdf.set_text_color(40, 44, 52)
    for ln in lines:
        pdf.set_x(x0 + 3)
        pdf.cell(0, line_h, ascii_only(ln), ln=1)
    pdf.set_y(y0 + height)
    pdf.ln(2.5)


def callout(pdf, title, text):
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 10)
    body = ascii_only(text)
    # estimate height
    pdf.set_xy(MARGIN + 6, pdf.get_y())
    start_y = pdf.get_y()
    pdf.set_x(MARGIN + 6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ACCENT_DK)
    pdf.multi_cell(pdf.w - 2 * MARGIN - 10, 5.4, ascii_only(title))
    pdf.set_x(MARGIN + 6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    pdf.multi_cell(pdf.w - 2 * MARGIN - 10, 5.4, body)
    end_y = pdf.get_y()
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1.2)
    pdf.line(MARGIN + 2, start_y, MARGIN + 2, end_y)
    pdf.ln(2.5)


def table(pdf, headers, rows, widths):
    avail = pdf.w - 2 * MARGIN
    total = sum(widths)
    widths = [w / total * avail for w in widths]
    line_h = 5.4
    # header
    if pdf.get_y() > pdf.h - 30:
        pdf.add_page()
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_fill_color(*TBL_HEAD)
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(*RULE)
    for w, hd in zip(widths, headers):
        pdf.cell(w, 7, ascii_only(hd), border=0, fill=True, align="L")
    pdf.ln(7)
    pdf.set_font("Helvetica", "", 9.3)
    for ri, row in enumerate(rows):
        # compute row height via wrapped lines
        cell_lines = []
        for w, c in zip(widths, row):
            txt = ascii_only(str(c))
            cell_lines.append(_wrap(pdf, txt, w - 2))
        rh = max(len(cl) for cl in cell_lines) * line_h + 1.6
        if pdf.get_y() + rh > pdf.h - 16:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_fill_color(*TBL_HEAD)
            pdf.set_text_color(255, 255, 255)
            for w, hd in zip(widths, headers):
                pdf.cell(w, 7, ascii_only(hd), border=0, fill=True, align="L")
            pdf.ln(7)
            pdf.set_font("Helvetica", "", 9.3)
        fill = ri % 2 == 1
        x0 = pdf.get_x()
        y0 = pdf.get_y()
        if fill:
            pdf.set_fill_color(*TBL_ALT)
            pdf.rect(x0, y0, sum(widths), rh, "F")
        pdf.set_text_color(*INK)
        x = x0
        for w, cl in zip(widths, cell_lines):
            pdf.set_xy(x + 1, y0 + 0.8)
            for line in cl:
                pdf.set_x(x + 1)
                pdf.cell(w - 2, line_h, line, ln=2)
            x += w
        pdf.set_xy(x0, y0 + rh)
        pdf.set_draw_color(*RULE)
        pdf.set_line_width(0.15)
        pdf.line(MARGIN, y0 + rh, pdf.w - MARGIN, y0 + rh)
    pdf.ln(3)


def _wrap(pdf, text, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if pdf.get_string_width(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines or [""]


RENDER = {
    "h1": h1, "h2": h2, "p": para, "bullet": bullet, "steps": steps,
    "code": code, "callout": callout, "table": table,
}


# ---------------------------------------------------------------------------
# The guide content
# ---------------------------------------------------------------------------
ROOM_ROWS = [
    ["1", "Intro to AppSec", "Foundations", "Source-and-sink mental model; the golden rule"],
    ["2", "Broken Access Control", "Foundations", "The #1 OWASP risk; IDOR; server-side checks"],
    ["3", "SQL Injection", "Web Exploits", "UNION/boolean injection; parameterized queries"],
    ["4", "Command Injection", "Web Exploits", "Shell metacharacters; avoid shell=True"],
    ["5", "Cross-Site Scripting", "Web Exploits", "Reflected/stored XSS; output encoding; CSP"],
    ["6", "SSRF", "Web Exploits", "Server-side request forgery; cloud metadata"],
    ["7", "Broken Authentication", "Web Exploits", "Sessions, JWT alg=none, token forging"],
    ["8", "Crypto Failures", "Web Exploits", "Weak hashing, secrets, transport security"],
    ["9", "Security Misconfiguration", "Web Exploits", "Headers, defaults, verbose errors"],
    ["10", "Insecure Deserialization", "Web Exploits", "pickle/yaml RCE; safe parsing"],
    ["11", "API Security", "AppSec", "BOLA/BFLA; OWASP API Top 10"],
    ["12", "AI / LLM Security", "AppSec", "Prompt injection; OWASP LLM Top 10"],
    ["13", "Threat Modeling", "AppSec", "STRIDE; data-flow diagrams"],
    ["14", "Secure Code Review", "AppSec", "Spotting vulnerable patterns by hand"],
    ["15", "SAST", "DevSecOps", "Static analysis with Bandit / Semgrep"],
    ["16", "DAST", "DevSecOps", "Dynamic scanning of a running app"],
    ["17", "Dependency Scanning (SCA)", "DevSecOps", "pip-audit; known-CVE components"],
    ["18", "Secret Scanning", "DevSecOps", "gitleaks; committed-credential detection"],
    ["19", "CI/CD Pipeline Security", "DevSecOps", "Build-time gates; failing on findings"],
    ["20", "IaC Security", "DevSecOps", "Checkov on Terraform; misconfig rules"],
    ["21", "Container Security", "DevSecOps", "Non-root, image hygiene"],
    ["22", "Kubernetes Security", "DevSecOps", "securityContext; privileged pods"],
    ["23", "Supply Chain Security", "DevSecOps", "SBOM; provenance; dependency risk"],
]

CONTENT = [
    ("h1", "0. What you are holding"),
    ("p", "examto is a free, self-service security lab that lives in your GitHub "
          "repository. It looks and works like TryHackMe / Hackversity: theory on "
          "the left, a lab and a live terminal on the right. You read, you try, you "
          "capture a flag or answer, you move on. This guide takes you from a cold "
          "start to finishing all 23 rooms without needing to ask anyone anything."),
    ("callout", "The one rule to remember",
     "You never pay for anything and you never wait for anyone. If a step asks you "
     "to buy a VM or sign up for a paid tier, you are off the path - come back here."),

    ("h1", "1. One-time setup (about 3 minutes)"),
    ("p", "You only do this once. It runs in your browser - nothing is installed on "
          "your own computer."),
    ("steps", [
        "Open your repo: github.com/kingkish269-ship-it/examto",
        "Click the green 'Code' button, choose the 'Codespaces' tab, then "
        "'Create codespace on main'.",
        "Wait for it to build. The .devcontainer in the repo auto-installs Python "
        "and the lab dependencies the first time.",
        "When the editor loads, you have a full Linux machine in your browser. "
        "This Codespace IS the lab machine you will attack and scan.",
    ]),
    ("callout", "Free hours",
     "GitHub gives personal accounts a monthly pool of free Codespaces hours. It is "
     "plenty for this course if you STOP the Codespace when you finish each session "
     "(see section 9). You will not be charged on the free tier."),

    ("h1", "2. Start the web lab"),
    ("p", "Every time you come back, open the Codespace again (github.com -> your "
          "repo -> Code -> Codespaces -> click the existing one). Then in the "
          "terminal at the bottom of the editor, pull the latest content and start "
          "the lab with a single command:"),
    ("code", [
        "git pull",
        "bash webapp/start.sh",
    ]),
    ("p", "start.sh installs the small web dependencies (flask, flask-sock) if they "
          "are missing and then launches the server. You will see a message that it "
          "is running on port 5000."),
    ("steps", [
        "A 'port forwarded' popup appears in the bottom-right. Click 'Open in "
        "Browser'. If you miss it, open the 'Ports' tab and click the globe icon "
        "next to port 5000.",
        "The lab opens in a new browser tab: room list on the left, room content in "
        "the middle, and a live terminal on the right.",
        "The terminal connects automatically. You do not need to press Ctrl+` or do "
        "anything in VS Code - the terminal in the page is the one you use.",
    ]),
    ("callout", "If the terminal says '[terminal closed]'",
     "That only happens when flask-sock did not install. Stop the server (Ctrl+C in "
     "the editor terminal) and re-run 'bash webapp/start.sh' - it installs the "
     "backend and the terminal then connects on its own."),

    ("h1", "3. How a room works (the 6 sections)"),
    ("p", "Every room has the same six sections. Work them top to bottom. The left "
          "pane shows the content; use the terminal on the right to actually do the "
          "work."),
    ("table",
     ["Section", "What you do"],
     [
        ["1. Brief", "A two-line 'why this matters'. Sets the scene."],
        ["2. Theory", "The concept explained plainly, with the vulnerable pattern "
                      "and the fix. This is the part you study."],
        ["3. Worked example", "A fully worked command/response so you see exactly "
                              "what 'good' looks like before you try."],
        ["4. Knowledge check", "Multiple-choice / short answers. You must get them "
                               "right to mark the section done. Instant grading."],
        ["5. Investigation", "Hands-on steps in the terminal: start the lab app, "
                             "send requests, read output. Hints provided."],
        ["6. Capture", "Enter the flag or the one-word answer you derived. Graded "
                       "against a hash - the answer is never stored in plaintext."],
     ],
     [26, 74]),
    ("p", "A room counts as complete when all six sections are marked done. Your "
          "progress is saved locally in the Codespace so you can resume."),
    ("callout", "Finish the whole room, not one command",
     "The Investigation section lists several steps for a reason. Run all of them. "
     "The Capture answer usually only makes sense after you have actually done the "
     "investigation, not after a single curl."),

    ("h1", "4. The full room order"),
    ("p", "Do them in this order. Each track builds on the one before it. Rooms 1-2 "
          "give you the mindset, 3-10 are the classic web exploits you must be able "
          "to demonstrate, 11-14 are application-security practice, and 15-23 are "
          "the DevSecOps tooling that gets you hired for pipeline and platform "
          "security roles."),
    ("table",
     ["#", "Room", "Track", "Core idea"],
     ROOM_ROWS,
     [6, 34, 20, 52]),

    ("h1", "5. The Python track (do this in parallel)"),
    ("p", "You told me Python is your weak spot. There is a separate, self-contained "
          "track that teaches exactly the Python an AppSec engineer needs, and tests "
          "you after each lesson. It does not need the web lab - run it straight in "
          "the Codespace terminal."),
    ("code", [
        "cd /workspaces/examto/learn-python",
        "cat README.md          # the plan and lesson list",
        "python3 check.py       # runs the tests for each lesson you have done",
    ]),
    ("bullet", [
        "14 lessons from variables up to calling HTTP APIs, including a lesson on "
        "the Microsoft Graph / Intune style API calls that match your background.",
        "Each lesson has an exercise file you edit; check.py grades it and tells you "
        "what is still failing.",
        "Aim for one lesson per day alongside one or two rooms. By the time you "
        "reach the SAST/review rooms the Python will feel natural.",
    ]),

    ("h1", "6. Using the real free tools"),
    ("p", "The rooms teach the logic with small offline stand-ins so they always run "
          "with zero setup. When you want to run the REAL industry tools against the "
          "lab code (the exact tools you will use on the job), use the tools-lab."),
    ("code", [
        "cd /workspaces/examto/tools-lab",
        "cat README.md          # what each tool is and when to use it",
        "bash install.sh        # installs the real tools into a local venv",
        "bash run_real_tools.sh # runs them all against the lab app and prints "
        "findings",
    ]),
    ("table",
     ["Tool", "Type", "What it catches in this repo"],
     [
        ["Bandit", "SAST (Python)", "pickle, subprocess shell=True, md5, raw SQL, urlopen"],
        ["Semgrep", "SAST (rules)", "Multiple injection and crypto patterns"],
        ["pip-audit", "SCA", "Known CVEs in the pinned dependencies"],
        ["Checkov", "IaC", "Terraform misconfigurations (public DB, open SG, etc.)"],
        ["sqlmap", "DAST", "Confirms the SQL injection in the lab app"],
        ["gitleaks", "Secrets", "Committed credentials / tokens"],
     ],
     [20, 22, 58]),
    ("callout", "Note on Semgrep in a fresh Codespace",
     "Semgrep needs a writable home for its settings. If it complains, run "
     "'export SEMGREP_SETTINGS_FILE=$PWD/.semgrep.yml' first. The run_real_tools.sh "
     "script already handles this for you."),

    ("h1", "7. A suggested weekly rhythm"),
    ("p", "You do not have to rush. A sustainable pace that finishes everything in "
          "about 4-5 weeks:"),
    ("table",
     ["Week", "Rooms", "Python", "Tools"],
     [
        ["1", "1-2 (foundations) + 3-5", "Lessons 1-4", "Bandit intro"],
        ["2", "6-10 (rest of web exploits)", "Lessons 5-8", "sqlmap, Semgrep"],
        ["3", "11-14 (AppSec)", "Lessons 9-11", "Code review with Bandit"],
        ["4", "15-19 (SAST/DAST/SCA/secrets/CICD)", "Lessons 12-14", "pip-audit, gitleaks"],
        ["5", "20-23 (IaC, containers, k8s, supply chain)", "Review", "Checkov"],
     ],
     [10, 46, 22, 22]),

    ("h1", "8. Prove it (build your evidence as you go)"),
    ("p", "Hiring managers for 70+ LPA remote AppSec/DevSecOps roles want proof, not "
          "a certificate list. As you finish rooms, capture evidence:"),
    ("bullet", [
        "Keep a short notes file per room: the vuln, how you exploited it, the fix. "
        "This becomes your talking points in interviews.",
        "Screenshot real tool output (Bandit/Checkov/sqlmap findings) - that is "
        "portfolio material.",
        "Push a 'writeups' folder to this same repo. A public repo of security "
        "writeups is a strong signal.",
        "Map each room to the job description language: 'Broken Access Control', "
        "'SAST in CI', 'IaC scanning', 'SBOM' are phrases recruiters search for.",
    ]),

    ("h1", "9. Stop the Codespace when you are done (saves your free hours)"),
    ("p", "This is the one piece of housekeeping that keeps everything free. "
          "Codespaces bill by the hour they are RUNNING, so stop it at the end of "
          "each session."),
    ("steps", [
        "In the Codespace editor, press F1 (or Ctrl+Shift+P) to open the command "
        "palette.",
        "Type 'Codespaces: Stop Current Codespace' and press Enter.",
        "Or, from github.com/codespaces, click the '...' next to your codespace and "
        "choose 'Stop codespace'.",
    ]),
    ("callout", "Stopping is not deleting",
     "Stopping keeps all your files and progress; it just powers the machine down so "
     "the clock stops. Next session you re-open it and pick up where you left off. "
     "Only use 'Delete' when you are completely finished with the course."),

    ("h1", "10. Quick command reference"),
    ("p", "The handful of commands you will actually use, in one place:"),
    ("code", [
        "# start / resume the web lab",
        "git pull && bash webapp/start.sh      # then open port 5000",
        "",
        "# python track",
        "cd learn-python && python3 check.py",
        "",
        "# real security tools against the lab",
        "cd tools-lab && bash install.sh && bash run_real_tools.sh",
        "",
        "# stop a stuck server",
        "Ctrl+C in the editor terminal",
        "",
        "# stop the codespace (saves hours):  F1 -> Codespaces: Stop",
    ]),
    ("h1", "11. Job-readiness checklist"),
    ("p", "You are ready to apply confidently when you can tick all of these:"),
    ("bullet", [
        "[ ] Finished all 23 rooms (every section, every capture).",
        "[ ] Finished the learn-python track - check.py passes all lessons.",
        "[ ] Ran every real tool in tools-lab and can explain each finding.",
        "[ ] Can explain Broken Access Control, SQLi, XSS, SSRF and the fix for each "
            "from memory.",
        "[ ] Can describe a DevSecOps pipeline: SAST + SCA + secret scan + IaC scan "
            "with a gate that fails the build.",
        "[ ] Have a public writeups repo and 3-4 screenshots of real tool output.",
        "[ ] Can tie your existing SC-100 / AWS Security / Zscaler ZTCA background to "
            "application and pipeline security in one sentence.",
    ]),
    ("callout", "Your edge",
     "Most AppSec candidates come from dev and are weak on cloud/network/endpoint. "
     "You are the opposite, and you now have the application + pipeline skills to "
     "match. That combination is exactly what platform-security and DevSecOps teams "
     "struggle to hire. Finish the rooms, show the evidence, and lean on it."),
]


def build():
    pdf = new_pdf()
    cover(pdf)
    pdf.add_page()
    for block in CONTENT:
        kind = block[0]
        RENDER[kind](pdf, *block[1:])
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "COMPLETE_GUIDE.pdf")
    pdf.output(out)
    print("wrote", out)


if __name__ == "__main__":
    build()
