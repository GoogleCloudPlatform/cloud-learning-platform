"""
Unit Tests for user ORM object
"""

from common.models import User
from common.testing.example_objects import TEST_USER


def test_new_user():
  # a placeholder unit test so github actions runs until we add more
  user = User.from_dict(TEST_USER)

  assert user.auth_id == TEST_USER["auth_id"]

def test_find_by_uuid():
  pass
