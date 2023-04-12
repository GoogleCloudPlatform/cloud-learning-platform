""" Import of the JSON file """
import json
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from json.decoder import JSONDecodeError
from common.utils.errors import ValidationError
# pylint: disable = broad-except


def add_data_to_db(content, new_content_obj):
  '''Insert the data into the database'''
  new_content_obj = new_content_obj.from_dict(content)
  new_content_obj.uuid = ""
  new_content_obj.save()
  new_content_obj.uuid = new_content_obj.id
  new_content_obj.update()
  new_content_uuid = new_content_obj.uuid
  return new_content_uuid


def json_import(json_file, json_schema, model_obj, object_name):
  """Importing a json file and validating the schema before
     inserting the data into the database"""
  try:
    if not json_file.filename.endswith(".json"):
      raise ValidationError("Valid JSON file type is supported")
    else:
      contents = json.load(json_file.file)
      inserted_data = []

      # Validating the JSON schema of each obj in the input JSON file
      # before inserting the data into the database
      if isinstance(contents, list):
        for content in contents:
          json_schema(**content)
      else:
        json_schema(**contents)
      if isinstance(contents, list):
        for content in contents:
          new_content_obj = model_obj()
          new_content_uuid = add_data_to_db(content, new_content_obj)
          inserted_data.append(new_content_uuid)
      else:
        new_content_obj = model_obj()
        new_content_uuid = add_data_to_db(contents, new_content_obj)
        inserted_data.append(new_content_uuid)
      return {
          "success": True,
          "message": f"Successfully created the {object_name}",
          "data": inserted_data
      }

  except JSONDecodeError as e:
    raise ValidationError("Provided JSON is invalid") from e

  except PydanticValidationError as err:
    error_res = json.loads(err.json())
    req_fields = [i["loc"][-1] for i in error_res]
    req_fields_str = "Missing required fields - "+ \
        ",".join("'"+i+"'" for i in req_fields)
    raise ValidationError(req_fields_str, data=error_res) from err

  except Exception as err:
    raise err
