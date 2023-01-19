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

from concurrent.futures import TimeoutError
import json
from google.cloud import pubsub_v1
from common.utils.logging_handler import Logger
from config import PUB_SUB_PROJECT_ID,DATABASE_PREFIX
from service import bq_service
subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(
    PUB_SUB_PROJECT_ID, DATABASE_PREFIX+"classroom-messeges-sub")


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
  """_summary_

  Args:
      message (pubsub_v1.subscriber.message.Message): _description_
  """
  data=json.loads(message.data)
  results = [{
        # "id":f"{message.message_id}",
        "collection":f"{data['collection']}",
        "event_type":f"{data['eventType']}",
        "resource":json.dumps(data["resourceId"])
    }]
  Logger.info(results)
  if bq_service.save(results):
    message.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
Logger.info(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
  try:
    # When `timeout` is not set, result() will block indefinitely,
    # unless an exception is encountered first.
    streaming_pull_future.result(timeout=40.0)
  except TimeoutError:
    streaming_pull_future.cancel()  # Trigger the shutdown.
    streaming_pull_future.result()  # Block until the shutdown is complete.
