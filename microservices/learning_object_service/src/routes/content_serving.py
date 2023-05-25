""" Content Serving endpoints """
import pathlib
from zipfile import BadZipFile
from typing import Optional
from typing_extensions import Literal
import traceback
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import RedirectResponse
from schemas.error_schema import NotFoundErrorResponseModel
from schemas.content_serving_schema import (
    GetSignedUrlModelResponse, ContentLinkInputModel, ContentLinkResponse,
    ContentPublishResponse, BatchJobModel, ListFilesAndFolderResponse,
    GetContentVersionsResponse)
from services.batch_job import initiate_batch_job
from services.content_version_handler import (link_content_and_create_version,
                                              get_content_versions,
                                              handle_publish_event,
                                              update_lr_resource_path)
from services.hierarchy_content_mapping import (get_file_and_folder_list,
                                                is_missing_linked_files,
                                                link_content_to_lr,
                                                link_srl_to_all_le)
from common.models import LearningResource, FAQContent, LearningExperience
from common.utils.content_processing import (ContentValidator, FileUtils, ALLOWED_CONTENT_TYPES)
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InternalServerError, PayloadTooLargeError)
from common.utils.http_exceptions import (BadRequest, ResourceNotFound,
                                          InternalServerError as
                                          InternalServerException,
                                          PayloadTooLarge)
from common.utils.gcs_adapter import GcsCrudService, is_valid_path, upload_file_to_bucket, upload_folder
from common.utils.logging_handler import Logger
from config import (SIGNURL_SA_KEY_PATH, RESOURCE_BASE_PATH,
                    CONTENT_SERVING_BUCKET, ERROR_RESPONSES, DATABASE_PREFIX,
                    VALIDATE_AND_UPLOAD_ZIP, CONTENT_FILE_SIZE,
                    ZIP_EXTRACTION_FOLDER, FAQ_BASE_PATH)

# pylint: disable = line-too-long
# pylint: disable = invalid-name
# pylint: disable = broad-except
router = APIRouter(tags=["Content Serving"], responses=ERROR_RESPONSES)

ALLOWED_CONTENT_VERSION_STATUS = Literal["published", "unpublished", "draft"]

contentValidator = ContentValidator()
fileHandler = FileUtils()

# pylint: disable = unspecified-encoding,consider-using-with


