"""
Functions for unified Sorting Logic
"""

def get_sorted_list(collection_manager,
                    sort_by="created_time",
                    sort_order="ascending"):
  """
    This function returns a sorted list from the firestore
    collection manager.
    --------------------------------------------------------
        Input:
            collection_manager: return value firestore collection.filter()
            sort_by `str`: key to sort the documents by
            sort_order `str`: if sort_order is ascending then data will be
                            in ascending order, descending otherwise.
        Output:
            sorted_list `list`: list of firestore documents in dict
  """
  collection_contents = collection_manager.fetch()
  collection_contents = [
      i.get_fields(reformat_datetime=True)
      for i in collection_contents
      if hasattr(i, sort_by)
  ]

  reverse = False
  if sort_order != "ascending":
    reverse = True

  return sorted(collection_contents,
                key=lambda document:document.get(sort_by),
                reverse=reverse)
