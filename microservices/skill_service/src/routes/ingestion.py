""" Data Ingestion APIs """
import traceback
import csv
import codecs
import requests
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form
from common.utils.logging_handler import Logger
from common.utils.errors import (InvalidFileType, ValidationError,
                                 ConflictError, ResourceNotFoundException,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          Conflict, ResourceNotFound,
                                          PayloadTooLarge)
from common.utils.gcs_adapter import is_valid_path, upload_file_to_bucket
from schemas.gcs_schema import GCSBucketInfoModel
from schemas.initaiate_batchjob_schema import (BatchJobModel,
                                               CredentialEngineRequestModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  ConflictResponseModel,
                                  NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel,
                                  UnauthorizedResponseModel)
from services.batch_job import initiate_batch_job
from services.ingest_osn import validate_osn_csv
from services.ingest_generic_csv import (parse_csv, validate_skills_csv,
                                         validate_competencies_csv,
                                         validate_categories_csv,
                                         validate_sub_domains_csv,
                                         validate_domains_csv)
from config import (CE_INGESTION_JOB_TYPE, CSV_INGESTION_JOB_TYPE,
                    EMSI_INGESTION_JOB_TYPE, DATABASE_PREFIX, CLIENT_ID,
                    CLIENT_SECRET, GCP_BUCKET, OSN_INGESTION_JOB_TYPE,
                    GENERIC_CSV_INGESTION_JOB_TYPE,
                    ALLOWED_SOURCES_FOR_GENERIC_CSV_INGESTION,
                    PAYLOAD_FILE_SIZE)
# pylint: disable = broad-exception-raised,line-too-long

router = APIRouter(
    tags=["Skill Ingestion APIs"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        },
        409: {
            "model": ConflictResponseModel
        },
        413: {
            "model": PayloadTooLargeResponseModel
        },
        401: {
            "model": UnauthorizedResponseModel
        }
    })


@router.post("/import/credential-engine", response_model=BatchJobModel)
def import_from_credential_engine(data: CredentialEngineRequestModel):
  """Batch job to import data from credential engine using competency-framework
  url that is passed in request body

  Args:
    - competency_frameworks (Array): link of competency framework urls present
      in credential engine.

  Raises:
    - HTTPException: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    data = {"links": data.competency_frameworks}
    for link in data["links"]:
      res = requests.get(url=link, timeout=10)
      if res.status_code != 200:
        raise Exception
    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(data, CE_INGESTION_JOB_TYPE, env_vars)
    Logger.info(response)
    return response
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/import/local-csv",
    response_model=BatchJobModel,
    name="Import from CSV",
    include_in_schema=False)
async def import_from_csv(competencies: Optional[UploadFile] = File(None),
                    skills: Optional[UploadFile] = File(None)):
  """Batch job to import data from csv's uploaded by user

  Args:
    - competencies: csv file to be uploaded by user
    - skills: csv file to be uploaded by user

  Raises:
    - HTTPException: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    if not skills and not competencies:
      raise ValidationError("Please upload a csv file to continue")

    input_data = {}
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    if competencies:
      if len(await competencies.read()) > PAYLOAD_FILE_SIZE:
        raise PayloadTooLargeError(
          f"File size is too large: {competencies.filename}"
        )
      await competencies.seek(0)
      competency_file_name = "competencies_" + str(date) + ".csv"
      competency_uri = upload_file_to_bucket(
          GCP_BUCKET, "skill-service/user-uploaded-csvs", competency_file_name,
          competencies.file)
      input_data["competency_uri"] = competency_uri
    else:
      input_data["competency_uri"] = None

    if skills:
      if len(await skills.read()) > PAYLOAD_FILE_SIZE:
        raise PayloadTooLargeError(
          f"File size is too large: {skills.filename}"
        )
      await skills.seek(0)
      skill_file_name = "skills_" + str(date) + ".csv"
      skill_uri = upload_file_to_bucket(GCP_BUCKET,
                                        "skill-service/user-uploaded-csvs",
                                        skill_file_name, skills.file)
      input_data["skill_uri"] = skill_uri
    else:
      input_data["skill_uri"] = None

    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(input_data, CSV_INGESTION_JOB_TYPE, env_vars)
    Logger.info(response)
    return response
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/import/gcs-csv",
    response_model=BatchJobModel,
    name="Import from CSV using GCS Path",
    include_in_schema=False)
