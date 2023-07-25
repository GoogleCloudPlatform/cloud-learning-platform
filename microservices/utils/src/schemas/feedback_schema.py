"""Pydantic Model for Feedback API"""
from pydantic import BaseModel

class FeedbackRequestModel(BaseModel):
  """Request Model"""
  user_comments: str
  course_feedback_option: str
  notes_feedback_option: str
  usage_feedback_option: str
  question_ref: str
  user_rating: str
  session_id: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "user_comments": "example",
            "course_feedback_option": "1",
            "notes_feedback_option": "example",
            "usage_feedback_option": "REpVDthThwQlxb",
            "question_ref": "REpVDthThwQlxb",
            "user_rating": "REpVDthTh",
            "session_id": "XTT8g9krGE5ojJrWYQYa"
        }
    }

class InlineFeedbackRequestModel(BaseModel):
  """Request Model"""
  context_ref: str
  covered_lus: list
  user_rating: str
  session_id: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "context_ref": "qwertyuiop23yjwfghe",
            "covered_lus": ["Define applied sociology"],
            "user_rating": "4",
            "session_id": "c05f9449-0e39-4dd3-8e7f-b859eb2b86e8"
        }
    }
