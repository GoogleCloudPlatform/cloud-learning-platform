""" LTI Token utils """
from datetime import datetime
from config import TOKEN_TTL, ISSUER
from common.models import Tool, User, LTIContentItem
from services.keys_manager import get_platform_public_keyset
from jose import jwt


def lti_claim_field(field_type, claim_type, suffix=None):
  """ Add claims field in the token """
  lti_suffix = ("-" + suffix) if suffix else ""
  return "https://purl.imsglobal.org/spec/lti{}/{}/{}".format(
      lti_suffix, field_type, claim_type)


def generate_token_claims(lti_request_type, client_id, login_hint,
                          lti_message_hint, nonce, redirect_uri):
  """ Generate claims for the token """
  tool = Tool.find_by_client_id(client_id)
  tool_info = tool.get_fields(reformat_datetime=True)

  if redirect_uri not in tool_info.get("redirect_uris"):
    raise Exception(f"Unknown redirect_uri {redirect_uri}")

  user = User.find_by_user_id(login_hint)
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
        "deep_link_return_url": ISSUER +
                                "/lti-service/api/v1/content-item-return"
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
  key_set = get_platform_public_keyset()
  token = jwt.encode(
      claims,
      key_set.get("web_key"),
      algorithm="RS256",
      headers={"kid": key_set.get("web_key").get("kid")})
  return token


def decode_token(token, key):
  decoded_token = jwt.decode(
      token=token, algorithms="RS256", key=key, audience=ISSUER)
  return decoded_token
