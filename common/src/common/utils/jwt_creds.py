"""Generate JWT credentials"""
import datetime
import json
import google.auth
from google.oauth2 import service_account
from google.auth import _helpers
from google.auth.transport.requests import AuthorizedSession

_DEFAULT_TOKEN_LIFETIME_SECS = 3600  # 1 hour in seconds
_GOOGLE_OAUTH2_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

# disabling for linting to pass
# pylint: disable = bad-classmethod-argument
class JwtCredentials(service_account.Credentials):
  """ JWT credentials class"""
  def _make_authorization_grant_assertion(self):
    """Create the OAuth 2.0 assertion.
        This assertion is used during the OAuth 2.0 grant to acquire an
        access token.
        Returns:
            bytes: The authorization grant assertion.
        """
    now = _helpers.utcnow()
    lifetime = datetime.timedelta(seconds=_DEFAULT_TOKEN_LIFETIME_SECS)
    expiry = now + lifetime

    payload = {
        "iat": _helpers.datetime_to_secs(now),
        "exp": _helpers.datetime_to_secs(expiry),
        # The issuer must be the service account email.
        "iss": self._service_account_email,
        # The audience must be the auth token endpoint's URI
        "aud": _GOOGLE_OAUTH2_TOKEN_ENDPOINT,
        "scope": _helpers.scopes_to_string(self._scopes or ()),
    }

    payload.update(self._additional_claims)

    # The subject can be a user email for domain-wide delegation.
    if self._subject:
      payload.setdefault("sub", self._subject)

    iam_payload = {"payload": json.dumps(payload)}

    default_creds, _ = google.auth.default()
    authed_session = AuthorizedSession(default_creds)
    iam_url = "https://iamcredentials.googleapis.com/v1/projects/-"\
    "/serviceAccounts/"+self._service_account_email + ":signJwt"
    response = authed_session.request("POST",
                                      url=iam_url,
                                      data=json.dumps(iam_payload))
    return response.json()["signedJwt"]

  @classmethod
  def from_default_with_subject(self, subject, service_account_email,
                                token_uri, scopes):
    """returns the JWT credentials object"""
    return self(signer=None,
                service_account_email=service_account_email,
                token_uri=token_uri,
                subject=subject,
                scopes=scopes)

