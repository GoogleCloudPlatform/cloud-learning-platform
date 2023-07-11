"""Module containing helper functions for item selection"""
from common.models import (ChooseTheFactItem, UserEvent,
                           AnswerAQuestionItem,LearningUnit,
                           ParaphrasingPracticeItem, CreateKnowledgeNotesItem)
import regex as re
import logging

def get_prev_contexts(user_events):
  """Creates a list of context using previous user events"""
  contexts = []
  user_events.reverse()
  for user_event in user_events:
    context = user_event.context
    if context and context not in contexts:
      contexts.append(context)
  return contexts

def filter_empty_user_events(all_user_events):
  """Removes user events which has no evaluation"""
  def empty_feedback(user_event):
    if "first_attempt" in user_event.feedback:
      return True
    return False

  filtered_user_events = filter(empty_feedback, all_user_events)
  return list(filtered_user_events)

def get_all_user_events(
  user_id, learning_unit_id, activity_type, session_id, window):
  """returns all user events"""
  items = UserEvent.collection.filter(session_ref=session_id).filter(
    user_id=user_id).filter(
      learning_unit=learning_unit_id).filter(
        activity_type=activity_type).order(
          "-last_modified_time").limit(window).fetch()
  items = sorted(items, key=lambda x:x.created_time)
  return list(items)


def get_all_assessment_items(learning_unit_id: str, activity_type: str,
                             reviewed, disable_items: dict = None) -> list:
  """
  Returns all assessments for a given lu and activity

  Parameters
  ----------
  learning_unit_id: str
  activity_type: str
  disable_items: dict
  reviewed: bool

  Returns
  -------
  assessments: list
  """
  learning_unit = LearningUnit.find_by_id(learning_unit_id)
  if activity_type == "choose_the_fact" and reviewed is not None:
    items = ChooseTheFactItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).filter(reviewed=True).fetch()
  elif activity_type == "choose_the_fact" and reviewed is None:
    items = ChooseTheFactItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).fetch()
  elif activity_type == "answer_a_question" and reviewed is not None:
    items = AnswerAQuestionItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).filter(reviewed=True).fetch()
  elif activity_type == "answer_a_question" and reviewed is None:
    items = AnswerAQuestionItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).fetch()
  elif activity_type == "paraphrasing_practice" and reviewed is not None:
    items = ParaphrasingPracticeItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).filter(reviewed=True).fetch()
  elif activity_type == "paraphrasing_practice" and reviewed is None:
    items = ParaphrasingPracticeItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).fetch()
  elif activity_type == "create_knowledge_notes" and reviewed is not None:
    items = CreateKnowledgeNotesItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).filter(reviewed=True).fetch()
  elif activity_type == "create_knowledge_notes" and reviewed is None:
    items = CreateKnowledgeNotesItem.collection.filter(
      learning_unit=learning_unit.key).filter(
      flag_problematic_question=False).fetch()
  else:
    raise Exception("Invalid activity type")

  if disable_items and activity_type in disable_items:
    filter_types = disable_items[activity_type]
    items = [item for item in items if item.question_type not in filter_types]
  return list(items)

def get_context(activity_type, item):
  """given the activity type and item this function returns context of item"""
  if item.context is not None:
    context = item.context.strip().lower()
    logging.info("Context form assessment item: %s", context)
    return context
  context = ""
  if activity_type=="choose_the_fact":
    question = item.question
    #pylint: disable=use-a-generator
    if all([
        ans.strip()[0].isupper()
        for ans in item.answer.split(",")
        if len(ans) > 0
    ]):
      answer = [ans.strip() for ans in item.answer.split(",")]
    else:
      answer = [item.answer]
    for i in range(len(answer)):
      rx = re.compile(r"_{2,}")
      question = rx.sub(answer[i], question, 1)
    context = question
  elif activity_type == "answer_a_question":
    question_type = item.question_type
    if question_type == "multihop":
      question = item.question
      answer = item.answer.split(", ")
      char_ind = ord("X")
      for i in range(len(answer)):
        question = question.replace(
          chr(char_ind+i), answer[i])
      context = question
    else:
      context = item.context
  elif activity_type == "paraphrasing_practice":
    context = item.question
  return context.lower()

def get_assessment_item(assessment_id, activity_type):
  """returns item given id"""
  if activity_type == "choose_the_fact":
    item = ChooseTheFactItem.find_by_id(assessment_id)
  elif activity_type == "answer_a_question":
    item = AnswerAQuestionItem.find_by_id(assessment_id)
  elif activity_type == "paraphrasing_practice":
    item = ParaphrasingPracticeItem.find_by_id(assessment_id)
  elif activity_type == "create_knowledge_notes":
    item = CreateKnowledgeNotesItem.find_by_id(assessment_id)
  else:
    raise Exception("Invalid activity type")
  return item
