"""Validate the request body using the schema."""
import json
from os.path import join, dirname
from jsonschema import validate
from functools import partial, wraps


def load_json_schema(schema_name):
  """Load and return the schema.

    Args:
        schema_name(string) - filename containing schema

    Returns:
        json containing the schema
    """
  relative_path = join("schemas", schema_name)
  absolute_path = join(dirname(__file__), relative_path)

  with open(absolute_path, encoding="utf-8", errors="ignore") as schema_file:
    return json.loads(schema_file.read())


def validate_crud(func, schema_name):
  """Validate the request body.

    Returns:
        Object of inner function validate_data()
    """

  # pylint: disable=inconsistent-return-statements
  @wraps(func)
  def validate_data(*args, **kwargs):
    """Decorator function to validate the request body.

        Returns error message if schema not validated
        """
    try:
      data = json.loads(args[0].request.body)
      if not data:
        return args[0].send_json(
            status=500, message="No fields to create or update", success=False)
      schema = load_json_schema(schema_name)
      validate(data, schema)
      request_keys = set(data.keys())
      schema_keys = set(schema["properties"].keys())
      if not schema_keys.issuperset(request_keys):
        return args[0].send_json(
            status=500, message="Invalid keys in request body", success=False)
      func(*args, **kwargs)
    except Exception as err:  # pylint: disable=broad-except
      return args[0].send_json(status=500, message=err.message, success=False)

  return validate_data


def validate_crud_async(func, schema_name):
  """Validate the request body.

    Returns:
        Object of inner function validate_data()
    """

  # pylint: disable=inconsistent-return-statements
  @wraps(func)
  async def validate_data(*args, **kwargs):
    """Decorator function to validate the request body.

        Returns error message if schema not validated
        """
    try:
      data = json.loads(args[0].request.body)
      if not data:
        return args[0].send_json(
            status=500, message="No fields to create or update", success=False)
      schema = load_json_schema(schema_name)
      validate(data, schema)
      request_keys = set(data.keys())
      schema_keys = set(schema["properties"].keys())
      if not schema_keys.issuperset(request_keys):
        return args[0].send_json(
            status=500, message="Invalid keys in request body", success=False)
      await func(*args, **kwargs)
    except Exception as err:  # pylint: disable=broad-except
      return args[0].send_json(status=500, message=err.message, success=False)

  return validate_data


validate_create_lu = partial(validate_crud, schema_name="lu_create_schema.json")
validate_update_lu = partial(
    validate_crud_async, schema_name="lu_update_schema.json")
validate_create_lo = partial(validate_crud, schema_name="lo_create_schema.json")
validate_update_lo = partial(
    validate_crud_async, schema_name="lo_update_schema.json")
validate_create_sub_competency = partial(
    validate_crud, schema_name="sub_competency_create_schema.json")
validate_update_sub_competency = partial(
    validate_crud, schema_name="sub_competency_update_schema.json")
validate_create_competency = partial(
    validate_crud, schema_name="competency_create_schema.json")
validate_update_competency = partial(
    validate_crud, schema_name="competency_update_schema.json")
validate_create_course = partial(
    validate_crud, schema_name="course_create_schema.json")
validate_update_course = partial(
    validate_crud, schema_name="course_update_schema.json")
validate_create_topic_tree = partial(
    validate_crud, schema_name="topic_tree_create_schema.json")
validate_update_topic_tree = partial(
    validate_crud_async, schema_name="topic_tree_update_schema.json")
validate_create_learning_content = partial(
    validate_crud, schema_name="learning_content_create_schema.json")
validate_update_learning_content = partial(
    validate_crud, schema_name="learning_content_update_schema.json")
validate_create_triple = partial(
    validate_crud, schema_name = "triple_create_schema.json")
validate_update_triple = partial(
    validate_crud, schema_name = "triple_update_schema.json")
validate_create_triple_from_lu = partial(
    validate_crud, schema_name = "triple_from_lu_schema.json")
validate_create_lu_from_lo = partial(
    validate_crud, schema_name="lu_from_lo_schema.json")

