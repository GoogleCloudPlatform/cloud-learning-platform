""" Assessment endpoints """
import traceback
import copy
from typing import Optional
from typing_extensions import Literal
from fastapi import APIRouter, UploadFile, File, Query, Request
from common.models import Assessment, LearningResource, LearningObject, Skill,Rubric
from common.utils.logging_handler import Logger
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.rest_method import put_method
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.assessment_schema import (BasicAssessmentModel,
                                       AssessmentsImportJsonResponse,
                                       AssessmentModel, AssessmentModelResponse,
                                       UpdateAssessmentModel, DeleteAssessment,
                                       HumanGradedAssessmentModel,
                                       AssessmentSearchModelResponse,
                                       AssessmentTypesResponse,
                                       AllAssessmentsModelResponse,
                                       AssessmentLinkResponse)
from schemas.rubric_criterion_schema import BasicRubricCriterionModel,UpdateRubricCriterionModel
from schemas.rubric_schema import RubricModel,UpdateRubricModel
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from services.data_utils import fetch_metadata
from services.rubric import create_rubric, update_rubric
from services.rubric_criteria import create_rubric_criterion, update_rubric_criterion
from services.assessment_content_helper import attach_files_to_assessment
from services.collection_handler import CollectionHandler
from config import (PAYLOAD_FILE_SIZE, ERROR_RESPONSES, CONTENT_SERVING_BUCKET,
                    USE_LEARNOSITY_SECRET, SERVICES,
                    AUTHORED_ASSESSMENT_TYPES)

