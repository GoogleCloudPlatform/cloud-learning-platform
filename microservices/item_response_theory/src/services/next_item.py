"""script for selecting next item"""
# pylint: disable=singleton-comparison,broad-exception-raised
from common.models import (UserAbility)
from common_ml.item_selection import (
  get_prev_contexts, filter_empty_user_events,
  get_all_user_events, get_all_assessment_items,
  get_context
)
from scipy.special import expit
import numpy as np
import random

# pylint: disable=simplifiable-if-statement,use-a-generator
def irt_evaluation(difficulty, discrimination, thetas):
  """ Evaluation of unidimensional IRT model.
  Evaluates an IRT model and returns the exact values.  This function
  supports only unidimemsional models
  Assumes the model
      P(theta) = 1.0 / (1 + exp(discrimination * (theta - difficulty)))
  Args:
      difficulty: (1d array) item difficulty parameters
      discrimination:  (1d array | number) item discrimination parameters
      thetas: (1d array) person abilities
  Returns:
      probabilities: (2d array) evaluation of sigmoid for given inputs
  """
  # If discrimination is a scalar, make it an array
  if np.atleast_1d(discrimination).size == 1:
    discrimination = np.full_like(difficulty, discrimination,
                                  dtype="float")

  kernel = thetas - difficulty[:, None]
  kernel *= discrimination[:, None]
  return expit(kernel)


def get_user_ability(user_id, learning_unit_id):
  """returns user ability"""
  item = UserAbility.collection.filter(
    user="users/"+user_id).filter(
      learning_unit="learning_units/"+learning_unit_id).get()
  if not item:
    return [0.0]
  return [item.ability]


def find_answer_probabilities(ability, difficulty, discrimination):
  """gets answer probabilities using irt evaluation"""
  ability = np.array(ability)
  difficulty = np.array(difficulty)
  discrimination = np.array(discrimination)
  probabilites = irt_evaluation(difficulty, discrimination, ability)
  return probabilites[:, 0]

def get_category(categories, index):
  """ returns difficulty level """
  if index in categories["easy"]:
    return "easy"
  elif index in categories["difficult"]:
    return "difficult"
  else:
    return "medium"


def filter_same_context_items(
    activity_type, prev_contexts, next_items, assessment_items, item_seq):
  print("Filtering same context items")
  print("Prev contexts: ", prev_contexts)
  for index in next_items:
    print("Index: ", index)
    item = assessment_items[item_seq[index]]
    item_context = get_context(activity_type, item).strip()
    print("Current item context:", item_context)
    if item_context in prev_contexts:
      continue
    else:
      return index
  return next_items[0]

def get_next_category_item(activity_type,
  mask, categories, prev_category, prev_correct,
  contexts, assessment_items, consider_prev_context):
  """returns next category,item based on previous responses"""
  if prev_category == "easy":
    if prev_correct:
      seq = ["medium", "difficult", "easy"]
    else:
      seq = ["easy", "medium", "difficult"]
  elif prev_category == "medium":
    if prev_correct:
      seq = ["difficult", "medium", "easy"]
    else:
      seq = ["easy", "medium", "difficult"]
  else:
    if prev_correct:
      seq = ["difficult", "medium", "easy"]
    else:
      seq = ["medium", "easy", "difficult"]

  item_seq = np.concatenate(
    (categories[seq[0]], categories[seq[1]], categories[seq[2]]))
  item_seq = item_seq.astype(int)
  print("Item Seq: ", item_seq)
  mask_seq = mask[item_seq]
  print("mask: ", mask)
  print("mask seq: ", mask_seq)
  next_items = np.argwhere(mask_seq==False).flatten()
  print("next item: ", next_items)
  if consider_prev_context and contexts:
    index = filter_same_context_items(activity_type,
      contexts, next_items, assessment_items, item_seq)
    print("Output: ", index)
    # index = next_items[output]
  else:
    index = next_items[0]
  print("Final Index: ", index)
  item_ind = item_seq[index]
  print("Item Ind: ", item_ind)
  return item_ind

