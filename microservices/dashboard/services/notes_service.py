"""Inactivate the notes for deleted session"""

import requests

from config import SERVICES

# pylint: disable= consider-using-f-string,missing-timeout
def is_archived_the_session_notes(session_id: str, user_id: str):
  """
  Inactivate the notes for deleted sessions
  Parameters
  ----------
  session_id: str
  token: str
  user_id: str

  Returns
  -------
  json
  """
  url = "http://{}:{}/notes/api/v1/is_archived?session_id={}&user_id={}".format(
    SERVICES["notes"]["host"], SERVICES["notes"]["port"], session_id, user_id)
  res = requests.get(url=url)

  return res.status_code
