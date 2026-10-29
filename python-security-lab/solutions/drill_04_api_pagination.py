"""Reference solution for Drill 4."""

from collections.abc import Callable


def collect_all_items(fetch_page: Callable[[str | None], dict]) -> list[dict]:
    items = []
    token = None
    seen_tokens = set()

    while True:
        page = fetch_page(token)
        items.extend(page.get("items", []))
        token = page.get("next_token")

        if not token:
            return items
        if token in seen_tokens:
            raise ValueError(f"Repeated pagination token: {token}")
        seen_tokens.add(token)
