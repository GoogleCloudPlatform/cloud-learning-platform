"""Base class for Node items"""

import sys
from common.models import BaseModel


#pylint:disable=dangerous-default-value
class NodeItem(BaseModel):
  """Node Item Class"""

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # "parent" is protected keyword in FireO
    self.parent_node = None
    self.parent_learning_content = None
    self.children_nodes = []

  # def __eq__(self, other):
  #     # TODO: double check this picks up porper class
  #     if isinstance(other, self.__class__):
  #         return self.__dict__ == other.__dict__

  class Meta:
    abstract = True

  def add_child(self, *args, **kwargs):
    """ looks up the object type of the child, needs to be imported"""
    # TODO: better way to do this introspection?
    child_object = getattr(sys.modules[self.module], self.child_type)
    child = child_object(*args, **kwargs)
    self.children_nodes.append(child)
    child.parent_node = self

    return child

  # TODO: remove this?
  #pylint: disable=redefined-builtin
  def add_child_from_dict(self, dict):
    """adds child from a dict"""
    child_object = getattr(sys.modules[self.module], self.child_type)
    child = child_object.from_dict(dict)

    self.children_nodes.append(child)
    child.parent_node = self

    return child

  # TODO: make transactional?
  def load_tree(self):
    """ loads entire tree """
    self.load_children()
    if self.children_nodes:
      for child in self.children_nodes:
        child.load_tree()

  def load_children(self):
    """loads child nodes"""
    # test to see if leaf node
    if self.child_type is not None:
      # TODO: ensure modules always avilable
      # TODO: order?
      child_object = getattr(sys.modules[self.module],
                           self.child_type)
      if hasattr(self, "uuid"):
        if isinstance(self.parent_node, list) or self.parent_node is None:
          children = child_object.collection.filter(
            "parent_node", "array_contains", self.uuid).fetch()
      else:
        children = child_object.collection.filter(
          "parent_node", "==", self.key).fetch()
      for child in children:
        self.children_nodes.append(child)

  # TODO: make transactional?
  def save_tree(self, *args, **kwargs):
    """saves entire tree"""
    super().save(*args, **kwargs)
    for child in self.children_nodes:
      child.save_tree(**kwargs)

  def update_tree(self, *args, **kwargs):
    """updates entire tree"""
    super().update(*args, **kwargs)
    for child in self.children_nodes:
      child.update_tree(*args, **kwargs)

  def delete_tree(self, *args, **kwargs):
    """deletes entire tree"""
    self.load_children()
    if self.children_nodes:
      for child in self.children_nodes:
        child.delete_tree(*args, **kwargs)
    self.delete_by_id(self.id)

  def delete_child_tree(self, *args, **kwargs):
    """deletes all child trees"""
    self.load_children()
    if self.children_nodes:
      for child in self.children_nodes:
        child.delete_tree(*args, **kwargs)

  def upsert_tree(self, *args, **kwargs):
    """upserts entire tree"""
    super().upsert(*args, **kwargs)
    for child in self.children_nodes:
      child.upsert_tree(*args, **kwargs)

  @classmethod
  def find_by_title(cls, title, is_deleted = False):
    return cls.collection.filter("title", "==",
      title).filter("is_deleted", "==", is_deleted).get()

  @classmethod
  def find_by_name(cls, name):
    return cls.collection.filter("name", "==", name).get()