def import_from_gcs_csv(file_info: GCSBucketInfoModel):
  """Batch job to import data from csv's stored in GCS

  Args:
    - bucket_name: name of bucket where files are stored
    - skills_file_name: file name with folders as prefix
    - competencies_file_name: file name with folders as prefix

  Raises:
    - HTTPException: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    if not file_info.competency_uri and not file_info.skill_uri:
      raise ValidationError("It's required to either \
                            provide competency or skill uri")

    data = {}

    if file_info.competency_uri:
      data["competency_uri"] = file_info.competency_uri

    if file_info.skill_uri:
      data["skill_uri"] = file_info.skill_uri

    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(data, CSV_INGESTION_JOB_TYPE, env_vars)
    Logger.info(response)
    return response
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/import/emsi", response_model=BatchJobModel)
def import_from_emsi(size: Optional[int] = None):
  """Batch job to import data from Emsi skills library using Emsi api's.

  Args:
    - size (int, optional): Number of skills to be imported. If not provided,
    - all skills will be imported.

  Raises:
    - HTTPException: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    data = {"size": size}
    env_vars = {
        "DATABASE_PREFIX": DATABASE_PREFIX,
        "CLIENT_ID": CLIENT_ID,
        "CLIENT_SECRET": CLIENT_SECRET
    }
    if size <= 0:
      raise ValidationError("Size cannot be less than or equal to 0")
    response = initiate_batch_job(data, EMSI_INGESTION_JOB_TYPE, env_vars)
    Logger.info(response)
    return response
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/import/osn",
    response_model=BatchJobModel,
    name="Import from OSN",
    include_in_schema=False)
