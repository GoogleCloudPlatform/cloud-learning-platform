# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FireO model for batch jobs"""

from fireo.fields import TextField, MapField, IDField, DateTime
from common.models import GCSPathField
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException


class BatchJob(BaseModel):
  """Batch job Data Model for Classroom services """
  id = IDField()
  job_type = TextField()
  status = TextField()
  logs = MapField(default={})
  input_data = MapField(default={})
  section_id = TextField()
  classroom_id = TextField()
  start_time = DateTime()
  end_time = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "batch_jobs"

# type -> Batch job type would be couse_copy/grade_import/cron_job(specific)
# status -> ready, running, failed, success
# logs -> {"errors": ["error1","error2"], "info": ["info1","info2"]}


class BatchJobModel(BaseModel):
  """ Model class for Kubernetes batch job service """
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
  result_data = MapField(default={})
  uuid = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "batch_jobs"

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
