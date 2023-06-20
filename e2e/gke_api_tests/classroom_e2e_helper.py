"""
Classroom e2e helper file
"""
import json
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
WORKSPACE_ADMIN_EMAIL = os.environ.get("WORKSPACE_ADMIN_EMAIL")

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
]
def get_creds():
  """_summary_

  Returns:
      _type_: _description_
  """
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  return a_creds.with_subject(WORKSPACE_ADMIN_EMAIL)

def create_course(name, section, description):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """
  
  service = build("classroom", "v1", credentials=get_creds())
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  new_course["ownerId"] = CLASSROOM_ADMIN_EMAIL
  new_course["courseState"] = "ACTIVE"
  course = service.courses().create(body=new_course).execute()
  return course