def import_from_osn_csv(csv_file: Optional[UploadFile] = File(None)):
  """Batch job to import data from OSN csv uploaded by user

  Args:
    - csv_file: csv file to be uploaded by user

  Raises:
    - HTTPException: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    if not csv_file:
      raise ValidationError("Please upload a csv file to continue")

    # validate data in provided csv
    csv_reader = csv.DictReader(
        codecs.iterdecode(csv_file.file, "utf-8"), delimiter=",")
    validate_osn_csv(list(csv_reader))

    input_data = {}
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    osn_data_file_name = f"osn_data_{str(date)}.csv"
    osn_uri = upload_file_to_bucket(GCP_BUCKET,
                                    "skill-service/user-uploaded-csvs",
                                    osn_data_file_name, csv_file.file)
    input_data["osn_uri"] = osn_uri

    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(input_data, OSN_INGESTION_JOB_TYPE, env_vars)
    Logger.info(response)
    return response

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/import/csv",
    name="Import from Generic CSV",
    response_model=BatchJobModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def import_from_generic_csv(source: ALLOWED_SOURCES_FOR_GENERIC_CSV_INGESTION,
                            skill_uri: Optional[str] = Form(default=None),
                            competency_uri: Optional[str] = Form(default=None),
                            category_uri: Optional[str] = Form(default=None),
                            domain_uri: Optional[str] = Form(default=None),
                            sub_domain_uri: Optional[str] = Form(default=None),
                            skills: Optional[UploadFile] = File(None),
                            competencies: Optional[UploadFile] = File(None),
                            categories: Optional[UploadFile] = File(None),
                            sub_domains: Optional[UploadFile] = File(None),
                            domains: Optional[UploadFile] = File(None)):
  """Batch job to import data from csv uploaded by user

  Args:
    - source(query param): name of registry/library through which data is acquired
    - skill_uri : GCS uri for the skills data csv file
    - competency_uri : GCS uri for the competencies data csv file
    - category_uri : GCS uri for the categories data csv file
    - domain_uri : GCS uri for the domains data csv file
    - sub_domain__uri : GCS uri for the sub domains data csv file
    - skills: csv file containing skills data
    - competencies: csv file containing competencies data
    - categories: csv file containing categories data
    - sub_domains: csv file containing sub domains data
    - domains: csv file containing domains data

  Raises:
    - HTTPException: 422 Unprocessable entity if file other than csv is passed
    - HTTPException: 500 Internal Server Error if data not correct or if
    something fails

  Returns: (BatchJobModel)
    - job_name: name of the batch job created
    - status: status of batch job
  """
  try:
    file_object_list = [skills, competencies, sub_domains, domains, categories]
    uri_object_list = [
        skill_uri, competency_uri, sub_domain_uri, domain_uri, category_uri
    ]

    file_check = any(i is not None for i in file_object_list)
    uri_check = any(i is not None for i in uri_object_list)

    if (not uri_check and not file_check) or (uri_check and file_check):
      raise ValidationError("Please either upload a CSV file or provide a "
                            "GCS CSV file URI but not both")

    input_data = {}
    input_data["source_name"] = source
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    if uri_check:
      if category_uri:
        input_data["category_uri"] = category_uri
        if is_valid_path(category_uri):
          categories_json_array = parse_csv(category_uri)
          validate_categories_csv(categories_json_array)
        else:
          raise ResourceNotFoundException(
              "file does not exist at the specified path.")
      else:
        input_data["category_uri"] = None

      if competency_uri:
        input_data["competency_uri"] = competency_uri
        if is_valid_path(competency_uri):
          competencies_json_array = parse_csv(competency_uri)
          validate_competencies_csv(competencies_json_array)
        else:
          raise ResourceNotFoundException(
              "file does not exist at the specified path.")
      else:
        input_data["competency_uri"] = None

      if domain_uri:
        input_data["domain_uri"] = domain_uri
        if is_valid_path(domain_uri):
          domains_json_array = parse_csv(domain_uri)
          validate_domains_csv(domains_json_array)
        else:
          raise ResourceNotFoundException(
              "file does not exist at the specified path.")
      else:
        input_data["domain_uri"] = None

      if sub_domain_uri:
        input_data["sub_domain_uri"] = sub_domain_uri
        if is_valid_path(sub_domain_uri):
          sub_domains_json_array = parse_csv(sub_domain_uri)
          validate_sub_domains_csv(sub_domains_json_array)
        else:
          raise ResourceNotFoundException(
              "file does not exist at the specified path.")
      else:
        input_data["sub_domain_uri"] = None

      if skill_uri:
        input_data["skill_uri"] = skill_uri
        if is_valid_path(skill_uri):
          skills_json_array = parse_csv(skill_uri)
          validate_skills_csv(skills_json_array)
        else:
          raise ResourceNotFoundException(
              "file does not exist at the specified path.")
      else:
        input_data["skill_uri"] = None

    if file_check:
      if skills:
        if not skills.filename.endswith(".csv"):
          raise InvalidFileType()

        # validate data in provided csv
        csv_reader = csv.DictReader(
            codecs.iterdecode(skills.file, "utf-8"), delimiter=",")
        validate_skills_csv(list(csv_reader))

        skill_file_name = "skills_" + str(date) + ".csv"
        skill_uri = upload_file_to_bucket(GCP_BUCKET,
                                          "skill-service/user-uploaded-csvs",
                                          skill_file_name, skills.file)
        input_data["skill_uri"] = skill_uri
      else:
        input_data["skill_uri"] = None

      if competencies:
        if not competencies.filename.endswith(".csv"):
          raise InvalidFileType()

        # validate data in provided csv
        csv_reader = csv.DictReader(
            codecs.iterdecode(competencies.file, "utf-8"), delimiter=",")
        validate_competencies_csv(list(csv_reader))

        competency_file_name = "competencies_" + str(date) + ".csv"
        competency_uri = upload_file_to_bucket(
            GCP_BUCKET, "skill-service/user-uploaded-csvs",
            competency_file_name, competencies.file)
        input_data["competency_uri"] = competency_uri
      else:
        input_data["competency_uri"] = None

      if categories:
        if not categories.filename.endswith(".csv"):
          raise InvalidFileType()

        # validate data in provided csv
        csv_reader = csv.DictReader(
            codecs.iterdecode(categories.file, "utf-8"), delimiter=",")
        validate_categories_csv(list(csv_reader))

        category_file_name = "categories_" + str(date) + ".csv"
        category_uri = upload_file_to_bucket(
            GCP_BUCKET, "skill-service/user-uploaded-csvs", category_file_name,
            categories.file)
        input_data["category_uri"] = category_uri
      else:
        input_data["category_uri"] = None

      if sub_domains:
        if not sub_domains.filename.endswith(".csv"):
          raise InvalidFileType()

        # validate data in provided csv
        csv_reader = csv.DictReader(
            codecs.iterdecode(sub_domains.file, "utf-8"), delimiter=",")
        validate_sub_domains_csv(list(csv_reader))

        sub_domain_file_name = "sub_domains_" + str(date) + ".csv"
        sub_domain_uri = upload_file_to_bucket(
            GCP_BUCKET, "skill-service/user-uploaded-csvs",
            sub_domain_file_name, sub_domains.file)
        input_data["sub_domain_uri"] = sub_domain_uri
      else:
        input_data["sub_domain_uri"] = None

      if domains:
        if not domains.filename.endswith(".csv"):
          raise InvalidFileType()

        # validate data in provided csv
        csv_reader = csv.DictReader(
            codecs.iterdecode(domains.file, "utf-8"), delimiter=",")
        validate_domains_csv(list(csv_reader))

        domain_file_name = "domains_" + str(date) + ".csv"
        domain_uri = upload_file_to_bucket(GCP_BUCKET,
                                           "skill-service/user-uploaded-csvs",
                                           domain_file_name, domains.file)
        input_data["domain_uri"] = domain_uri
      else:
        input_data["domain_uri"] = None

    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(input_data, GENERIC_CSV_INGESTION_JOB_TYPE,
                                  env_vars)
    Logger.info(response)
    return response
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except InvalidFileType as e:
    Logger.error(e)
    raise BadRequest("Invalid file type. CSV file expected") from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/import/csv/info")
def generic_csv_import_details():
  """
  Details for csv that will be provided to generic csv ingestion route.

    - query param: source
      (accepted values for source: "snhu", "emsi", "osn", "credential_engine")

  ### Skill csv schema:

    - **id***: a unique identifier
    - **name***: name of skill
    - **description***: short description for the given skill
    - **aligned_competency**: list of id’s of competency separated by “,”(comma) to which the given skill is aligned
    - **aligned_domain**: list of id’s of domain separated by “,”(comma) to which the given skill is aligned
    - **aligned_sub_domain**: list of id’s of sub_domain separated by “,”(comma) the to which the given skill is aligned
    - **keywords**: list of chosen words separated by “,”(comma) that improve searching for this node
    - **major_occupation**: list of codes separated by “,”(comma) for major occupation
    - **minor_occupation**: list of codes separated by “,”(comma) for minor occupation
    - **broad_occupation**: list of codes separated by “,”(comma) for broad occupation
    - **detailed_occupation**: list of codes separated by “,”(comma) for detailed occupation
    - **onet_alignment**: list of codes of onet jobs separated by “,”(comma) that aligns with the given skill
    - **standard_alignment**: standard alignment of skill
    - **credential_alignment**: credential alignment of skill
    - **organization_alignment**: organization alignment of skill
    - **{EXTERNAL_SOURCE}_skill_alignment_name**: name of skill as per external registry. {EXTERNAL_SOURCE} needs to be replaced with registry/library name(eg. osn_skill_alignment_name). The accepted registry/library are "osn", "snhu", "emsi".
    - **{EXTERNAL_SOURCE}_skill_alignment_id**: id of skill as per external registry. {EXTERNAL_SOURCE} needs to be replaced with registry/library id(eg. osn_skill_alignment_id). The accepted registry/library are "osn", "snhu", "emsi".
    - **certifications**: certifications
    - **author**: name of author
    - **creator**: name of creator
  ---
  ### Competency csv schema:

    - **id***: a unique identifier
    - **name***: name of competency
    - **description***: short description for the given competency
    - **aligned_domain**: list of id’s of domain separated by “,”(comma) the to which the given skill is aligned
    - **aligned_sub_domain**: list of id’s of sub_domain separated by “,”(comma) the to which the given competency is aligned
    - **keywords**: list of chosen words separated by “,”(comma) that improve searching for this node
    - **major_occupation**: list of codes separated by “,”(comma) for major occupation
    - **minor_occupation**: list of codes separated by “,”(comma) for minor occupation
    - **broad_occupation**: list of codes separated by “,”(comma) for broad occupation
    - **detailed_occupation**: list of codes separated by “,”(comma) for detailed occupation
    - **onet_alignment**: list of codes of onet jobs separated by “,”(comma) that aligns with the given competency
    - **standard_alignment**: standard alignment of competency
    - **credential_alignment**: credential alignment of competency
    - **organization_alignment**: organization alignment of competency
    - **subject_code**: code of subject which is mapped to given competency
    - **level**: level of competency
    - **course_code**: course code which is mapped to given competency
    - **course_title**: course title which is mapped to given competency
  ---
  ### Category csv schema:

    - **id***: a unique identifier
    - **name***: name of the category
    - **description**: short description for the given category
    - **keywords**: list of chosen words separated by “,”(comma) that improve searching for this node
    - **aligned_domain**: list of id’s of domain separated by “,”(comma) the to which the given category is aligned
    - **aligned_sub_domain**: list of id’s of sub_domain separated by “,”(comma) the to which the given category is aligned
  ---

  ### Subdomain csv schema:

    - **id***: a unique identifier
    - **name***: name of subdomain
    - **description**: short description for the given subdomain
    - **keywords**: list of chosen words separated by “,”(comma) that improve searching for this node
    - **aligned_domain**: list of id’s of domain separated by “,”(comma) the to which the given subdomain is aligned
  ---
  ### Domain csv schema:

    - **id***: a unique identifier
    - **name***: name of domain
    - **description**: short description for the given domain
    - **keywords**: list of chosen words separated by “,”(comma) that improve searching for this node
  """
  return {
      "success":
          True,
      "message":
          """
      query param: source
      accepted values for source: "snhu", "emsi", "osn", "credential_engine"

      Skill csv schema:

      id*: a unique identifier
      name*: name of skill
      description*: short description for the given skill
      aligned_competency: list of id’s of competency separated by “,”(comma) to which the given skill is aligned
      aligned_domain: list of id’s of domain separated by “,”(comma) to which the given skill is aligned
      aligned_sub_domain: list of id’s of sub_domain separated by “,”(comma) the to which the given skill is aligned
      keywords: list of chosen words separated by “,”(comma) that improve searching for this node
      major_occupation: list of codes separated by “,”(comma) for major occupation
      minor_occupation: list of codes separated by “,”(comma) for minor occupation
      broad_occupation: list of codes separated by “,”(comma) for broad occupation
      detailed_occupation: list of codes separated by “,”(comma) for detailed occupation
      onet_alignment: list of codes of onet jobs separated by “,”(comma) that aligns with the given skill
      standard_alignment: standard alignment of skill
      credential_alignment: credential alignment of skill
      organization_alignment: organization alignment of skill
      {EXTERNAL_SOURCE}_skill_alignment_name: name of skill as per external registry. {EXTERNAL_SOURCE} needs to be replaced with registry/library name(eg. osn_skill_alignment_name). The accepted registry/library are "osn", "snhu", "emsi".
      {EXTERNAL_SOURCE}_skill_alignment_id: id of skill as per external registry. {EXTERNAL_SOURCE} needs to be replaced with registry/library id(eg. osn_skill_alignment_id). The accepted registry/library are "osn", "snhu", "emsi".
      certifications: certifications
      author: name of author
      creator: name of creator


      Competency csv schema:

      id*: a unique identifier
      name: name of competency
      description*: short description for the given competency
      aligned_domain: list of id’s of domain separated by “,”(comma) the to which the given skill is aligned
      aligned_sub_domain: list of id’s of sub_domain separated by “,”(comma) the to which the given competency is aligned
      keywords: list of chosen words separated by “,”(comma) that improve searching for this node
      major_occupation: list of codes separated by “,”(comma) for major occupation
      minor_occupation: list of codes separated by “,”(comma) for minor occupation
      broad_occupation: list of codes separated by “,”(comma) for broad occupation
      detailed_occupation: list of codes separated by “,”(comma) for detailed occupation
      onet_alignment: list of codes of onet jobs separated by “,”(comma) that aligns with the given competency
      standard_alignment: standard alignment of competency
      credential_alignment: credential alignment of competency
      organization_alignment: organization alignment of competency
      subject_code: code of subject which is mapped to given competency
      level: level of competency
      course_code: course code which is mapped to given competency
      course_title: course title which is mapped to given competency


      Category csv schema:

      id*: a unique identifier
      name*: name of the category
      description: short description for the given category
      keywords: list of chosen words separated by “,”(comma) that improve searching for this node
      aligned_domain: list of id’s of domain separated by “,”(comma) the to which the given category is aligned
      aligned_sub_domain: list of id’s of sub_domain separated by “,”(comma) the to which the given category is aligned


      Subdomain csv schema:

      id*: a unique identifier
      name*: name of subdomain
      description: short description for the given subdomain
      keywords: list of chosen words separated by “,”(comma) that improve searching for this node
      aligned_domain: list of id’s of domain separated by “,”(comma) the to which the given subdomain is aligned


      Domain csv schema:

      id*: a unique identifier
      name*: name of domain
      description: short description for the given domain
      keywords: list of chosen words separated by “,”(comma) that improve searching for this node
    """,
      "data": {}
  }
