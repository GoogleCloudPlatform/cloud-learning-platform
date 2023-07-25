"""Custom Fields for Fireo"""

from fireo.fields import Field
import os
# pylint: disable = broad-exception-raised

# pylint: disable=broad-exception-raised

GCS_BUCKET = os.environ.get("PROJECT_ID")

class GCSPathField(Field):
  """Custom field to save only GCS file path to firestore and
    return full URI when retrieved"""

  def db_value(self, val):
    """Storing modfied val to DB"""
    if val:
      try:
        blob_name = "/".join(val.split("gs://")[1].split("/")[1:])
        return blob_name
      except Exception as e:
        raise Exception("Invalid GCS URI: " + str(val)) from e
    return val

  def field_value(self, val):
    """Returning complete path"""
    if val and val.startswith("gs://"):
      return val
    elif val:
      return "gs://" + GCS_BUCKET + "/" + val
    return val
