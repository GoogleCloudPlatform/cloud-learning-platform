"""Unit Test for Association Group Handler"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from schemas.schema_examples import (BASIC_USER_MODEL_EXAMPLE,
                                     BASIC_ASSOCIATION_GROUP_EXAMPLE)
from services.association_group_handler import (
    remove_user_from_association_group,
    remove_instructor_from_dag,
    remove_instructor_from_lag)
from testing.test_config import (API_URL)
from common.models import UserGroup, User, AssociationGroup
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

def set_up_data():
  """Function for setup data"""
  lag_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  lag_dict["association_type"] = "learner"
  lag_dict["is_immutable"] = True
  lag_dict["users"] = []
  lag_dict["associations"] = {}
  lag_dict["uuid"] = ""
  lag_doc = AssociationGroup.from_dict(lag_dict)
  lag_doc.save()
  lag_doc.uuid = lag_doc.id
  lag_doc.update()

  dag_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  dag_dict["association_type"] = "discipline"
  dag_dict["is_immutable"] = True
  dag_dict["users"] = []
  dag_dict["associations"] = {}
  dag_dict["uuid"] = ""
  dag_doc = AssociationGroup.from_dict(dag_dict)
  dag_doc.save()
  dag_doc.uuid = dag_doc.id
  dag_doc.update()

  return lag_doc.uuid, dag_doc.uuid


def test_remove_learner_from_association_group(clean_firestore):
  lag_uuid, _ = set_up_data()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["user_type"] = "learner"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  lag_doc.users = [{"status": "active", "user": user.user_id}]
  lag_doc.update()

  remove_user_from_association_group(user.user_id, user.user_type, user.status)

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  assert len(lag_doc.users) == 0


def test_remove_coach_from_association_group(clean_firestore):
  lag_uuid, _ = set_up_data()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["user_type"] = "coach"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  lag_doc.associations = {
      "coaches": [{
          "status": "active",
          "coach": user.user_id
      }]
  }
  lag_doc.update()

  remove_user_from_association_group(user.user_id, user.user_type, user.status)

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  assert len(lag_doc.associations["coaches"]) == 0


def test_remove_assessor_from_association_group(clean_firestore):
  _, dag_uuid = set_up_data()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["user_type"] = "assessor"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  dag_doc = AssociationGroup.find_by_uuid(dag_uuid)
  dag_doc.users = [{
      "status": "active",
      "user": user.user_id,
      "user_type": user.user_type
  }]
  dag_doc.update()

  remove_user_from_association_group(user.user_id, user.user_type, user.status)

  dag_doc = AssociationGroup.find_by_uuid(dag_uuid)
  assert len(dag_doc.users) == 0


def test_remove_instructor_from_association_group(clean_firestore):
  lag_uuid, dag_uuid = set_up_data()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["user_type"] = "instructor"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  lag_doc.associations = {
      "instructors": [{
          "curriculum_pathway_id": "random_pathway_id",
          "status": "active",
          "instructor": user.user_id
      }]
  }
  lag_doc.update()

  dag_doc = AssociationGroup.find_by_uuid(dag_uuid)
  dag_doc.users = [{
      "status": "active",
      "user": user.user_id,
      "user_type": user.user_type
  }]
  dag_doc.update()

  remove_instructor_from_dag(user.user_id, user.status)

  dag_doc = AssociationGroup.find_by_uuid(dag_uuid)
  assert len(dag_doc.users) == 0

  remove_instructor_from_lag(user.user_id)

  lag_doc = AssociationGroup.find_by_uuid(lag_uuid)
  assert len(lag_doc.associations["instructors"]) == 0
