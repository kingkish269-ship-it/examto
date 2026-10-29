"""Drill 2: safely read nested security data."""


def get_nested(data: dict, path: list[str], default=None):
    """Return a nested dictionary value or *default* when unavailable."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def resource_label(finding: dict) -> str:
    """Return 'type:name', using 'unknown' for missing values."""
    resource_type = get_nested(finding, ["resource", "type"], "unknown")
    resource_name = get_nested(finding, ["resource", "name"], "unknown")
    return f"{resource_type}:{resource_name}"
