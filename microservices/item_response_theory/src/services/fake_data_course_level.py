"""Generates fake user events on course level"""

import random
import fireo
from common.models import (
    ChooseTheFactItem, AnswerAQuestionItem, ParaphrasingPracticeItem,
    CreateKnowledgeNotesItem, Course, User, UserEvent
)
from services.get_all_learning_units import get_all_learning_units

# pylint: disable=unused-argument
def create_fake_users(count = 50):
  """Creates fake users"""
  users = []
  for i in range(count):
    user = User()
    user.first_name = "user_" + str(i)
    user.last_name = "last_name"
    user.email = "user_fake" + "@gmail.com"
    user.save()
    users.append(user)
    print("Created User: ", i)
  return users


def add_events(items, user, learning_unit, activity_type, batch, course_id):
  """Creates fake user events"""
  evaluation_flag = {
    1:"correct",
    0:"incorrect"
  }
  for item_ind in range(len(items)):
    item = items[item_ind]
    user_event = UserEvent()
    user_event.user_id = user.id
    user_event.learning_item_id = item.id
    user_event.activity_type = activity_type
    user_event.raw_response = {}
    user_event.course_id = course_id
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
    user_event.learning_unit = learning_unit
    user_event.save(batch=batch)

def create_user_events(
    learning_unit, all_users, ctf_items, aaq_items,
    paraphrase_items, ckn_items, course_id):
  """Creates User events for each user"""
  for user_ind in range(len(all_users)):
    print("Data generated for user: ", user_ind, all_users[user_ind].id)
    user = all_users[user_ind].id
    batch = fireo.batch()

    add_events(
      ctf_items, user, learning_unit, "choose_the_fact", batch, course_id)
    add_events(
      aaq_items, user, learning_unit, "answer_a_question", batch, course_id)
    add_events(
      paraphrase_items, user, learning_unit,
      "paraphrasing_practice", batch, course_id)
    add_events(
      ckn_items, user, learning_unit, "create_knowledge_notes",
      batch, course_id)
    batch.commit()


def generate_irt_data_course_level(num_users, course_id):
  """Generates fake IRT data at a course level"""
  course = Course.find_by_id(course_id)
  print("Course Name: ", course.title)

  all_lus = get_all_learning_units("course", course_id)
  print("Fetched all Learning Units: ", len(all_lus))

  users = create_fake_users(num_users)
  print("\n****Fake Users Created ****: ", num_users)

  for ind, lu_id in enumerate(all_lus):
    print("\n\n For Learning Unit : ", ind)
    # learning_unit = LearningUnit.find_by_id(lu_id)
    ctf_items = list(ChooseTheFactItem.collection.filter(
      learning_unit="learning_units/"+lu_id).fetch())
    print("No of CTF Items: ", len(ctf_items))
    aaq_items = list(AnswerAQuestionItem.collection.filter(
      learning_unit="learning_units/"+lu_id).fetch())
    print("No of AAQ Items: ", len(aaq_items))
    paraphrase_items = list(ParaphrasingPracticeItem.collection.filter(
      learning_unit="learning_units/"+lu_id).fetch())
    print("No of Paraphrase Items: ", len(paraphrase_items))
    ckn_items = list(CreateKnowledgeNotesItem.collection.filter(
      learning_unit="learning_units/"+lu_id).fetch())
    print("No of Create Knowledge Notes Items: ", len(ckn_items))
    create_user_events(
      lu_id, users, ctf_items, aaq_items, paraphrase_items,
      ckn_items, course_id)

