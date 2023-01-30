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
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  os.getenv("PROJECT_ID")

# generate credentials using SA json keys
GKE_POD_SA_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CREDENTIALS = service_account.Credentials.from_service_account_info(
    GKE_POD_SA_KEY)

try:
  # create publisher client object using credentials
  publisher = pubsub_v1.PublisherClient(credentials=CREDENTIALS)
  # create subscriber client object using credentials
  subscriber = pubsub_v1.SubscriberClient(credentials=CREDENTIALS)

  topic_name = DATABASE_PREFIX + "classroom-messeges"
  subscription_name = DATABASE_PREFIX + "classroom-messeges-sub"
  #generate complete topic path using topic name and project id
  topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID, topic_name)

  #generate complete subscription path using subscription name and project id
  subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT_ID,
                                                   subscription_name)

  topic = publisher.create_topic(request={"name": topic_path})
  print(f"Created Pub/Sub topic: {topic.name}")
  subscription = subscriber.create_subscription(request={
      "name": subscription_path,
      "topic": topic_path,
      "ack_deadline_seconds":600
  })
  print(f"Subscription created: {subscription.name}")
except AlreadyExists:
  print(f"{topic_name} already exists.")
except Exception as e:
  print(f"Error occured while creating topic: {topic_path}. \nError: {str(e)}")
