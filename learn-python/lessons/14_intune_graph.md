# Module 5 · Lesson 14 — Apply Intune tags via Microsoft Graph

This is a **real interview task**: "write Python that applies tags to devices in
Intune using the API." Here is exactly how it works, and you build it.

## The big picture

Microsoft Intune is managed through the **Microsoft Graph API**. Two steps:

1. **Get a token** (app-only, "client credentials"): your script authenticates
   as an Azure AD app registration and receives a bearer token.
2. **Call Graph** with that token to read or change things — here, apply
   **scope tags** (`roleScopeTagIds`) to a device configuration.

"Tags" in Intune usually means one of:
- **Scope tags** (`roleScopeTagIds`) — RBAC tags on configs/policies/devices
  (what this lesson does),
- **Device category** — a category assigned to a device,
- Azure AD device **extension attributes**.

## Step 1 — get a token

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
body (form): client_id, client_secret,
             scope=https://graph.microsoft.com/.default,
             grant_type=client_credentials
```
The JSON response contains `access_token`. In code:

```python
response = session.post(url, data=data)
token = response.json()["access_token"]
```

## Step 2 — apply the scope tag

```
PATCH https://graph.microsoft.com/v1.0/deviceManagement/deviceConfigurations/{id}
headers: Authorization: Bearer <token>, Content-Type: application/json
body:    {"roleScopeTagIds": ["2"]}
```
In code:

```python
session.patch(url, headers={"Authorization": f"Bearer {token}", ...},
              json={"roleScopeTagIds": tag_ids})
```

## Your task

Open `exercises/ex14.py`. `get_token` is almost done — replace `BLANK` with
`"access_token"` so it returns the token from the JSON response. Read
`apply_scope_tag` carefully; that is the pattern you will reuse for any Graph
call.

## Test (offline — no tenant needed)

```bash
python3 check.py 14
```
The test uses a **fake session** so it runs with no real Azure account. That is
also how you unit-test API code at work: inject a fake HTTP client.

## Running it for real (reference)

1. In Entra ID, create an **App registration**; add a **client secret**.
2. Give it **application** Graph permission
   `DeviceManagementConfiguration.ReadWrite.All` and grant admin consent.
3. `pip install requests`, then pass a real `requests.Session()`:
   ```python
   import requests
   s = requests.Session()
   token = get_token(TENANT, CLIENT_ID, CLIENT_SECRET, s)
   apply_scope_tag("<config-id>", ["2"], token, s)
   ```
Keep the client secret in an environment variable, never in code.

## The other "some tasks" interviewers ask

Same token, different Graph calls — all follow this exact pattern:
- **List managed devices:** `GET /deviceManagement/managedDevices`
- **Set a device category:** `PATCH /deviceManagement/managedDevices/{id}`
  with `{"deviceCategoryDisplayName": "Finance"}`
- **List configurations:** `GET /deviceManagement/deviceConfigurations`
- **Create a scope tag:** `POST /deviceManagement/roleScopeTags`

Learn the pattern once (token → request → parse JSON) and you can do any of them.
That pattern is Tiers 2–3 of `../PYTHON_FOR_YOUR_DOMAIN.md`.
