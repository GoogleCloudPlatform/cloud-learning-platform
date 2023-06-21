"""Functions to create user_events collections"""
import pandas as pd
import uuid
import random
from common.models import UserEvent
from common.utils.errors import ValidationError
from services.create_fake_data import save_items_in_batches
from config import REQUIRED_FIELDS

def create_user_event(gcs_path):
  df = pd.read_csv(gcs_path)

  req_list = list(REQUIRED_FIELDS.keys())
  all_user_events = []

  for ind in df.index:
    user_event_data = {}
    #adding required fields
    for req_field in req_list:
      if df[req_field][ind] == " ":
        raise ValidationError(
          f"Missing required field in the csv: {req_field[0]}")

      elif req_field == "is_correct":
        if df[req_field][ind] not in REQUIRED_FIELDS["is_correct"]:
          val_allowed = REQUIRED_FIELDS["is_correct"]
          raise ValidationError(
            f"is_correct can only accept the following values:{val_allowed}")
        else:
          field = req_field
          value = int(df[req_field][ind])
          user_event_data[field] = value

      elif not isinstance(df[req_field][ind],REQUIRED_FIELDS[req_field]):
        print(type(df[req_field][ind]))
        raise ValidationError(
          f"Wrong data type of the field: {req_field}")

      else:
        field = req_field
        value = df[req_field][ind]
        user_event_data[field] = value

    #TODO: Feedback needs to be changed from a map field to a flat field
    # accordingly the data trainign endpoitns are to be updated
    # issue reference: 3486
    user_event_data["feedback"] = {}
    user_event_data["feedback"]["first_attempt"] = {}
    user_event = UserEvent()
    print(user_event_data)
    #adding the required fields
    user_event.learning_item_id = user_event_data["learning_item_id"]
    user_event.activity_type = user_event_data["activity_type"]
    user_event.user_id = user_event_data["user_id"]
    if(user_event_data["is_correct"]) == 1:
      user_event_data["feedback"][
        "first_attempt"] = {
          "evaluation_flag":"correct",
          "score":1}
    else:
      user_event_data["feedback"][
        "first_attempt"] = {
          "evaluation_flag":"incorrect",
          "score":0}
    user_event.feedback = user_event_data["feedback"]
    user_event.is_correct = user_event_data["is_correct"]
    user_event.learning_unit = user_event_data["learning_unit"]
    user_event.course_id = user_event_data["course_id"]
    user_event.session_ref = user_event_data["session_id"]
    all_user_events.append(user_event)

  save_items_in_batches(all_user_events)
  return len(all_user_events)

def create_synthetic_data(num):
  data = {}
  data["learning_item_id"]=[]
  data["activity_type"] = []
  data["user_id"] = []
  data["learning_unit"] =[]
  data["course_id"]=[]
  data["is_correct"]=[]
  data["session_id"]=[]
  for _ in range(0,num):
    lid = uuid.uuid4()
    lid = "lid"+str(lid).split("-")[2]
    lu = "lu"+ str(random.randint(1,10))
    act_type = "act" + str(random.randint(1,5))
    user = "user" + str(random.randint(1,7))
    session_id = "session"+str(random.randint(1,3))+"_"+user
    course = "course"+ str(random.randint(1,3))
    correct = random.randint(0,1)
    data["learning_item_id"].append(lid)
    data["activity_type"].append(act_type)
    data["user_id"].append(user)
    data["learning_unit"].append(lu)
    data["course_id"].append(course)
    data["is_correct"].append(correct)
    data["session_id"].append(session_id)
  df= pd.DataFrame(data)
  return df


