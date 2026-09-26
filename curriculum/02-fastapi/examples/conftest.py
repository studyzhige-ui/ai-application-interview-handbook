"""The normal run requires the documented target; compatibility runs are explicit."""
from importlib.metadata import version
import pytest


def pytest_addoption(parser):
    parser.addoption("--allow-compat", action="store_true", default=False,
                     help="Run compatible examples on a non-target version; skip version-specific tests explicitly.")


def pytest_sessionstart(session):
    installed = version("fastapi")
    if installed != "0.141.1" and not session.config.getoption("--allow-compat"):
        raise pytest.UsageError(
            f"Course target is FastAPI 0.141.1; installed={installed}. "
            "Install requirements.txt, or use --allow-compat for a LIMITED compatibility check."
        )
