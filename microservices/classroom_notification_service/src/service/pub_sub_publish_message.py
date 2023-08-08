"""Pub/Sub message publish helper file
"""
from config import PUB_SUB_PROJECT_ID, DATABASE_PREFIX
from google.cloud import pubsub_v1
import json


def send_message(message):
  """Method to publish a message to pubsub

  Args:
      message (dict): The data dict which contains details of messages.

  Returns:
      Bool: return bool based on message publish
  """
  if message is None:
    return True
  publisher = pubsub_v1.PublisherClient()
  topic_path = publisher.topic_path(
    PUB_SUB_PROJECT_ID, (DATABASE_PREFIX + "lms-notifications"))
  future = publisher.publish(topic_path,
                             data=json.dumps(message).encode("utf-8"),
                             store_to_bq="true")
  if future.result():
    return True
  return False
