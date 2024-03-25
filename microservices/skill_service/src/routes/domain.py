""" Domain endpoints """
from typing import Optional
from fastapi import APIRouter, UploadFile, File
from common.models import Domain
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.domain_schema import (DomainModel, UpdateDomainModel,
                                   GetDomainResponseModel,
                                   PostDomainResponseModel,
                                   UpdateDomainResponseModel,
                                   DomainImportJsonResponse, DeleteDomain,
                                   AllDomainResponseModel, BasicDomainModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Domain"],
    responses=ERROR_RESPONSES)


@router.get(
    "/domains", response_model=AllDomainResponseModel, name="Get all Domains")
def get_domains(source_name: Optional[str] = None,
                skip: int = 0,
                limit: int = 10):
  """The get domains endpoint will return an array domains from
  firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of domain array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllDomainResponseModel: Array of Domain Object
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    collection_manager = Domain.collection
    if source_name:
      collection_manager = collection_manager.filter("source_name", "==",
                                                     source_name)
    domains = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    domains = [i.get_fields(reformat_datetime=True) for i in domains]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": domains
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/domain/{uuid}",
    response_model=GetDomainResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_domain(uuid: str,
              fetch_tree: Optional[bool] = False):
  """The get domain endpoint will return the domain from firestore of
  which uuid is provided

  Args:
      uuid (str): Unique identifier for domain
      fetch_tree: `bool`
        Flag to determine whether to fetch tree or not

  Raises:
      ResourceNotFoundException: If the domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetDomainResponseModel: Domain Object
  """
  try:
    domain = Domain.find_by_uuid(uuid)
    domain_fields = domain.get_fields(reformat_datetime=True)

    if fetch_tree:
      ParentChildNodesHandler.load_child_nodes_data(domain_fields)
      ParentChildNodesHandler.load_immediate_parent_nodes_data(domain_fields)

    return {
        "success": True,
        "message": "Successfully fetched the domain",
        "data": domain_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/domain", response_model=PostDomainResponseModel)
def create_domain(input_domain: DomainModel):
  """The create domain endpoint will add the domain in request body to the
  firestore

  Args:
      input_domain (DomainModel): input domain to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostDomainResponseModel: Domain Object
  """
  try:
    input_domain_dict = {**input_domain.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_domain_dict)

    new_domain = Domain()
    new_domain = new_domain.from_dict(input_domain_dict)
    new_domain.uuid = ""
    new_domain.save()
    new_domain.uuid = new_domain.id
    new_domain.update()

    domain_fields = new_domain.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        domain_fields, Domain, operation="add")
    ParentChildNodesHandler.update_parent_references(
        domain_fields, Domain, operation="add")

    return {
        "success": True,
        "message": "Successfully created the domain",
        "data": domain_fields
    }

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/domain/{uuid}",
    response_model=UpdateDomainResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_domain(uuid: str, input_domain: UpdateDomainModel):
  """Update a domain with the uuid passed in the request body

  Args:
      input_domain (DomainModel): Required body of the domain

  Raises:
      ResourceNotFoundException: If the domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateDomainResponseModel: Domain Object
  """
  try:
    existing_domain = Domain.find_by_uuid(uuid)

    input_domain_dict = {**input_domain.dict(exclude_unset=True)}
    domain_fields = existing_domain.get_fields()

    ParentChildNodesHandler.compare_and_update_nodes_references(
        input_domain_dict, domain_fields, Domain)

    for key, value in input_domain_dict.items():
      domain_fields[key] = value
    for key, value in domain_fields.items():
      setattr(existing_domain, key, value)

    existing_domain.update()
    domain_fields = existing_domain.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the domain",
        "data": domain_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/domain/{uuid}",
    response_model=DeleteDomain,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_domain(uuid: str):
  """Delete a domain with the given uuid from firestore

  Args:
      uuid (str): Unique id of the domain

  Raises:
      ResourceNotFoundException: If the domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    domain = Domain.find_by_uuid(uuid)
    domain_fields = domain.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        domain_fields)
    ParentChildNodesHandler.update_child_references(
        domain_fields, Domain, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        domain_fields, Domain, operation="remove")

    Domain.collection.delete(domain.key)

    return {"success": True, "message": "Successfully deleted the domain"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/domain/import/json",
    response_model=DomainImportJsonResponse,
    name="Import Domains from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_domains(json_file: UploadFile = File(...)):
  """Create domains from json file

  Args:
    json_file (UploadFile): Upload json file consisting of domains.
    json_schema should match DomainModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    DomainImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicDomainModel,
        model_obj=Domain,
        object_name="domains")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
