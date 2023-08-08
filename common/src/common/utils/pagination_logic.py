"""
Functions for unified Pagination Logic
"""

def get_slice(sorted_list, skip, limit):
  """
    This function provides custom pagination logic
    --------------------------------------------------------
        Input:
            sorted_list `list`: python list
            skip `int`: offset value
            limit `int`: step value
  """
  return sorted_list[skip * limit:skip * limit + limit]
