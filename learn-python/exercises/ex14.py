# Module 5 - Lesson 14: Apply tags in Intune via Microsoft Graph
# This is a real interview-style task. Read lessons/14_intune_graph.md.
# Replace BLANK, then run:  python3 check.py 14
#
# The functions take a `session` (a requests.Session in real life). That lets
# you test them offline with a fake session — and it is good design.

def get_token(tenant, client_id, client_secret, session):
    # Get an app-only (client credentials) token for Microsoft Graph.
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    response = session.post(url, data=data)
    # The JSON response has an "access_token" field. Return it.
    return response.json()[BLANK]        # BLANK -> "access_token"


def apply_scope_tag(config_id, tag_ids, token, session):
    # Apply Intune scope tags to a device configuration via Microsoft Graph.
    # (Read this one — you don't change it. This is the pattern you'd reuse.)
    url = f"https://graph.microsoft.com/v1.0/deviceManagement/deviceConfigurations/{config_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"roleScopeTagIds": tag_ids}
    return session.patch(url, headers=headers, json=body)
