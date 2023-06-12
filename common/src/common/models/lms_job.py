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
"""Module to add jobs in FireO"""
from fireo.fields import TextField, MapField, IDField, DateTime
from common.models import BaseModel


class LmsJob(BaseModel):
  """LMS job Data Model"""
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
    collection_name = BaseModel.DATABASE_PREFIX + "lms_jobs"


# type -> LMS job type would be couse_copy/grade_import/cron_job(specific)
# status -> ready, running, failed, success
# logs -> {"errors": ["error1","error2"], "info": ["info1","info2"]}
