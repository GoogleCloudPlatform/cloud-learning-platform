"""CRUD for Competency"""

from common.models import Course, Competency, LearningContentItem
from common.utils.cache_service import delete_key
from common.utils.errors import ResourceNotFoundException

#pylint: disable=redefined-builtin,broad-exception-raised,protected-access


class CompetencyService():
  """Class for Competency"""

  def create_course_competency(self, course_id, competency):
    """creates a competency"""
    comp = Competency()
    for key, value in competency.items():
      setattr(comp, key, value)
    parent = Course.find_by_id(course_id)
    if parent:
      comp.save()
      parent.competency_ids.append(comp.id)
      parent.save()
    return self.get_course_competency(comp.id, parent.id)

  def get_course_competency(self, id, parent_id):
    """returns competency given id"""
    course = Course.find_by_id(parent_id)
    competency = Competency.find_by_id(id)
    if competency:
      if not id in course.competency_ids:
        raise ResourceNotFoundException(
            "This competency is not associated with current course")
      try:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        return competency_item
      except (TypeError, KeyError) as e:
        raise Exception("Failed to fetch competency") from e
    else:
      raise ResourceNotFoundException("Competency with this ID does not exists")

  def get_course_all_competencies(self, course_id):
    """returns all competencies given course"""
    competency_list = []
    course = Course.find_by_id(course_id)
    try:
      course.load_children()
      for competency in course.competencies:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        competency_list.append(competency_item)
      return competency_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all competencies") from e

  def update_course_competency(self, id, competency, parent_id):
    """updates all fields and/or parent of a competency"""
    course = Course.find_by_id(parent_id)
    comp = Competency.find_by_id(id)
    if not id in course.competency_ids:
      raise ResourceNotFoundException(
          "This competency is not associated with current course")
    try:
      competency_fields = comp.get_fields()
      for key, value in competency.items():
        competency_fields[key] = value
      for key, value in competency_fields.items():
        setattr(comp, key, value)
      comp.update()
      return self.get_competency(comp.id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update the competency") from e

  def delete_course_competency(self, id, parent_id):
    """deletes a competency"""
    competency = Competency.find_by_id(id)
    if competency:
      # competency.delete_tree()
      parent = Course.find_by_id(parent_id)
      if id in parent.competency_ids:
        parent.competency_ids.remove(id)
        parent.save()
      else:
        raise ResourceNotFoundException(
            "Course does not have this competency associated")

  def create_competency(self, competency):
    """creates a competency"""
    comp = Competency()
    for key, value in competency.items():
      setattr(comp, key, value)
    comp.save()
    return self.get_competency(comp.id)

  def get_competency(self, id, is_text_required=False):
    """returns competency given id"""
    competency = Competency.find_by_id(id)
    try:
      competency_item = competency.get_fields(reformat_datetime=True)
      competency_item["id"] = competency.id
      if is_text_required:
        competency.load_children()
        competency_text = []
        for sub_competency in competency.sub_competencies:
          sub_competency.load_children()
          for learning_objective in sub_competency.learning_objectives:
            competency_text.extend(learning_objective.text.split("<p>"))
        competency_item["text"] = competency_text
      return competency_item
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch competency") from e

  def get_all_competencies(self):
    """returns all competencies given course"""
    competency_list = []
    try:
      competencies = Competency.collection.fetch()
      for competency in competencies:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        competency_list.append(competency_item)
      return competency_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all competencies") from e

  def update_competency(self, id, competency):
    """updates all fields and/or parent of a competency"""
    comp = Competency.find_by_id(id)
    try:
      competency_fields = comp.get_fields()
      for key, value in competency.items():
        competency_fields[key] = value
      for key, value in competency_fields.items():
        setattr(comp, key, value)
      comp.update()
      return self.get_competency(comp.id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update the competency") from e

  def delete_competency(self, id):
    """deletes a competency"""
    competency = Competency.find_by_id(id)
    all_courses = Course.collection.fetch()
    for course in all_courses:
      associated_comp_ids = course.competency_ids
      if id in associated_comp_ids:
        associated_comp_ids.remove(id)
        course.competency_ids = associated_comp_ids
        course.save()
        # removing the cached course as topic tree
        # changes on deleting the competency
        delete_key(course.id)

    all_lc = LearningContentItem.collection.fetch()
    for lc in all_lc:
      associated_comp_ids = lc.competency_ids
      if id in associated_comp_ids:
        associated_comp_ids.remove(id)
        lc.competency_ids = associated_comp_ids
        lc.save()

    competency.delete_tree()

  def create_learning_content_competency(self, content_id, competency):
    """creates a competency"""
    comp = Competency()
    for key, value in competency.items():
      setattr(comp, key, value)
    parent = LearningContentItem.find_by_id(content_id)
    if parent:
      comp.save()
      parent.competency_ids.append(comp.id)
      parent.save()
    return self.get_learning_content_competency(comp.id, parent.id)

  def get_learning_content_competency(self, id, parent_id):
    """returns competency given id"""
    learning_content = LearningContentItem.find_by_id(parent_id)
    competency = Competency.find_by_id(id)
    if competency:
      if not id in learning_content.competency_ids:
        raise ResourceNotFoundException(
            "This competency is not associated with current Learning Content")
      try:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        return competency_item
      except (TypeError, KeyError) as e:
        raise Exception("Failed to fetch competency") from e

  def get_all_learning_content_competencies(self, content_id):
    """returns all competencies given course"""
    competency_list = []
    learning_content = LearningContentItem.find_by_id(content_id)
    try:
      learning_content.load_children()
      for competency in learning_content.competencies:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        competency_list.append(competency_item)
      return competency_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all competencies") from e

  def update_learning_content_competency(self, id, competency, parent_id):
    """updates all fields and/or parent of a competency"""
    learning_content = LearningContentItem.find_by_id(parent_id)
    comp = Competency.find_by_id(id)
    if not id in learning_content.competency_ids:
      raise ResourceNotFoundException(
          "This competency is not associated with current course")
    try:
      competency_fields = comp.get_fields()
      for key, value in competency.items():
        competency_fields[key] = value
      for key, value in competency_fields.items():
        setattr(comp, key, value)
      comp.update()
      return self.get_competency(comp.id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update the competency") from e

  def delete_learning_content_competency(self, id, parent_id):
    """deletes a competency"""
    Competency.find_by_id(id)
    parent = LearningContentItem.find_by_id(parent_id)
    if id in parent.competency_ids:
      parent.competency_ids.remove(id)
      parent.save()
    else:
      raise ResourceNotFoundException(
          "Learning Content does not have this competency associated")
