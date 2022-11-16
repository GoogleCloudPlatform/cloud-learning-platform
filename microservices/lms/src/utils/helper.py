""" Helper Functions"""

from google.cloud import secretmanager
import google_crc32c
import json

def get_gke_pd_sa_key_from_secret_manager():
    """Copy course  API

  Args:
  Returns:
    return the POD service account keys in JSON format
    """""
    
    client = secretmanager.SecretManagerServiceClient()
    secret_id="gke-pod-sa-key"
    version_id="1"
    secret_name = f"projects/core-learning-services-dev/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": secret_name})
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        return response
    payload = response.payload.data.decode("UTF-8")
    response = json.loads(payload)
    return response

def convert_cohort_to_cohort_model(cohort):
    loaded_cohort = cohort.to_dict()
    course_template = loaded_cohort.pop("course_template").to_dict()
    loaded_cohort["course_template"] = course_template["key"]
    return loaded_cohort
