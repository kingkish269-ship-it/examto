"""Guardrails for an LLM application (input, output, secrets, tool access).

These are the defensive controls for the OWASP Top 10 for LLM Applications.
Pure standard library; no model or API key required. The mock "model" lives in
assistant.py and deliberately obeys injected instructions so you can see the
guardrails do (or not do) their job.
"""

from __future__ import annotations

import html
import re

# Signals of a prompt-injection / jailbreak attempt. Real systems add a model-
# based classifier, but pattern matching catches the common, cheap attacks and
# is enough to learn the control.
INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior|above) instructions",
    r"disregard (the )?(previous|above|system)",
    r"forget (your|the) (instructions|rules)",
    r"you are now",
    r"act as",
    r"reveal (your|the) (system prompt|instructions|api key|secret)",
    r"print (your|the) (system prompt|instructions)",
    r"do anything now",
    r"\bDAN\b",
    r"developer mode",
    r"override (the )?(rules|policy|safety)",
]


def detect_injection(text: str) -> list[str]:
    """Return the injection patterns found in *text* (empty list = clean)."""
    found = []
    for pat in INJECTION_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            found.append(pat)
    return found


def redact_secrets(text: str, secrets: list[str]) -> str:
    """Replace any known secret that leaked into output with [REDACTED]."""
    out = text
    for secret in secrets:
        if secret:
            out = out.replace(secret, "[REDACTED]")
    return out


def sanitize_output(text: str) -> str:
    """Encode LLM output before it is placed into HTML (insecure output
    handling is OWASP LLM02). Treat model output as untrusted."""
    return html.escape(text)


# Destructive tools require elevated authorization. Giving an LLM unchecked
# tool access is OWASP LLM08 (Excessive Agency).
TOOL_POLICY = {
    "search": {"roles": {"user", "admin"}},
    "send_email": {"roles": {"admin"}},
    "delete_account": {"roles": {"admin"}},
}


def authorize_tool(tool: str, role: str) -> bool:
    """Return True only if *role* is permitted to invoke *tool*."""
    policy = TOOL_POLICY.get(tool)
    if policy is None:
        return False  # unknown tool: deny by default
    return role in policy["roles"]
