""" Content Serving endpoints """
import traceback
from fastapi import (APIRouter, UploadFile, File,
                      Response, status)
from fastapi.responses import (FileResponse)
from common.models import Assessment, LearnerProfile, User, SubmittedAssessment
from common.utils.content_processing import (ContentValidator, FileUtils,
                                             ALLOWED_CONTENT_TYPES)

from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InternalServerError, PayloadTooLargeError)
from common.utils.http_exceptions import (BadRequest, ResourceNotFound,
                                          InternalServerError as
                                          InternalServerException,
                                          PayloadTooLarge)
from common.utils.gcs_adapter import (is_valid_path,
                                      upload_file_to_bucket,
                                      get_blob_from_gcs_path,
                                      GcsCrudService)
from common.utils.logging_handler import Logger
from config import (CONTENT_SERVING_BUCKET, ERROR_RESPONSES,
                    CONTENT_FILE_SIZE, ASSESSMENT_SUBMISSION_BASE_PATH,
                    ASSESSMENT_AUTHORING_BASE_PATH, SIGNURL_SA_KEY_PATH)
from schemas.assessment_content import (  FileUploadResponseModel,
                                          GetSignedURLListResponseModel)
from services.assessment_content_helper import (
  create_zip_for_assessment_contents
)
from starlette.background import BackgroundTasks

# pylint: disable = line-too-long
# pylint: disable = broad-except
router = APIRouter(tags=["Content Serving"], responses=ERROR_RESPONSES)

contentValidator = ContentValidator()
fileHandler = FileUtils()

# pylint: disable = unspecified-encoding,consider-using-with

# Function for File Clean up after response
def file_clean_up(background_tasks: BackgroundTasks, files_to_delete):
  for file_to_delete in files_to_delete:
    background_tasks.add_task(fileHandler.deleteFile,
                                filepath=file_to_delete)

@router.post(
  "/assessment-submission/upload-sync/{learner_id}/{assessment_id}",
  response_model = FileUploadResponseModel,
  name="Upload files for assessment submission"
)
async def upload_assessment_response(learner_id: str,
                                     assessment_id: str,
                                     content_file: UploadFile = File(...)):
  """Function to upload assessment response"""
  try:
    # check file size
    if len(await content_file.read()) > CONTENT_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {content_file.filename}")

    # check if the valid content type header is set
    if content_file.content_type not in ALLOWED_CONTENT_TYPES:
      raise ValidationError("content_type not allowed")

    file_name = content_file.filename
    file_extension = file_name.split(".")[-1]

    if contentValidator.checkExtensionAndContentHeader(
        content_file.content_type, file_extension) is False:
      msg = "Content Type header and file extension does not match. "
      msg += f"Received header contentType: {content_file.content_type}, "
      msg += f"received file extension .{file_extension}"
      raise ValidationError(msg)

    assesment_details = Assessment().find_by_id(assessment_id)
    if assesment_details is None:
      raise ValidationError(
        f"No assessment wit id {assessment_id} found"
      )
    max_attempts = assesment_details.max_attempts
    lp = LearnerProfile.collection.\
      filter("learner_id", "==", learner_id).get()
    if lp is None:
      raise ValidationError(
        f"No learner profile with learner id {learner_id} found"
      )
    learner_profile = lp.get_fields()
    cur_attempts = learner_profile.get("progress",{}).get("assessments",{}).\
      get(assessment_id,{}).get("num_attempts")
    if cur_attempts is None:
      cur_attempts = 0

    # Determine Location for assessment submission
    content_upload_folder = f"{ASSESSMENT_SUBMISSION_BASE_PATH}/{learner_id}/{assessment_id}/temp"
    file_path = f"{content_upload_folder}/{file_name}"

    path_exists = f"gs://{CONTENT_SERVING_BUCKET}/{file_path}"

    # Check if file already exists with same name
    if cur_attempts < max_attempts:
      if is_valid_path(path_exists) is False:
        # Go to the start of stream by file.seek(0)
        await content_file.seek(0)

        # Upload to GCS
        upload_file_to_bucket(CONTENT_SERVING_BUCKET, content_upload_folder,
                              content_file.filename, content_file.file)

        return {
            "success": True,
            "message": "Successfully uploaded file",
            "data": {
                "resource_path": file_path
            }
        }

      else:
        raise ValidationError(
            "File with same name already exists"
        )
    else:
      raise ValidationError(
        f"current attempt {cur_attempts} cannot be greater than max attempts {max_attempts}"
        )

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e

