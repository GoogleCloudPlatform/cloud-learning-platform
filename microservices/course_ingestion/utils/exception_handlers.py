"""
This Script is using for handle user defined Exception for LearningContent
"""


class LearningContentNotFound(Exception):
  """
  Exception for LearningContentNotFound
  Parameter
  --------
  err: str
  Return
  ------
  String
  """

  def __init__(self, err, *args) -> None:
    super().__init__(args)
    self.err = err

  def __str__(self) -> str:
    return f"{self.err}"


class LearningContentIDMissing(Exception):
  """
  Exception for LearningContentIDNotFound
  Parameter
  --------
  err: str
  Return
  ------
  String
  """

  def __init__(self, err, *args) -> None:
    super().__init__(args)
    self.err = err

  def __str__(self) -> str:
    return f"{self.err}"
