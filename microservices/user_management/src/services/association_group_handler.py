"""Functions to fetch data from association groups"""
from services.collection_handler import CollectionHandler
from common.models import AssociationGroup
from concurrent.futures import ThreadPoolExecutor
# pylint:disable=line-too-long


def is_learner_association_group(association_group_fields):
  return association_group_fields.get("association_type") == "learner"


def is_discipline_association_group(association_group_fields):
  return association_group_fields.get("association_type") == "discipline"


def get_all_learner_association_groups():
  learner_association_groups = AssociationGroup.collection.filter(
                "association_type", "==", "learner").fetch()
  learner_group_fields = [i.get_fields() for i in learner_association_groups]
  return learner_group_fields


def check_instructor_discipline_association(instructor_id,
                                            curriculum_pathway_id,
                                            discipline_group_fields):
  """Checks if given instructor is actively associated to any discipline
  in any discipline association group"""
  is_instructor_active = False
  for group in discipline_group_fields:
    for user_dict in group.get("users"):
      if instructor_id == user_dict["user"] and \
        user_dict["status"] == "active":
        for curriculum_pathway_dict in group.get("associations").get(
            "curriculum_pathways"):
          if curriculum_pathway_id == curriculum_pathway_dict["curriculum_pathway_id"] \
            and curriculum_pathway_dict["status"] == "active":
            is_instructor_active = True
  return is_instructor_active


def fetch_firestore_doc(data: dict, collection: str=None, key_name: str=None):
  doc_fields = CollectionHandler.get_document_from_collection(
            collection, data.get(key_name))
  if key_name == "instructor":
    if data.get("curriculum_pathway_id"):
      curriculum_pathway_fields = CollectionHandler.get_document_from_collection(
          "curriculum_pathways", data.get("curriculum_pathway_id"))
      doc_fields["curriculum_pathway_id"] = curriculum_pathway_fields
  data[key_name] = doc_fields
  return data

def load_learner_group_field_data(association_group_fields):
  """Fetches entire documents from respective collections for fields in
  association group of learner type"""
  if association_group_fields.get("users"):
    user_details = []

    child_count = len(association_group_fields.get("users"))
    with ThreadPoolExecutor(max_workers=child_count) as executor:
      user_details = list(
        executor.map(fetch_firestore_doc,
                     association_group_fields.get("users"), "users", "user"))

    association_group_fields["users"] = user_details

  if association_group_fields.get("associations").get("coaches"):
    coaches_list = association_group_fields.get("associations").get("coaches")
    coach_details = []

    child_count = len(coaches_list)
    with ThreadPoolExecutor(max_workers=child_count) as executor:
      coach_details = list(executor.map(
        fetch_firestore_doc, coaches_list, "users", "coach"))
    association_group_fields["associations"]["coaches"] = coach_details

  if association_group_fields.get("associations").get("instructors"):
    instructors_list = association_group_fields.get("associations").get(
        "instructors")
    instructor_details = []

    with ThreadPoolExecutor(max_workers=child_count) as executor:
      instructor_details = list(executor.map(
        fetch_firestore_doc, instructors_list, "users", "instructor"))
    association_group_fields["associations"]["instructors"] = instructor_details

  if association_group_fields.get("associations").get("curriculum_pathway_id"):
    curriculum_pathway_id = association_group_fields.get("associations").get(
        "curriculum_pathway_id")
    if curriculum_pathway_id:
      curriculum_pathway_fields = CollectionHandler.get_document_from_collection(
          "curriculum_pathways", curriculum_pathway_id)
      association_group_fields["associations"]["curriculum_pathway_id"] = \
        curriculum_pathway_fields

  return association_group_fields


def load_discipline_group_field_data(association_group_fields):
  """Fetches entire documents from respective collections for fields in
  association group of discipline type"""
  if association_group_fields["users"]:
    user_details = []

    child_count = len(association_group_fields.get("users"))
    with ThreadPoolExecutor(max_workers=child_count) as executor:
      user_details = list(
        executor.map(fetch_firestore_doc,
                     association_group_fields.get("users"), "users", "user"))
    association_group_fields["users"] = user_details

  if association_group_fields.get("associations").get("curriculum_pathways"):
    curriculum_pathway_list = association_group_fields.get("associations").get(
        "curriculum_pathways")
    curriculum_pathway_details = []

    with ThreadPoolExecutor(max_workers=child_count) as executor:
      user_details = list(
        executor.map(fetch_firestore_doc,
                     curriculum_pathway_list, "curriculum_pathways", "curriculum_pathway_id"))
    association_group_fields["associations"]["curriculum_pathways"] = \
      curriculum_pathway_details

  return association_group_fields


def instructor_exists_in_lag(association_grp, instructor_uuid):
  """
      This function checks if an instructor belongs to a
      learner assoication group
      ---------------------------------------------------
      Args:
        association_grp: Association Group firestore document
        instructor_uuid: UUID of the instructor
      ---------------------------------------------------
      Returns:
        True: If the instructor exists
        False: Otherwise
    """
  instructor_list = association_grp.associations.get("instructors",[])
  for instructor in instructor_list:
    if instructor["instructor"] == instructor_uuid:
      return True
  return False

