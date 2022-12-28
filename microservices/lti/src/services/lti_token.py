""" LTI Token utils """
import json
from datetime import datetime
from jose import jwt, jws
from common.models import Tool, TempUser, LTIContentItem, LineItem
from services.keys_manager import get_platform_public_keyset
from config import TOKEN_TTL, ISSUER


def lti_claim_field(field_type, claim_type, suffix=None):
  """ Add claims field in the token """
  lti_suffix = ("-" + suffix) if suffix else ""
  # pylint: disable-next=line-too-long
  return f"https://purl.imsglobal.org/spec/lti{lti_suffix}/{field_type}/{claim_type}"


def generate_token_claims(lti_request_type, client_id, login_hint,
                          lti_message_hint, nonce, redirect_uri):
  """ Generate claims for the token """
  tool = Tool.find_by_client_id(client_id)
  tool_info = tool.get_fields(reformat_datetime=True)

  if redirect_uri not in tool_info.get("redirect_uris"):
    raise Exception(f"Unknown redirect_uri {redirect_uri}")

  user = TempUser.find_by_user_id(login_hint)
  user = user.get_fields(reformat_datetime=True)
  token_claims = {
      "iss": ISSUER,
      "aud": client_id,
      "nonce": nonce,
      "iat": int(datetime.now().timestamp()),
      "exp": int(datetime.now().timestamp()) + TOKEN_TTL,
      "sub": login_hint,
      "given_name": user.get("last_name"),
      "first_name": user.get("first_name"),
      "name": user.get("first_name") + " " + user.get("last_name"),
      "email": user.get("email")
  }

  if lti_request_type == "deep_link":
    token_claims[lti_claim_field("claim", "deep_linking_settings", "dl")] = {
        "accept_types": ["link", "file", "html", "ltiResourceLink", "image"],
        "accept_presentation_document_targets": ["iframe", "window", "embed"],
        "accept_multiple": False,
        "auto_create": False,
        "title": "",
        "text": "",
        "deep_link_return_url": ISSUER + "/lti/api/v1/content-item-return"
    }

    token_claims[lti_claim_field("claim",
                                 "message_type")] = "LtiDeepLinkingRequest"

  if lti_request_type == "resource_link":
    token_claims[lti_claim_field("claim",
                                 "message_type")] = "LtiResourceLinkRequest"

    lti_content_item = LTIContentItem.find_by_uuid(lti_message_hint)

    content_item_info = lti_content_item.content_item_info
    if content_item_info:
      if content_item_info.get("url"):
        token_claims[lti_claim_field(
            "claim", "target_link_uri")] = content_item_info.get("url")
      else:
        token_claims[lti_claim_field("claim",
                                     "target_link_uri")] = tool_info["tool_url"]

    if "custom" in content_item_info.keys():
      token_claims[lti_claim_field("claim",
                                   "custom")] = content_item_info.get("custom")

    if "lineItem" in content_item_info.keys():
      line_item = LineItem.find_by_resource_link_id(lti_content_item.uuid)

      token_claims[lti_claim_field("claim", "endpoint", "ags")] = {
          "scope": [
              lti_claim_field("scope", "lineitem", "ags"),
              lti_claim_field("scope", "result.readonly", "ags"),
              lti_claim_field("scope", "score", "ags")
          ],
          "lineitems": ISSUER + "/lti-service/api/v1/1234/line_items",
          "lineitem": ISSUER + "/lti-service/api/v1/1234/line_items/" +
                      line_item.uuid
      }

    resource_link_claim_info = {
        "id": lti_message_hint,
        "title": content_item_info.get("title"),
        "description": content_item_info.get("text")
    }

    token_claims[lti_claim_field("claim",
                                 "resource_link")] = resource_link_claim_info

  token_claims[lti_claim_field("claim", "version")] = "1.3.0"
  token_claims[lti_claim_field("claim",
                               "deployment_id")] = tool_info["deployment_id"]

  if user.get("user_type") == "learner":
    token_claims[lti_claim_field("claim", "roles")] = [
        "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Student"
    ]
  elif user.get("user_type") == "faculty":
    token_claims[lti_claim_field("claim", "roles")] = [
        "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Faculty",
        "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"
    ]
    # Role claims for Admin -
    # http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator
    # http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator

  return token_claims


def encode_token(claims):
  """Generates a token by encoding the given claims using the private key"""
  key_set = get_platform_public_keyset()
  token = jwt.encode(
      claims,
      key_set.get("web_key"),
      algorithm="RS256",
      headers={"kid": key_set.get("web_key").get("kid")})
  return token


def decode_token(token, key, audience):
  """Decodes a given token and verifies it using the provided public key"""
  decoded_token = jwt.decode(
      token=token, algorithms="RS256", key=key, audience=audience)
  return decoded_token


def get_unverified_token_claims(token):
  """Decodes a given token using the provided public key"""
  unverified_claims = jws.get_unverified_claims(token=token).decode("UTF-8")
  return json.loads(unverified_claims)
