"""Prepare data for training IRT models"""

import os
from common.models import UserEvent
from collections import defaultdict
import json
import pandas as pd
from girth_mcmc.utils import tag_missing_data_mcmc

# pylint: disable=simplifiable-if-statement
class IRTData():
  """Prepare data for training IRT Models"""
  def __init__(self):
    pass

  def create_type_one_train_data(
      self, learning_unit_id, output_file_path="data/irt_data.jsonlines"):
    """Prepares data for type 1 irt model"""
    all_user_events = list(UserEvent.collection.\
      filter(learning_unit=learning_unit_id).fetch())
    all_user_events = self.filter_empty_user_events(all_user_events)
    item_type_dict = {}
    user_item_mapping = defaultdict(list)
    for user_event in all_user_events:
      user_id = user_event.user_id
      assessment_id = user_event.learning_item_id
      item_type_dict[assessment_id] = user_event.activity_type
      item = {
        assessment_id: self.response(user_event.feedback)
      }
      user_item_mapping[user_id].append(item)
    irt_data = []
    for user_id, assessment_items in user_item_mapping.items():
      user_data = {"subject_id": user_id , "responses": {}}
      for item in assessment_items:
        user_data["responses"] = {**user_data["responses"], **item}
      irt_data.append(user_data)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8", errors="ignore") as f:
      f.write("\n".join(map(json.dumps, irt_data)))
    return output_file_path, item_type_dict

  def response(self, feeback):
    """Returns whether user answered an item correctly or not"""
    if feeback["first_attempt"]["evaluation_flag"]=="correct" or\
      ("second_attempt" in feeback and\
        feeback["second_attempt"]["evaluation_flag"]=="correct"):
      return True
    else:
      return False

  def filter_empty_user_events(self, all_user_events):
    """Removes user events which has no evaluation"""
    def empty_feedback(user_event):
      if "first_attempt" in user_event.feedback:
        return True
      return False

    filtered_user_events = filter(empty_feedback, all_user_events)
    return list(filtered_user_events)

  def create_type_two_train_data(self, learning_unit_id):
    """Prepares data for training type 2 IRT model"""
    learning_unit_key = "learning_units/" + learning_unit_id
    print("Learning Unit key: {}".format(learning_unit_key))
    all_user_events = list(UserEvent.collection.filter(
      learning_unit=learning_unit_id).fetch())
    all_user_events = self.filter_empty_user_events(all_user_events)
    print("Fetched ALL USER EVENTS: {}".format(len(all_user_events)))
    if len(all_user_events) == 0:
      print("No User Events to train IRT.")
      return ([], {}, {}, {})
    item_type_dict = {}
    user_item_mapping = defaultdict(list)
    for i, user_event in enumerate(all_user_events):
      if i%200 ==0:
        print(i)
      user_id = user_event.user_id
      assessment_id = user_event.learning_item_id
      item_type_dict[assessment_id] = user_event.activity_type
      item = {
        assessment_id: self.response(user_event.feedback)
      }
      user_item_mapping[user_id].append(item)
    df = pd.DataFrame(columns=item_type_dict.keys())
    item_index_to_id = {}
    for i, column in enumerate(df.columns):
      item_index_to_id[i] = column
    for user_id, items in user_item_mapping.items():
      user_items = {}
      for item in items:
        user_items = {**user_items, ** item}
      user_items = {**user_items, **{"user_id": user_id}}
      df = df.append(user_items, ignore_index=True)
    user_index_to_id = {}
    for i, user_id in enumerate(df["user_id"]):
      user_index_to_id[i] = user_id

    df = df.drop(["user_id"], axis = 1)
    df = df.fillna(-999)
    data = df.to_numpy().transpose()
    data = tag_missing_data_mcmc(data, [0, 1])
    result = (data, item_type_dict, user_index_to_id, item_index_to_id)
    print("Data Shape: ",result[0].shape)
    return result

