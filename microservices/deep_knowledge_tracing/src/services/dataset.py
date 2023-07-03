"""to load and process dataset"""
import pandas as pd
import tensorflow as tf
import numpy as np
from common.models import UserEvent
from services.data_models_utils import filter_events_with_empty_feedback
from sklearn.preprocessing import LabelEncoder
#pylint: disable=no-value-for-parameter,unexpected-keyword-arg,redundant-keyword-arg
class Dataset():
  """docstring for Dataset class"""
  verbose = 1 # Verbose = {0,1,2}
  lu_id_encoder = LabelEncoder()
  batch_size = 2
  MASK_VALUE = -1.
  all_lu_ids = []
  @staticmethod
  def import_dataset(course_id=None):
    """imports user events from firestore and
    creates dataset with required fields"""

    if course_id:
      events =  list(UserEvent.collection.filter(
        "course_id","==",course_id).fetch())
    else:
      events = list(UserEvent.collection.fetch())
    events_list = []
    for i in events:
      #TODO logic to be removed
      #temporary logic for transition parent_node to user_id
      event_dict = i.get_fields()
      if i.parent_node:
        event_dict["user_id"] = i.parent_node
      events_list.append(event_dict)

    events_df = pd.DataFrame(events_list)
    events_df = events_df[events_df.apply(
      filter_events_with_empty_feedback,axis=1)]
    events_df["correct"] = events_df["feedback"].apply(
      lambda x : x["second_attempt"]["evaluation_flag"]
       if "second_attempt" in x.keys() else
        x["first_attempt"]["evaluation_flag"])
    events_df["correct"] = events_df["correct"].apply(
      lambda x: 1.0 if x=="correct" else 0.0)
    events_df["user_ids"] = events_df["user_id"]
    events_df["lu_ids"] = events_df["learning_unit"]
    events_df = events_df.sort_values(by=["last_modified_time"])
    #TODO to be replaced with all lus from lu collection
    all_lu_ids = list(events_df["lu_ids"].unique())
    events_df = events_df.groupby(["user_ids","session_ref"]).filter(
      lambda q: len(q) > 1)
    Dataset.lu_id_encoder.fit(all_lu_ids)
    events_df["encoded_lu"] = events_df["lu_ids"].apply(
      lambda x : Dataset.lu_id_encoder.transform([x])[0])
    events_df["lu_skill_with_answer"] =  events_df.apply(
      lambda x: x["encoded_lu"]* 2 + x["correct"],axis=1)
    return events_df,all_lu_ids

  @staticmethod
  def load_dataset(course_id=None, batch_size=None, shuffle=True):
    """imports dataset, encodes and creates TF dataset"""
    if batch_size is not None:
      Dataset.batch_size = batch_size
    df,all_lu_ids = Dataset.import_dataset(course_id)
    seq = df.groupby(["user_ids","session_ref"]).apply(
      lambda r: (
          r["lu_skill_with_answer"].values[:-1],
          r["encoded_lu"].values[1:],
          r["correct"].values[1:],
      ))

    nb_users = len(seq)
    dataset = tf.data.Dataset.from_generator(
        generator=lambda: seq,
        output_types=(tf.int32, tf.int32, tf.float32)
    )

    if shuffle:
      dataset = dataset.shuffle(buffer_size=nb_users)

    # Step 6 - Encode categorical features and merge skills with labels to
    #compute target loss.
    # More info: https://github.com/tensorflow/tensorflow/issues/32142
    Dataset.features_depth = int(df["lu_skill_with_answer"].max()+1)
    Dataset.skill_depth = int(df["encoded_lu"].max()+1)
    Dataset.all_lu_ids = all_lu_ids
    dataset = dataset.map(
      lambda feat, skill, label: (
          tf.one_hot(feat, depth=Dataset.features_depth),
          tf.concat(
              values=[
                  tf.one_hot(skill, depth=Dataset.skill_depth),
                  tf.expand_dims(label, -1)
              ],
              axis=-1
          )
      ))

    # Step 7 - Pad sequences per batch
    dataset = dataset.padded_batch(
        batch_size=Dataset.batch_size,
        padding_values=(Dataset.MASK_VALUE, Dataset.MASK_VALUE),
        padded_shapes=([None, None], [None, None]),
        drop_remainder=True
    )

    length = nb_users // Dataset.batch_size
    #pylint: disable=line-too-long
    return dataset,length,Dataset.features_depth,Dataset.skill_depth,Dataset.lu_id_encoder

  @staticmethod
  def split_dataset(dataset, total_size, test_fraction, val_fraction=None):
    """splits dataset into train, validation and test sets"""
    def split(dataset, split_size):
      split_set = dataset.take(split_size)
      dataset = dataset.skip(split_size)
      return dataset, split_set

    if not 0 < test_fraction < 1:
      raise ValueError("test_fraction must be between (0, 1)")

    if val_fraction is not None and not 0 < val_fraction < 1:
      raise ValueError("val_fraction must be between (0, 1)")

    test_size = np.ceil(test_fraction * total_size)
    train_size = total_size - test_size

    if test_size == 0 or train_size == 0:
      raise ValueError("The train and test \
      datasets must have at least 1 element.\
      Reduce the\
        split fraction or get more data.")

    train_set, test_set = split(dataset, test_size)

    val_set = None
    if val_fraction:
      val_size = np.ceil(train_size * val_fraction)
      train_set, val_set = split(train_set, val_size)

    return train_set, test_set, val_set

  @staticmethod
  def get_target(y_true, y_pred):
    """"encodes target vectors"""
    # Get skills and labels from y_true
    mask = 1. - tf.cast(tf.equal(y_true, Dataset.MASK_VALUE), y_true.dtype)
    y_true = y_true * mask

    skills, y_true = tf.split(y_true, num_or_size_splits=[-1, 1], axis=-1)

    # Get predictions for each skill
    y_pred = tf.reduce_sum(y_pred * skills, axis=-1, keepdims=True)

    return y_true, y_pred

  #pylint: disable=unused-argument
  @staticmethod
  def process_request_user_events(lu_encoder,user_id, user_events,
  features_depth):
    """returns encoded user events passed through API request"""
    events_df = pd.DataFrame(user_events)

    events_df["encoded_lu"] = events_df["learning_unit"].apply(
      lambda x : lu_encoder.transform([x])[0])
    events_df["lu_skill_with_answer"] =  events_df.apply(
      lambda x: x["encoded_lu"]* 2 + x["is_correct"],axis=1)
    casted_input = tf.cast(
    [events_df["lu_skill_with_answer"]], tf.int32, name=None)
    encoded_input = tf.one_hot(casted_input,depth=features_depth)
    return encoded_input

  @staticmethod
  def process_db_user_events(lu_encoder,user_id=None,
  session_id=None,features_depth=None):
    """returns preprocessed, encoded data taken from database for inference"""
    user_events = UserEvent.collection.filter(user_id=user_id).filter(
      session_ref=session_id).fetch()
    events_list = []
    for i in user_events:
      events_list.append(i.get_fields())
    events_df = pd.DataFrame(events_list)
    events_df = events_df[events_df.apply(
      filter_events_with_empty_feedback,axis=1)]
    events_df["correct"] = events_df["feedback"].apply(
      lambda x : x["second_attempt"]["evaluation_flag"
      ] if "second_attempt" in x.keys() else x[
        "first_attempt"]["evaluation_flag"])
    events_df["correct"] = events_df["correct"].apply(
      lambda x : 1.0 if x=="correct" else 0.0)
    events_df["lu_ids"] = events_df["learning_unit"]
    events_df = events_df.sort_values(by=["last_modified_time"])
    events_df["encoded_lu"] = events_df["lu_ids"].apply(
      lambda x : lu_encoder.transform([x])[0])
    events_df["lu_skill_with_answer"] =  events_df.apply(
      lambda x: x["encoded_lu"]* 2 + x["correct"],axis=1)
    casted_input = tf.cast(
    [events_df["lu_skill_with_answer"]], tf.int32, name=None)
    encoded_input = tf.one_hot(casted_input,depth=features_depth)
    return encoded_input
