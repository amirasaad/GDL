import pytest

from gdrive.users.models import User
from gdrive.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


def pytest_generate_tests(metafunc):
    # called once per each test function
    if hasattr(metafunc.cls, "params"):
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
        argnames = sorted(funcarglist[0])
        metafunc.parametrize(
            argnames,
            [[funcargs[name] for name in argnames] for funcargs in funcarglist],
        )
