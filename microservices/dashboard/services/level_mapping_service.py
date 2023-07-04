"""Utility method for getting level based on context type"""
from config import LEVEL_MAPPING


def get_level_mapping(context_type):
  """
        Returns level of context_type based on
        a predefined mapping from config
        Args:
            context_type: String
        Returns:
            level: String
    """
  if context_type in LEVEL_MAPPING:
    return LEVEL_MAPPING[context_type]
  return "level0"