def remove_instructor_from_lag(instructor_uuid):
  """Function to remove instructor from learner association groups"""
  # Filter Learner Association Groups
  association_grp_manager = AssociationGroup.collection
  association_grp_manager = association_grp_manager.filter(
      "association_type", "==", "learner")
  learner_association_grp_list = association_grp_manager.fetch()

  # Remove User from Learner Association Groups

  # We are iterating over the list because we do not have
  # access to curriculum pathway id
  for learner_association_grp in learner_association_grp_list:
    if instructor_exists_in_lag(learner_association_grp, instructor_uuid) is True:
      new_lag_instructor_list = []
      for instructor in learner_association_grp.associations["instructors"]:
        if instructor["instructor"] != instructor_uuid:
          new_lag_instructor_list.append(instructor)

      # Update Learner association group
      lag_associations = learner_association_grp.associations
      lag_associations["instructors"] = new_lag_instructor_list
      learner_association_grp.associations = lag_associations
      learner_association_grp.update()

def remove_instructor_from_dag(instructor_uuid, instructor_status):
  """Function to remove instructor from discipline association groups"""
  comparison_key = "users"
  comparator = {
          "status": instructor_status,
          "user": instructor_uuid,
          "user_type": "instructor"
      }

  # Filter Discipline Association Groups
  discipline_association_manager = AssociationGroup.collection
  discipline_association_manager = discipline_association_manager.filter(
      "association_type", "==", "discipline")
  discipline_association_manager = discipline_association_manager.filter(
        comparison_key, "array_contains", comparator)
  discipline_association_list = discipline_association_manager.fetch()

  # Remove Instructor from all linked Discipline Association Groups
  for discipline_association_grp in discipline_association_list:
    new_dag_instructor_list = []
    for instructor in discipline_association_grp.users:
      if instructor["user"] != instructor_uuid:
        new_dag_instructor_list.append(instructor)

    # Update Discipline association group
    discipline_association_grp.users = new_dag_instructor_list
    discipline_association_grp.update()

def remove_user_from_association_group(user_uuid, user_type, user_status):
  """
        This function removes the references of the given user
        from all the linked association groups
        --------------------------------------------------------
        Args:
        user_uuid: uuid of the user whose reference should be removed
        user_type: type of the user that should be removed
        user_status: status of the given user
    """
  try:

    # Setting up variables
    association_group_type = "learner"
    if user_type in ["instructor", "assessor"]:
      association_group_type = "discipline"

    comparison_key = ""
    comparator = {}
    if user_type == "learner":
      comparison_key = "users"
      comparator = {"status": user_status, "user": user_uuid}

    elif user_type == "assessor":
      comparison_key = "users"
      comparator = {
          "status": user_status,
          "user": user_uuid,
          "user_type": "assessor"
      }
    elif user_type == "coach":
      comparison_key = "associations.coaches"
      comparator = {"status": user_status, "coach": user_uuid}

    # Filter required association groups
    association_grp_manager = AssociationGroup.collection
    association_grp_manager = association_grp_manager.filter(
        "association_type", "==", association_group_type)
    association_grp_manager = association_grp_manager.filter(
        comparison_key, "array_contains", comparator)
    association_grp_list = association_grp_manager.fetch()

    # User should be removed from each Association Group
    for association_group_doc in association_grp_list:

      # Create a reference list of users
      doc_user_list = []
      if user_type in ["learner", "assessor"]:
        doc_user_list = association_group_doc.users
      elif user_type == "coach":
        doc_user_list = association_group_doc.associations["coaches"]

      user_uuid_key = "user"
      if user_type == "coach":
        user_uuid_key = "coach"

      # Create a new list of users which excludes given user
      user_list = []
      for record in doc_user_list:
        if record[user_uuid_key] != user_uuid:
          user_list.append(record)

      # Update the association group with new list of users
      if user_type in ["learner", "assessor"]:
        association_group_doc.users = user_list
      elif user_type == "coach":
        association_group_doc.associations["coaches"] = user_list

      association_group_doc.update()

  except Exception as e:
    print(e)

def update_refs_for_user_by_type(user_doc):
  """
        Update the references for the User in all Association Groups.
        The function checks the type of the user and updates the
        references appropraitely using the following
        user_type and association_grp type mapping.

        1. learner: learner_association_grp
        2. coach: learner_association_grp
        3. instructor: learner_association_grp, discipline_association_grp
        4. assessor: discipline_association_grp

        --------------------------------------------------------
        Args:
        user_doc: User firestore document
    """

  if user_doc.user_type == "instructor":
    remove_instructor_from_lag(user_doc.user_id)
    remove_instructor_from_dag(user_doc.user_id, "active")
    remove_instructor_from_dag(user_doc.user_id, "inactive")
  else:
    remove_user_from_association_group(user_doc.user_id, user_doc.user_type,
                                      "active")
    remove_user_from_association_group(user_doc.user_id, user_doc.user_type,
                                     "inactive")

def remove_discipline_from_learner_association_group(discipline_id):
  """Function to remove discipline from learner association groups"""
  # Logic to remove instructor associated from learner association group
  # Fetch all learner association groups
  learner_group_fields = get_all_learner_association_groups()

  # Find Learner Association Group in which discipline to remove exists
  # & remove instructor linked to given discipline (curriculum_pathway_id)
  for group in learner_group_fields:
    for instructor_dict in group.get("associations",{}).get("instructors",[]):
      if discipline_id == \
          instructor_dict.get("curriculum_pathway_id"):
        group.get("associations").get("instructors")[:] = [
          instructor for instructor in group.get("associations").get(
          "instructors") if instructor.get("curriculum_pathway_id") != \
            discipline_id]
        learner_association_group_object = AssociationGroup.find_by_uuid(
          group["uuid"])
        for key, value in group.items():
          setattr(learner_association_group_object, key, value)
        learner_association_group_object.update()
