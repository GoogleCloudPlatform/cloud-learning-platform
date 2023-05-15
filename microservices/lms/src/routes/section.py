""" Section endpoints """
import traceback
import datetime
from common.models import Cohort, CourseTemplate, Section
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ClassroomHttpException,
                                          InternalServerError,
                                          ResourceNotFound, BadRequest,
                                          CustomHTTPException
                                          )
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from common.utils.bq_helper import insert_rows_to_bq
from common.utils.jwt_creds import JwtCredentials
from fastapi import APIRouter, Request,BackgroundTasks,status
from googleapiclient.errors import HttpError
from schemas.classroom_courses import EnableNotificationsResponse
from schemas.error_schema import (ConflictResponseModel,
                                  InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import (
    DeleteSectionResponseModel,
    GetSectiontResponseModel, SectionDetails, SectionListResponseModel,
    UpdateSectionResponseModel,TeachersListResponseModel,
    GetTeacherResponseModel,AssignmentModel,GetCourseWorkList,
    ImportGradeResponseModel)
from schemas.update_section import UpdateSection
from services import common_service
from services.section_service import copy_course_background_task,\
update_grades
from utils.helper import (convert_section_to_section_model,
                          convert_assignment_to_assignment_model,
                          FEED_TYPES,
                    convert_coursework_to_short_coursework_model)
from config import BQ_TABLE_DICT,BQ_DATASET
# disabling for linting to pass
# pylint: disable = broad-except
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


router = APIRouter(prefix="/sections",
                   tags=["Sections"],
                   responses={
                       500: {
                           "model": InternalServerErrorResponseModel
                       },
                       404: {
                           "model": NotFoundErrorResponseModel
                       },
                       409: {
                           "model": ConflictResponseModel
                       },
                       422: {
                           "model": ValidationErrorResponseModel
                       }
                   })

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}

@router.post("",
             status_code=status.HTTP_202_ACCEPTED)
