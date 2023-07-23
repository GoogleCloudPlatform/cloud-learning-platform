"""
student learner profile integration service
"""
from common.models import Session
from common.utils.http_exceptions import InternalServerError

def create_session(user_id: str = None):
  """ Create a new session"""
  try:
    new_session = Session()
    data = {"user_id": user_id}
    new_session = new_session.from_dict(data)
    new_session.user_id = user_id
    new_session.session_id = ""
    new_session.save()
    new_session.session_id = new_session.id
    new_session.update()

    return new_session.get_fields(reformat_datetime=True)
  except Exception as e:
    raise InternalServerError(str(e)) from e
