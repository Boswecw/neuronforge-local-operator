import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "experiment_memory"
RECORDS_DIR = FIXTURES / "records"
INVALID_DIR = FIXTURES / "invalid"
GOLDEN_DIR = FIXTURES / "golden"


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def records_dir():
    return RECORDS_DIR


@pytest.fixture(scope="session")
def invalid_dir():
    return INVALID_DIR


@pytest.fixture(scope="session")
def golden_dir():
    return GOLDEN_DIR