router = APIRouter(tags=["Assessments"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.get("/assessment/search", response_model=AssessmentSearchModelResponse)
def search_assessment(name: Optional[str] = None):
  """
  Search for assessment based on the name

  Args:
      name(str): Name of the assessment. Defaults to None.

  Returns:
      AssessmentSearchModelResponse: List of assessment objects
  """
  result = []
  if name:
    # fetch assessment that matches name
    name_node_items = Assessment.find_by_name(name)
    if name_node_items:
      result = [
          name_node_item.get_fields(reformat_datetime=True)
          for name_node_item in name_node_items
      ]
    return {
        "success": True,
        "message": "Successfully fetched the assessment",
        "data": result
    }
  else:
    return BadRequest("Missing or invalid request parameters")


@router.get("/assessment/types", response_model=AssessmentTypesResponse)
def get_assessment_types():
  """
  Search for assessment based on the name

  Args:
      name(str): Name of the assessment. Defaults to None.

  Returns:
      AssessmentSearchModelResponse: List of assessment objects
  """
  return {
      "success": True,
      "message": "Successfully fetched the assessment types",
      "data": AUTHORED_ASSESSMENT_TYPES
  }


@router.get("/assessments", response_model=AllAssessmentsModelResponse)
def get_assessments(skip: int = Query(0, ge=0, le=2000),
                    limit: int = Query(10, ge=1, le=100),
                    sort_by: Optional[str] = "created_time",
                    sort_order: Optional[Literal["ascending", "descending"]] =
                    "descending",
                    search: Optional[str] = None):
  """The get assessments endpoint will return an array assessments
    from firestore

    Args:
        skip (int): Number of objects to be skipped
        limit (int): Size of assessment array to be returned
        sort_by (str): Data Model Fields name
        sort_order (str): ascending/descending
        search_query (str)

    Raises:
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        AllAssessmentsModelResponse: Array of Assessment Item Object
    """
  try:
    collection_manager = Assessment.collection
    fetch_length = skip + limit
    data = collection_manager.order(f"{sort_by}").fetch() \
      if sort_order == "ascending" else collection_manager.order(
      f"-{sort_by}").fetch()

    assessments = [CollectionHandler.loads_field_data_from_collection(
        i.get_fields(reformat_datetime=True)) for i in data]

    filtered_assessments = [] if search else assessments

    if search and len(search):
      for assessment in assessments:
        if search.lower() in assessment["name"].lower():
          filtered_assessments.append(assessment)
        elif search.lower() in assessment["type"].lower():
          filtered_assessments.append(assessment)
        elif assessment["references"].get("competencies"):
          filtered_assessments.append(assessment)
        elif assessment["references"].get("skills"):
          filtered_assessments.append(assessment)

      for assessment in filtered_assessments:
        modified_competencies = []
        modified_skills = []
        for competency in assessment["references"]["competencies"]:
          modified_competency = {
            "uuid": competency["uuid"],
            "name": competency["title"]
          }
          modified_competencies.append(modified_competency)
        assessment["references"]["competencies"] = modified_competencies
        for skill in assessment["references"]["skills"]:
          modified_skill = {"uuid": skill["uuid"], "name": skill["name"]}
          modified_skills.append(modified_skill)
        assessment["references"]["skills"] = modified_skills

    count = 10000
    response = {
      "records": filtered_assessments[skip:fetch_length],
      "total_count": count
    }
    return {
        "success": True,
        "message": "Successfully fetched the assessments",
        "data": response
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/assessment/{uuid}",
    response_model=AssessmentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_assessment(uuid: str, fetch_tree: bool = False):
  """The get assessment endpoint will return the assessment from
    firestore of which uuid is provided

    Args:
        uuid (str): Unique identifier for assessment
        fetch_tree (bool): Flag to determine whether or not to
        load the child_nodes data in the response

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        AssessmentModel: Assessment Object
    """
  try:
    assessment = Assessment.find_by_id(uuid)
    assessment = assessment.get_fields(reformat_datetime=True)
    if fetch_tree:
      assessment = ParentChildNodesHandler.load_child_nodes_data(
          assessment)
    return {
        "success": True,
        "message": "Successfully fetched the assessment",
        "data": assessment
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/assessment", response_model=AssessmentModelResponse)
def create_assessment(input_assessment: AssessmentModel):
  """The create assessment endpoint will add the assessment to the
    firestore if it does not exist.If the assessment exist then it will
    update the assessment.

    Args:
        input_assessment (AssessmentModel): input assessment to be inserted

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        str: UUID(Unique identifier for assessment)
    """
  try:

    input_assessment_dict = {**input_assessment.dict()}

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_assessment_dict)

    if USE_LEARNOSITY_SECRET:
      input_assessment_dict = fetch_metadata(input_assessment_dict)

    if input_assessment_dict.get("is_autogradable", False) is True:
      max_attempts = None
    else:
      max_attempts = input_assessment_dict.get("max_attempts", None)
    input_assessment_dict["max_attempts"] = max_attempts

    new_assessment = Assessment()
    new_assessment = new_assessment.from_dict(input_assessment_dict)
    new_assessment.uuid = ""

    new_assessment.save()
    new_assessment.uuid = new_assessment.id
    new_assessment.update()
    assessment_fields = new_assessment.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        assessment_fields, Assessment, operation="add")
    ParentChildNodesHandler.update_parent_references(
        assessment_fields, Assessment, operation="add")

    return {
        "success": True,
        "message": "Successfully created the assessment",
        "data": assessment_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/assessment/{uuid}",
    response_model=AssessmentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_assessment(uuid: str, input_assessment: UpdateAssessmentModel):
  """Update a assessment

    Args:
        input_assessment (AssessmentModel): Required body of
        assessment

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        JSON: Success/Fail Message
    """
  try:

    input_assessment_dict = {**input_assessment.dict()}
    if USE_LEARNOSITY_SECRET:
      input_assessment_dict = fetch_metadata(input_assessment_dict)
    assessment_fields = CommonAPIHandler.update_document(
        Assessment, uuid, input_assessment_dict)

    return {
        "success": True,
        "message": "Successfully updated the assessment",
        "data": assessment_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/assessment/{uuid}",
    response_model=DeleteAssessment,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_assessment(uuid: str):
  """Delete a assessment from firestore

    Args:
        uuid (str): Unique id of the assessment

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        JSON: Success/Fail Message
    """
  try:
    assessment = Assessment.find_by_id(uuid)
    assessment_fields = assessment.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        assessment_fields)
    ParentChildNodesHandler.update_child_references(
        assessment_fields, Assessment, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        assessment_fields, Assessment, operation="remove")

    Assessment.delete_by_uuid(assessment.uuid)

    return {"success": True, "message": "Successfully deleted the assessment"}
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post(
    "/assessment/import/json",
    response_model=AssessmentsImportJsonResponse,
    name="Import Assessment Items from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_assessments(json_file: UploadFile = File(...)):
  """Create assessments from json file

  Args:
    json_file (UploadFile): Upload json file consisting of assessments.
    json_schema should match AssessmentModel

  Raises:
    Exception: 500 Internal Server Error if something fails
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {json_file.filename}")
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicAssessmentModel,
        model_obj=Assessment,
        object_name="assessment")
    return final_output
  except PayloadTooLargeError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post("/assessment/human-graded", response_model=AssessmentModelResponse)
def create_human_graded_assessment(input_assessment:HumanGradedAssessmentModel):
  """The create assessment endpoint will add the assessment to the
    firestore if it does not exist.If the assessment exist then it will
    update the assessment.
    Additionally, for these human graded assessments it creates the rubrics
    and rubric criterion and established the aprent child relationship

    Args:
        input_assessment (HumanGradedAssessmentModel): input human graded
        assessment to be inserted

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        str: UUID(Unique identifier for assessment)
    """
  try:

    input_assessment_dict = {**input_assessment.dict()}
    resource_paths = input_assessment_dict.get("resource_paths")
    author_id = input_assessment_dict.get("author_id")

    rubrics_list = input_assessment_dict["child_nodes"]["rubrics"]
    performance_indicators = []
    #Creation of rubric_criteria
    #Parse the dictionary to create the rubric criterion(leaf_node)
    performance_indicators = []
    for rubric_index in range(0,len(rubrics_list)):
      rubric = rubrics_list[rubric_index]
      #Validating the schema of rubric datamodel
      RubricModel(**rubric)
      rubric_criteria_list = rubric["child_nodes"]["rubric_criteria"]
      for index in range(0,len(rubric_criteria_list)):
        rc_data = {**rubric_criteria_list[index]}
        performance_indicators.extend(rc_data.get("performance_indicators", []))
        rubric_criteria_create_req =\
          BasicRubricCriterionModel(**rubric_criteria_list[index])
        rubric_create_response = \
          create_rubric_criterion(rubric_criteria_create_req)
        #Replacing the rubric dictionary with child_nodes uuid
        rubric["child_nodes"]["rubric_criteria"][index] =\
          rubric_create_response["data"]["uuid"]

      rubric_create_req = RubricModel(**rubric)
      rubric_create_response = create_rubric(rubric_create_req)
      rubrics_list[rubric_index] = rubric_create_response["data"]["uuid"]

    #Updating the input_assessment_request with child_node uuids
    input_assessment_dict["child_nodes"]["rubrics"] = rubrics_list

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_assessment_dict)

    if input_assessment_dict.get("type") == "project":
      input_assessment_dict["max_attempts"] = 3
    else:
      input_assessment_dict["max_attempts"] = 1
    new_assessment = Assessment()
    new_assessment = new_assessment.from_dict(input_assessment_dict)
    new_assessment.uuid = ""
    # Validate if the skill ID exists in Firestore DB
    for skill_id in performance_indicators:
      _ = Skill.find_by_id(skill_id)
    references = new_assessment.references
    references["skills"] = performance_indicators
    new_assessment.references = references

    new_assessment.save()
    new_assessment.uuid = new_assessment.id
    if resource_paths and author_id:
      updated_resource_paths = attach_files_to_assessment(author_id,
          new_assessment.id, resource_paths, CONTENT_SERVING_BUCKET)
      new_assessment.resource_paths = updated_resource_paths
    new_assessment.update()
    assessment_fields = new_assessment.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        assessment_fields, Assessment, operation="add")
    ParentChildNodesHandler.update_parent_references(
        assessment_fields, Assessment, operation="add")

    return {
        "success": True,
        "message": "Successfully created the assessment",
        "data": assessment_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.put(
    "/assessment/replace/{old_assessment_id}",
    name="Link real assessment to placeholder assessment",
    response_model=AssessmentLinkResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def replace_old_assessment(new_assessment_id: str,old_assessment_id: str,
                                   request: Request):
  """
    This endpoint replaces the old assessment with the new assessment,
    and upates the hierarchy along with the subsequent nodes.
    ------------------------------------------------
    Input:

    old_assessment_id: `str`
    UUID of the original(placeholder) assessment

    new_assessment_id: `str`
    UUID of the new authored assessment
  """
  try:
    #Fetch the details of the placeholder assessment
    placeholder_assessment_data=get_assessment(old_assessment_id)["data"]
    # update_dict = source_data.copy()

    #Required fields to be updated
    update_dict={}
    update_dict["parent_nodes"]=placeholder_assessment_data["parent_nodes"]
    update_dict["order"]=placeholder_assessment_data["order"]
    update_dict["prerequisites"]=placeholder_assessment_data["prerequisites"]

    update_data= UpdateAssessmentModel(**update_dict)

    #Update the authored assessment
    update_assessment(new_assessment_id,update_data)

    #Identify the nodes to update the node pre-reqs
    if "learning_objects" in placeholder_assessment_data["parent_nodes"]:
      if placeholder_assessment_data["parent_nodes"]["learning_objects"]:
        parent_node_uuid =\
          placeholder_assessment_data["parent_nodes"]["learning_objects"][0]
        parent_node_data = LearningObject.find_by_id(parent_node_uuid).to_dict()

        neighbour_nodes=parent_node_data["child_nodes"]

        #Check the neighboruing learning_resource nodes
        if "learning_resources" in neighbour_nodes:
          dependent_lr_nodes = neighbour_nodes["learning_resources"]
          for lr in dependent_lr_nodes:
            lr_data=LearningResource.find_by_id(lr).to_dict()
            if lr_data["order"]>placeholder_assessment_data["order"]:
              for i in range(len(lr_data["prerequisites"]["assessments"])):
                if lr_data["prerequisites"]["assessments"][i] ==\
                  old_assessment_id:
                  lr_data["prerequisites"]["assessments"][i]=new_assessment_id

                  headers = {"Authorization": request.headers.get\
                             ("Authorization")}
                  request_body_data= {"prerequisites":{
                "assessments":lr_data["prerequisites"]["assessments"]}}
                  #pylint: disable=line-too-long,consider-using-f-string
                  api_url = \
                    "http://{}:{}/learning-object-service/api/v1/learning-resource/{}".format(
                  SERVICES["learning-object-service"]["host"],
                  SERVICES["learning-object-service"]["port"],
                  lr_data["uuid"])
                  query_params= {"create_version": False}
                  put_method(url=api_url,query_params=query_params,\
                             request_body=request_body_data,token=\
                              headers.get("Authorization"))

        #Check the neightbouring assessment nodes
        if "assessments" in neighbour_nodes:
          dependent_assessment_nodes = neighbour_nodes["assessments"]
          for assessment in dependent_assessment_nodes:
            assessment_data= Assessment.find_by_id(assessment).to_dict()
            if assessment_data["order"]>placeholder_assessment_data["order"]:
              for i in range\
                (len(assessment_data["prerequisites"]["assessments"])):
                if assessment_data["prerequisites"]["assessments"][i] ==\
                  old_assessment_id:
                  assessment_data["prerequisites"]["assessments"][i]=\
                    new_assessment_id
                  assessment_update_prereq={"prerequisites":
                                            assessment_data["prerequisites"]}
                  assessment_update_prereq_data=\
                    UpdateAssessmentModel(**assessment_update_prereq)
                  update_assessment(assessment_data["uuid"],\
                                    assessment_update_prereq_data)

        #Remove or delink the placeholder assessment
        delink_update_dict={}
        delink_update_dict["parent_nodes"]={}
        delink_update_dict["order"]= None
        delink_update_dict["prerequisites"]={}

        delink_data= UpdateAssessmentModel(**delink_update_dict)

        #Update the placeholder assessment
        update_assessment(old_assessment_id,delink_data)

    authored_assessment_data = get_assessment(new_assessment_id)["data"]

    return {
      "success": True,
      "message": "Successfully linked the assessment",
      "data": authored_assessment_data
              }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.put(
    "/assessment/human-graded/{uuid}",
    response_model=AssessmentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_human_graded_assessment(uuid: str,
                                   input_assessment: UpdateAssessmentModel):
  """Update a human graded assessment

    Args:
        input_assessment (AssessmentModel): Required body of
        human graded assessment

    Raises:
        ResourceNotFoundException: If the assessment does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        JSON: Success/Fail Message
    """
  try:

    input_assessment_dict = {**input_assessment.dict()}
    update_dict = copy.deepcopy(input_assessment_dict)

    #get the list of performance indicators
    performance_indicators = []
    existing_assessment = get_assessment(uuid)
    existing_rubrics = existing_assessment["data"]["child_nodes"]["rubrics"]
    if "child_nodes" in update_dict and update_dict["child_nodes"]:
      rubric_updates = update_dict["child_nodes"]["rubrics"]
      new_rubric_list = []
      new_rubric_criterion_list = []
      for rubric_update in rubric_updates:
        #For existing rubrics
        if "uuid" in rubric_update and\
          rubric_update["uuid"] in existing_rubrics:
          rubric = Rubric.find_by_id(rubric_update["uuid"])
          rubric_data = rubric.get_fields(reformat_datetime=True)
          existing_rubric_criteria =\
            rubric_data["child_nodes"]["rubric_criteria"]
          for rubric_criteria_update in\
            rubric_update["child_nodes"]["rubric_criteria"]:
            #For existing rubric_criteria
            performance_indicators.extend(
              rubric_criteria_update.get("performance_indicators",[]))
            if "uuid" in rubric_criteria_update and\
              rubric_criteria_update["uuid"] in existing_rubric_criteria:
              print("Need to update existing rubric")
              rubric_criteria_uuid = rubric_criteria_update["uuid"]
              update_rubric_criteria_dict =\
                UpdateRubricCriterionModel(**rubric_criteria_update)
              update_criterion_response =\
                update_rubric_criterion(rubric_criteria_uuid,\
                                        update_rubric_criteria_dict)
              new_rubric_criterion_list.append(
                update_criterion_response["data"]["uuid"])
            else:
              #For a new rubric criteria
              performance_indicators.extend(rubric_criteria_update.get(
                "performance_indicators",[]))
              new_rubric_criteria =\
                BasicRubricCriterionModel(**rubric_criteria_update)
              rubric_criterion_response =\
                create_rubric_criterion(new_rubric_criteria)
              new_rubric_criterion_list.append(
                rubric_criterion_response["data"]["uuid"])
            rubric_update["child_nodes"]["rubric_criteria"] =\
              new_rubric_criterion_list
            rubric_uuid = rubric_update["uuid"]
            rubric_update_dict = UpdateRubricModel(**rubric_update)
            update_rubric_response = update_rubric(
              rubric_uuid, rubric_update_dict)
          new_rubric_list.append(update_rubric_response["data"]["uuid"])
        else:
          #For new rubrics
          #For new rubric criteria
          new_rubric_criteria_list = []
          for new_rubric_criteria_update in\
            rubric_update["child_nodes"]["rubric_criteria"]:
            performance_indicators.extend(new_rubric_criteria_update.get(
              "performance_indicators",[]))
            new_rubric_criteria =\
              BasicRubricCriterionModel(**new_rubric_criteria_update)
            rubric_criterion_response = create_rubric_criterion(
              new_rubric_criteria)
            new_rubric_criteria_list.append(
              rubric_criterion_response["data"]["uuid"])
          rubric_update["child_nodes"]["rubric_criteria"] =\
            new_rubric_criteria_list
          #Create the new rubric
          new_rubric = RubricModel(**rubric_update)
          rubric_response = create_rubric(new_rubric)
          new_rubric_list.append(rubric_response["data"]["uuid"])

      update_dict["child_nodes"]["rubrics"] = new_rubric_list
      #Performance Indicators
      # Validate if the skill ID exists in Firestore DB
      unique_performance_indicators = set(performance_indicators)
      for skill_id in unique_performance_indicators:
        _ = Skill.find_by_id(skill_id)
      update_dict["references"]["skills"] = unique_performance_indicators

    assessment_fields = CommonAPIHandler.update_document(
        Assessment, uuid, update_dict)
    return {
        "success": True,
        "message": "Successfully updated the assessment",
        "data": assessment_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
