""" extraction endpoints """

from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from common.utils.gcs_adapter import is_valid_path
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from schemas.extraction_schema import (BasicExtractionInputModel,
                                      PostExtractionResponseModel)
from services.extraction.extract_entities import extract_entities
from services.extraction.config import DOCAI_ENTITY_MAPPING
from services.extraction.utils_functions import (save_prior_experience_items,
                                                get_doc_type)
from config import ERROR_RESPONSES


router = APIRouter(
    tags=["Extraction"],
    responses=ERROR_RESPONSES)

@router.post(
    "/extract",
    response_model=PostExtractionResponseModel,
    name="Extract Prior Experiences")
async def extraction(input_doc_data: BasicExtractionInputModel):
  """
  Extracts the document with given gcs_uri and doc_class
    Args:
      doc_class (str): class of document - transcript or others
      doc_type (str): Document type- pdf or xlsx or png, etc)
      context (str): Additional info that might help- like organsiation
                      name/degree type etc
      gcs_url (str): location of the document/transcript uploaded
    Returns:
      200 : PDF files are successfully classified and database updated
      500 : HTTPException: 500 Internal Server Error if something fails
      422 : Input validation error
  """
  try:
    input_doc_data_dict = {**input_doc_data.dict()}
    context = input_doc_data_dict["context"]
    doc_class = input_doc_data_dict["doc_class"]
    gcs_url_list = input_doc_data_dict["gcs_urls"]
    # validations
    if context not in DOCAI_ENTITY_MAPPING.keys():
      raise ValidationError(f"Invalid context: {context}. Allowed context are: "
        f"{list(DOCAI_ENTITY_MAPPING.keys())}")
    if doc_class not in DOCAI_ENTITY_MAPPING[context].keys():
      raise ValidationError(f"Invalid doc_class: {doc_class}. Allowed doc_class"
        f" are: {list(DOCAI_ENTITY_MAPPING[context].keys())}")
    for path in gcs_url_list:
      if not is_valid_path(path):
        raise ResourceNotFoundException(
          "Could not find the file. Please check the gcs_url")
    doc_types = get_doc_type(gcs_url_list)
    for doc_type in doc_types:
      if doc_type not in ["pdf"]:
        raise ValidationError(f"Invalid document type: {doc_type}."
          f" Supported types are: pdf")
    extraction_output = await run_in_threadpool(
      extract_entities, gcs_url_list, doc_class, context)
    #check if extract_entities returned None when parser not available
    if extraction_output:
      save_prior_experience_items(extraction_output)
      return {
      "success": True,
      "message": "Successfully parsed the transcript",
      "data": extraction_output
    }
    else:
      return {
      "success": True,
      "message": "Successfully parsed the transcript but no data was extracted"
                  "since relevant fields were not found",
      "data": []
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
