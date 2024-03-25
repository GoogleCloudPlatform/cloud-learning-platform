""" Config used for testing in unit tests """
# pylint: disable=line-too-long
import os

API_URL = "http://localhost/skill-service/api/v1"

TEST_IMPORT_URLS = [
    "https://credentialengineregistry.org/resources/ce-ece7cefa-3c0f-42fe-9e51-f24e5489aa0c"
]

TEST_EMSI_URL = "https://emsiservices.com/skills/versions/latest/skills?fields=id%2Cname%2Ctype%2CinfoUrl%2Ctags&limit=10"

TESTING_FOLDER_PATH = os.path.join(os.getcwd(), "testing")