def select_from_category(
    mask, categories, activity_type, prev_item_ind=None, prev_correct=None,
    contexts=None, assessment_items=None, consider_prev_context=False):
  """selects next item based on previous responses"""
  if prev_item_ind!=None:
    prev_category = get_category(categories, prev_item_ind)
    return get_next_category_item(activity_type,
      mask, categories, prev_category, prev_correct,
      contexts, assessment_items, consider_prev_context)
  else:
    choices = []
    for key, value in categories.items():
      if len(value) > 0:
        choices.append(key)
    choice = random.choice(choices)
    return categories[choice][random.choice(
      list(range(len(categories[choice]))))]

def create_categories(probs):
  """returns custom categories"""
  categories = {
    "easy": [],
    "medium": [],
    "difficult": []
  }
  sorted_index = np.argsort(probs)
  num_items = len(probs)
  if num_items <3:
    categories["easy"] = sorted_index[:1]
    categories["difficult"] = sorted_index[1:]
    return categories
  limit = num_items // 3
  categories["easy"] = sorted_index[:limit]
  categories["medium"] = sorted_index[limit:-limit]
  categories["difficult"] = sorted_index[-limit:]

  np.random.shuffle(sorted_index[:limit])
  np.random.shuffle(sorted_index[limit:-limit])
  np.random.shuffle(sorted_index[-limit:])
  return categories

def find_prev_correct(feeback):
  """returns flag to check previous response"""
  if feeback["first_attempt"]["evaluation_flag"]=="correct" or\
    ("second_attempt" in feeback and\
      feeback["second_attempt"]["evaluation_flag"]=="correct"):
    return True
  else:
    return False


def next_item(
  learning_unit_id, user_id, activity_type, session_id, prev_context_count):
  """main method for item selection"""
  assessment_items = get_all_assessment_items(learning_unit_id, activity_type)
  print("No of assessment items: ", len(assessment_items))
  if not assessment_items:
    print("No Assessment Items found")
    raise Exception("No Assessment Items found")
  ability = get_user_ability(user_id, learning_unit_id)
  prev_user_events = get_all_user_events(
    user_id, learning_unit_id, activity_type,
    session_id, len(assessment_items))
  prev_user_events = filter_empty_user_events(prev_user_events)
  contexts =[]
  if prev_context_count >=1:
    contexts = get_prev_contexts(prev_user_events[-prev_context_count:])
    consider_prev_context = True
  else:
    consider_prev_context = False

  difficulty = []
  discrimination = []
  id_to_idx = {}
  idx_to_id = {}
  for i, item in enumerate(assessment_items):
    if item.difficulty_score:
      difficulty.append(item.difficulty_score)
    else:
      difficulty.append(0.0)
    if item.discrimination:
      discrimination.append(item.discrimination)
    else:
      discrimination.append(0.0)
    id_to_idx[item.id] = i
    idx_to_id[i] = item.id

  assessment_probs = find_answer_probabilities(
    np.array(ability),
    np.array(difficulty),
    np.array(discrimination)
  )

  mask = np.full(len(difficulty), False, dtype=bool)
  for user_event in prev_user_events:
    assessment_id = user_event.learning_item_id
    mask[id_to_idx[assessment_id]] = True
  if np.sum(mask) == len(difficulty):
    mask = ~mask
    prev_user_events = []

  categories = create_categories(assessment_probs)


  if prev_user_events:
    prev_item_ind = id_to_idx[prev_user_events[-1].learning_item_id]
    prev_correct = find_prev_correct(prev_user_events[-1].feedback)
    result = select_from_category(
      mask, categories, activity_type, prev_item_ind, prev_correct,
      contexts, assessment_items, consider_prev_context)
  else:
    result = select_from_category(mask, categories, activity_type)

  print("Item id to index: ", id_to_idx)
  print("Index to ID: ", idx_to_id)

  assessment_id = idx_to_id[result]
  return {"data": {
    "item_id": assessment_id
    }}
