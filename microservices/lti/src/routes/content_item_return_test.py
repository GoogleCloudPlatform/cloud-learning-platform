"""
  Unit tests for LTI Platform Auth endpoints
"""
import os
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long

from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from testing.test_config import API_URL
import mock
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.content_item_return import router
  from schemas.schema_examples import BASIC_TOOL_EXAMPLE

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

test_key_set = {
    "key": "test_rsa_key",
    "key_id": "key_hash_value",
    "public_keyset": {
        "keys": [{
            "kty": "RSA",
            "alg": "RS256",
            "kid": "key_hash_value",
            "use": "sig",
            "e": "v92b7ey9o",
            "n": "obvr189yr398bPNv"
        }]
    },
    "web_key": {
        "kty": "RSA",
        "alg": "RS256",
        "kid": "key_hash_value",
        "use": "sig",
        "e": "v92b7ey9o",
        "n": "obvr189yr398bPNv"
    }
}


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
@mock.patch("routes.content_item_return.get_remote_keyset")
@mock.patch("routes.content_item_return.get_unverified_token_claims")
@mock.patch("routes.content_item_return.decode_token")
def test_token(mock_token, mock_claims, mock_key_set, clean_firestore,
               create_tool):

  test_tool = create_tool
  test_claims = {
      "https://purl.imsglobal.org/spec/lti/claim/message_type":
          "LtiDeepLinkingResponse",
      "https://purl.imsglobal.org/spec/lti/claim/version":
          "1.3.0",
      "https://purl.imsglobal.org/spec/lti/claim/deployment_id":
          "63cadc04-247a-48ce-a2e0-978a8d083f45",
      "iss":
          test_tool.client_id,
      "aud":
          "https://ef26-103-199-92-113.in.ngrok.io",
      "iat":
          1672925046,
      "exp":
          1672925346,
      "nonce":
          "42f15eb07d27b0c91e51",
      "https://purl.imsglobal.org/spec/lti-dl/claim/content_items": [{
          "type": "html",
          "html": "<h1>A Custom Title</h1>"
      }, {
          "type": "link",
          "title": "My Home Page",
          "url": "https://something.example.com/page.html",
          "icon": {
              "url": "https://lti.example.com/image.jpg",
              "width": 100,
              "height": 100
          },
          "thumbnail": {
              "url": "https://lti.example.com/thumb.jpg",
              "width": 90,
              "height": 90
          }
      }, {
          "type": "image",
          "url": "https://www.example.com/image.png",
          "https://www.example.com/resourceMetadata": {
              "license": "CCBY4.0"
          }
      }, {
          "type": "ltiResourceLink",
          "title": "A title",
          "text": "This is a link to an activity that will be graded",
          "url": "https://lti-ri.imsglobal.org/lti/tools/3495/launches",
          "icon": {
              "url": "https://lti.example.com/image.jpg",
              "width": 100,
              "height": 100
          },
          "thumbnail": {
              "url": "https://lti.example.com/thumb.jpg",
              "width": 90,
              "height": 90
          },
          "lineItem": {
              "scoreMaximum": 87,
              "label": "Chapter 12 quiz",
              "resourceId": "xyzpdq1234",
              "tag": "originality"
          },
          "available": {
              "startDateTime": "2022-12-28T13:24:06+00:00",
              "endDateTime": "2023-01-17T13:24:06+00:00"
          },
          "submission": {
              "endDateTime": "2023-01-11T13:24:06+00:00"
          },
          "custom": {
              "quiz_id": "az-123",
              "duedate": "2023-01-11T13:24:06+00:00"
          },
          "window": {
              "targetName": "examplePublisherContent"
          },
          "iframe": {
              "height": 890,
              "width": 890
          }
      }, {
          "type": "file",
          "title": "A file like a PDF that is my assignment submissions",
          "url": "https://my.example.com/assignment1.pdf",
          "mediaType": "application/pdf",
          "expiresAt": "2023-01-13T13:24:06+00:00"
      }],
      "https://purl.imsglobal.org/spec/lti-dl/claim/msg":
          "Successfuly added 5 Content Items from Reference Implementation",
      "https://purl.imsglobal.org/spec/lti-dl/claim/log":
          "Reference Implementation requested that the following type of content items be added: [\"html_link\", \"html_item\", \"image_item\", \"lti_link\", \"file_link\"]"
  }

  mock_token.return_value = test_claims
  mock_claims.return_value = test_claims

  mock_key_set.return_value = test_key_set
  url = f"{API_URL}/content-item-return"
  resp = client_with_emulator.post(url, data={"JWT": "eys.ej3k.sa4f"})

  assert resp.status_code == 200
