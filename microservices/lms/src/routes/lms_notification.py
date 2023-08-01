"""
Script to replay messages to lms pub/sub
"""
import traceback
from fastapi import APIRouter, BackgroundTasks
from google.cloud import pubsub_v1
from common.utils.bq_helper import run_query
from common.utils.logging_handler import Logger
from common.utils.errors import (ValidationError)
from common.utils.http_exceptions import (InternalServerError, BadRequest, Conflict)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.lms_notification import ReplayNotificationResponseModel, InputReplayNotificationModel
from config import BQ_TABLE_DICT, BQ_DATASET, PROJECT_ID, DATABASE_PREFIX

TABLE_ID = (f"`{PROJECT_ID}.{BQ_DATASET}."
            + f"{BQ_TABLE_DICT['BQ_NOTIFICATION_TABLE']}`")

router = APIRouter(prefix="/lms-notifications",
                                    tags=["Notification"],
                                    responses={
                                        500: {
                                            "model":
                                            InternalServerErrorResponseModel
                                        },
                                        409: {
                                            "model": ConflictResponseModel
                                        },
                                        422: {
                                            "model":
                                            ValidationErrorResponseModel
                                        }
                                    })


@router.post("/replay",response_model=ReplayNotificationResponseModel,
             status_code=202)
def replay_notifications(input_dates: InputReplayNotificationModel,
                         background_tasks: BackgroundTasks):
  """Create a Cohort endpoint
      Args:
          input_dates (InputReplayNotificationModel): input dates to filter
          notifications

      Raises:
          Exception: 500 Internal Server Error if something went wrong
          Exception: 422 Unprocessable Entity if input date is invalid(ie. 
          not a timestamp)
      Returns:
          ReplayNotificationResponseModel: On successful publish of messages
  """
  try:
    input_dates_dict = {**input_dates.dict()}
    start_date = input_dates_dict.get("start_date")
    end_date = input_dates_dict.get("end_date")
    if bool(start_date) & bool(end_date) & (start_date <= end_date):
      background_tasks.add_task(
        publish_messages,
        start_date, end_date
      )
      return {
      "message": "Successfully started publish messages backgrund task",
      "data": None
      }

    raise ValidationError("input dates are invalid or start_date is greater"
                          +" than end_date")
  except Conflict as conflict:
    Logger.error(conflict)
    raise Conflict(str(conflict)) from conflict
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


def publish_messages(start_date, end_date):
  """Utility funcition will publish messages
  Args: start_date and end_date datetime timetsamp
  """
  try:
    query=f"""Select * from {TABLE_ID}
        WHERE publish_time >= timestamp("{start_date}")
        AND publish_time <= timestamp("{end_date}")"""
    result = run_query(query)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID,
                                      (DATABASE_PREFIX + "lms-notifications"))
    Logger.info("Publish messages background task has been started")
    for row in result:
      row = dict(row)
      result = publisher.publish(topic_path,
                              data=row["data"].encode("utf-8"),
                              store_to_bq="false")
      if result:
        Logger.info(
          f"successfully pushed message {row['message_id']} to pub/sub")
      else:
        Logger.info(
          f"Failed to push message {row['message_id']} to pub/sub")

    Logger.info("Publish messages background task has been completed")

  except Conflict as conflict:
    Logger.error(conflict)
    raise Conflict(str(conflict)) from conflict
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
