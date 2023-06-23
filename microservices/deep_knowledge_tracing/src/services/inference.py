"""script for inference"""
from services.dataset import Dataset
from services.metrics import (BinaryAccuracy,AUC,Precision,
Recall)
from services.dkt import DKTModel
from services.train import Trainer
from services.data_models_utils import get_learning_units,get_all_courses
from config import MODEL_PARAMS_DIR,MODEL_WEIGHTS_PATH
from sklearn.preprocessing import LabelEncoder
import json
import pickle
import os
import ast
from common.utils.logging_handler import Logger
from common.utils.gcs_adapter import download_blob
#pylint: disable=unnecessary-comprehension,broad-exception-raised
class Inference():
  """docstring for Inference class"""
  course_ids = []
  lu_encoders = {}
  nb_skills = {}
  nb_features = {}
  models = {}
  lu_ids = {}

  @staticmethod
  def predict(course_id = None,user_id = None,
  user_events = None, session_id = None):
    """returns prediction scores for all lus for a given course"""
    if course_id:
      if course_id not in Inference.course_ids:
        Inference.set_params(course_id)
      if Inference.models[course_id] is not None:
        if session_id and not user_events:
          encoded_user_events = Dataset.process_db_user_events(
            Inference.lu_encoders[course_id],
            user_id=user_id,session_id = session_id,
            features_depth=Inference.nb_features[course_id])
        elif user_events and not session_id:
          encoded_user_events = Dataset.process_request_user_events(
            Inference.lu_encoders[course_id],
            user_id=user_id,user_events = user_events,
            features_depth=Inference.nb_features[course_id]
          )
        lu_scores = Inference.models[course_id].predict(
          encoded_user_events)[:,-1,:]
        flatten_scores = (lu_scores.flatten().tolist())
        response = {}
        for i in range(len(Inference.lu_ids[course_id])):
          response[Inference.lu_ids[course_id][i]]=flatten_scores[i]
        response_sorted = {k: v for k, v in sorted(
          response.items(), key=lambda item: item[1],reverse=True)}
        return response_sorted

      else:
        raise Exception("The course does not have learning units")
    else:
      raise Exception("Course id is required")

  @staticmethod
  def get_model(nb_features=101,nb_skills=50):
    """returns model"""
    dkt_model = DKTModel(
      nb_features=nb_features,
      nb_skills=nb_skills)
    dkt_model.compile(
      optimizer=Trainer.optimizer,
      metrics=[BinaryAccuracy(), AUC(), Precision(), Recall()])
    return dkt_model

  @staticmethod
  def set_params(course_id):
    """loads model params and model weights"""
    Inference.course_ids.append(course_id)
    base_path = MODEL_PARAMS_DIR+"/"+course_id+"/"
    download_blob(MODEL_WEIGHTS_PATH+"/"+course_id,
    MODEL_PARAMS_DIR+"/"+course_id)
    if os.path.exists(base_path):
      with open(base_path+"params.json","rb") as params_file:
        model_params = ast.literal_eval(json.loads(params_file.read()))
      Inference.nb_skills[course_id] = model_params["nb_skills"]
      Inference.nb_features[course_id] = model_params["nb_features"]
      Inference.lu_ids[course_id] = model_params["lu_ids"]
      model = Inference.get_model(
        nb_features = Inference.nb_features[course_id],
        nb_skills = Inference.nb_skills[course_id])
      model.load_weights(base_path+"weights/bestmodel")
      Inference.models[course_id] = model
      with open(base_path+"lu_encoder.pkl","rb") as lu_encoder_file:
        Inference.lu_encoders[course_id] = pickle.load(lu_encoder_file)
    else:
      Logger.info(
        "No model weights found for the given course. Using default weights"
        )
      lu_ids = get_learning_units(course_id)
      if len(lu_ids)>0:
        Inference.lu_encoders[course_id] = LabelEncoder().fit(lu_ids)
        Inference.models[course_id] = Inference.get_model(
        nb_features = 2*len(lu_ids)+1,
        nb_skills = len(lu_ids))
      else:
        Logger.info("The course does not have learning units")
        Inference.lu_encoders[course_id] = None
        Inference.models[course_id] = None
      Inference.nb_skills[course_id] = len(lu_ids)
      Inference.nb_features[course_id] = 2*len(lu_ids)+1
      Inference.lu_ids[course_id] = lu_ids

  @staticmethod
  def load_all_models():
    """loads models for all possible courses"""
    courses = get_all_courses()
    for course in courses:
      Logger.info("Loading model weights ----")
      Logger.info("Course id - %s" % course.id)
      Logger.info("Course Title - %s" % course.title)
      Inference.set_params(course.id)




