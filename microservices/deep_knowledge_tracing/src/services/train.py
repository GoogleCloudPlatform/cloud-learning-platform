"""train file"""
from services.dataset import Dataset
from services.metrics import (BinaryAccuracy,AUC,Precision,
Recall)
from services.dkt import DKTModel
from tensorflow.keras.optimizers.legacy import Adam
from common.utils.logging_handler import Logger
from common.utils.gcs_adapter import upload_folder
import tensorflow as tf
import json
import pickle
from config import MODEL_PARAMS_DIR,GCS_BUCKET

class Trainer():
  """docstring for Trainer class"""
  verbose = 1 # Verbose = {0,1,2}
  model_params_dir = MODEL_PARAMS_DIR +"/" # File to save the model.
  log_dir = "logs" # Path to save the logs.
  optimizer = Adam() # Optimizer to use
  lstm_units = 100 # Number of LSTM units
  batch_size = 32 # Batch size
  epochs = 10 # Number of epochs to train
  dropout_rate = 0.3 # Dropout rate
  test_fraction = 0.2 # Portion of data to be used for testing
  validation_fraction = 0.2 # Portion of training data to be used for
  #validation
  train_set = None
  val_set = None
  test_set = None
  nb_features = None
  nb_skills = None
  lu_encoder = None
  model = None
  all_lu_ids = []
  @staticmethod
  def get_train_params(request_body):
    course_id = request_body.get("course_id","")
    dataset, length, nb_features, nb_skills,lu_encoder = Dataset.load_dataset(
      course_id=course_id)
    Trainer.train_set,Trainer.test_set,Trainer.val_set = Dataset.split_dataset(
      dataset, length,
      test_fraction=Trainer.test_fraction,
      val_fraction=Trainer.validation_fraction)
    set_sz = length * Trainer.batch_size
    test_set_sz = set_sz *Trainer.test_fraction
    val_set_sz = (set_sz - test_set_sz) * Trainer.validation_fraction
    train_set_sz = set_sz - test_set_sz - val_set_sz
    Logger.info("============= Data Summary =============")
    Logger.info("Total number of students: {}".format(set_sz))
    Logger.info("Training set size: {}".format(train_set_sz))
    Logger.info("Validation set size: {}".format(val_set_sz))
    Logger.info("Testing set size: {}".format(test_set_sz))
    Logger.info("Number of skills: {}".format(nb_skills))
    Logger.info("Number of features in the input: {}".format(nb_features))
    Trainer.nb_features = nb_features
    Trainer.nb_skills = nb_skills
    Trainer.lu_encoder = lu_encoder

  @staticmethod
  def save_model_parameters(path):
    config_json = {}
    config_json["nb_skills"] = Trainer.nb_skills
    config_json["nb_features"] = Trainer.nb_features
    config_json["lu_ids"] = Dataset.all_lu_ids
    with open(path+"params.json", "w", encoding="utf-8", errors="ignore") as fp:
      json_string = json.dumps(str(config_json), indent=2)
      fp.write(json_string)
    with open(path+"lu_encoder.pkl","wb") as output_file:
      pickle.dump(Trainer.lu_encoder,output_file)

  @staticmethod
  def get_compiled_model():

    Trainer.model = DKTModel(
      nb_features=Trainer.nb_features,
      nb_skills=Trainer.nb_skills,
      hidden_units=Trainer.lstm_units,
      dropout_rate=Trainer.dropout_rate)
    Trainer.model.compile(
      optimizer=Trainer.optimizer,
      metrics=[BinaryAccuracy(), AUC(), Precision(), Recall()])
    Logger.info(Trainer.model.summary())

  @staticmethod
  def train(request_body):
    Trainer.get_train_params(request_body)
    Trainer.get_compiled_model()
    course_id = request_body.get("course_id","")
    if course_id:
      ckpt_path = Trainer.model_params_dir+course_id+"/"+"weights/bestmodel"
    else:
      ckpt_path = Trainer.model_params_dir+"default/weights"
    history = Trainer.model.fit(dataset=Trainer.train_set,epochs=Trainer.epochs,
    verbose=Trainer.verbose, validation_data=Trainer.val_set,
    callbacks=[tf.keras.callbacks.ModelCheckpoint(
      ckpt_path,save_best_only=True,
      save_weights_only=True),
      tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=3)])
    Trainer.save_model_parameters(Trainer.model_params_dir+course_id+"/")
    evaluation_scores = Trainer.model.evaluate(Trainer.test_set)
    upload_folder(GCS_BUCKET,Trainer.model_params_dir+"/"+course_id,
    "ml-models/dkt/"+course_id)
    return history.history,dict(
      zip(Trainer.model.metrics_names,evaluation_scores)
      )

  @staticmethod
  def predict(course_id=None,user_id=None,session_id=None):
    if course_id:
      #TODO load model weights for given course
      pass
    encoded_user_events = Dataset.get_inference_user_events(
      lu_encoder=Dataset.lu_encoder,user_id=user_id,
    session_id = session_id,features_depth=None)
    lu_scores = Trainer.model.predict(encoded_user_events)[:,-1,:]
    flatten_scores = (lu_scores.flatten().tolist())
    response = {}
    for i in range(len(Dataset.all_lu_ids)):
      response[Dataset.all_lu_ids[i]]=flatten_scores[i]
    return response