@router.get(
    "/content-serving/list-contents",
    name="List files and Folders at a given prefix",
    response_model=ListFilesAndFolderResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def list_all_files(prefix: Optional[str] = None,
                   list_madcap_contents: Optional[bool] = False):
  try:

    prefix, folders_list, files_list = get_file_and_folder_list(
        prefix, list_madcap_contents)

    return {
        "success": True,
        "message": "Successfully listed all files and folder at given prefix",
        "data": {
            "prefix": prefix,
            "folders": folders_list,
            "files": files_list
        }
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.get(
    "/content-serving/{uuid}",
    response_model=GetSignedUrlModelResponse,
    name="Get Signed URL for video/html5",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_signed_url(uuid: str, is_faq: bool = False, redirect: bool = False):
  """ Generate Signed URL for content based on resource_path
    of a learning_resource or a faq
        ### Args:
        uuid: `str`
            UUID of FAQ/Learning Resource.
        is_faq: `bool`
            This flag determins which collection to be used to
            fetch the resource data
        redirect: `bool`
            Response type for the signed url. Defaults to False.
            If set False, returns a Json response with 200 status code.
            Else returns a redirect with signed url with 307 status code.
        ### Raises:
        ResourceNotFoundException:
            Raised when the requested resource does not exists. <br/>
        Exception 500:
            Internal Server Error. Raised if something went wrong.
        ### Returns:
        Signed URL JSON response: \
        `GetSignedURLModelResponse`
    """
  try:

    BASE_PATH = ""
    resource_type = ""
    resource_path = ""
    if is_faq is True:
      faq_resource = FAQContent.find_by_uuid(uuid)
      faq_resource = faq_resource.get_fields(reformat_datetime=True)
      BASE_PATH = FAQ_BASE_PATH

      if faq_resource["resource_path"] in ["", None]:
        raise ValidationError(
            "Cannot create signed URL for a FAQ without resource_path")

      resource_type = "faq_html"
      resource_path = faq_resource["resource_path"]
    else:
      learning_resource = LearningResource.find_by_id(uuid)
      learning_resource = learning_resource.get_fields(reformat_datetime=True)
      BASE_PATH = RESOURCE_BASE_PATH
      resource_type = learning_resource["type"]

      if learning_resource["type"] == "":
        raise ResourceNotFoundException(
            f"No resource type found for resource with uuid {uuid}")

      resource_path = learning_resource["resource_path"]
      if resource_path == "":
        raise ResourceNotFoundException(
            f"No resource path found for resource with uuid {uuid}")

    gcs_service = GcsCrudService(CONTENT_SERVING_BUCKET, SIGNURL_SA_KEY_PATH)

    actual_path = ""
    if BASE_PATH in resource_path:
      actual_path = resource_path
    else:
      actual_path = f"{BASE_PATH}/{resource_path}"

    path_exists = is_valid_path(f"gs://{CONTENT_SERVING_BUCKET}/{actual_path}")
    if path_exists is True:
      signed_url = gcs_service.generate_url(
          actual_path, 60)

      if redirect is False:
        return {
            "success": True,
            "message": "Successfully fetched the signed url",
            "data": {
                "signed_url": signed_url,
                "resource_type": resource_type,
                "resource_uuid": uuid
            }
        }

      return RedirectResponse(signed_url)

    else:
      raise ResourceNotFoundException(
          "Provided resource path does not exist on GCS bucket")

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e


@router.post(
    "/content-serving/upload/sync",
    response_model=ListFilesAndFolderResponse,
    name="Synchronous Content Upload API",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
async def upload_content_sync(content_file: UploadFile = File(...), is_faq: bool=False):
  """ Upload the learning content and recieve a singed url for preview
        ### Args:
        content_file: `Binary File`
            Binary File object to be uploaded. Always Required.
        is_faq: bool
            If True, the content will be uploaded to faq content folder
            If False, the content will be uploaded to learning resource
                      content folder

        Note: This API is capable of uploading Zips as well as standalone
        content files. But this API does not handle SRL upload.
        ### Raises:
        ResourceNotFoundException:
            Raised when the requested resource does not exists. <br/>
        Exception 500:
            Internal Server Error. Raised if something went wrong.
        ### Returns:
        Signed URL JSON response: \
        `ContentUploadResponse`
    """

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
    file_name_without_ext = file_name[:-(len(file_extension) + 1)]

    if contentValidator.checkExtensionAndContentHeader(
        content_file.content_type, file_extension) is False:
      msg = "Content Type header and file extension does not match. "
      msg += f"Received header contentType: {content_file.content_type}, "
      msg += f"received file extension .{file_extension}"
      raise ValidationError(msg)

    UPLOAD_BASE_PATH = RESOURCE_BASE_PATH
    if is_faq is True:
      UPLOAD_BASE_PATH = FAQ_BASE_PATH
    content_upload_folder = f"{UPLOAD_BASE_PATH}/{file_name_without_ext}"

    if file_extension == "zip":
      # save zip file locally
      await content_file.seek(0)
      content = await content_file.read()

      zipfile_path = pathlib.Path.cwd(
      ) / f"{ZIP_EXTRACTION_FOLDER}/{content_file.filename}"
      zipfile_path.write_bytes(content)

      zipfile_path = f"{ZIP_EXTRACTION_FOLDER}/{content_file.filename}"

      # unzip files to zip_extraction folder
      filename_without_ext = file_name.split(".")[0]
      local_dest_path = f"{ZIP_EXTRACTION_FOLDER}/extracted/{filename_without_ext}"
      fileHandler.unzipPackage(zipfile_path, local_dest_path)

      # recreate zip structure on GCS
      upload_folder(CONTENT_SERVING_BUCKET, local_dest_path,
                    content_upload_folder)

      # Cleanup Temporary Files
      fileHandler.deleteFile(zipfile_path)
      fileHandler.deleteFolder(local_dest_path)

    else:
      # Go to the start of stream by file.seek(0)
      await content_file.seek(0)

      # Upload to GCS
      upload_file_to_bucket(CONTENT_SERVING_BUCKET, content_upload_folder,
                            content_file.filename, content_file.file)

    prefix, folders_list, files_list = get_file_and_folder_list(
        content_upload_folder)

    msg = "Successfully uploaded the learning content"
    if is_faq is True:
      msg = "Successfully uploaded the faq content"
    return {
        "success": True,
        "message": msg,
        "data": {
            "prefix": prefix,
            "folders": folders_list,
            "files": files_list
        }
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except BadZipFile as e:
    print(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.post(
    "/content-serving/upload/async",
    response_model=BatchJobModel,
    name="Asynchronous Content Upload API",
    include_in_schema=False,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
async def upload_content_async(content_file: UploadFile = File(...)):
  """ Upload the learning content and recieve a singed url for preview
        ### Args:
        content_file: `File`
            Binary File object to be uploaded. Always Required.
        ### Raises:
        ResourceNotFoundException:
            Raised when the requested resource does not exists. <br/>
        Exception 500:
            Internal Server Error. Raised if something went wrong.
        ### Returns:
        Signed URL JSON response: \
        `ContentUploadResponse`
    """
  try:
    # check if the valid content type header is set
    if content_file.content_type != "application/zip":
      raise ValidationError("Content Type as application/zip is only supported")

    file_name = content_file.filename
    file_extension = file_name.split(".")[-1]
    file_name_without_ext = file_name[:-(len(file_extension) + 1)]

    if contentValidator.checkExtensionAndContentHeader(
        content_file.content_type, file_extension) is False:
      msg = "Content Type header and file extension does not match. "
      msg += f"Received header contentType: {content_file.content_type}, "
      msg += f"received file extension .{file_extension}"
      raise ValidationError(msg)

    # Go to the start of stream by file.seek(0)
    await content_file.seek(0)
    # upload zip file to gcs bucket
    gsutil_uri = upload_file_to_bucket(
        CONTENT_SERVING_BUCKET,
        f"{RESOURCE_BASE_PATH}/zip/{file_name_without_ext}",
        content_file.filename, content_file.file)

    # create a batch job
    env_vars = {
        "DATABASE_PREFIX": DATABASE_PREFIX,
        "CONTENT_SERVING_BUCKET": CONTENT_SERVING_BUCKET,
        "RESOURCE_BASE_PATH": RESOURCE_BASE_PATH
    }
    input_data = {"gsutil_uri": gsutil_uri, "filename": content_file.filename}

    response = initiate_batch_job(input_data, VALIDATE_AND_UPLOAD_ZIP, env_vars)

    response["data"]["meta_data"] = {
        "message": f"""File will be uploaded at {f"{RESOURCE_BASE_PATH}/{file_name_without_ext}"}"""
    }

    return response

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except BadZipFile as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.put(
    "/content-serving/link/{uuid}",
    name="Link Content to Learning Resource",
    include_in_schema=False,
    response_model=ContentLinkResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def link_content_to_resource(uuid: str, input_data: ContentLinkInputModel):
  """
    This endpoint Links a resource_path with a learning resource.
    The response will contain a content version and a signed url
    for preview.
    ------------------------------------------------
    Input:

    uuid: `str`
    UUID of the learnig resource

    input_data: `dict`
      {
        "resource_path: `str`,
        "type": `str`
      }
  """
  try:
    input_dict = input_data.dict()

    new_content = link_content_and_create_version(uuid,
                                                  input_dict["resource_path"],
                                                  input_dict["type"])

    gcs_service = GcsCrudService(CONTENT_SERVING_BUCKET, SIGNURL_SA_KEY_PATH)
    signed_url = gcs_service.generate_url(
        f"""{RESOURCE_BASE_PATH}/{new_content["resource_path"]}""", 60)

    return {
        "success": True,
        "message": "Successfully linked learning resource with content",
        "data": {
            "signed_url": signed_url,
            "resource_type": new_content["type"],
            "resource_uuid": new_content["uuid"]
        }
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.put(
    "/content-serving/publish/{uuid}",
    response_model=ContentPublishResponse,
    include_in_schema=False,
    name="Publish content",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
async def publish_content_handler(uuid: str, target_version_uuid: str = None):
  """ Upload the learning content and recieve a singed url for preview
        ### Args:
          uuid: `str`
            UUID of the learning resource that is connected to the
            learning hierarchy
          target_version_uuid: `str`
            UUID of the target version of the content to be published
    """

  try:

    _ = LearningResource.find_by_id(uuid)

    published_doc_dict = handle_publish_event(uuid, target_version_uuid)

    gcs_service = GcsCrudService(CONTENT_SERVING_BUCKET, SIGNURL_SA_KEY_PATH)
    signed_url = gcs_service.generate_url(
        f"""{RESOURCE_BASE_PATH}/{published_doc_dict["resource_path"]}""", 60)

    return {
        "success": True,
        "message": "Successfully published content",
        "data": {
            "signed_url": signed_url,
            "resource_type": published_doc_dict["type"],
            "resource_uuid": published_doc_dict["uuid"]
        }
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.get(
    "/content-serving/content-versions/{uuid}",
    name="List all content versions for a resource",
    response_model=GetContentVersionsResponse,
    include_in_schema=False,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def list_content_versions(uuid: str,
                          skip: int = 0,
                          limit: int = 5,
                          status: ALLOWED_CONTENT_VERSION_STATUS = None):
  """
    This endpoint returns a list of content versions available for a
    give Learning Resource UUID.
    ------------------------------------------------
    Input:

    uuid: `str`
    UUID of the learnig resource
  """
  try:
    content_versions_list = get_content_versions(uuid, status, skip, limit)
    return {
        "success": True,
        "message": "Successfully fetched content version for learning resource",
        "data": content_versions_list
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.post(
    "/content-serving/upload/madcap/{le_uuid}",
    response_model=ListFilesAndFolderResponse,
    name="Synchronous Content Upload API for Madcap",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
async def upload_madcap_export(le_uuid: str,
                               is_srl: bool = False,
                               content_file: UploadFile = File(...)):

  try:

    # check file size
    if len(await content_file.read()) > CONTENT_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {content_file.filename}")

    learning_experience = LearningExperience.find_by_id(le_uuid)

    # check if the valid content type header is set
    if content_file.content_type not in ["application/zip","application/x-zip-compressed"]:
      raise ValidationError(
          f"Only content_type: application/zip or application/x-zip-compressed is allowed. Received content_type: {content_file.content_type}"
      )

    file_name = content_file.filename
    file_extension = file_name.split(".")[-1]
    file_name_without_ext = file_name[:-(len(file_extension) + 1)]

    if is_srl is True and file_name_without_ext[0:3] != "SRL":
      raise ValidationError(
          """File name should start with the prefix "SRL". eg: "SRL_file_1.zip" """
      )

    if contentValidator.checkExtensionAndContentHeader(
        content_file.content_type, file_extension) is False:
      msg = "Content Type header and file extension does not match. "
      msg += f"Received header contentType: {content_file.content_type}, "
      msg += f"received file extension .{file_extension}"
      raise ValidationError(msg)

    content_upload_folder = f"{RESOURCE_BASE_PATH}/{file_name_without_ext}"

    # save zip file locally
    await content_file.seek(0)
    content = await content_file.read()

    zipfile_path = pathlib.Path.cwd(
    ) / f"{ZIP_EXTRACTION_FOLDER}/{content_file.filename}"
    zipfile_path.write_bytes(content)

    zipfile_path = f"{ZIP_EXTRACTION_FOLDER}/{content_file.filename}"

    # unzip files to zip_extraction folder
    filename_without_ext = file_name.split(".")[0]
    local_dest_path = f"{ZIP_EXTRACTION_FOLDER}/extracted/{filename_without_ext}"
    fileHandler.unzipPackage(zipfile_path, local_dest_path)

    flag_1, err_msg_1 = contentValidator.isValidMadcapExport(
        folder_path=local_dest_path,
        folder_name=filename_without_ext,
        check_srl=is_srl)

    if flag_1 is False:
      raise ValidationError(err_msg_1)

    is_update_lr_required = False
    if is_srl is False:
      if learning_experience.resource_path != "":
        is_update_lr_required = True
        # override only if all the file names map 1:1
        flag_2, err_msg_2 = is_missing_linked_files(
            local_dest_path, learning_experience.resource_path)
        if flag_2 is False:
          raise ValidationError(err_msg_2)
    else:
      if learning_experience.srl_resource_path != "":
        is_update_lr_required = True
        # override only if all the file names map 1:1
        flag_2, err_msg_2 = is_missing_linked_files(local_dest_path,
                                    learning_experience.srl_resource_path)
        if flag_2 is False:
          raise ValidationError(err_msg_2)

    # recreate zip structure on GCS
    upload_folder(CONTENT_SERVING_BUCKET, local_dest_path,
                  content_upload_folder)

    # Cleanup Temporary Files
    fileHandler.deleteFile(zipfile_path)
    fileHandler.deleteFolder(local_dest_path)

    prefix, folders_list, files_list = get_file_and_folder_list(
        content_upload_folder, True)

    if is_srl is False:
      # Add resource_path to the Learning Experience
      learning_experience.resource_path = prefix
      learning_experience.update()
    else:
      learning_experience.srl_resource_path = prefix
      learning_experience.update()

    # Update links of child Learning Resources
    if is_update_lr_required is True:
      if is_srl is False:
        _, _, new_file_paths = get_file_and_folder_list(
            learning_experience.resource_path, True)
        update_lr_resource_path(learning_experience.uuid, new_file_paths)

    if is_srl is False:
      return {
          "success": True,
          "message": f"Successfully uploaded the content for learning experience with uuid {le_uuid}",
          "data": {
              "prefix": prefix,
              "folders": folders_list,
              "files": files_list
          }
      }

    # Provide SRL access to all Sibling LE
    le_siblings = link_srl_to_all_le(le_uuid, prefix)

    for le_dict in le_siblings:
      if is_update_lr_required is True:
        _, _, new_file_paths = get_file_and_folder_list(
            prefix, True)
        # Update resource paths for all LRs
        update_lr_resource_path(le_dict["uuid"], new_file_paths)

    return {
        "success": True,
        "message": f"Successfully uploaded the SRL content for learning experience with uuid {le_uuid}",
        "data": {
            "prefix": prefix,
            "folders": folders_list,
            "files": files_list
        }
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except BadZipFile as e:
    print(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


@router.post(
    "/content-serving/link/madcap/{le_uuid}/{lr_uuid}",
    name="Link Madcap Content to Learning Resource",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
async def link_madcap_to_lr(
    le_uuid: str,
    lr_uuid: str,
    input_json: ContentLinkInputModel,
    is_srl: bool = False,
):
  try:
    input_dict = input_json.dict()
    resource_path = input_dict["resource_path"]
    resource_type = input_dict["type"]

    link_content_to_lr(le_uuid, lr_uuid, resource_path, resource_type, is_srl)

    return {
        "success": True,
        "message": f"Successfully linked content to Learning Resource with uuid {lr_uuid}"
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e
