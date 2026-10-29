import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vulnerable_app import create_app  # noqa: E402


@pytest.fixture
def insecure():
    app = create_app(secure=False)
    app.testing = True
    return app.test_client(), app


@pytest.fixture
def secure():
    app = create_app(secure=True)
    app.testing = True
    return app.test_client(), app
