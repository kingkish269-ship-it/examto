"""Reference solution for Drill 6."""

import time
from collections.abc import Callable

RETRYABLE_ERRORS = (TimeoutError, ConnectionError)


def call_with_retry(
    operation: Callable[[], object],
    max_attempts: int = 3,
    sleep_fn: Callable[[float], None] = time.sleep,
):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except RETRYABLE_ERRORS:
            if attempt == max_attempts:
                raise
            sleep_fn(2 ** (attempt - 1))

    raise RuntimeError("Retry loop ended unexpectedly")
