""" Function to get all discipline list for given program
"""
from common.models import AssociationGroup
from common.utils.collection_references import collection_references


def get_all_discipline_for_given_program(uuid, nodes):
  """
  Args:
    uuid (str): uuid of the node from where to traverse.
    nodes (list): list to be used to return list of nodes
  Returns:
    nodes (list): List of uuids of discipline
  """
  node = collection_references["curriculum_pathways"].find_by_uuid(uuid)
  node = node.get_fields(reformat_datetime=True)
  if node.get("alias", "") == "discipline":
    nodes.append(node["uuid"])
    return
  child_nodes = node.get("child_nodes", [])
  if child_nodes:
    for child_level in child_nodes:
      for child_uuid in child_nodes[child_level]:
        get_all_discipline_for_given_program(child_uuid, nodes)

  nodes = list(set(nodes))
  return nodes

def get_all_assign_user_for_given_instructor_or_coach(uuid, user_type):
  """
    Args:
    uuid (str): uuid of the instructor or coach
    user_type (str): type the the given uuid (instructor/coach)
  Returns:
    users (list): List of users belong to the given instructor
  """

  association_groups = AssociationGroup.collection.filter(
        "association_type", "==", "learner"
        ).order("-created_time").fetch()

  learner_list = []

  staff_type = "instructors"
  if user_type == "coach":
    staff_type = "coaches"

  for association_group in association_groups:
    if any((staff.get(user_type,"") == uuid and
            staff.get("status","") == "active") for staff in
           association_group.associations.get(staff_type,[])):
      learner_list.extend(association_group.users)

  users = list({learner["user"] for learner in learner_list if
                learner.get("status", "")=="active"})
  return users
