"""Pub/Sub Setup"""
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
import json
import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from google.oauth2 import service_account
from bq_helper import create_bigquery_dataset,create_table_using_sql,BQ_DATASET,GCP_PROJECT

# disabling for linting to pass
# pylint: disable = broad-exception-raised

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  PROJECT_ID
# generate credentials using SA json keys
GKE_POD_SA_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
"iam.serviceAccounts.actAs"
CREDENTIALS = service_account.Credentials.from_service_account_info(
    GKE_POD_SA_KEY)

# create publisher client object using credentials
publisher = pubsub_v1.PublisherClient(credentials=CREDENTIALS)
# create subscriber client object using credentials
subscriber = pubsub_v1.SubscriberClient(credentials=CREDENTIALS)

def create_topic_subs(topic_path,
                      subscription_requests):
  """_summary_

  Args:
      topic_path (_type_): _description_
      subscription_requests (_type_): _description_
  """
  try:
    create_topic(topic_path)
    for subscription_request in subscription_requests:
      create_subscription(subscription_request)
  except AlreadyExists:
    print(f"{topic_path} already exists.")
  except Exception as e:
    print(f"Error occured while creating topic: {topic_path}."
          + f" \nError: {str(e)}")

def create_subscription(subscription_request):
  try:
    subscription = subscriber.create_subscription(
        request=subscription_request)
    print(f"Subscription created: {subscription.name}")
  except AlreadyExists:
    print(f"{subscription_request['name']} already exists.")
  except Exception as e:
    print(
        f"Error occured while creating subscription: {subscription_request['name']}."
        + f" \nError: {str(e)}")

def create_topic(topic_path):
  try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created Pub/Sub topic: {topic.name}")
  except AlreadyExists:
    print(f"{topic_path} already exists.")
  except Exception as e:
    print(f"Error occured while creating topic: {topic_path}."
          + f" \nError: {str(e)}")

if __name__ == "__main__":
  cls_topic_name = DATABASE_PREFIX + "classroom-notifications"
  lms_topic_name = DATABASE_PREFIX + "lms-notifications"
  cls_subscription_name = DATABASE_PREFIX + "classroom-notifications-sub"
  lms_subscription_name = DATABASE_PREFIX + "lms-notifications-push-sub"
  lms_bq_subscription_name = DATABASE_PREFIX + "lms-notifications-bq-sub"
  #generate complete topic path using topic name and project id
  cls_topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID, cls_topic_name)
  lms_topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID, lms_topic_name)

  #generate complete subscription path using subscription name and project id
  cls_subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT_ID,
                                                  cls_subscription_name)
  lms_subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT_ID,
                                                  lms_subscription_name)
  lms_bq_subscription_path = subscriber.subscription_path(
      PUB_SUB_PROJECT_ID, lms_bq_subscription_name)
  create_topic_subs(cls_topic_path,
                    [{
                        "name": cls_subscription_path,
                        "topic": cls_topic_path,
                        "ack_deadline_seconds": 600
                    }])
  # webhook_url = ("https://gcp-classroom-dev.cloudpssolutions.com"
  #                 + "/lms/api/test/webhook")
  # oidc_token = pubsub_v1.types.PushConfig.OidcToken(
  #     service_account_email=
  # f"pub-sub-test@{PROJECT_ID}.iam.gserviceaccount.com")
  # push_config = pubsub_v1.types.PushConfig(
  #   push_endpoint=webhook_url,
  #   oidc_token=oidc_token)
  # subscription request for push config
  # {
  #                       "name": lms_subscription_path,
  #                       "topic": lms_topic_path,
  #                       "push_config": push_config,
  #                   },
  create_bigquery_dataset()
  query = (
    "CREATE TABLE IF NOT EXISTS lms-notifications (subscription_name STRING,"
  + " message_id STRING, publish_time TIMESTAMP, data JSON, attributes JSON);")
  create_table_using_sql(query,"lms-notifications")
  bigquery_table_id = f"{GCP_PROJECT}.{BQ_DATASET}.lms-notifications"
  bigquery_config = pubsub_v1.types.BigQueryConfig(
    table=bigquery_table_id,write_metadata=True,use_topic_schema=True)
  create_topic_subs(lms_topic_path,
                    [{
                        "name": lms_bq_subscription_path,
                        "topic": lms_topic_path,
                        "bigquery_config": bigquery_config,
                        "filter": "attributes.store_to_bq = \"true\""
                    }])
