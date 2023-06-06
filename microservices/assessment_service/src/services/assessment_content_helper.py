"""
  Helper Functions for file operations for assessment submission
  and creation
"""
from datetime import datetime
from common.models import Assessment
from common.utils.gcs_adapter import (move_file_within_bucket,
                                      is_valid_path,
                                      download_file_from_gcs)
from common.utils.errors import ResourceNotFoundException
from common.utils.logging_handler import Logger
from config import ( ASSESSMENT_AUTHORING_BASE_PATH,
                      ASSESSMENT_SUBMISSION_BASE_PATH,
                      TEMP_FOLDER,
                      DOWNLOADS_FOLDER,
                      CONTENT_SERVING_BUCKET
                      )
from services.zip_file_processor import create_zip_file

def download_files_for_assessment(assessment_id):
  """
    This function downloads content associated with an assessment
    to temp/downloads/<assessment_id> on the container
    -------------------------------------------------------
    Input:
      assessment_id `str`: UUID of the assessment for which files are
                            to be downloaded
    --------------------------------------------------------
    Output:
      download_locations `list[str]`: List of the locations where files
                            are downloaded
  """
  assessment = Assessment.find_by_uuid(assessment_id)
  resource_paths = assessment.resource_paths

  # Identify missing files if any
  missing_files_list = []
  for file_path in resource_paths:
    file_on_gcs = f"gs://{CONTENT_SERVING_BUCKET}/{file_path}"
    if is_valid_path(file_on_gcs) is False:
      missing_files_list.append(file_path)

  if len(missing_files_list) != 0:
    # Generate Error log
    err_msg = f"Total missing files: {len(missing_files_list)} \n"
    err_msg += "Following files were not found for"
    err_msg += f" assessment {assessment_id} \n"
    for file in missing_files_list:
      err_msg += file

    raise ResourceNotFoundException(err_msg)

  # Download Files
  download_locations = []
  for file in resource_paths:
    gsutil_uri = f"gs://{CONTENT_SERVING_BUCKET}/{file}"
    dest_path = f"{TEMP_FOLDER}/{DOWNLOADS_FOLDER}/{assessment_id}/"
    download_location = download_file_from_gcs(gsutil_uri,dest_path)
    download_locations.append(download_location)

  Logger.info(f"Downloaded File: {download_locations}")

  return download_locations

def create_zip_for_assessment_contents(assessment_id):
  """
    This function generates zipfile for all the files linked to
    the assessment
    -------------------------------------------------------
    Input:
      assessment_id `str`: UUID of the assessment
    -------------------------------------------------------
    Output:
      zip_location `str`: location of the generated zip file
      zip_name `str`: name of the zip file for download
      downloaded_files `str`: list of downloaded file locations
                      linked to the assessment
  """
  # Download files from GCS
  downloaded_files = download_files_for_assessment(assessment_id)

  # Get the current timestamp
  timestamp = datetime.now()
  timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

  # Create Zip
  zip_name = f"{assessment_id} {timestamp_str}.zip"
  zip_location = create_zip_file(downloaded_files,
                                  zip_name)

  # pylint: disable=line-too-long
  Logger.info(f"zip file created for assessment {assessment_id} at {zip_location}")

  return zip_location, zip_name, downloaded_files

def attach_files_to_assessment_submission(learner_id, assessment_id, attempt_id,
                                          resource_paths, bucket_name):
  """
        This function will relocate uploaded files for an
        assessment submission to the required folder represented
        by the attempt_id
        ---------------------------------------------------
        Input:
            learner_id `str`: uuid of the learner
            assessment_id `str`: uuid of the assessment
            attempt_id `str`: unique id for the submission
            resource_paths [str] : list of file resource path which should be
                                   relocated
            bucket_name `str`: bucket where files are present
        ---------------------------------------------------
        Output:
            relocated_files [str]: list of the file paths after relocation
    """
  relocated_files = []
  for file_source in resource_paths:
    file_name = file_source.split("/")[-1]
    file_destination = f"{ASSESSMENT_SUBMISSION_BASE_PATH}/"+\
        f"{learner_id}/{assessment_id}/{attempt_id}/{file_name}"
    file_location = move_file_within_bucket(
        bucket_name=bucket_name,
        src_path=file_source,
        dest_path=file_destination)
    relocated_files.append(file_location)

  return relocated_files

def attach_files_to_assessment(user_id, assessment_id, resource_paths,
        bucket_name):
  """
        This function will relocate uploaded files for an
        assessment creation to the required folder represented
        by the assessment_id
        ---------------------------------------------------
        Input:
            user_id `str`: uuid of the staff
            assessment_id `str`: uuid of the assessment
            resource_paths [str] : list of file resource path which should be
                                   relocated
            bucket_name `str`: bucket where files are present
        ---------------------------------------------------
        Output:
            relocated_files [str]: list of the file paths after relocation
    """
  relocated_files = []
  for file_source in resource_paths:
    file_name = file_source.split("/")[-1]
    file_destination = f"{ASSESSMENT_AUTHORING_BASE_PATH}/{user_id}/"+\
        f"{assessment_id}/{file_name}"
    file_location = move_file_within_bucket(
        bucket_name=bucket_name,
        src_path=file_source,
        dest_path=file_destination)
    relocated_files.append(file_location)
  return relocated_files
