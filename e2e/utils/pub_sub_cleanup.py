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
from google.oauth2 import service_account
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  os.getenv("PROJECT_ID")

# generate credentials using SA json keys
GKE_POD_SA_KEY = json.loads(os.environ.get("GKE_CLASSROOM_POD_SA_KEY"))
CREDENTIALS = service_account.Credentials.from_service_account_info(
  GKE_POD_SA_KEY)
# create publisher client object using credentials
publisher = pubsub_v1.PublisherClient(credentials=CREDENTIALS)
# create subscriber client object using credentials
subscriber = pubsub_v1.SubscriberClient(credentials=CREDENTIALS)

def clean_pub_sub(topic_path, subscription_paths):
  try:
    for subscription_path in subscription_paths:
      delete_subscription(subscription_path)
    publisher.delete_topic(request={"topic": topic_path})
    print(f"Deleted Pub/Sub topic: {topic_path}")
  except Exception as e:
    print("Error occured while deleting topic:"
        + f" {topic_path} \nError: {str(e)}")

def delete_subscription(subscription_path):
  try:
    subscriber.delete_subscription(
          request={"subscription": subscription_path})
    print(f"Subscription deleted: {subscription_path}")
  except Exception as e:
    print("Error occured while deleting Subscription:" +
          f" {subscription_path} \nError: {str(e)}")

if __name__ == "__main__":
  if not DATABASE_PREFIX:
    raise Exception(
        "DATABASE_PREFIX is not defined. Deleting Pub/Sub skipped.")
  cls_topic_name = DATABASE_PREFIX + "classroom-notifications"
  lms_topic_name = DATABASE_PREFIX + "lms-notifications"
  cls_subscription_name = DATABASE_PREFIX + "classroom-notifications-sub"
  lms_subscription_name = DATABASE_PREFIX + "lms-notifications-push-sub"
  lms_bq_subscription_name = DATABASE_PREFIX + "lms-notifications-bq-sub"
  #generate complete topic path using topic name and project id
  cls_topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID, cls_topic_name)
  lms_topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID, lms_topic_name)

  #generate complete subscription path using subscription name and project id
  cls_subscription_path = subscriber.subscription_path(
    PUB_SUB_PROJECT_ID,cls_subscription_name)
  lms_subscription_path = subscriber.subscription_path(
    PUB_SUB_PROJECT_ID, lms_subscription_name)
  lms_bq_subscription_path = subscriber.subscription_path(
      PUB_SUB_PROJECT_ID, lms_bq_subscription_name)
  clean_pub_sub(cls_topic_path, [cls_subscription_path])
  clean_pub_sub(
    lms_topic_path,[lms_subscription_path,lms_bq_subscription_path])
