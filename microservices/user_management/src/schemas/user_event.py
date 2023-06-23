"""
Pydantic Model for UserEvent API's
"""
from typing import Optional, List
from pydantic import BaseModel, Extra


class UserEventModel(BaseModel):
  """User Pydantic Model"""
  session_ref: Optional[str]
  raw_response: Optional[dict]
  feedback: Optional[dict]
  learning_item_id: str
  activity_type: str
  learning_unit: str
  course_id: str
  flow_type: str
  hint: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "session_ref": "fjdsalfjaslf",
            "raw_response": {
                "first_attempt": "microanalytic theory"
            },
            "feedback": {
                "first_attempt": {
                    "feedback_text": "can be improved",
                    "evaluation_score": 0.4,
                    "evaluation_flag": "incorrect"
                }
            },
            "learning_item_id": "dfkjasfals",
            "activity_type": "choose_the_fact",
            "learning_unit": "sjfdjfalfd39",
            "course_id": "fjkadsfalsdfa",
            "flow_type": "Let AITutor Guide Me"
        }
    }


class UserEventWithParent(UserEventModel):
  user_id: Optional[str]
  id: str


class UserEventModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created User Event"
  data: UserEventWithParent

  class Config():
    orm_mode = True
    schema_extra = {
      "example":{
        "success": True,
        "message": "Successfully created the User Event",
        "data": {
        "raw_response" : {"first_attempt": "microanalytic theory"},
        "feedback": {
          "first_attempt": {
            "feedback_text": "can be improved",
            "evaluation_score":0.4,
            "evaluation_flag":"incorrect"
            }
          },
        "learning_item_id": "dfkjasfals",
        "activity_type": "choose_the_fact",
        "learning_unit": "sjfdjfalfd39",
        "user_id": "jfkdajetieqte",
        "course_id": "fjkadsfalsdfa",
        "flow_type": "Let AITutor Guide Me",
        "id": "fdjksafakdsf"
      }
    }
  }

class UpdateUserEventModel(BaseModel):
  """User Pydantic Model"""
  session_ref: Optional[str]
  raw_response: Optional[dict]
  feedback: Optional[dict]
  learning_item_id: Optional[str]
  activity_type: Optional[str]
  user_id: Optional[str]
  course_id: Optional[str]
  flow_type: Optional[str]
  hint: Optional[str]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {
        "example": {
        "session_ref": "fjdsalfjaslf",
        "raw_response" : {"first_attempt": "microanalytic theory"},
        "feedback": {
          "first_attempt": {
            "feedback_text": "can be improved",
            "evaluation_score":0.4,
            "evaluation_flag":"incorrect"
            }
        },
        "learning_item_id": "dfkjasfals",
        "activity_type": "choose_the_fact",
        "user_id": "dfkajkfjalk",
        "course_id": "fjkadsfalsdfa",
        "flow_type": "Let AITutor Guide Me"
        }
    }


class GetUserEvent(UserEventModelResponse):
  message: Optional[str] = "Successfully fetched User Event"

  class Config():
    orm_mode = True
    schema_extra = {
      "example":{
        "success": True,
        "message": "Successfully fetched the User Event",
        "data": {
        "raw_response" : {"first_attempt": "microanalytic theory"},
        "feedback": {
          "first_attempt": {
            "feedback_text": "can be improved",
            "evaluation_score":0.4,
            "evaluation_flag":"incorrect"
          }
        },
        "learning_item_id": "dfkjasfals",
        "activity_type": "choose_the_fact",
        "learning_unit": "sjfdjfalfd39",
        "user_id": "jfkdajetieqte",
        "course_id": "fjkadsfalsdfa",
        "flow_type": "Let AITutor Guide Me",
        "id": "dsfalfjdasjlfk"
      }
      }
    }


class GetAllUserEvents(UserEventModelResponse):
  message: Optional[str] = "Successfully fetched all UserEvents"
  data: List[UserEventWithParent]

  class Config():
    orm_mode = True
    schema_extra = {
      "example":{
        "success": True,
        "message": "Successfully fetched the User Event",
        "data": [{
        "raw_response" : {"first_attempt": "microanalytic theory"},
        "feedback": {
          "first_attempt": {
            "feedback_text": "can be improved",
            "evaluation_score":0.4,
            "evaluation_flag":"incorrect"
          }
        },
        "learning_item_id": "dfkjasfals",
        "activity_type": "choose_the_fact",
        "learning_unit": "sjfdjfalfd39",
        "user_id": "jfkdajetieqte",
        "course_id": "fjkadsfalsdfa",
        "flow_type": "Let AITutor Guide Me",
        "id": "dfsafakljdfa"
      }]
      }
    }


class DeleteUserEvent(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the User Event"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the User Event"
        }
    }
