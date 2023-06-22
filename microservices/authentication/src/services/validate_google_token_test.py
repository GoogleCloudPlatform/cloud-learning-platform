"""
utility methods to execute unit tests for module validate_google_token.py
"""
from unittest import mock
from services.validate_google_token import validate_google_oauth_token
from schemas.schema_examples import DECODED_TOKEN_EXAMPLE

token = "eyewiuovnhy3b.oiuewvryn919123b85n913vnp19qvm92vb.w9euvyn0f091823b"


@mock.patch("services.validate_google_token.id_token.verify_oauth2_token")
def test_validate_google_token(mock_validate_google_oauth_token):

  mock_validate_google_oauth_token.return_value = DECODED_TOKEN_EXAMPLE
  result = validate_google_oauth_token(token)

  assert result["email"] == DECODED_TOKEN_EXAMPLE["email"]
