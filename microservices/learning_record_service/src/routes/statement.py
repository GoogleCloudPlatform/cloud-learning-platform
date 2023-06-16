""" xAPI Statement endpoints """
import traceback
from datetime import datetime
import json
from uuid import uuid4
from fastapi import APIRouter, Request, Query
from typing import List
from requests.exceptions import ConnectTimeout
from common.models import Verb, Agent, Session
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, ConnectionTimeout)
from common.utils.logging_handler import Logger
from common.utils.collection_references import collection_references
from utils.bq_handler import (insert_data_to_bq, fetch_data_using_query_from_bq)
from schemas.statement_schema import (GetAllStatementsResponseModel,
                                      LRSDetailsResponseModel,
                                      GetStatementResponseModel,
                                      InputStatementsModel,
                                      PostStatementsResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  ConnectionTimeoutResponseModel)
# pylint: disable = unused-import
from config import PROJECT_ID, BQ_LRS_TABLE, BQ_LRS_DATASET, ERROR_RESPONSES

# pylint: disable = broad-except, line-too-long, bare-except

router = APIRouter(tags=["xAPI Statement"], responses=ERROR_RESPONSES)


@router.get("/about", response_model=LRSDetailsResponseModel)
def get_details_about_lrs():
  """
  Get details endpoint will fetch the details about Learning Record Store

  Returns:
    AboutResponseModel: About Response Object
  """
  try:
    # Details to be fetched about the LRS
    lrs_details = {"version": "1.0.3"}

    return {
        "success": True,
        "message": "Successfully fetched the details about LRS",
        "data": lrs_details
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/statement/{uuid}",
    response_model=GetStatementResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    response_model_exclude_none=True)
def get_xapi_statement(uuid: str):
  """
  Get xAPI statement fetches the statement with the given id from the LRS

  Args:
    uuid (str): Unique id of the xAPI statement to be fetched

  Returns:
    GetStatementResponseModel: xAPI Statement Object
  """
  try:
    # Query of the xAPI statement to be fetched from the LRS
    query = f"""SELECT * FROM `{PROJECT_ID}.{BQ_LRS_DATASET}.{BQ_LRS_TABLE}` \
      WHERE uuid = '{uuid}'"""
    final_output = fetch_data_using_query_from_bq(query)

    if final_output:
      final_output = final_output[0]

      final_output["context"] = json.loads(final_output["context"])
      final_output["result"] = json.loads(final_output["result"])
      final_output["authority"] = json.loads(final_output["authority"])
      final_output["verb"]["canonical_data"] = json.loads(
          final_output["verb"]["canonical_data"])
      final_output["object"]["canonical_data"] = json.loads(
          final_output["object"]["canonical_data"])
      final_output["stored"] = final_output["stored"].strftime(
          "%Y-%m-%d %H:%M:%S %z")
      final_output["timestamp"] = final_output["timestamp"].strftime(
          "%Y-%m-%d %H:%M:%S %z")
    else:
      raise ResourceNotFoundException(f"xAPI Statement with '{uuid}' not found")
    return {
        "success": True,
        "message": "Successfully fetched the statement",
        "data": final_output
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/statements",
    response_model=GetAllStatementsResponseModel,
    responses={422: {
        "model": ValidationErrorResponseModel
    }},
    response_model_exclude_none=True)
