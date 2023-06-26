"""
Generic function for Sorting is implemented
"""


def collection_sorting(collection_manager: any, sort_by: str,
                       sort_order: str, skip: int, limit: int) -> any:
  """
  Generic Function for Firestore Collection Sorting Logic
  :collection_manager: Object
  :sort_by: string
  :sort_order: const(ascending, descending)
  :return: Firestore Object
  """

  return collection_manager.order(f"{sort_by}").offset(
    skip).fetch(limit) if sort_order == "ascending" else \
    collection_manager.order(f"-{sort_by}").offset(skip).fetch(limit)
