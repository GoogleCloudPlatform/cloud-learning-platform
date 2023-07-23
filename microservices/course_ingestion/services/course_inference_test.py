"""Test file for course inference"""

import pytest
import sys

# disabling as we need to append path for common
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
# pylint: disable=protected-access

sys.path.append("../../common/src")
import common
from common.utils.gcs_adapter import GcsCrudService
from common.utils.errors import ResourceNotFoundException
from common.models import (Course, Competency, LearningContentItem)
from testing.example_objects import (TEST_COURSE, TEST_LEARNING_CONTENT,
                                     TEST_COMPETENCY)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock

with mock.patch("google.cloud.logging.Client",
                side_effect=mock.MagicMock()) as mok:
  from services.course_inference import CourseService


# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


class TestGcsCrudService(GcsCrudService):

  def __init__(self, bucket_name):
    self.bucket_name = bucket_name

  def get_bucket_folders(self, prefix):
    self.prefix = prefix
    return []
class GCSObject:
  name = "course-resources/test/test.pdf"


@pytest.fixture(name="get_course_object")
def get_course_object():
  """returns LU object"""
  course_obj = CourseService()
  return course_obj


def test_create_course(clean_firestore, get_course_object):
  """tests create course"""
  function_output = get_course_object.create_course(TEST_COURSE)
  assert isinstance(function_output, dict)
  assert "id" in function_output
  assert Course.find_by_id(function_output["id"]) is not None


def test_get_course(clean_firestore, get_course_object):
  """tests get_course"""
  with pytest.raises(ResourceNotFoundException):
    get_course_object.get_course("test_id")
  course = Course.from_dict(TEST_COURSE)
  course.save()
  function_output = get_course_object.get_course(course.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == course.id


def test_get_all_courses(clean_firestore, get_course_object):
  """tests get all courses"""

  course = Course.from_dict(TEST_COURSE)
  course.save()
  function_output = get_course_object.get_all_courses(skip=0, limit=10,
                                                      sort_by="descending",
                                                      order_by="title",
                                                      competencies=False,
                                                      search_query=None)
  assert isinstance(function_output, dict)


def test_delete_course(clean_firestore, get_course_object):
  """tests delete_course"""
  with pytest.raises(ResourceNotFoundException):
    get_course_object.delete_course("test_id")
  course = Course.from_dict(TEST_COURSE)
  course.save()
  # pylint: disable=assignment-from-no-return
  function_output = get_course_object.delete_course(course.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    Course.find_by_id(course.id)


def test_update_course(clean_firestore, get_course_object):
  """tests update_course"""
  with pytest.raises(ResourceNotFoundException):
    get_course_object.update_course("test_id", [])
  course = Course.from_dict(TEST_COURSE)
  course.save()
  with pytest.raises(Exception):
    get_course_object.update_course(course.id, [])
  updated_course_fields = {"title": "Updated title"}
  function_output = get_course_object.update_course(course.id,
                                                    updated_course_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == course.id
  assert function_output["title"] == updated_course_fields["title"]


def test_add_competencies(clean_firestore, get_course_object):
  """tests add_competencies"""
  with pytest.raises(ResourceNotFoundException):
    get_course_object.add_competencies("test_id", [])
  course = Course.from_dict(TEST_COURSE)
  course.save()
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  with pytest.raises(Exception):
    get_course_object.add_competencies(course.id, None)
  function_output = get_course_object.add_competencies(
    course.id, {"competency_ids": [competency.id]})
  assert isinstance(function_output, dict)
  assert function_output["id"] == course.id
  assert function_output["competencies"][0]["id"] == competency.id


def test_get_all_learning_content_competencies(clean_firestore,
                                               get_course_object):
  """tests get all competencies from learning content"""
  with pytest.raises(ResourceNotFoundException):
    get_course_object.get_all_learning_content_competencies(["abcd"])
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  lc = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  lc.competency_ids = [competency.id]
  lc.save()
  fetched_competencies = get_course_object. \
    get_all_learning_content_competencies([lc.id])
  assert isinstance(fetched_competencies, list)
  assert fetched_competencies == [competency.id]


@mock.patch("services.course_inference.GcsCrudService")
@mock.patch("services.course_inference.set_key")
@mock.patch("services.course_inference.set_key_normal")
def test_validate_the_course_pdf(mock_gcs_adapter, mock_set_key,
                                 mock_set_key_normal):
  """
  Unit test to validate the course PDF with correct payload
  Parameters
  ----------
  Returns
  -------
  None
  """
  req_body = [{
    "filename": "sample1.2.pdf",
    "body": "Hello world"
  }]
  course_obj = CourseService()
  mock_gcs_adapter.return_value = TestGcsCrudService(req_body[0]["filename"])
  res = course_obj.validate_upload_course_pdf_service(course_pdf=req_body,
                                                      user_id="12344")
  mock_set_key.return_value = "sample.pdf"
  mock_set_key_normal.return_value = "Hello World"
  assert res["message"] is not None
  assert res["validation"] is True


@mock.patch("services.course_inference.GcsCrudService")
@mock.patch("services.course_inference.set_key")
@mock.patch("services.course_inference.set_key_normal")
def test_validate_the_course_pdf_with_incorrect_file(mock_gcs_adapter,
                                                     mock_set_key,
                                                     mock_set_key_normal):
  """
  Unit test to validate the course PDF with correct payload
  Parameters
  ----------
  Returns
  -------
  None
  """
  req_body = [{
    "filename": "sample.jpg",
    "body": "Hello world"
  }]
  course_obj = CourseService()
  mock_gcs_adapter.return_value = TestGcsCrudService(req_body[0]["filename"])
  res = course_obj.validate_upload_course_pdf_service(course_pdf=req_body,
                                                      user_id="12344")
  mock_set_key.return_value = "sample.pdf"
  mock_set_key_normal.return_value = "Hello World"
  assert res["message"] is not None
  assert res["validation"] is False


@mock.patch("services.course_inference.set_key")
@mock.patch("services.course_inference.set_key_normal")
@mock.patch("services.course_inference.GcsCrudService")
def test_validate_the_course_pdf_with_incorrect_file_format(
mock_set_key, mock_set_key_normal, mock_gcs_adapter):
  """
  Unit test to validate the course PDF with correct payload
  Parameters
  ----------
  Returns
  -------
  None
  """
  req_body = [{
    "filename": "sample",
    "body": "Hello world"
  }]
  course_obj = CourseService()
  mock_gcs_adapter.return_value = TestGcsCrudService(req_body[0]["filename"])

  res = course_obj.validate_upload_course_pdf_service(course_pdf=req_body,
                                                      user_id="12344")
  mock_set_key.return_value = "sample.pdf"
  mock_set_key_normal.return_value = "Hello World"
  assert res["message"] is not None
  assert res["validation"] is False


@mock.patch("services.course_inference.set_key")
@mock.patch("services.course_inference.set_key_normal")
@mock.patch("services.course_inference.GcsCrudService")
def test_validate_the_course_pdf_with_existing_file(mock_set_key,
                                                    mock_set_key_normal,
                                                    mock_gcs_adapter):
  """
  Unit test to validate the course PDF with correct payload
  Parameters
  ----------
  Returns
  -------
  None
  """
  req_body = [{
    "filename": "test.pdf",
    "body": "Hello world"
  }]
  course_obj = CourseService()
  mock_gcs_adapter.return_value = TestGcsCrudService(req_body[0]["filename"])
  res = course_obj.validate_upload_course_pdf_service(course_pdf=req_body,
                                                        user_id="12344")
  mock_set_key.return_value = "test.pdf"
  mock_set_key_normal.return_value = "Hello World"
  assert res["message"] is not None


@mock.patch("services.course_inference.get_key")
@mock.patch("services.course_inference.get_key_normal")
@mock.patch("services.course_inference.delete_key")
@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService,
                   "upload_file_to_gcs_bucket")
def test_upload_course_pdf(mock_get_key,
                           mock_get_key_normal,
                           mock_delete_key,
                           mock_gcs_adapter,
                           mock_upload_file_to_gcs_bucket
                           ):
  """
  Unit test to upload course PDF to GCS bucket
  Parameters
  ----------
  None
  Returns
  -------
  None
  """
  obj = GCSObject()
  course_obj = CourseService()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_upload_file_to_gcs_bucket.return_value = {"gs_path": f"gs://{obj.name}"}
  res = course_obj.upload_course_pdf_service(user_id="12344")

  assert res is not None

@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService, "fetch_all_blobs")
def test_fetch_all_course_pdf(mock_fetch_all_blobs, mock_gcs_adapter):
  """
  Unit Test to fetch all the course PDF
  Parameters
  ----------
  mock_fetch_all_blobs

  Returns
  -------
  None
  """
  course_obj = CourseService()
  obj = GCSObject()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_fetch_all_blobs.return_value = [obj, ]
  res = course_obj.fetch_all_course_pdf_service(search_query=None)
  assert res[0]["file_path"] == obj.name
  assert isinstance(res, list)


@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService, "fetch_all_blobs")
def test_search_course_pdf(mock_fetch_all_blobs, mock_gcs_adapter):
  """
  Unit Test to search the course PDF
  Parameters
  ----------
  mock_fetch_all_blobs

  Returns
  -------
  None
  """
  course_obj = CourseService()
  obj = GCSObject()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_fetch_all_blobs.return_value = [obj, ]
  res = course_obj.fetch_all_course_pdf_service(search_query="test")
  assert res[0]["file_path"] == obj.name
  assert isinstance(res, list)


