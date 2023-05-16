"""service file to create learner and learner profile"""
#pylint: disable=broad-exception-raised,redefined-builtin,unused-argument
#from common.utils.rest_method import post_method, delete_method, put_method
from common.utils.errors import ValidationError, ConflictError
from common.models import Learner, LearnerProfile, Achievement
#from config import SLP_BASE_URL
#pylint: disable=broad-exception-raised


# pylint: disable = broad-exception-raised

def create_learner(headers: dict = None,
                   learner_dict: dict = None):
  """Post request to student learner profile service to create learner"""
  # TODO: Enable API call to SLP service after SLP is moved to CLP
  # api_url = f"{SLP_BASE_URL}/learner"
  # response = post_method(url=api_url,
  #                        request_body=learner_dict,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to create learner")
  # learner_id = response.json().get("data").get("uuid")
  # return learner_id
  new_learner = Learner()
  learner = Learner.collection.filter("email_address", "==",
    learner_dict.get("email_address", "").lower()).filter(
    "is_deleted", "==", False).get()
  # Checking if a learner document already exists with the same email id
  if learner is not None:
    email = learner_dict.get("email_address", "").lower()
    raise ConflictError(
        f"Learner with the given email address {email} already exists")
  # Checking if the learner email id and backup email id are the same
  if learner_dict.get("email_address", "").lower() == \
    learner_dict.get("backup_email_address", "").lower():
    raise ValidationError(
      "Primary email address and backup email address cannot be the same.")
  new_learner = new_learner.from_dict(learner_dict)
  new_learner.uuid = ""
  new_learner.save()
  new_learner.uuid = new_learner.id
  new_learner.update()
  return new_learner.uuid


def create_learner_profile(headers: dict = None,
                           learner_id: str = None,
                           learner_profile_dict: dict = None):
  """Post request to student learner profile service to create learner
  profile"""
  # TODO: Enable API call to SLP service after SLP is moved to CLP
  # api_url = f"{SLP_BASE_URL}/learner/{learner_id}/learner-profile"
  # if learner_profile_dict is None:
  #   learner_profile_dict = {}
  # response = post_method(url=api_url,
  #                        request_body=learner_profile_dict,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to create learner profile")
  learner = Learner.find_by_uuid(learner_id)\
  # Check if learner is archived
  if learner.is_archived is True:
    raise ValidationError("Learner Profile cannot be created for the Learner"
                          f" id: {learner_id} which is archived")
  # Checking if a learner_profile already exists with the same learner id
  learner_profile = LearnerProfile.collection.\
    filter("learner_id", "==", learner_id).get()
  if learner_profile is not None:
    raise ConflictError(
        f"Learner Profile with the given learner id: {learner_id} "
        "already exists")
  new_learner_profile = LearnerProfile()
  learner_profile_dict["learner_id"] = learner_id
  if learner_profile_dict["achievements"]:
    for achievement_id in learner_profile_dict["achievements"]:
      Achievement.find_by_id(achievement_id)
  new_learner_profile = new_learner_profile.from_dict(
      learner_profile_dict)
  new_learner_profile.uuid = ""
  new_learner_profile.save()
  new_learner_profile.uuid = new_learner_profile.id
  new_learner_profile.update()


def delete_learner(headers: dict = None,
                   learner_id: str = None):
  """Delete request to student learner profile service to delete learner"""
  # TODO: Enable API call to SLP service after SLP is moved to CLP
  # api_url = f"{SLP_BASE_URL}/learner/{learner_id}"
  # response = delete_method(url=api_url,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to delete learner")
  Learner.delete_by_uuid(learner_id)


def delete_learner_profile(headers: dict = None,
                           learner_id: str = None):
  """Delete request to student learner profile service to delete learner
  profile"""
  # TODO: Enable API call to SLP service after SLP is moved to CLP
  # api_url = f"{SLP_BASE_URL}/learner/{learner_id}/learner-profile"
  # response = delete_method(url=api_url,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to delete learner profile")
  existing_learner_profile = LearnerProfile.find_by_learner_id(learner_id)
  learner_profile_id = existing_learner_profile.uuid
  LearnerProfile.delete_by_uuid(learner_profile_id)


def update_learner(headers: dict = None,
                   learner_id: str = None,
                   learner_dict: dict = None):
  """PUT request to student-learner-profile service to update learner"""
  # TODO: Enable API call to SLP service after SLP is moved to CLP
  # api_url = f"{SLP_BASE_URL}/learner/{learner_id}"
  # response = put_method(url=api_url,
  #                       request_body=learner_dict,
  #                       token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to update learner")
  existing_learner = Learner.find_by_uuid(learner_id)

  archive = learner_dict.get("is_archived")
  if archive is not None:
    Learner.archive_by_uuid(learner_id, archive=archive)

  learner_fields = existing_learner.get_fields()

  # Check if the existing backup email and updated primary email are the same
  # pylint: disable=C0301
  if (learner_dict.get("email_address", "").lower() == \
    learner_fields["backup_email_address"] and \
    learner_fields["backup_email_address"]) or \
    learner_dict.get("backup_email_address", "").lower() == \
    learner_fields["email_address"]:
    raise ValidationError(
      "Primary email address and backup email address cannot be the same.")

  if learner_dict.get("email_address") and \
    learner_dict.get("backup_email_address"):
    if learner_dict["email_address"] == \
      learner_dict["backup_email_address"]:
      raise ValidationError(
        "Primary email address and backup email address cannot be the same.")

  for key, value in learner_dict.items():
    if value is not None:
      learner_fields[key] = value
  for key, value in learner_fields.items():
    setattr(existing_learner, key, value)
  existing_learner.update()
