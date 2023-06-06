"""Functions for submitted assessment endpoints."""
import traceback
import requests
from requests.exceptions import ConnectTimeout
import datetime
from learnosity_sdk.request import Init
from common.utils.logging_handler import Logger
from config import (LEARNOSITY_CONSUMER_KEY, LEARNOSITY_URL,
                    LEARNOSITY_CONSUMER_SECRET, LEARNOSITY_DOMAIN,
                    AUTOGRADED_TAGS, USE_LEARNOSITY_SECRET)

#pylint: disable=unnecessary-list-index-lookup,simplifiable-if-expression
def learnosity_request(url, service, request, user_id=None, action="get"):
  """Create signed request for Learnosity"""
  try:
    security = {
        "consumer_key": LEARNOSITY_CONSUMER_KEY,
        "domain": LEARNOSITY_DOMAIN
    }
    if user_id is not None:
      security["user_id"] = user_id
    security["timestamp"] = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M")
    consumer_secret = LEARNOSITY_CONSUMER_SECRET

    init = Init(service, security, consumer_secret, request, action)
    req = init.generate()

    res = requests.post(LEARNOSITY_URL + url, data=req, timeout=15)
    response = res.json()

    Logger.info(f"Request :: {req}")
    Logger.info(f"Status :: {res.status_code}")
    Logger.info(f"Response :: {response}")

    return response
  except ConnectTimeout as e:
    Logger.info(f"Status :: {res.status_code}")
    Logger.info(f"Response :: {response}")
    raise ConnectTimeout("Learnosity Data API: Connection Timeout") from e
  except Exception as e:
    Logger.info(f"Status :: {res.status_code}")
    Logger.error(traceback.print_exc())
    raise e


def fetch_activity(activity_template_id):
  """Fetch tags for a particular activity"""
  if not activity_template_id:
    return []

  url = "/itembank/activities"
  request = {"references": [activity_template_id]}
  response = learnosity_request(url, "data", request)
  response = response.get("data")
  if response:
    # FIXME: Extract tag Literal instead of whole dict
    return response[0]

  return {}


def fetch_items(item_ids):
  """Fetch tags for a particular activity"""
  if not item_ids:
    return []
  url = "/itembank/items"
  request = {"references": item_ids}
  response = learnosity_request(url, "data", request)
  if response:
    return response.get("data")
  return []


def fetch_response(user_id, session_id, activity_id=None):
  """Fetch responses for a particular activity"""
  if user_id is None or session_id is None:
    return {}

  url = "/sessions/responses"
  request = {"user_id": [user_id], "session_id": [session_id]}
  if activity_id:
    request["activity_id"] = [activity_id]
  response = learnosity_request(url, "data", request, user_id)
  response = response.get("data")
  if response:
    return response[0]

  return {}


def identify_autogradable_assessment(tags):
  """Function to identify if the given assessment is
  auto-gradable or not"""
  for tag in AUTOGRADED_TAGS:
    if tag not in tags:
      return False
  return True


def update_item_responses(items, responses):
  """Function to add responses in items"""
  if not items:
    return items
  responses = responses.get("responses", None)
  if responses:
    for response in responses:
      if "item_reference" in response:
        items[response["item_reference"]]["pass"] = True if response.\
          get("score", None) and response.get("max_score", None) and \
            response["score"] == response["max_score"] else False
  else:
    # if no session data is found items are failed
    for item in items:
      items[item]["pass"] = False
  return items


def fetch_metadata(assessment):
  """Function to fetch assessment metadata"""
  activity_id = assessment.get("assessment_reference", {})
  if activity_id is not None:
    activity_id = activity_id.get("activity_template_id", None)
  if activity_id and USE_LEARNOSITY_SECRET:
    activity = fetch_activity(activity_id)
    assessment["is_autogradable"] = \
      identify_autogradable_assessment(activity.get("tags", []))

    item_refs = activity.get("data", {}).get("items", [])
    item_refs = [item["reference"] for item in item_refs]
    items = []
    for i in range(0, len(item_refs), 50):
      items.extend(fetch_items(item_refs[i:i + 50]))

    item_tags = {}
    for i, _ in enumerate(items):
      ref = items[i]["reference"]
      tags = items[i]["tags"]
      for tag in tags:
        if tag not in AUTOGRADED_TAGS:
          # assuming there is only skill mapped to an item
          item_tags[ref] = {
            "skill": tags[tag][0],
            "competency": tag
          }

    assessment["metadata"] = {"items": item_tags}
  return assessment


def get_user_name(user_data):
  """
  Function to get User Name from User Data
  Args:
    user_data: dict
  Returns:
    name: str
  """
  if user_data:
    name = user_data.get("first_name", "") + " " + \
      user_data.get("last_name", "")
    return name
