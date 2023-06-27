# Copyright 2023 Google LLC
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

"""
  Jobs Service config file
"""
# pylint: disable=unspecified-encoding,line-too-long
import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

JOB_TYPES = Literal["emsi_ingestion", "csv_ingestion", "unified_alignment",
                    "credential_engine_ingestion", "skill_embedding_db_update",
                    "role_skill_alignment", "knowledge_embedding_db_update",
                    "wgu_ingestion", "e2e_test", "generic_csv_ingestion"]

