# Room: Web & API Fundamentals

**Topic:** AppSec foundations · **Difficulty:** beginner

## Story
Before you can secure an app, you must know how it talks. Every attack rides on
an HTTP request.

## Theory (3 min)
A request has a **method** (GET/POST/PUT/DELETE), a **path**, **headers**
(including cookies and `Authorization`), and a **body**. The server reads these
**inputs** and may pass them to a **sink** (DB, file, shell, HTML). Responses
carry a **status code** (200 ok, 401 unauth, 403 forbidden, 500 error) and
headers. APIs are the same, usually exchanging **JSON** and using a **bearer
token** for auth.

Key terms: **source** = where untrusted input enters; **sink** = the dangerous
operation it reaches. Security lives in between.

## What you'll do
Read this, then in the terminal: `curl -s -D - https://example.com -o /dev/null`
and look at the method, status, and headers.

## Going further
`appsec-lab/exercises/00_how_web_apps_work.md`.
