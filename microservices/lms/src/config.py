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

"""
  Sample Service config file
"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
# CLASSROOM_SA_KEY_PATH = "./keys/{}-classroom-sa-key.json".format(PROJECT_ID)
CLASSROOM_SA_KEY_PATH = "utils/service.json"
# CLASSROOM_KEY = os.getenv("CLASSROOM_SA_KEYS","")
CLASSROOM_KEY={
  "type": "service_account",
  "project_id": "core-learning-services-dev",
  "private_key_id": "b0fde31fcd02857b474ca2807af55320756ac0f5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCDoDKK8A1ljSFg\np/OBXHObLcpbd3XWb142vrmfTW7QKS/8V05McJrxod6coYIPaH7vPnmBRuDAWlWT\nWK652JBLtJmWG8phdNZzBT/cM+UyjT+x3T23TghwYC8zmoqeeeFcqyecYZcrAybj\nwH14+5n5Zr1c9017iJ13VJN11kgqvfUTNl7edx70tfoWVuJ8zUYYPjwN+QpDG2UJ\nLc5YOzyBo4zpmliGzE7mZ3u+hgyUJsB4lpNh5Snc2AS6V2UgEyDLtufwcFEYHImU\ngPyYitP6A63OANBUw9NEEsppYE4tOo1mZzzvrY/MDcbZXue7FyzH6KvcXI4SpdM8\nuVsoTXubAgMBAAECggEAF8lmCOS7zwvTqdeAMnMGM1dxl9j9Uxy6LnOGMQs5yOWA\nlf4jGL5KyfsCM1Uen3E3az3jkGDCMhDBIUkn/k7sOLow/UcVakpGjO+4bC92ro2H\nIroEMrGn5cMEFLPLdDs7ZldJ58FdI7lEmGkLY8c4OrF97CSG/JmiN1Px+Bwa25pJ\nLG8bW8k/3A7VT1pm8X0824qsGGpOyXc/3/etEAEvySb6C3ShCSfruvRg8aHRyyVR\nnoMiXDg90kfvu/Dl67AglP6pIYLesftT6j+kgHKuo4zJ9Ah5/WtQ1vwjBiEOdb08\nI94JGTybP+qzRrlzTJf7SQXsvmpXoUl6ysNZkt6vHQKBgQC4ADHgynWginfOds/m\nQ5D1T4RRZL5KtYr50k8dKW1kbwzryokDXNWVv8ncz7PqkKwpbtWqfRg2el9+aHol\no8FAHnSoh3M1cQN6OL025rO4LlT3KhLUEq6Cs5CWEVvBzym7Ij6YbZN1xPyb1EyM\nN/wC4yBrFPluzIhXhtREtR3JbQKBgQC3IXjaDaNH2f1Ljj3HYzKaUulpxH0G6OYE\nwOHN1zl+Dzi3vj/TxNwFJFJ3hGzKnPdY7i2Hbw9qqvZ0Z0VyfCKT4tOu3Yb3K18u\nmgPugJYDLoJFv3KEyD4Nxxkvyb6cPMjrv5a4CuDzh8aqvu+qHW7LrDt02ni5wVHS\npElEWx98JwKBgQCOQfBOOJm61nOMWAWipIh1cNX/S+Fnx3Y8ceIizL270bPutTc7\nN1IWpiI+qwMSDmpc2kktt+u5auFbzRDq+vFVTnapOZfUMJ0cqLN5t+IpOwEL2yaV\neiAcAxJ9Q8xqSm2cNfypQsaoXfVj0T6hhkM8RDfzMlMq281pxl9lA5aU/QKBgQCJ\nH1cObwfD1UYEPQ2lLnHFfC+qMqYrdlhFVue86VrzORKPArVoLA9TCk91joKnc8EB\npdYRgudYR4sivfESOEDr2vwGA3n7uU4b5tbqzv2EhF6nOyLUqdtNFbeWQMmo0xre\n6yY/yGWH9DKdxzpNdpxvhRc/+BZNgKNzxe/WbyS0IQKBgFBirLLkmFcGHfw+FFWf\nSMLPXzwwwFyEBjGeko1deGigahc1ZZvcKDElIGhAVz/5eIUdnBpHcaRzKZq/pmfp\nUE4txgwZnLBLH3N4jCaUiXbIU8ZxRBEcxG7g1Rjs/o+d0iqjz1NBhptK6fKuwl8Z\nLC66BpnOH1KPvak9kzqDs9do\n-----END PRIVATE KEY-----\n",
  "client_email": "gke-pod-sa@core-learning-services-dev.iam.gserviceaccount.com",
  "client_id": "104636564660654922211",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gke-pod-sa%40core-learning-services-dev.iam.gserviceaccount.com"
}

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

CLASSROOM_ADMIN_EMAIL = os.getenv("CLASSROOM_ADMIN_EMAIL")