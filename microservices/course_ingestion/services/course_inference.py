"""
CRUD for course
"""
import re
from typing import Dict
from utils.paginator import pagination
from common.utils.gcs_adapter import GcsCrudService
from common.utils.errors import ResourceNotFoundException, PayloadTooLargeError
from common.models import Course, Competency, LearningContentItem
from common.utils.cache_service import set_key, get_key, delete_key, \
  set_key_normal, get_key_normal
from config import PROJECT_ID, PAYLOAD_FILE_SIZE


# pylint: disable=redefined-builtin,broad-exception-raised,protected-access
# pylint: disable=raising-bad-type


class CourseService():
  """Class for course"""

  def create_course(self, course):
    """creates a course"""
    new_course = Course()
    from_learning_content = course.get("add_competencies_from_learning_content",
                                       False)
    if from_learning_content:
      course["competency_ids"] = self.get_all_learning_content_competencies(
        course.get("learning_content_ids", []))
    for key, value in course.items():
      if key != "competency_ids":
        setattr(new_course, key, value)
      elif key == "competency_ids":
        if not from_learning_content:
          self.validate_new_competencies(value)
        setattr(new_course, key, list(set(value)))
    new_course.save()
    return self.get_course(new_course.id)

  def get_all_learning_content_competencies(self, learning_content_ids):
    all_competencies = []
    for lc_id in learning_content_ids:
      learning_content = LearningContentItem.find_by_id(lc_id)
      learning_content.load_children()
      for competency in learning_content.competencies:
        all_competencies.append(competency.id)
    return all_competencies

  def get_all_courses(self, skip: int, limit: int, sort_by: str, order_by: str,
                      competencies: bool, search_query: str):
    """returns all the courses"""
    course_list = []
    ord_by = order_by
    if sort_by == "ascending" and order_by != "title":
      ord_by = order_by
    elif sort_by == "descending" and order_by != "title":
      ord_by = "-{}".format(order_by)
    courses = Course.collection.order(ord_by).fetch()
    if courses:
      try:
        for course in courses:
          course_dict = course.get_fields(reformat_datetime=True)
          course_dict["id"] = course.id
          competency_list = []
          if competencies:
            course.load_children()
            for competency in course.competencies:
              competency_item = competency.get_fields(reformat_datetime=True)
              competency_item["id"] = competency.id
              competency_list.append(competency_item)
            course_dict["competencies"] = competency_list
          course_dict.pop("competency_ids", None)
          course_list.append(course_dict)

        if search_query is not None:
          course_list = [course for course in course_list if
                         search_query.lower() in course["title"].lower()]

        if sort_by == "ascending" and order_by == "title":
          course_list = sorted(course_list, key=lambda i: i["title"].lower())
        elif sort_by == "descending" and order_by == "title":
          course_list = sorted(course_list, key=lambda i: i["title"].lower(),
                               reverse=True)
        if skip == 0 and limit == 0:
          return course_list
        elif skip < 0 or limit < 0:
          raise Exception("The skip and limit value should be a positive "
                          "number")
        else:
          result = pagination(payload=course_list, skip=skip, limit=limit)
          return {"data": result, "total_rec": len(course_list)}
      except (TypeError, KeyError) as e:
        raise Exception("Failed to fetch all courses") from e
    else:
      raise ResourceNotFoundException("No courses found")

  def get_course(self, id):
    """returns course details for a given course id"""
    course = Course.find_by_id(id)
    try:
      course_dict = course.get_fields(reformat_datetime=True)
      course_dict["id"] = course.id
      course.load_children()
      competency_list = []
      for competency in course.competencies:
        competency_item = competency.get_fields(reformat_datetime=True)
        competency_item["id"] = competency.id
        competency_list.append(competency_item)
      course_dict["competencies"] = competency_list
      course_dict.pop("competency_ids", None)
      return course_dict
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch the course") from e

  def validate_new_competencies(self, competency_ids):
    """Validates competency ids if they exist or not
    from the competency ids list"""
    for id in competency_ids:
      Competency.find_by_id(id)

  def update_course(self, id, course_request):
    """updates a given course"""
    course = Course.find_by_id(id)
    try:
      course_fields = course.get_fields()
      for key, value in course_request.items():
        if key != "competency_ids":
          course_fields[key] = value
        elif key == "competency_ids":
          self.validate_new_competencies(value)
          course_fields[key] = list(set(value))
      for key, value in course_fields.items():
        setattr(course, key, value)
      course.update()
      return self.get_course(id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update course") from e

  def delete_course(self, id):
    """deletes course given course id"""
    course = Course.find_by_id(id)
    course.delete_by_id(id)

  def add_competencies(self, id, request_body):
    """Updates and adds new competencies to the course"""
    course = Course.find_by_id(id)
    try:
      course_fields = course.get_fields()
      for key, value in request_body.items():
        if key != "competency_ids":
          course_fields[key] = value
      for key, value in course_fields.items():
        setattr(course, key, value)
      new_competency_ids = request_body.get("competency_ids", [])
      if new_competency_ids:
        existing_comp_ids = course_fields["competency_ids"]
        new_competency_ids = set(new_competency_ids) - set(existing_comp_ids)
        new_competency_ids = list(new_competency_ids)
        self.validate_new_competencies(new_competency_ids)
        course_fields["competency_ids"].extend(new_competency_ids)
        setattr(course, "competency_ids", course_fields["competency_ids"])
      course.update()
      return self.get_course(id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update the course") from e

  def fetch_course_linked_contents(self, course_id: str) -> list:
    """
    Function is used to fetch course level learning contents
    :param course_id: str
    :return: list
    """
    result = []
    doc_key = f"courses/{course_id}"
    course_details = Course.collection.get(key=doc_key)
    content_details = LearningContentItem.collection.fetch()
    for content in content_details:
      lin_comp = []
      for com_id in content.competency_ids:
        for cou_com in course_details.competency_ids:
          if com_id == cou_com:
            lin_comp.append(cou_com)
      if lin_comp:
        if len(lin_comp) == len(content.competency_ids):
          partial_linked = False
        else:
          partial_linked = True
        res = {
          "lc_title": content.title,
          "lc_id": content.id,
          "partial_linked": partial_linked,
          "linked_competencies": lin_comp
        }
        result.append(res)
    return result

  def validate_upload_course_pdf_service(self, course_pdf: object,
                                         user_id: str) -> Dict:
    """
    Function is used to upload course pdf to gcs bucket
    :param course_pdf: file object
    :param user_id: string
    :return: string
    """
    file = course_pdf[0]
    gcs_service = GcsCrudService(PROJECT_ID)

    try:
      search = re.search(".pdf$", file["filename"].lower())
      if search is not None:
        folders = gcs_service.fetch_all_blobs(prefix="course-resources")
        folders = [blob.name for blob in folders if ".pdf" in blob.name.lower()]
        gs_files = [gs_file.split("/")[2] for gs_file in folders]

        if file["filename"].lower() not in gs_files:
          res = {"validation": True, "message": "File is ready to upload"}
        else:
          res = {"validation": False,
                 "message": f"The file already exists under this file name "
                            f"'{file['filename'].split('.')[0]}'. Click "
                            f"'Cancel' to cancel the upload or 'Yes' to "
                            f"overwrite the existing file. "}

        if len(file["body"]) <= PAYLOAD_FILE_SIZE:
          set_key(key=f"{user_id}_file_name", value=file["filename"],
                  expiry_time=600)
          set_key_normal(key=f"{user_id}_file_body", value=file["body"],
                         expiry_time=600)
        else:
          raise PayloadTooLargeError(
            "File size is too large to upload,please use the file upto 80MB")

        return res

      else:
        return {"validation": False,
                "message": f"Invalid file format"
                           f" {file['filename'].split('.')[1]}, Course file "
                           f"must be in PDF format only,other formats will not "
                           f"be accepted. Please try again with the PDF file. "}
    except IndexError:
      return {"validation": False,
              "message": f"There is no file extension in the file called "
                         f"'{file['filename']}'.So, upload the PDF file with "
                         f"the file extension."}

  def upload_course_pdf_service(self, user_id: str) -> Dict[str, str]:
    """
    Function to upload the PDF file to gcs bucket
    :param user_id: str
    :return: str
    """
    file_name = get_key(key=f"{user_id}_file_name")
    file_body = get_key_normal(key=f"{user_id}_file_body")
    res = GcsCrudService(PROJECT_ID).upload_file_to_gcs_bucket(
      file_name=file_name, file_body=file_body,
      parent_folder_name="course-resources")
    res["file_name"] = file_name

    delete_key("file_name")
    delete_key("file_body")

    return res

  def fetch_all_course_pdf_service(self, search_query: str) -> list:
    """
    Function to fetch all the PDF file from GCS bucket
    :param search_query: string
    :return: list
    """
    gs_path = []
    gcs_service = GcsCrudService(PROJECT_ID)
    blobs = gcs_service.fetch_all_blobs(prefix="course-resources")
    for blob in blobs:
      path = f"gs://{PROJECT_ID}/{blob.name}"
      file_name = blob.name.lower()
      if ".pdf" in file_name.lower():
        if search_query is None:
          gs_path.append({
            "gs_path": path,
            "file_path": file_name,
            "file_name": file_name.split("/")[2].split(".")[0]
          })
        else:
          if search_query.lower() in (file_name.split("/")[2].split(".")[
            0].lower()):
            gs_path.append({
              "gs_path": path,
              "file_path": file_name,
              "file_name": file_name.split("/")[2].split(".")[0]
            })
    return gs_path

  def delete_the_blob_from_bucket(self, gs_path: str) -> str:
    """
    Function to delete the blob from the GCS bucket
    :param gs_path: string
    :return: str
    """
    gcs_service = GcsCrudService(PROJECT_ID)
    res = gcs_service.delete_file_from_gcs_bucket(blob_name=gs_path)

    return res
