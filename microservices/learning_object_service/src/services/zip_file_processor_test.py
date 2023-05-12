"""Unit test for zip_file_processor service"""
import shutil
from services.zip_file_processor import recreate_zip_structure_on_gcs

# pylint: disable=unused-import
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from schemas.schema_examples import BASIC_LEARNING_RESOURCE_EXAMPLE
from testing.test_config import (TESTING_FOLDER_PATH)
from config import (ZIP_EXTRACTION_FOLDER)

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=line-too-long

def test_recreate_zip_structure_on_gcs(clean_firestore, mocker):
  mocker.patch("services.zip_file_processor.upload_folder")
  mocker.patch("services.zip_file_processor.download_file_from_gcs", return_value=f"{ZIP_EXTRACTION_FOLDER}/sample_upload_scorm.zip")

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/sample_upload_scorm.zip"
  shutil.copyfile(file_path,f"{ZIP_EXTRACTION_FOLDER}/sample_upload_scorm.zip")

  input_data = {
    "gsutil_uri": "fake_uri",
    "filename": "sample_upload_scorm.zip"
  }
  res = recreate_zip_structure_on_gcs(input_data)

  assert res["success"] is True
  assert res["message"] == "Successfully uploaded the learning content"
