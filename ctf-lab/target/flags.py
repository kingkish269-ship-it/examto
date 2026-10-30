"""Flag definitions for the CTF target (no third-party imports).

Kept separate from the Flask app so the answer-key generator and tests can
import the flags without requiring Flask.
"""

FLAGS = {
    "idor": "FLAG{idor_broke_object_level_authz}",
    "sqli": "FLAG{union_select_all_the_things}",
    "traversal": "FLAG{dot_dot_slash_escapes_webroot}",
    "xss": "FLAG{reflected_script_hit_the_admin_bot}",
    "session": "FLAG{forged_token_means_broken_auth}",
    "ssrf": "FLAG{ssrf_reached_the_metadata_service}",
    "cmdi": "FLAG{semicolon_started_a_second_command}",
    "jwt": "FLAG{alg_none_is_not_a_signature}",
}

INTERNAL_METADATA = {
    "/latest/meta-data/iam/security-credentials/role": FLAGS["ssrf"],
}
