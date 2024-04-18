import sys
import pytest


from pathlib import Path, WindowsPath

from api_tests.settings.config import AppEnvSettings

path = Path(__file__)
if sys.platform == "win32":
    path = WindowsPath(__file__)
INCLUDE_TESTS_IN_PYTHONPATH = path.parent / "tests"
INCLUDE_VERIFICATIONS_IN_PYTHONPATH = path.parent / "verifications"
try:
    sys.path.index(INCLUDE_TESTS_IN_PYTHONPATH.as_posix())
    sys.path.index(INCLUDE_VERIFICATIONS_IN_PYTHONPATH.as_posix())
except ValueError:
    sys.path.append(INCLUDE_TESTS_IN_PYTHONPATH.as_posix())
    sys.path.append(INCLUDE_VERIFICATIONS_IN_PYTHONPATH.as_posix())


def pytest_addoption(parser):
    """
    Parse cli command to get any other base url in case that we want to run the api
    tests against other test environments such as review apps
    :param parser:
    :return:
    """
    parser.addoption(
        "--env",
        action="store",
        default="staging",
        help="Choose environment to perform the test: staging, review_app_url",
    )


@pytest.fixture(scope="session", autouse=True)
def app_env_settings(request):
    env = request.config.getoption("--env").lower()
    app_env_settings = AppEnvSettings(env)
    return app_env_settings