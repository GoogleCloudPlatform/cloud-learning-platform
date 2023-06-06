"""
Pydantic Model for Assessment Item API's
"""
from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel
from schemas.schema_examples import (UPLOAD_SUBMITTED_ASSESSMENT_EXAMPLE,
                                     SUBMITTED_ASSESSMENT_EXAMPLE,
                                     UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE,
                                     FULL_SUBMITTED_ASSESSMENT_EXAMPLE)


class UploadSubmittedAssessment(BaseModel):
  assessment_id: str
  learner_id: str
  submission_gcs_paths: str

  class Config():
    orm_mode = True
    schema_extra = {"example": UPLOAD_SUBMITTED_ASSESSMENT_EXAMPLE}


class SubmittedAssessmentRequestModel(BaseModel):
  assessment_id: str
  learner_id: str
  learner_session_id: str
  attempt_no: Optional[int] = 1
  submission_gcs_paths: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {"example": SUBMITTED_ASSESSMENT_EXAMPLE}


class SubmittedRubric(BaseModel):
  rubric_criteria_id: str
  result: str
  feedback: Optional[str]

class UpdateAssessorIdRequestModel(BaseModel):
  assessor_id: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": {"assessor_id": "assessor_id"}}

class Comment(BaseModel):
  """Comment Pydantic Model"""
  comment: str
  type: Literal["non-eval", "flag"]
  access: str
  author: str
  created_time: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "comment": "abcd",
            "type": "flag",
            "access": "accessor",
            "author": "abcd",
            "created_time": ""
        }
    }


class DeleteSubmittedAssessment(BaseModel):
  """Delete SubmittedAssessment Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the submitted_assessment"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the submitted_assessment"
        }
    }


class FullSubmittedAssessmentModel(BaseModel):
  """Get SubmittedAssessment Pydantic Model"""
  assessment_id: str
  learner_id: str
  assessor_id: Optional[str]
  type: str
  plagiarism_score: Optional[float]
  plagiarism_report_path: Optional[str]
  result: Optional[str]
  pass_status: Optional[bool]
  status: str
  is_flagged: bool
  is_autogradable: bool
  comments: Optional[List[Comment]]
  timer_start_time: str
  attempt_no: int
  learner_session_id: Optional[str]
  learner_session_data: Optional[dict]
  assessor_session_id: Optional[str]
  submission_gcs_paths: Optional[List[str]] = []
  metadata: Optional[dict]
  submitted_rubrics: Optional[List[SubmittedRubric]]
  overall_feedback: Optional[str]
  uuid: str
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str

  class Config():
    orm_mode = True
    arbitrary_types_allowed = True
    schema_extra = {"example": FULL_SUBMITTED_ASSESSMENT_EXAMPLE}


class UpdateSubmittedAssessmentModel(BaseModel):
  """Update SubmittedAssessment Pydantic Model"""
  assessment_id: Optional[str]
  learner_id: Optional[str]
  assessor_id: Optional[str]
  type: Optional[str]
  plagiarism_score: Optional[float]
  plagiarism_report_path: Optional[str]
  result: Optional[str]
  pass_status: Optional[bool]
  status: Optional[str]
  is_flagged: Optional[bool]
  is_autogradable: Optional[bool]
  comments: Optional[Comment]
  attempt_no: Optional[int]
  learner_session_id: Optional[str]
  learner_session_data: Optional[dict]
  assessor_session_id: Optional[str]
  metadata: Optional[dict]
  submitted_rubrics: Optional[List[SubmittedRubric]]
  overall_feedback: Optional[str]
  submission_gcs_paths: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE}


class SubmittedAssessmentResponseModel(BaseModel):
  """SubmittedAssessment Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the submitted_assessment"
  data: Optional[FullSubmittedAssessmentModel]

class TotalCountFullResponseModel(BaseModel):
  records: Optional[List[FullSubmittedAssessmentModel]]
  total_count: int

class AllSubmittedAssessmentResponseModel(BaseModel):
  """SubmittedAssessment Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the submitted_assessment"
  data: Optional[TotalCountFullResponseModel]


class ReadyForEvaluationModel(FullSubmittedAssessmentModel):
  unit_name: Optional[str] = ""
  discipline_name: Optional[str] = ""
  learner_name: Optional[str] = ""
  assigned_to: Optional[str] = ""
  instructor_name: Optional[str] = ""
  instructor_id: Optional[str] = ""
  max_attempts: Optional[int] = 3
  is_autogradable: Optional[bool] = False


class SubmittedAssessmentAssessorResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = \
    "Successfully fetched the ready for evaluation submitted assessment"
  data: Optional[ReadyForEvaluationModel]

class TotalCountResponseModel(BaseModel):
  records: Optional[List[ReadyForEvaluationModel]]
  total_count: int

class AllSubmittedAssessmentAssessorResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = \
    "Successfully fetched the ready for evaluation submitted assessments"
  data: Optional[TotalCountResponseModel]

class ReplaceAssessorofSubmittedAssessmentsResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = \
    "Successfully updated the assessor of submitted assessments"


class SubmittedAssessmentUniqueData(BaseModel):
  """Unique data fields for competency, result and type of Submitted
  Assessment"""
  discipline_names: List[str] = []
  unit_names: List[str] = []
  types: List[str] = []
  results: List[str] = []


class SubmittedAssessmentUniqueResponseModel(BaseModel):
  """Unique values for SubmittedAssessment Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] =\
      "Successfully fetched the unique values for submitted assessments"
  data: Optional[SubmittedAssessmentUniqueData]


class ManualEvaluationModel(BaseModel):
  """Pydantic model for manual evaluation submitted assessments"""
  learning_object: str
  learning_object_name: str
  submitted_assessments: List[ReadyForEvaluationModel]

class TotalCountManualResponseModel(BaseModel):
  records: Optional[List[ManualEvaluationModel]]
  total_count: int

class ManualEvaluationResponseModel(BaseModel):
  """Response model for manual evaluation submitted assessments"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the submitted assessments"
  data: Optional[TotalCountManualResponseModel]
