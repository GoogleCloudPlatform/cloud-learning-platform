""" Sub Domain endpoints """
from typing import Optional
from fastapi import APIRouter, UploadFile, File
from common.models import SubDomain
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.sub_domain_schema import (
    SubDomainModel, UpdateSubDomainModel, GetSubDomainResponseModel,
    PostSubDomainResponseModel, UpdateSubDomainResponseModel, DeleteSubDomain,
    SubDomainImportJsonResponse, AllSubDomainsResponseModel,
    BasicSubDomainModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Sub Domain"],
    responses=ERROR_RESPONSES)


@router.get(
    "/sub-domains",
    response_model=AllSubDomainsResponseModel,
    name="Get all Subdomains")
def get_sub_domains(source_name: Optional[str] = None,
                    skip: int = 0,
                    limit: int = 10):
  """The get sub-domains endpoint will return an array sub-domains from
  firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of sub-domain array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllSubDomainsResponseModel: Array of SubDomain Object
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    collection_manager = SubDomain.collection
    if source_name:
      collection_manager = collection_manager.filter("source_name", "==",
                                                     source_name)
    sub_domains = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    sub_domains = [i.get_fields(reformat_datetime=True) for i in sub_domains]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": sub_domains
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/sub-domain/{uuid}",
    response_model=GetSubDomainResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_sub_domain(uuid: str,
                  fetch_tree: Optional[bool] = False):
  """The get sub_domain endpoint will return the sub_domain from firestore of
  which uuid is provided

  Args:
      uuid (str): Unique identifier for sub_domain
      fetch_tree: `bool`
        Flag to determine whether to fetch tree or not

  Raises:
      ResourceNotFoundException: If the sub_domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetSubDomainResponseModel: SubDomain Object
  """
  try:
    sub_domain = SubDomain.find_by_uuid(uuid)
    sub_domain_fields = sub_domain.get_fields(reformat_datetime=True)

    if fetch_tree:
      ParentChildNodesHandler.load_child_nodes_data(sub_domain_fields)
      ParentChildNodesHandler.load_immediate_parent_nodes_data(
          sub_domain_fields)

    return {
        "success": True,
        "message": "Successfully fetched the sub_domain",
        "data": sub_domain_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/sub-domain", response_model=PostSubDomainResponseModel)
def create_sub_domain(input_sub_domain: SubDomainModel):
  """The create sub_domain endpoint will add the sub_domain in request body to
  the firestore

  Args:
      input_sub_domain (SubDomainModel): input sub_domain to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostSubDomainResponseModel: SubDomain Object
  """
  try:
    input_sub_domain_dict = {**input_sub_domain.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_sub_domain_dict)

    new_sub_domain = SubDomain()
    new_sub_domain = new_sub_domain.from_dict(input_sub_domain_dict)
    new_sub_domain.uuid = ""
    new_sub_domain.save()
    new_sub_domain.uuid = new_sub_domain.id
    new_sub_domain.update()

    sub_domain_fields = new_sub_domain.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        sub_domain_fields, SubDomain, operation="add")
    ParentChildNodesHandler.update_parent_references(
        sub_domain_fields, SubDomain, operation="add")

    return {
        "success": True,
        "message": "Successfully created the sub_domain",
        "data": sub_domain_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/sub-domain/{uuid}",
    response_model=UpdateSubDomainResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_sub_domain(uuid: str, input_sub_domain: UpdateSubDomainModel):
  """Update a sub_domain with the uuid passed in the request body

  Args:
      input_sub_domain (SubDomainModel): Required body of the sub_domain

  Raises:
      ResourceNotFoundException: If the sub_domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateSubDomainResponseModel: SubDomain Object
  """
  try:
    existing_sub_domain = SubDomain.find_by_uuid(uuid)

    input_sub_domain_dict = {**input_sub_domain.dict(exclude_unset=True)}
    sub_domain_fields = existing_sub_domain.get_fields()

    ParentChildNodesHandler.compare_and_update_nodes_references(
        input_sub_domain_dict, sub_domain_fields, SubDomain)

    for key, value in input_sub_domain_dict.items():
      sub_domain_fields[key] = value
    for key, value in sub_domain_fields.items():
      setattr(existing_sub_domain, key, value)
    existing_sub_domain.update()

    sub_domain_fields = existing_sub_domain.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the sub_domain",
        "data": sub_domain_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/sub-domain/{uuid}",
    response_model=DeleteSubDomain,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_sub_domain(uuid: str):
  """Delete a sub_domain with the given uuid from firestore

  Args:
      uuid (str): Unique id of the sub_domain

  Raises:
      ResourceNotFoundException: If the sub_domain does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    sub_domain = SubDomain.find_by_uuid(uuid)
    sub_domain_fields = sub_domain.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        sub_domain_fields)
    ParentChildNodesHandler.update_child_references(
        sub_domain_fields, SubDomain, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        sub_domain_fields, SubDomain, operation="remove")

    SubDomain.collection.delete(sub_domain.key)

    return {"success": True, "message": "Successfully deleted the sub_domain"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/sub-domain/import/json",
    response_model=SubDomainImportJsonResponse,
    name="Import Subdomains from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_sub_domains(json_file: UploadFile = File(...)):
  """Create sub_domains from json file

  Args:
    json_file (UploadFile): Upload json file consisting of sub_domains.
    json_schema should match SubDomainModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    SubDomainImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicSubDomainModel,
        model_obj=SubDomain,
        object_name="sub_domains")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
