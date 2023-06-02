"""Script for validation and uploading zip files to gcs"""
from zipfile import BadZipFile
from common.utils.content_processing import (ContentValidator, FileUtils)
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InternalServerError)
from common.utils.http_exceptions import (BadRequest, ResourceNotFound,
                                          InternalServerError as
                                          InternalServerException)
from common.utils.gcs_adapter import upload_folder, download_file_from_gcs
from config import (RESOURCE_BASE_PATH, CONTENT_SERVING_BUCKET, ZIP_EXTRACTION_FOLDER)

# pylint: disable = line-too-long

contentValidator = ContentValidator()
fileHandler = FileUtils()

def recreate_zip_structure_on_gcs(input_data):
  """
    This function will uploaded large zip file and
    upload it to the required folder
    -------------------------------------------------------------
    Input Params

    input_data: `dict`
    The input data dict contains the following keys:
    1. gsutil_uri: `str`
        This will hold the actual gcs path from which the zip
        is to be downloaded
        eg:
        gsutil_uri: gs://content_serving_bkt/lr/zip/{lr_id}/{filename}
    2. filename: `str`
        name of the uploaded zip file
    -------------------------------------------------------------
    Response

    Success:
    {
        "success": True,
        "message": "Successfully uploaded the learning content
        and updated the learning resource",
        "data": {
            "signed_url": signed_url,
            "resource_type": resource_type
        }
    }

    Failure 1:
    {
        "success": False,
        "message": "Some error occured while uploading the content.
        Unable to locate the mentioned entrypoint after upload.",
        "data": None
    }

    Failure 2:
    {
        "success": False,
        "message": "Mentioned entrypoint {entry_point} does not
        exist in the content package.",
        "data": None
    }
    """
  try:

    gsutil_uri = input_data["gsutil_uri"]
    filename = input_data["filename"]

    # file will be downloaded to the zip_extraction folder
    zipfile_path = download_file_from_gcs(gsutil_uri, f"{ZIP_EXTRACTION_FOLDER}/{filename}")

    # unzip files to zip_extraction folder
    filename_without_ext = filename.split(".")[0]
    local_dest_path = f"{ZIP_EXTRACTION_FOLDER}/extracted/{filename_without_ext}"
    fileHandler.unzipPackage(zipfile_path, local_dest_path)

    # recreate zip structure on GCS
    upload_folder(
        CONTENT_SERVING_BUCKET, local_dest_path,
        f"{RESOURCE_BASE_PATH}/{filename_without_ext}"
    )

    # Cleanup Temporary Files
    # Delete zip file
    fileHandler.deleteFile(zipfile_path)
    # Delete extracted contents of zip file recursively
    fileHandler.deleteFolder(local_dest_path)

    return {
        "success": True,
        "message": "Successfully uploaded the learning content",
        "data": None
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except BadZipFile as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e
