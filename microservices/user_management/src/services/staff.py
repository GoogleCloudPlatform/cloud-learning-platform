"""Service file for Staff"""
from common.models import Staff
from common.utils.errors import ConflictError


def create_staff(input_staff):
  """Method to create a Staff"""
  existing_staff = Staff.find_by_email(input_staff.email)
  if existing_staff is not None:
    raise ConflictError(
      f"Staff with the given email: {input_staff.email} already exists")
  staff_dict = {**input_staff.dict()}
  staff = Staff()
  staff = staff.from_dict(staff_dict)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()
  staff = staff.get_fields(reformat_datetime=True)
  return staff

def update_staff(uuid, input_staff):
  """Method to update Staff"""
  existing_staff = Staff.find_by_uuid(uuid)
  input_staff_dict = {**input_staff.dict(exclude_unset=True)}
  staff_fields = existing_staff.get_fields()
  for key, value in input_staff_dict.items():
    if value is not None:
      staff_fields[key] = value
  for key, value in staff_fields.items():
    setattr(existing_staff, key, value)
  existing_staff.update()
  staff_fields = existing_staff.get_fields(reformat_datetime=True)
  return staff_fields
