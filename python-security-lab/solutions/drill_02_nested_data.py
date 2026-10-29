"""Reference solution for Drill 2."""


def get_nested(data: dict, path: list[str], default=None):
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def resource_label(finding: dict) -> str:
    resource_type = get_nested(finding, ["resource", "type"], "unknown")
    resource_name = get_nested(finding, ["resource", "name"], "unknown")
    return f"{resource_type}:{resource_name}"
