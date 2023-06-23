"""Generates fake data"""

import random
from common.models import (User, UserEvent, ChooseTheFactItem,
  LearningUnit, LearningObjective)
import fireo

# pylint: disable=unused-argument
def create_fake_users(count = 50):
  """Creates fake users"""
  batch = fireo.batch()
  for i in range(count):
    user = User()
    user.name = "user_" + str(i)
    user.email = "ser_"  + str(1) + "@gmail.com"
    user.user_id = "id" + str(i)
    user.save(batch=batch)
  batch.commit()

def create_fake_assessments(
    learning_unit, count=50, item_type="choose_the_fact"):
  """Creates fake assessments"""
  batch = fireo.batch()
  for _ in range(count):
    ctf_item = ChooseTheFactItem()
    ctf_item.answer = "fake_answer"
    ctf_item.question = "fake_question"
    ctf_item.options = ["option 1", "fake_answer", "option 2"]
    ctf_item.learning_unit = learning_unit
    ctf_item.save(batch=batch)
  batch.commit()

def create_user_events(learning_unit, num_users = 50, num_item = 50):
  """Creates User Events"""
  evaluation_flag = {
    1:"correct",
    0:"incorrect"
  }
  all_users = list(User.collection.fetch())
  all_items = list(ChooseTheFactItem.collection.fetch())
  for user_ind in range(num_users):
    print("Data generated for user: ", user_ind, all_users[user_ind].id)
    batch = fireo.batch()
    user = all_users[user_ind]
    for item_ind in range(num_item):
      item = all_items[item_ind]
      user_event = UserEvent()
      user_event.user_id = user.id
      user_event.learning_item_id = item.id
      user_event.activity_type = "choose_the_fact"
      user_event.raw_response = {}
      evaluation_score = random.getrandbits(1)
      first_attempt = {
            "feedback_text": "",
            "evaluation_score":evaluation_score,
            "evaluation_flag":evaluation_flag[evaluation_score]
          }
      second_attempt = {}

      if evaluation_score==0:
        evaluation_score = random.getrandbits(1)
        second_attempt = {
            "feedback_text": "",
            "evaluation_score":evaluation_score,
            "evaluation_flag":evaluation_flag[evaluation_score]
          }
      user_event.feedback = {
        "first_attempt": first_attempt,
        "second_attempt": second_attempt
        }
      user_event.learning_unit = learning_unit.id
      user_event.save(batch=batch)
    batch.commit()
  return learning_unit.id


def generate_irt_data(num_users, num_items, item_type):
  """Generates fake users, assessment items and user events for IRT"""
  learning_obj = LearningObjective(title="Sample LO", text = "")
  learning_obj.save()
  learning_unit = LearningUnit(title = "LU 1", text ="")
  learning_unit.parent_node = learning_obj
  learning_unit.save()
  create_fake_users(num_users)
  create_fake_assessments(learning_unit, num_items, item_type)
  lu_id = create_user_events(learning_unit, num_users, num_items)
  # print(len(list(UserEvent.collection.fetch())))
  return lu_id

if __name__ == "__main__":
  generate_irt_data(50, 50, "choose_the_fact")