def create_section(sections_details: SectionDetails,
                  request: Request,
                   background_tasks: BackgroundTasks
                   ):
  """Create section API
  Args:
    name (section): Section name
    description (str):Description
    classroom_template_id(str):course_template_id id from firestore
    cohort_id(str):cohort id from firestore
    teachers(list):List of teachers to be added
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    course_template_details = CourseTemplate.find_by_id(
        sections_details.course_template)
    cohort_details = Cohort.find_by_id(sections_details.cohort)
    # Get course by course id for copying from master course
    current_course = classroom_crud.get_course_by_id(
        course_template_details.classroom_id)
    if current_course is None:
      raise ResourceNotFoundException(
          "classroom  with id" +
          f" {course_template_details.classroom_id} is not found")
    template_drive_folder_id = current_course["teacherFolder"]["id"]
    background_tasks.add_task(copy_course_background_task,
                              course_template_details,
                             sections_details,
                             cohort_details,template_drive_folder_id,
                             headers,message = "started process")
    Logger.info(f"Background Task called for the cohort id {cohort_details.id}\
                course template {course_template_details.id} with\
                 section name{sections_details.name}")
    return { "success": True,
            "message": "Section will be created shortly",
            "data": None}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}", response_model=GetSectiontResponseModel)
def get_section(section_id: str):
  """Get a section details from db

  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section_details = []
    section_details = Section.find_by_id(section_id)
    # Get course by course id
    new_section = convert_section_to_section_model(section_details)
    return {"data": new_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{section_id}/teachers",response_model=TeachersListResponseModel)
def get_teachers_list(section_id: str, request: Request):
  """Get a list of teachers for a section details from db

  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 Section with section id is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    teacher_details = []
    headers = {"Authorization": request.headers.get("Authorization")}
    section_details = Section.find_by_id(section_id)
    teachers= section_details.teachers
    if teachers == []:
      return{"data":teacher_details}
    for teacher in teachers:
      result = common_service.call_search_user_api(headers=headers,
      email=teacher)
      if result.json()["data"] !=[]:
        teacher_details.append(result.json()["data"][0])
    return {"data": teacher_details}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}/teachers/{teacher_email}",
response_model=GetTeacherResponseModel)
def get_teacher(section_id: str,teacher_email:str,request: Request):
  """Get teacher for a section .If teacher is present in given section
    get teacher details else throw
  Args:
      section_id (str): section_id in firestore
      teacher_email(str): teachers email Id
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 Section with section id is not found
      HTTPException: 404 Teacher with teacher email is not found
  Returns:
    {"status":"Success","data":}: Returns section details from  db,
    {'status': 'False'} if raises an exception
  """
  try:
    teacher_email=teacher_email.lower()
    headers = {"Authorization": request.headers.get("Authorization")}
    section_details = Section.find_by_id(section_id)
    teachers= section_details.teachers
    if teacher_email in teachers:
      result = common_service.call_search_user_api(headers=headers,
      email=teacher_email)
      if result.json()["data"] == [] or result.json()["data"] is None :
        raise ResourceNotFoundException(
          f"{teacher_email} not found in Users data")
      else :
        return {"data": result.json()["data"][0]}
    else:
      raise ResourceNotFoundException(f"{teacher_email}\
        not found in teachers list of the section")
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.delete("/{section_id}", response_model=DeleteSectionResponseModel)
def delete_section(section_id: str):
  """Get a section details from db and archive record
  from section collection and
  google classroom course

  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
  Returns:
    {"message": "Successfully deleted section"}
  """
  try:
    section_details = Section.find_by_id(section_id)
    classroom_crud.update_course_state(section_details.classroom_id,\
      "ARCHIVED")
    Section.soft_delete_by_id(section_id)
    return {
        "message": f"Successfully archived the Section with id {section_id}"
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("", response_model=SectionListResponseModel)
def section_list(skip: int = 0, limit: int = 10):
  """Get a all section details from db

  Args:
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException:
        500 If refereced course_template and cohort object does not exists in db
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError(
          "Invalid value passed to \"limit\" query parameter")

    sections = Section.fetch_all(skip, limit)
    sections_list = list(map(convert_section_to_section_model, sections))
    return {"data": sections_list}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@router.patch("", response_model=UpdateSectionResponseModel)
def update_section(sections_details: UpdateSection,request: Request):
  """Update section API

  Args:
    id(str): id of the section in firestore
    course_state:Updated course state it can be any one of
    [ACTIVE,ARCHIVED,PROVISIONED,DECLINED,SUSPENDED]
    section_name (section): Section name
    description (str):Description
    course_id(str):course_id of google classroom
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if course_id or section_id is not found
  Returns:
    {"status":"Success","data":{}}: Returns Updated course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    section = Section.find_by_id(sections_details.id)
    new_course = classroom_crud.update_course(sections_details.course_id,
                                              sections_details.section_name,
                                              sections_details.description)
    if new_course is None:
      raise ResourceNotFoundException(
          "Course with Course_id"
          f" {sections_details.course_id} is not found in classroom")
    add_teacher_list = list(
        set(sections_details.teachers) - set(section.teachers))
    for i in add_teacher_list:
      invitation_object = classroom_crud.invite_user(
                            sections_details.course_id,i,"TEACHER")
      # Storing classroom details
      classroom_crud.acceept_invite(invitation_object["id"],i)
      user_profile = classroom_crud.get_user_profile_information(i)
      data = {
      "first_name":user_profile["name"]["givenName"],
      "last_name": user_profile["name"]["familyName"],
      "email":i,
      "user_type": "faculty",
      "user_groups": [],
      "status": "active",
      "is_registered": True,
      "failed_login_attempts_count": 0,
      "access_api_docs": False,
      "gaia_id":user_profile["id"],
      "photo_url" :  user_profile["photoUrl"]
        }
      common_service.create_teacher(headers,data)
    remove_teacher_list = list(
        set(section.teachers) - set(sections_details.teachers))
    for i in remove_teacher_list:
      classroom_crud.delete_teacher(sections_details.course_id, i)
    section.section = sections_details.section_name
    section.description = sections_details.description
    section.teachers = sections_details.teachers
    section.update()
    updated_section = convert_section_to_section_model(section)
    rows=[{
      "sectionId":sections_details.id,\
      "courseId":sections_details.course_id,\
      "classroomUrl":updated_section["classroom_url"],\
        "name":sections_details.section_name,\
        "description":sections_details.description,\
          "cohortId":updated_section["cohort"].split("/")[1],\
          "courseTemplateId":updated_section["course_template"].split("/")[1],\
          "timestamp":datetime.datetime.utcnow()
    }]
    insert_rows_to_bq(
      rows=rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"]
      )
    return {"data": updated_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.patch("/{section_id}/update_classroom_code",
              response_model=GetSectiontResponseModel)
def update_section_classroom_code(section_id:str):
  """_summary_

  Args:
      section_id (str): _description_
      classroom_code (str): _description_

  Raises:
      ResourceNotFound: _description_
      InternalServerError: _description_

  Returns:
      _type_: _description_
  """
  try:
    section=Section.find_by_id(section_id)
    course=classroom_crud.get_course_by_id(section.classroom_id)
    if course is None:
      raise ResourceNotFoundException(
          "Classroom with section id" +
          f" {section_id} is not found")
    section.classroom_code=course["enrollmentCode"]
    section.update()
    return {
      "message":"Successfully updated the classroom code",
      "data":convert_section_to_section_model(section)
      }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.post("/{section_id}/enable_notifications",
             response_model=EnableNotificationsResponse)
def section_enable_notifications_pub_sub(section_id:str):
  """Resgister section with a pub/sub topic

  Args:
      section_id (str): unique section id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
      ClassroomHttpException: raise error according to the HTTPError exception
  Returns:
      _type_: _description_
  """
  try:
    section = Section.find_by_id(section_id)
    responses = [
        classroom_crud.enable_notifications(
            section.classroom_id, i) for i in FEED_TYPES
    ]
    return {
          "message":
          "Successfully enable the notifications of the course using section "
          + f"{section_id} id",
          "data":responses
      }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}/assignments/{assignment_id}",
            response_model=AssignmentModel)
def get_assignment(section_id: str, assignment_id: str):
  """Get course work details using section id and course work id
  Args:
      section_id (str): section unique id
      assignment_id (str): course work/assignment unique id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ClassroomHttpException: raise error according to the HTTPError exception
      ResourceNotFound: 404 Section with section id is not found
  Returns:
      AssignmentModel: AssignmentModel object which
        contains all the course work details
  """
  try:
    section = Section.find_by_id(section_id)
    assignment = classroom_crud.get_course_work(course_id=section.classroom_id,
                                                course_work_id=assignment_id)
    return convert_assignment_to_assignment_model(assignment)
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{section_id}/get_coursework_list",
            response_model=GetCourseWorkList)
def get_coursework_list(section_id: str):
  """Get course work details using section id
  Args:
      section_id (str): section unique id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ClassroomHttpException: raise error according to the HTTPError exception
      ResourceNotFound: 404 Section with section id is not found
  Returns:
      AssignmentModel: AssignmentModel object which
        contains all the course work details
  """
  try:
    data=[]
    course_work_list = classroom_crud.get_course_work_list\
      (section_id=section_id)
    for x in course_work_list:
      data.append(convert_coursework_to_short_coursework_model(x))
    return {"data":data}
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
@router.patch("/{section_id}/coursework/{coursework_id}",
              response_model=ImportGradeResponseModel,
              status_code=status.HTTP_202_ACCEPTED)
def import_grade(section_id: str,coursework_id:str,
                 background_tasks: BackgroundTasks):
  """Get a section details from db and use the coursework Id
  Args:
      section_id (str): section_id in firestore
      coursework_id(str): coursework_id of coursework in classroom
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found or
        coursework is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section = Section.find_by_id(section_id)
    classroom_course = classroom_crud.get_course_by_id(section.classroom_id)
    folder_id = classroom_course["teacherFolder"]["id"]
    result = classroom_crud.get_course_work(
    section.classroom_id,coursework_id)
    #Get url mapping of google forms view links and edit ids
    # url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form(
    #   folder_id)
    url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
    is_google_form_present = False
    if "materials" in result.keys():
      for material in result["materials"]:
        if "form" in material.keys():
          is_google_form_present = True
          form_details = \
            url_mapping[material["form"]["formUrl"]]

          form_id = form_details["file_id"]
          # Get all responses for the form if no responses of
          # the form then return
          all_responses_of_form = classroom_crud.\
          retrieve_all_form_responses(form_id)
          if all_responses_of_form =={}:
            raise ResourceNotFoundException(
              "Responses not available for google form")
          background_tasks.add_task(update_grades,all_responses_of_form,
                                    section,coursework_id)

      if is_google_form_present:
        return {
           "message":"Grades for coursework will be updated shortly"}
      else:
        raise ResourceNotFoundException(
          f"Form is not present for coursework_id {coursework_id}"
          )
    else:
      raise ResourceNotFoundException(
          f"Form is not present for coursework_id {coursework_id}"
          )
  except HttpError as hte:
    Logger.error(hte)
    message = str(hte)
    if hte.resp.status == 404:
      message = "Coursework not found"
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=message,
                              data=None) from hte
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e

@router.post("/test_jwt")
def test_jwt():
  SCOPES = ['https://www.googleapis.com/auth/drive']
  _DEFAULT_TOKEN_LIFETIME_SECS = 3600  # 1 hour in seconds
  _GOOGLE_OAUTH2_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
  creds = JwtCredentials.from_default_with_subject(
    "lms_admin_teacher@dhodun.altostrat.com",
    "gke-pod-sa@core-learning-services-dev.iam.gserviceaccount.com",
    _GOOGLE_OAUTH2_TOKEN_ENDPOINT,
    scopes=SCOPES)


  service = build('drive', 'v3', credentials=creds)
  page_token = None
  while True:
    response = service.files().list(
      q=
      "(name contains \"e2e\") and (mimeType=\"application/vnd.google-apps.folder\")",
      spaces='drive',
      fields='nextPageToken, files(id, name)',
      corpora='allDrives',
      includeItemsFromAllDrives='true',
      supportsAllDrives='true',
      pageToken=page_token).execute()
    for file in response.get('files', []):
      print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
      break
  return  response