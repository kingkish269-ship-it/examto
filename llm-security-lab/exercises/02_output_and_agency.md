# 02 — Output handling and excessive agency (LLM02, LLM08)

## Insecure output handling (LLM02)

An attacker plants `<script>…</script>` in a product review. The app retrieves
that review, the model echoes it, and the app renders it in a page — stored XSS,
delivered through the model.

```bash
python3 -c "import assistant as a; print(a.respond('summarize this review', secure=False, retrieved=a.POISONED_DOC)['text'])"
```

Insecure mode returns the raw `<script>`. Secure mode encodes it to
`&lt;script&gt;`. **Treat model output as untrusted input to the next system.**

## Excessive agency (LLM08)

The model can call tools (`search`, `send_email`, `delete_account`). If the app
executes whatever the model decides, injected text can trigger destructive
actions.

```bash
python3 -c "import assistant as a; print(a.respond('delete my account now', secure=False, role='user')['tool_executed'])"
```

Insecure mode executes `delete_account` for a normal user. Secure mode enforces
`guard.authorize_tool`: destructive tools require an admin role.

## Control

- Encode/validate model output for the sink it flows into (HTML, SQL, shell).
- Give the model/agent the least privilege: scope tools, require authorization
  for destructive ones, and keep a human in the loop for high-impact actions.

## Extend it

Add a `transfer_funds` tool to `TOOL_POLICY` restricted to admins, and a test
proving a user role is denied.
