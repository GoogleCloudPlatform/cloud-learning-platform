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

"""class and methods for logs handling."""

import logging
from common.config import CLOUD_LOGGING_ENABLED
import google.cloud.logging

if CLOUD_LOGGING_ENABLED:
  client = google.cloud.logging.Client()
  client.setup_logging()

  logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
else:
  logging.basicConfig(level=logging.INFO)



class Logger():
  """class def handling logs."""

  @staticmethod
  def info(message):
    """Display info logs."""
    logging.info(message)

  @staticmethod
  def warning(message):
    """Display warning logs."""
    logging.warning(message)

  @staticmethod
  def error(message):
    """Display error logs."""
    logging.error(message)
