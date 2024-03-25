"""Module to create and save embedding to Embedding Database"""

from sentence_transformers import SentenceTransformer, CrossEncoder
from services.data_source import update_data_source_fields
import numpy as np
from torch import nn
import pandas as pd
import json
import uuid
import requests
import time
import os
from common.utils.gcs_adapter import upload_blob
from common.utils.logging_handler import Logger
from config import (
  MATCHING_ENGINE_BUCKET_NAME, SERVICES, EMBEDDING_ENDPOINT_ID,
  EMBEDDINGS_DIMENSION,
  APPROXIMATE_NEIGHBOR_COUNT,
  DISTANCE_MEASURE_TYPE,
  LEAF_NODE_EMB_COUNT,
  LEAF_NODES_TO_SEARCH_PRECENT
)

# pylint: disable=broad-exception-raised,consider-using-f-string

class Embedding():
  """Creates Embeddings and save to Embedding Database"""
  bi_encoders = {
    "all-mpnet-base-v2": SentenceTransformer("all-mpnet-base-v2"),
    "msmarco-bert-base-dot-v5": SentenceTransformer(
      "msmarco-bert-base-dot-v5")
  }

  cross_encoders = {
    "cross-encoder/ms-marco-MiniLM-L-12-v2": CrossEncoder(
                                "cross-encoder/ms-marco-MiniLM-L-12-v2",
                                default_activation_function=nn.Sigmoid()),
    "cross-encoder/nli-distilroberta-base": CrossEncoder(
                                "cross-encoder/nli-distilroberta-base",
                                default_activation_function=nn.Sigmoid()),
    "cross-encoder/stsb-roberta-large": CrossEncoder(
                                "cross-encoder/stsb-roberta-large",
                                default_activation_function=nn.Sigmoid())
  }

  def __init__(
      self,
      bi_encoder_model_name,
      cross_encoder_model_name,
      max_seq_length = 256):
    Embedding.bi_encoders[
      bi_encoder_model_name].max_seq_length = max_seq_length
    Embedding.cross_encoders[
      cross_encoder_model_name].max_seq_length = max_seq_length
    self.bi_encoder = Embedding.bi_encoders[bi_encoder_model_name]
    self.cross_encoder = Embedding.cross_encoders[cross_encoder_model_name]

  def generate_embeddings(self, docs):
    """
    Method to generate document embeddings

    Args:
      docs (List[str]): List of texts to be converted into embeddings

    Returns:
      embeddings: List of generated embeddings
    """
    embeddings = self.bi_encoder.encode(
      docs, convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1)[:, None]
    return embeddings

  def search_docs(self, queries, top_k): # pylint: disable=W0613
    """
    Given a list of queries, this method returns the top_k matches
    from the bi_encoder search result

    Args:
      queries List(str) - List of all queries
      top_k (int) - number of expected results

    Results:
      doc_ids List(str) - Firestore document ids of each skill candidate
    """
    skill_embeddings = self.generate_embeddings(queries).tolist()
    doc_ids = self.batch_search_ann_service(self.DB_INDEX, skill_embeddings)
    return doc_ids


  def batch_search_ann_service(self, index_name, query_embeddings):
    """
    Given a list of query embeddings, this method retrieves the top k documents
    from the ANN matching service

    Args:
      index_name (str) - index to search the matching service
      query_embeddings (List(List)) - n X 768 dimension query embedding vectors

    Results:
      prediction (json object) - json object containing the retrieved document
                ids for each query vector
    """
    Logger.info(type(query_embeddings))
    index_exists, index_id = self.check_index_exist(index_name, True)
    if index_exists:
      prediction = json.loads(
        requests.post(
          url="http://{}:{}/matching-engine/api/v1/query/result".\
              format(
              SERVICES["matching-engine"]["host"],
              SERVICES["matching-engine"]["port"]
            ),
          json={
            "deployed_index_id": index_id,
            "index_endpoint_id": EMBEDDING_ENDPOINT_ID,
            "queries": query_embeddings
            },
          timeout=10
          ).content
        )
      Logger.info(prediction)
      return prediction["data"]
    else:
      raise Exception("Please create an embeddings index first.")


  def rerank_docs(self, query_doc_list):
    """
    Given a list of query and bi_encoder retrieved docs,
    this method reranks the docs

    Args:
      query_doc_list List[List[str]] -
        Two dimensional list containing query doc pair

    Returns: scores for each pair of query and doc
    """
    scores = self.cross_encoder.predict(query_doc_list)
    scores = [np.round(score.item(), 3) for score in scores]
    return scores

  def check_index_exist(self, display_name, check_deployed=False):
    """
    Check if an index with a "display_name" exists in ANN service

    Args:
      display_name - display name for the index
      check_deployed (bool) - check if the index is deployed or not

    Returns:
      exists (bool) - True if index exists, else False
      index_id (str) - index id with the display name
    """
    exists = False
    index_id = None
    data = json.loads(
      requests.get(
        url="http://{}:{}/matching-engine/api/v1/index".\
            format(
            SERVICES["matching-engine"]["host"],
            SERVICES["matching-engine"]["port"],
          ),
          timeout=10
        ).content)["data"]
    for index_info in data:
      if check_deployed:
        if index_info["display_name"] == display_name and index_info[
          "deployed_indexes"]:
          exists = True
          index_id = index_info["deployed_indexes"][0]["deployed_index_id"]
      else:
        if index_info["display_name"] == display_name:
          exists = True
          index_id = index_info["index_id"]
    return (exists, index_id)

  def populate_embedding_db(
      self, gcs_path, index_name, index_desc, object_type=None):
    """Populate the embedding database and deploy the index
    to index endpoint
    Args:
      gcs_path: str - GCS path of embedding CSV files
      index_name: str - Name of index to create/update
      index_desc: str - Description of index
      object_type: str - type of object (skill/knowledge)
    Returns:
      None"""
    output = self.update_matching_engine_index(
      gcs_path, index_name, index_desc)
    Logger.info("INDEX CREATED : {}".format(output))
    status = self.wait_for_process_creation(output["name"])
    Logger.info("STATUS OF EMBEDDING CREATION JOB: {}".format(status))
    if not status:
      raise Exception("Failed to created index")

    index_id = output["name"].split("/")[-3]
    # Update index ID in data source collection after creation:
    if object_type:
      _ = update_data_source_fields(object_type, self.DB_INDEX, index_id)
    Logger.info("Updated Matching Engine index ID in data sources collection")

    self.deploy_to_index_endpoint(
      self.DB_INDEX + "-deployed-index",
      output["name"],
      index_endpoint_id=EMBEDDING_ENDPOINT_ID)


  def update_matching_engine_index(
      self, gcs_path, index_name, index_desc):
    """Creates or updates an Embedding index.
    Args:
      gcs_path: str - GCS path of embedding CSV files
      index_name: str - Name of index to create/update
      index_desc: str - Description of index
    Returns:
      prediction - dict with keys name and status of operation
      """
    Logger.info("Values are: {} {}".format(gcs_path, index_desc))
    prediction = json.loads(
      requests.post(
        url="http://{}:{}/matching-engine/api/v1/index".\
            format(
            SERVICES["matching-engine"]["host"],
            SERVICES["matching-engine"]["port"],
          ),
        json={
          "display_name": index_name,
          "description": index_desc,
          "embeddings_gcs_path": gcs_path,
          "embeddings_dimension": EMBEDDINGS_DIMENSION,
          "approximate_neighbor_count": APPROXIMATE_NEIGHBOR_COUNT,
          "distance_measure_type": DISTANCE_MEASURE_TYPE,
          "leaf_node_embedding_count": LEAF_NODE_EMB_COUNT,
          "leaf_nodes_to_search_percent": LEAF_NODES_TO_SEARCH_PRECENT
          },
        timeout=10).content)["data"]
    return prediction

  def wait_for_process_creation(self, operation_id):
    """Polls and waits till the operation is completed
    Args:
      operation_d: str - Id of running operation
    Returns:
      boolean: True if operation is successful"""
    Logger.info("Started Polling Process")
    running = True
    while running:
      time.sleep(300)
      prediction = json.loads(
        requests.get(
          url="http://{}:{}/matching-engine/api/v1/index/operation/".\
              format(
              SERVICES["matching-engine"]["host"],
              SERVICES["matching-engine"]["port"],
            ),
          params={
            "name": operation_id
            },
          timeout=10).content)["data"]
      Logger.info("In Waiting LOOP with status: {}".format(prediction))
      prediction = prediction["status"]
      if prediction == "running":
        running = True
      elif prediction == "completed":
        running = False
      else:
        running = False
        return False
    return True

  def check_deployed_index_exist(
      self, index_endpoint_id, index_display_name):
    """Checks if a deployed index exist for given index name
    Args:
      index_endpoint_id: str - Id of index endpoint
      index_display_name: str: Display name of index
    Returns:
      boolean: Deployed index exist or not
    """
    data = json.loads(
      requests.get(
        url="http://{}:{}/matching-engine/api/v1/index-endpoint/{}".\
            format(
            SERVICES["matching-engine"]["host"],
            SERVICES["matching-engine"]["port"],
            index_endpoint_id
          ),
        timeout=10
        ).content)["data"]["deployed_indexes"]
    exists = False
    for index in data:
      if index["display_name"] == index_display_name:
        exists = True
    return exists

  def deploy_to_index_endpoint(
      self, display_name, index, index_endpoint_id):
    """Deploys a created index to index endpoint
    Args:
      display_name: str - Name of Index Endpoint
      index : Name of Index
      index_endpoint_id: str - index endpoint id
    Returns:
      None
    """
    index_id = index.split("/")[-3]

    deployed_index_exists = self.check_deployed_index_exist(
      index_endpoint_id, display_name)
    Logger.info(
      "Is there already an existing index endpoint: {}".format(
        deployed_index_exists))

    if deployed_index_exists:
      return deployed_index_exists

    prediction = json.loads(
      requests.post(
        url="http://{}:{}/matching-engine/api/v1/deploy".\
            format(
            SERVICES["matching-engine"]["host"],
            SERVICES["matching-engine"]["port"],
          ),
        json={
          "deployed_index_display_name": display_name,
          "index_id": index_id,
          "index_endpoint_id": index_endpoint_id
          },
        timeout=10).content)["data"]
    Logger.info(prediction)
    Logger.info("Waiting for Index Deployment")
    self.wait_for_process_creation(prediction["name"])

  def export_embedding_csv(
      self, docs, doc_ids, index_name, file_name=None):
    """Generates the embedding and exports the csv to GCS
    Args:
      docs: List[str]: List of all texts
      doc_ids: List[str] of doc ids
      index_name: str - Name of Index to store embeddings
      file_name: str - Name of csv file
    return:
      output: str - GCS bucket in which CSV is stored
    """
    if file_name:
      file_name = file_name + ".csv"
    else:
      file_name = str(uuid.uuid4()) + ".csv"

    embeddings = self.generate_embeddings(docs)
    df = pd.DataFrame(doc_ids)
    df = pd.concat([df, pd.DataFrame(embeddings)], axis=1)
    df.to_csv(file_name, index=False,header=False)
    blob_name = "matching-engine/" + index_name
    blob_with_filename = blob_name + "/" + file_name
    upload_blob(MATCHING_ENGINE_BUCKET_NAME, file_name, blob_with_filename)
    os.remove(file_name)
    output = "gs://{}/{}".format(MATCHING_ENGINE_BUCKET_NAME, blob_name)
    return output