def get_all_xapi_statements(agent_uuid: str = None,
                            verb_name: str = None,
                            object_name: str = None,
                            skip: int = Query(0, ge=0, le=2000),
                            limit: int = Query(10, ge=1, le=100)
):
  """
  Get all xAPI statements fetches the statements with the provide filters
  from the LRS

  Args:
    agent (str): JSON encoded object containing an IFI to match an
                  agent or group
    verb (str): String matching the statement's verb identifier
    activity (str): String matching the statement's activity identifier
    skip (int): No of xAPI statements to be skipped
    limit (int): Size of xAPI statements array to be returned

  Returns:
    GetAllStatementsResponseModel: List of xAPI Statement Objects
  """
  try:
    where_clause = ""
    if agent_uuid or verb_name or object_name:
      where_clause = "WHERE "

    if agent_uuid:
      where_clause = where_clause + f" actor.uuid = '{agent_uuid}'"
    if verb_name:
      where_clause = where_clause + f" {'And' if agent_uuid else ''}\
         verb.name = '{verb_name}'"

    if object_name:
      where_clause = where_clause + f"{'And' if agent_uuid or verb_name else ''}\
         object.name = '{object_name}'"

    query = f"""
    SELECT * 
    FROM `{PROJECT_ID}.{BQ_LRS_DATASET}.{BQ_LRS_TABLE}` {where_clause}
    ORDER BY stored DESC
    LIMIT {limit} OFFSET {skip}
    """

    final_output = fetch_data_using_query_from_bq(query)
    for each_row in final_output:
      each_row["context"] = json.loads(each_row["context"])
      each_row["result"] = json.loads(each_row["result"])
      each_row["authority"] = json.loads(each_row["authority"])
      each_row["verb"]["canonical_data"] = json.loads(
          each_row["verb"]["canonical_data"])
      each_row["object"]["canonical_data"] = json.loads(
          each_row["object"]["canonical_data"])
      each_row["stored"] = each_row["stored"].strftime("%Y-%m-%d %H:%M:%S %z")
      each_row["timestamp"] = each_row["timestamp"].strftime(
          "%Y-%m-%d %H:%M:%S %z")
    return {
        "success": True,
        "message": "Successfully fetched the statements",
        "data": final_output
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


def post_process_statement(statement):
  """Post Process the statement"""

  statement["object"]["canonical_data"] = json.dumps(statement["object"].get(
      "canonical_data", {}))
  statement["uuid"] = str(uuid4())
  statement["stored"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f %z")
  if not statement.get("timestamp"):
    statement["timestamp"] = statement["stored"]
  return statement

@router.post(
    "/statements",
    response_model=PostStatementsResponseModel,
    responses={
        404: {
            "model": NotFoundErrorResponseModel
        },
        408: {
            "model": ConnectionTimeoutResponseModel
        }
    })

def post_xapi_statements(req: Request,
                         input_statements: List[InputStatementsModel]):
  """
  Post xAPI statements will insert the input statements to the LRS

  Args:
    input_statements (InputStatementsModel): Required body of the
      input statements to be inserted to the LRS

  Returns:
    PostStatementsResponseModel: List of inserted statements unique ids
  """
  try:
    _ = {"Authorization": req.headers.get("authorization")}
    # xAPI statements need to be inserted into the LRS
    rows_to_be_inserted = []
    incoming_statements = [i.dict(exclude_none=True) for i in input_statements]
    output_resp = []
    for each_statement in incoming_statements:
      # Validation for Agent uuid
      Agent.find_by_uuid(each_statement["actor"]["uuid"])
      # Validation for verb
      verb_name = each_statement["verb"]["name"]
      if not Verb.find_by_name(verb_name):
        raise ResourceNotFoundException(
        f"Verb with given name {verb_name} is not found"
        )
      # Validation for activity
      collection_references[each_statement["object_type"]].find_by_uuid(
        each_statement["object"]["uuid"]
      )

      # Validation for session
      Session.find_by_uuid(each_statement["session_id"])

      #process statement json
      each_statement["context"] = json.dumps(each_statement.get("context", {}))
      each_statement["result"] = json.dumps(each_statement.get("result", {}))
      each_statement["authority"] = json.dumps(
          each_statement.get("authority", {}))
      each_statement["verb"]["canonical_data"] = json.dumps(
          each_statement["verb"].get("canonical_data", {}))

      each_statement = post_process_statement(each_statement)
      output_resp.append(each_statement["uuid"])

      rows_to_be_inserted.append(each_statement)

    Logger.info("Inserting Data to BigQuery")
    insert_data_to_bq(BQ_LRS_TABLE, rows_to_be_inserted)

    return {
        "success": True,
        "message": "Successfully added the given statement/s",
        "data": output_resp
    }

  except ConnectTimeout as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ConnectionTimeout(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
