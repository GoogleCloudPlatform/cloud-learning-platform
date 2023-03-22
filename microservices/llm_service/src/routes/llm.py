""" LLM endpoints """
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.utils.logging_handler import Logger
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.assessment_schema import (LLMModel, LLMGenerateResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["LLMs"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.post("/llm_service/generate", response_model=LLMGenerateResponse)
def generate(prompt: Required[str] = "", config: Optional[dict] = {}):
  """
  Generate text with an LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse: 
  """
  result = []
  if prompt:

    return {
        "success": True,
        "message": "Successfully generated text",
        "data": result
    }
  else:
    return BadRequest("Missing or invalid request parameters")

