# Module 2 - Lesson 5: Dictionaries and .get
# Read lessons/05_dicts.md. Replace BLANK. Then: python3 check.py 5
def get_severity(finding):
    # finding like {"id": "F1", "severity": "HIGH"}
    # return severity, or "UNKNOWN" if the key is missing
    return finding.get("severity", BLANK)  # BLANK -> "UNKNOWN"
