import json
from pathlib import Path

import pytest

from tenji.mfc_response import MFCResponse

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> str:
    """Returns the raw contents of a fixture file."""
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


@pytest.fixture
def fixture_text():
    return read_fixture


@pytest.fixture
def mfc_response():
    """Builds an MFCResponse from a fixture file."""

    def _build(name: str) -> MFCResponse:
        return MFCResponse(read_fixture(name))

    return _build


@pytest.fixture
def mfc_window_response():
    """Wraps a fixture in the JSON envelope MFC uses for modal windows."""

    def _build(name: str) -> MFCResponse:
        body = json.dumps({"htmlValues": {"WINDOW": read_fixture(name)}})
        return MFCResponse(body)

    return _build
