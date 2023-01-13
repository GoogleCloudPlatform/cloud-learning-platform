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
import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  os.getenv("PROJECT_ID")
topic_id=DATABASE_PREFIX+"classroom-messeges"
subscription_id=DATABASE_PREFIX+"classroom-messeges-sub"
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(PUB_SUB_PROJECT_ID,topic_id)
subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT_ID,
                                                 subscription_id)
try:
  topic = publisher.create_topic(request={"name": topic_path})
  print(f"Created Pub/Sub topic: {topic.name}")
  subscription = subscriber.create_subscription(request={
      "name": subscription_path,
      "topic": topic_path
  })
  print(f"Subscription created: {subscription.name}")
except AlreadyExists:
  print(f"{topic_id} already exists.")
except Exception as e:
  print(f"Error occured while creating topic: {topic_path}. \nError: {str(e)}")
