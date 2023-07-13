"""
    utility methods to execute unit tests for module level_mapping_service.py
"""
#pylint: disable=wrong-import-position
import pytest
import sys
sys.path.append("../../common/src")
from services.level_mapping_service import get_level_mapping
from config import LEVEL_MAPPING


@pytest.mark.parametrize("key", list(LEVEL_MAPPING.keys()))
def test_get_level_mapping(key):
  assert get_level_mapping(key) == LEVEL_MAPPING[key]


def test_get_level_mapping_invalid_context_type():
  assert get_level_mapping("_course") == "level0"
  assert get_level_mapping("COURSE") == "level0"
  assert get_level_mapping("CoUrSe") == "level0"
