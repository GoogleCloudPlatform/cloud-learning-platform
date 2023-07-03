"""FireO model for batch jobs"""
from fireo.fields import TextField, MapField, IDField
from common.models import GCSPathField
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException

class BatchJobModel(BaseModel):
  """Model class for batch job"""
  id_ = IDField()
  name = TextField(required=True, default="")
  input_data = TextField()
  type = TextField(required=True)
  status = TextField(required=True)
  message = TextField(required=True, default="")
  generated_item_id = TextField()
  output_gcs_path = GCSPathField()
  errors = MapField(default={})
  job_logs = MapField(default={})
  metadata = MapField(default={})
  uuid = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX+"batch_jobs"

  @classmethod
  def find_by_name(cls, name):
    job = cls.collection.filter("name", "==", name).get()
    if job:
      return job
    else:
      raise ResourceNotFoundException(f"Invalid {cls.__name__} name: {name}")

  @classmethod
  def find_by_uuid(cls, name):
    job = cls.collection.filter("uuid", "==", name).get()
    if job:
      return job
    else:
      raise ResourceNotFoundException(f"Invalid {cls.__name__} name: {name}")
