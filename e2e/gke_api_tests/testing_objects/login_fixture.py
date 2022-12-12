import pytest
from setup import user_login


@pytest.fixture(scope="module", autouse=True)
def user_login_fixture():
  user_login()