@router.post(
  "/assessment-authoring/upload-sync/{user_id}",
  response_model = FileUploadResponseModel,
  name="Upload files for assessment authoring"
)
async def upload_assessment_content(user_id: str,
                                     content_file: UploadFile = File(...)):
  """Function to upload assessment content"""
  try:
    # check file size
    if len(await content_file.read()) > CONTENT_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {content_file.filename}")

    # check if the valid content type header is set
    if content_file.content_type not in ALLOWED_CONTENT_TYPES:
      raise ValidationError("content_type not allowed")

    file_name = content_file.filename
    file_extension = file_name.split(".")[-1]

    if contentValidator.checkExtensionAndContentHeader(
        content_file.content_type, file_extension) is False:
      msg = "Content Type header and file extension does not match. "
      msg += f"Received header contentType: {content_file.content_type}, "
      msg += f"received file extension .{file_extension}"
      raise ValidationError(msg)

    # Validate User UUID
    _=User.find_by_uuid(user_id)

    # Determine Location for assessment submission
    content_upload_folder = f"{ASSESSMENT_AUTHORING_BASE_PATH}/{user_id}/temp"
    file_path = f"{content_upload_folder}/{file_name}"

    path_exists = f"gs://{CONTENT_SERVING_BUCKET}/{file_path}"

    # Check if file already exists with same name
    if is_valid_path(path_exists) is False:
      # Go to the start of stream by file.seek(0)
      await content_file.seek(0)

      # Upload to GCS
      upload_file_to_bucket(CONTENT_SERVING_BUCKET, content_upload_folder,
                            content_file.filename, content_file.file)

      return {
          "success": True,
          "message": "Successfully uploaded file",
          "data": {
              "resource_path": file_path
          }
      }

    else:
      raise ValidationError(
          "File with same name already exists"
      )

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e

@router.get(
    "/assessment-content/{assessment_uuid}/signed-url",
    response_model=GetSignedURLListResponseModel,
    name="Get Signed URL for submitted files")
def get_signed_url_for_submitted_assessment(assessment_uuid: str,
                                            response: Response,
                                            is_submitted_assessment: bool = False):
  """ Generate Signed URL for files uploaded for submitted assessments
      -------------------------------------------------------------------------
      Input:
        assessment_uuid: `str`
          UUID of Assessment/Submitted Assessment.

        is_submitted_assessment: `bool`
          A flag determining, which data model to use for generating the
          signed URLs. Default value is False, which means, it will look
          for the document in Assessment datamodel.

        Note: This api provides a list of signed urls mapped to the
        uploaded files.

        If signed url generation fails for some files,
        then partial success response will be returned

        If signed url generation fails for all files,
        then internal server error response will be returned

      -------------------------------------------------------------------------
      Output:
        Signed URL List JSON response: \
        `GetSignedURLListModelResponse`
    """
  try:

    file_list = []

    if is_submitted_assessment is True:
      submitted_assessment = SubmittedAssessment.find_by_uuid(assessment_uuid)
      file_list = submitted_assessment.submission_gcs_paths
    else:
      assessment = Assessment.find_by_uuid(assessment_uuid)
      file_list = assessment.resource_paths

    response_list = []

    is_partial_success = False
    fail_count = 0

    gcs_service = GcsCrudService(CONTENT_SERVING_BUCKET, SIGNURL_SA_KEY_PATH)

    for file_path in file_list:

      path_exists = is_valid_path(f"gs://{CONTENT_SERVING_BUCKET}/{file_path}")
      # Genrate URL if file exists
      if path_exists is True:
        blob = get_blob_from_gcs_path(f"gs://{CONTENT_SERVING_BUCKET}/{file_path}")
        signed_url = gcs_service.generate_url(
            file_path, 60)
        record = {
          "file_size_bytes": int(blob.size),
          "file_path": file_path,
          "signed_url": signed_url,
          "status": "Signed url generated successfully"
        }

        # Check if signed url is generated successfully
        if not isinstance(signed_url, str):
          record["status"] = "Some error occured while generating singed url"
          record["signed_url"] = None

          is_partial_success = True
          fail_count += 1

        response_list.append(record)
      else:
        # partial success when file not found
        record = {
          "file_size_bytes": 0,
          "file_path": file_path,
          "signed_url": None,
          "status": "File Not Found"
        }
        response_list.append(record)

        is_partial_success = True
        fail_count += 1

    if is_partial_success is True:
      # Generate partial success response
      if fail_count < len(file_list):
        # If error occured for few files
        return {
          "success": True,
          "message": "Could not generate urls for some files",
          "data": response_list
        }
      else:
        # If error occured for all file
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
          "success": False,
          "message": "Some error occured while generating signed urls",
          "data": response_list
        }
    else:
      # Generate success response
      return {
        "success": True,
        "message": "Successfully generated signed urls for all files",
        "data": response_list
      }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except InternalServerException as e:
    raise InternalServerError(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e

@router.get(
  "/assessment-content/{assessment_uuid}/download-all",
  name="Download all files of assessment"
)
def download_all(assessment_uuid: str, background_tasks: BackgroundTasks):
  """
    This API will generate a zip of all the files linked to an assessment
    -------------------------------------------------------
    Input
      assessment_uuid `str`: UUID of the assessment
    -------------------------------------------------------
    Output
      a zip file as `FileResponse`
  """
  try:

    # Validate Assessment
    assessment = Assessment.find_by_uuid(assessment_uuid)

    # Validate Resources are linked to assessment
    if assessment.resource_paths is None or \
      len(assessment.resource_paths) == 0:

      err_msg = f"Cannot generate zip because Assessment {assessment_uuid}"
      err_msg += " does not have any resources linked."
      err_msg += " Please attach files to the assessment before generating zip"
      raise ValidationError(err_msg)

    # Generate zip file
    zip_location,zip_name, downloaded_files = \
      create_zip_for_assessment_contents(assessment_uuid)

    # Clean up
    files_to_delete = downloaded_files
    files_to_delete.append(zip_location)

    file_clean_up(background_tasks, files_to_delete)

    return FileResponse(zip_location, filename= zip_name)

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except InternalServerException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
