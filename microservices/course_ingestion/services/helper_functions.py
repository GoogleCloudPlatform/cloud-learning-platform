"""Caching topic tree"""
from common.utils.cache_service import set_key, get_key

#pylint: disable=redefined-builtin
def cache_topic_tree(topic_tree, id):
  """Parse fireo object so that is can be json serializable"""
  set_key(id, topic_tree)

def get_tree_from_cache(level, id):
  """Returns topic tree if present in cache else None"""
  if level != "course":
    return None
  cached_output = get_key(id)
  if cached_output:
    return cached_output
  return None

