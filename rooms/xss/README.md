# Room: Cross-Site Scripting (XSS, OWASP A03)

**Topic:** OWASP Top 10 · **Difficulty:** core

## Story
Your input is echoed into a page and runs as code in a victim's browser.

## Theory (2 min)
**Reflected XSS:** the app puts your input into HTML without encoding, so
`<script>...</script>` executes. Impact: steal session tokens, act as the
victim. The fix is **contextual output encoding** (HTML-encode data before it
hits the page) plus a strong **Content-Security-Policy** as a second layer.

## What you'll do
Read `appsec-lab/exercises/03_xss.md`, start the app, and attack `/greet` with a
`<script>` payload; watch it reflected. The DAST room does this hands-on.

## Going further
`appsec-lab/` (fix = `markupsafe.escape`) and the `dast` room.
