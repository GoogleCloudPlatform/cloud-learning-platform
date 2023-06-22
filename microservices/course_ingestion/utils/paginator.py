"""Custom Paginator"""


def pagination(payload: list, skip: int,
               limit: int) -> list:
  """
  Function can be used to pagination for API's
  :param skip: int
  :param limit: int
  :param payload: List
  :return: List
  """

  res = payload[skip:limit]
  return res
