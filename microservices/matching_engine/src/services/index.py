"""Performs CRUD on matching engine service indexes"""
from google.protobuf import struct_pb2
from google.cloud import aiplatform_v1beta1
import proto
from config import (REGION,PROJECT_NUMBER,PARENT,ENDPOINT)
from utils.logging_handler import Logger
from services.operation import OperationService

class IndexService():
  """class for index service"""
  def get_index_client(self):
    """
      Returns index client object
    """
    return aiplatform_v1beta1.IndexServiceClient(
      client_options=dict(api_endpoint=ENDPOINT)) #pylint: disable=use-dict-literal

  def parse_dict_to_index(self, input_params: dict):
    """
      Converts input params dict to format required for index creation
      Args:
        input_params - dict of all index related params required to create index
      Returns:
        reformated index nested dict
    """
    tree_ah_config = struct_pb2.Struct(
      fields={
          "leafNodeEmbeddingCount": struct_pb2.Value(
            number_value=input_params["leaf_node_embedding_count"]),
          "leafNodesToSearchPercent": struct_pb2.Value(
            number_value=input_params["leaf_nodes_to_search_percent"]),
      }
  )

    algorithm_config = struct_pb2.Struct(
      fields={"treeAhConfig": struct_pb2.Value(struct_value=tree_ah_config)}
    )

    config = struct_pb2.Struct(
      fields={
          "dimensions": struct_pb2.Value(
            number_value=input_params["embeddings_dimension"]),
          "approximateNeighborsCount": struct_pb2.Value(
            number_value=input_params["approximate_neighbor_count"]),
          "distanceMeasureType": struct_pb2.Value(
            string_value=input_params["distance_measure_type"]),
          "algorithmConfig": struct_pb2.Value(struct_value=algorithm_config),
          "shardSize": struct_pb2.Value(
            string_value=input_params.get("shard_size","SHARD_SIZE_SMALL"))
      }
    )

    metadata = struct_pb2.Struct(
      fields={
          "config": struct_pb2.Value(struct_value=config),
          "contentsDeltaUri": struct_pb2.Value(
            string_value=input_params["embeddings_gcs_path"]),
      }
    )

    ann_index = {
      "display_name": input_params["display_name"],
      "description": input_params["description"],
      "metadata": struct_pb2.Value(struct_value=metadata),
    }

    if input_params.get("name",""):
      ann_index["name"] = input_params["name"]

    return ann_index

  def reformat_index_dict(self, index: dict):
    """
      Reformats index dict before updating index
      Args:
        index - index fields dict
      Returns:
        reformatted index fields dict
    """
    index_dict = {}
    index_dict["display_name"] = index["display_name"]
    index_dict["description"] = index["description"]
    index_dict["approximate_neighbor_count"] = index[
      "metadata"]["config"]["approximateNeighborsCount"]
    index_dict["embeddings_dimension"] = index["metadata"][
      "config"]["dimensions"]
    index_dict["leaf_node_embedding_count"] = index["metadata"][
      "config"]["algorithmConfig"]["treeAhConfig"]["leafNodeEmbeddingCount"]
    index_dict["leaf_nodes_to_search_percent"] = index["metadata"][
      "config"]["algorithmConfig"]["treeAhConfig"]["leafNodesToSearchPercent"]
    index_dict["distance_measure_type"] = index["metadata"][
      "config"]["distanceMeasureType"]
    index_dict["shard_size"] = index["metadata"][
      "config"]["shardSize"]
    return index_dict

  def get_all_indexes(self):
    """
      Returns all indexes that exist in the matching engine service
    """
    index_client = self.get_index_client()
    indexes = index_client.list_indexes(parent = PARENT)
    indexes = [proto.Message.to_dict(i) for i in indexes]
    for index in indexes:
      index["index_id"] = index["name"].split("/")[-1]
      index.pop("name",None)
    return indexes

  def get_name_from_id(self, index_id: str):
    """
      Returns index_name given index_id
      Args:
        index_id - id of index
      Return:
        index_name
    """
    return f"projects/{PROJECT_NUMBER}/locations/{REGION}/indexes/{index_id}"

  def get_index(self, index_id: str, return_dict: bool = True):
    """
      Returns a particular index given index id
      Args:
        index_id - id of index
        return_dict - Flag to decide response type - dict or protobufMessage
      Return:
        index details
    """
    index_client = self.get_index_client()
    index_name = self.get_name_from_id(index_id)
    index = index_client.get_index(name = index_name)
    if return_dict:
      index = proto.Message.to_dict(index)
      index["index_id"] = index["name"].split("/")[-1]
      index.pop("name",None)
    return index

  def check_index_exist(self, display_name):
    """
    Check if an index with a "display_name" exists in
      Matching Engine ANN service

    Args:
      display_name - display name for the index

    Returns:
      exists (bool) - True if index exists, else False
      index_id (str) - index id with the display name
    """
    exists = False
    index_id = None
    data = self.get_all_indexes()
    for index_info in data:
      if index_info["display_name"] == display_name:
        exists = True
        index_id = index_info["index_id"]
    return (exists, index_id)

  def create_index(self, input_params: dict):
    """
      Triggers an operation to create index
      Args:
        input_params - dict params for creating index
      Returns:
        long running operation
    """
    Logger.info(f"Input Params are: {input_params}")
    index_display_name = input_params.get("display_name")
    index_exists, index_id = self.check_index_exist(index_display_name)
    Logger.info(f"Index already exists: {index_exists} ID: {index_id}")
    if index_exists:
      return self.update_index(index_id, input_params)
    ann_params = self.parse_dict_to_index(input_params)
    index_client = self.get_index_client()
    operation = index_client.create_index(
      parent=PARENT, index=ann_params).operation
    return OperationService().parse_to_dict(operation, metadata_required=False)

  def update_index(self, index_id: str, input_params: dict):
    """
      Triggers an operation to update index
      Args:
        index_id - id of the index to update
        input_params - dict params to be updated for given index
      Returns:
        long running operation
    """
    index = self.get_index(index_id)
    index_dict = self.reformat_index_dict(index)
    index_dict["name"] = self.get_name_from_id(index_id)
    for i in input_params:
      index_dict[i] = input_params[i]
    index_client = self.get_index_client()
    operation = index_client.update_index(
      index = self.parse_dict_to_index(index_dict)).operation
    return OperationService().parse_to_dict(operation, False)

  def delete_index(self, index_id: str):
    """
      Triggers an operation to delete index
      Args:
        index_id - id of the index to delete
      Returns:
        long running operation
    """
    index_name = self.get_name_from_id(index_id = index_id)
    index_client = self.get_index_client()
    operation = index_client.delete_index(name = index_name).operation
    return OperationService().parse_to_dict(operation, False)

  def get_index_operation(self, name):
    """
      Returns status of index operation
      Args:
        name - operation name
      Returns:
        long running operation
    """
    grpc_channel = self.get_index_client().transport.grpc_channel
    return OperationService().get_operation(name, grpc_channel, False)
