"""Functions to train IRT Models"""

# pylint: disable=protected-access
from typing import Optional
import pyro
from py_irt.config import IrtConfig
from py_irt.training import IrtModelTrainer
from collections import defaultdict
from services.prepare_data import IRTData
from girth_mcmc import GirthMCMC

def train_type_one(
    learning_unit: str, model_type: Optional[str] = "2pl"):
  """Training pipeline for type 1 IRT model"""
  pyro.clear_param_store()
  model_type = "2pl"
  irt_data_path, item_type_dict = \
    IRTData().create_type_one_train_data(learning_unit)
  config = IrtConfig(
    model_type=model_type, initializers=["difficulty_sign"],
    epochs=5000, lr=0.1, priors="hierarchical")
  trainer = IrtModelTrainer(config=config, data_path=irt_data_path)
  trainer.train(device="cpu")
  item_correctness = trainer._dataset.get_item_accuracies()
  summary = trainer.best_params

  item_ids = summary["item_ids"]
  diff = summary["diff"]
  diff_mapping = {}
  for key, value in item_ids.items():
    ind = int(key)
    diff_mapping[value] = diff[ind]
  item_difficulty = dict(sorted(diff_mapping.items(), key = lambda x:x[1]))

  item_discrimination = {}
  if model_type == "2pl":
    disc = summary["disc"]
    disc_mapping = {}
    for key, value in item_ids.items():
      ind = int(key)
      disc_mapping[value] = disc[ind]
    item_discrimination = dict(sorted(
      disc_mapping.items(), key = lambda x:x[1]))

  subject_ids = summary["subject_ids"]
  ability = summary["ability"]
  ability_mapping = {}
  for key, value in subject_ids.items():
    ind = int(key)
    ability_mapping[value] = ability[ind]
  user_ability = dict(sorted(ability_mapping.items(), key=lambda x:x[1]))

  user_correctness = {}
  index_accuracy = defaultdict(lambda: {"correct": 0, "total": 0})
  for user_id, response in zip(
    trainer._dataset.observation_subjects, trainer._dataset.observations):
    index_accuracy[user_id]["correct"] +=response
    index_accuracy[user_id]["total"] +=1

  for key, value in index_accuracy.items():
    key = subject_ids[key]
    user_correctness[key] = value
  return {
    "user_ability": user_ability,
    "item_difficulty": item_difficulty,
    "item_correctness": item_correctness,
    "item_discrimination": item_discrimination,
    "user_correctness": user_correctness,
    "item_type_dict": item_type_dict
  }

def train_type_two(learning_unit: str, model_type: Optional[str] = "2pl"):
  """Training pipeline for type 2 IRT model"""
  data, item_type_dict, user_index_to_id, item_index_to_id = \
    IRTData().create_type_two_train_data(learning_unit)
  print("DATA PREPERATION COMPLETE")
  if len(data) == 0:
    print("No Data to train IRT. Skipping training")
    return {}
  if model_type == "1pl":
    girth_model = GirthMCMC(model="1PL",
                          options={"variational_inference": True,
                                  "variational_samples": 10000,
                                  "n_samples": 10000})
  else:
    girth_model = GirthMCMC(model="2PL",
                          options={"variational_inference": True,
                                  "variational_samples": 10000,
                                  "n_samples": 10000})
  results = girth_model(data, progressbar=False)
  user_correctness_list = list(data.sum(axis = 0))
  item_correctness_list = list(data.sum(axis = 1))
  user_ability = {}
  user_correctness = defaultdict(lambda: {"correct": 0, "total": 0})
  attempted_items = ~data.mask
  for i in range(len(results["Ability"])):
    user_id = user_index_to_id[i]
    user_ability[user_id] = results["Ability"][i]
    user_correctness[user_id]["correct"] = int(user_correctness_list[i])
    user_correctness[user_id]["total"] = int(attempted_items.sum(axis=0)[i])

  item_difficulty = {}
  item_discrimination = {}
  item_correctness = defaultdict(lambda: {"correct": 0, "total": 0})
  for i in range(len(results["Difficulty"])):
    item_id = item_index_to_id[i]
    item_difficulty[item_id] = results["Difficulty"][i]
    if model_type=="2pl":
      item_discrimination[item_id] = results["Discrimination"][i]
    item_correctness[item_id]["correct"] = int(item_correctness_list[i])

    item_correctness[item_id]["total"] = int(attempted_items.sum(axis=1)[i])

  user_ability = dict(sorted(user_ability.items(), key=lambda x:x[1]))
  item_difficulty = dict(sorted(item_difficulty.items(), key=lambda x:x[1]))
  item_discrimination = dict(
    sorted(item_discrimination.items(), key=lambda x:x[1]))
  print("Training Complete for current LU")
  return {
    "user_ability": user_ability,
    "item_difficulty": item_difficulty,
    "item_correctness": item_correctness,
    "item_discrimination": item_discrimination,
    "user_correctness": user_correctness,
    "item_type_dict": item_type_dict
  }


  