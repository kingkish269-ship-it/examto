"""Load starter drills or reference solutions based on USE_SOLUTIONS."""

import importlib
import os


def load_drill(name: str):
    package = "solutions" if os.getenv("USE_SOLUTIONS") == "1" else "drills"
    return importlib.import_module(f"{package}.{name}")
