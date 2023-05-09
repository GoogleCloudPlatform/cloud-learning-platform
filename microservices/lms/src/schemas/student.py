"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel, constr
from schemas.schema_examples import INVITE_STUDENT, COURSE_ENROLLMENT_USER_EXAMPLE


class UserModel(BaseModel):
  """Course Enrollment User Response Model"""
  user_id: str
  first_name: str
  last_name: str
  email: constr(min_length=7,
                max_length=128,
                regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                to_lower=True)
  user_type: str
  status: str
  gaia_id: Optional[str] = ""
  photo_url: Optional[str] = ""
  course_enrollment_id: str
  invitation_id: Optional[str] = ""
  section_id: str
  cohort_id: str
  classroom_id: str
  enrollment_status: str
  classroom_url: str

  class Config():
    orm_mode = True
    schema_extra = {"example": COURSE_ENROLLMENT_USER_EXAMPLE}


class AddStudentResponseModel(BaseModel):
  """Add Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Added the Student"
  data: Optional[dict] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Added the Student",
            "data": {
                "course_enrollment_id": "2xBnBjqm2X3eRgVxE6Bv",
                "student_email": "test_user@gmail",
                "section_id": "fake-section-id",
                "cohort_id": "fake-cohort-id",
                "classroom_id": "123453333",
                "classroom_url": "https://classroom.google.com/c/NTYzMhjhjrx"
            }
        }
    }


class AddStudentModel(BaseModel):
  """Input Model to add student in section"""
  email: constr(min_length=7,
                max_length=128,
                regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                to_lower=True)
  access_token: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "email": "email@gmail.com",
            "access_token": "test_token"
        }
    }


class GetStudentDetailsResponseModel(BaseModel):
  """Get Student Details Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the student list"
  data: Optional[UserModel] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Success",
            "data": COURSE_ENROLLMENT_USER_EXAMPLE
        }
    }


class InviteStudentToSectionResponseModel(BaseModel):
  """Invite Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Invited the Student"
  data: Optional[dict] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Invited the Student",
            "data": INVITE_STUDENT
        }
    }


class UpdateInviteResponseModel(BaseModel):
  """Invite Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Updated the invitation status"
  data: Optional[dict] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Invited the Student",
            "data": {
                "list_coursenrolment": [
                    "courseenrollment_id1", "courseenrollment_id2",
                    "courseenrollment_id3"
                ]
            }
        }
    }


class GetProgressPercentageResponseModel(BaseModel):
  """Get Progress Percentage"""
  success: Optional[bool] = True
  data: int = None


class GetProgressPercentageCohortResponseModel(BaseModel):
  """Get Progress Percentage"""
  success: Optional[bool] = True
  data: list = None

class GetOverallPercentage(BaseModel):
  """Get Overall Percentage"""
  success:Optional[bool]=True
  data: Optional[list] =None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "data":None
      }
      }
