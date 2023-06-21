"""script for populating fake data for local dev env"""
import random
from common.models import User, UserEvent, ChooseTheFactItem, LearningUnit
import fireo
from datetime import datetime

#pylint: disable=unused-argument,redefined-builtin
def create_fake_learning_units(count=10):
  """creates dummy learning units"""
  all_lus = []
  for i in range(count):
    lu = LearningUnit()
    lu.title = "fake title "+str(i)
    lu.text = "fake text "+str(i)
    lu.sc_id = str(i//10)
    all_lus.append(lu)
  save_items_in_batches(all_lus)

# pylint: disable=unused-argument
def create_fake_users(count = 50):
  """creates dummy users"""
  all_users = []
  for i in range(count):
    user = User()
    user.name = "user_" + str(i)
    user.email = "ser_"  + str(1) + "@gmail.com"
    all_users.append(user)
  save_items_in_batches(all_users)

def create_fake_assessments(count=500, type="ctf"):
  """creates dummy assessment items of type ctf"""
  all_learning_units = list(LearningUnit.collection.fetch())
  n = count//len(all_learning_units)
  all_items = []
  for i in range(count):
    ctf_item = ChooseTheFactItem()
    ctf_item.answer = ["fake_answer"]
    ctf_item.question = "fake_question"
    ctf_item.options = ["option 1", "fake_answer", "option 2"]
    ctf_item.learning_unit = all_learning_units[i//n]
    all_items.append(ctf_item)
  save_items_in_batches(all_items)

def save_items_in_batches(items):
  """Function to save items in batches on Firestore"""
  input_datetime = datetime.now()
  for i in range(0, len(items) - 1, 500):
    batch = fireo.batch()
    for item in items[i:min(i + 500, len(items))]:
      item.save(input_datetime = input_datetime, batch = batch)
    batch.commit()
  return input_datetime

def create_user_events(num_users = 30, num_item = 50):
  """creates dummy user events"""
  all_users = list(User.collection.fetch())
  all_items = list(ChooseTheFactItem.collection.fetch())
  all_user_events = []
  evaluation_flag = {
    1:"correct",
    0:"incorrect"
  }
  for user_ind in range(num_users):
    user = all_users[user_ind]
    for item_ind in range(num_item):
      item = all_items[item_ind]
      if user_ind ==0:
        response = 1
      elif user_ind == 49:
        response = 0
      else:
        response = random.getrandbits(1)
      user_event = UserEvent()
      user_event.user_id = user.id
      user_event.learning_item_id = item.id
      user_event.raw_response = {"first_attempt": response}
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
      user_event.activity_type = "ctf"
      lu = item.learning_unit.get()
      user_event.learning_unit_id = lu.id
      user_event.session_ref = lu.sc_id
      all_user_events.append(user_event)
  save_items_in_batches(all_user_events)

def generate_dkt_data(num_users, num_lus, type):
  """creates dummy data to train dkt"""
  create_fake_users(num_users)
  create_fake_learning_units(num_lus)
  create_fake_assessments(num_lus*3, type)
  create_user_events(num_users, num_lus*3)
