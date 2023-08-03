"""Dummy routers for testing"""
import base64
import json
from fastapi import APIRouter, Depends, Request
from common.utils.logging_handler import Logger
from utils.pub_sub_auth import validate_pub_sub_token
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)

router = APIRouter(prefix="/lms/api/test",
                   tags=["Dummy"],
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

@router.post("/webhook",
          dependencies=[Depends(validate_pub_sub_token)])
async def pub_sub_webhook(request: Request):
  """_summary_

  Args:
      request (Request): _description_

  Returns:
      _type_: _description_
  """
  data = await request.json()
  data["message"]["data"] = json.loads(
      base64.b64decode(data["message"]["data"]).decode("utf-8"))
  Logger.info(f"decoded data:{data}")
  return {}
