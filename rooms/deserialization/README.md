# Room: Insecure Deserialization (OWASP A08)

**Topic:** OWASP Top 10 · **Difficulty:** advanced

## Story
Turning attacker-controlled bytes back into objects can run their code.

## Theory (2 min)
`pickle.loads()` on untrusted data executes code during deserialization —
remote code execution, the worst outcome. Same risk: unsafe `yaml.load`, Java
native serialization. Fix: **never deserialize untrusted data with pickle/yaml**;
use a data-only format (JSON). If you must, sign the data and verify before
parsing, and restrict allowed types.

## What you'll do
Read `appsec-lab/exercises/07_insecure_deserialization.md`; see a pickle payload
run code, then the JSON-based fix.

## Going further
`appsec-lab/` deserialization lab with an RCE proof test.
