"""
  Endpoints related to DKT training
"""
import traceback
from fastapi import APIRouter  #, HTTPException
from schemas.dkt_schema import (TrainDKTRequest, TrainDKTResponse,
                                CreateDataDKTRequest, CreateDataDKTResponse,
                                PredictDKTRequest,InferenceDKTRequest,
                                PredictDKTResponse)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from services.create_fake_data import generate_dkt_data
from services.inference import Inference
from services.batch_job import initiate_batch_job
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from config import DKT_JOB_TYPE

router = APIRouter(
    prefix="",
    tags=["Deep Knowledge Tracing"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get("/fake_data/",include_in_schema=False)
def test_fake_data():
  return {"success": True, "message": "Successfully test fake data route"}


@router.post("/fake_data/",
include_in_schema=False, response_model=CreateDataDKTResponse)
def create_fake_data(request_body: CreateDataDKTRequest):
  try:
    generate_dkt_data(request_body.num_users, request_body.num_lus,
                      request_body.item_type)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"success": True, "message": "Successfully generated fake data"}


@router.post("/train/", response_model=TrainDKTResponse)
def train_dkt(request_body: TrainDKTRequest):
  """Starts training DKT model for a given course"""
  try:
    request_body = request_body.__dict__
    response = initiate_batch_job(request_body,
                                  DKT_JOB_TYPE)
    Logger.info(response)
    return response
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post("/inference/",
 response_model=PredictDKTResponse)
def inference_dkt(request_body: InferenceDKTRequest):
  try:
    response = Inference.predict(
        course_id=request_body.course_id,
        user_id=request_body.user_id,
        user_events = request_body.user_events, session_id = None)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully generated predictions from dkt model",
      "data": response
  }

@router.post("/predict/",include_in_schema=False,
 response_model=PredictDKTResponse)
def predict_dkt(request_body: PredictDKTRequest):
  try:
    response = Inference.predict(
        course_id=request_body.course_id,
        user_id=request_body.user_id, user_events = None,
        session_id=request_body.session_id)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully generated predictions from dkt model",
      "data": response
  }
