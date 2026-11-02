"""Playwright artifacts: screenshots, video and traces, with environment guardrails."""
import os
from pathlib import Path
import pytest

ENVIRONMENT = os.environ.get("TEST_ENV", "local").lower()
ALLOWED = {"local", "ci", "staging", "production"}
if ENVIRONMENT not in ALLOWED:
    raise RuntimeError(f"Unknown TEST_ENV: {ENVIRONMENT}")

@pytest.fixture(scope="session")
def base_url():
    url = os.environ.get("BASE_URL", "http://127.0.0.1:5173")
    if ENVIRONMENT == "production" and not url.startswith("https://"):
        raise RuntimeError("Production BASE_URL must use HTTPS")
    return url.rstrip("/")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1440, "height": 900}, "record_video_dir": "artifacts/videos"}

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "headless": True}

@pytest.fixture(autouse=True)
def forbid_mutating_production_tests(request):
    if ENVIRONMENT == "production" and not request.node.get_closest_marker("smoke"):
        pytest.skip("Production is read-only: run only smoke tests")
