from concurrent.futures import TimeoutError
import json
from google.cloud import pubsub_v1
from google.cloud import bigquery
from common.utils.logging_handler import Logger
from config import PUB_SUB_PROJECT_ID,DATABASE_PREFIX,PROJECT_ID
subscriber = pubsub_v1.SubscriberClient()
bq = bigquery.Client()
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
        "id":f"{message.message_id}",
        "collection":f"{data['collection']}",
        "event_type":f"{data['eventType']}",
        "resource":json.dumps(data["resourceId"])
    }]
  Logger.info(results)
  errors = bq.insert_rows(
    table=bq.get_table(f"{PROJECT_ID}.test.pub_sub_test_table")
    , rows=results)
  if errors == []:
    message.ack()
    Logger.info(f"New data pushed data:{data}")
  else:
    Logger.info(f"Encountered errors while inserting rows: {errors}")


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
