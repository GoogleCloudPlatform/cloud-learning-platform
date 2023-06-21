"""Module to add FAQ Content in FireO"""
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField, BooleanField

# TODO: Use this function to validate the FAQ Type
def check_faq_type(field_val):
  faq_types = ["faq_item", "faq_group"]
  if field_val.lower() in faq_types:
    return True
  return (False, "FAQ Type must be one of " +
          ",".join("'" + i + "'" for i in faq_types))

class FAQContent(BaseModel):
  """FAQContent Class"""
  # schema for object
  uuid = TextField(required=True)
  resource_path = TextField()
  name = TextField(max_length=100)
  curriculum_pathway_id = TextField()
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "faq_contents"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    faq_content = FAQContent.collection.filter("uuid", "==", uuid).filter(
        "is_deleted", "==", is_deleted).get()
    if faq_content is None:
      raise ResourceNotFoundException(f"FAQ with uuid {uuid} not found")
    return faq_content