@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService, "fetch_all_blobs")
def test_search_course_pdf_with_incorrect_query(mock_fetch_all_blobs,
                                                mock_gcs_adapter):
  course_obj = CourseService()
  obj = GCSObject()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_fetch_all_blobs.return_value = [obj, ]
  res = course_obj.fetch_all_course_pdf_service(search_query="sample")
  assert not res
  assert isinstance(res, list)

@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService, "fetch_all_blobs")
def test_search_course_pdf_with_partial_query(mock_fetch_all_blobs,
                                              mock_gcs_adapter):
  course_obj = CourseService()
  obj = GCSObject()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_fetch_all_blobs.return_value = [obj, ]
  res = course_obj.fetch_all_course_pdf_service(search_query="te")
  assert res[0]["file_path"] == obj.name
  assert isinstance(res, list)

@mock.patch("services.course_inference.GcsCrudService")
@mock.patch.object(common.utils.gcs_adapter.GcsCrudService,
                   "delete_file_from_gcs_bucket")
def test_delete_blob(mock_delete_file_from_gcs_bucket, mock_gcs_adapter):
  """
  Unit to delete the blob from the GCS bucket
  Parameters
  ----------
  Returns
  -------
  None
  """
  course_obj = CourseService()
  obj = GCSObject()
  mock_gcs_adapter.return_value = TestGcsCrudService(obj.name)
  mock_delete_file_from_gcs_bucket.return_value = "test is deleted successfully"
  res = course_obj.delete_the_blob_from_bucket(gs_path=obj.name)
  assert res == "test is deleted successfully"
