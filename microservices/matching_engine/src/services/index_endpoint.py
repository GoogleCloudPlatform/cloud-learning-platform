"""Module to handle index endpoint level CRUD operations"""
from google.cloud import aiplatform_v1beta1
import proto
from config import (REGION,PROJECT_NUMBER,PARENT,ENDPOINT,VPC_NETWORK_NAME)
from services.operation import OperationService

# pylint: disable=line-too-long

class IndexEndpointService():
  """class for performing index endpoint services"""
  def get_name_from_id(self, index_endpoint_id):
    """
      Returns index_endpoint_name given index_endpoint_id
      Args:
        index_endpoint_id - id of index endpoint
      Return:
        index_endpoint_name
    """
    return f"projects/{PROJECT_NUMBER}/locations/{REGION}/indexEndpoints/{index_endpoint_id}"

  def get_index_endpoint_client(self):
    """
      Returns index endpoint client object
    """
    return aiplatform_v1beta1.IndexEndpointServiceClient(
      client_options=dict(api_endpoint=ENDPOINT) #pylint: disable=use-dict-literal
  )

  def get_all_index_endpoints(self):
    """
      Returns all index endpoints
    """
    index_endpoint_client = self.get_index_endpoint_client()
    index_endpoints = index_endpoint_client.list_index_endpoints(
      parent = PARENT)
    index_endpoints = [proto.Message.to_dict(i) for i in index_endpoints]
    for index_endpoint in index_endpoints:
      index_endpoint["index_endpoint_id"] = index_endpoint[
        "name"].split("/")[-1]
      index_endpoint.pop("name",None)
    return index_endpoints

  def get_index_endpoint(self, index_endpoint_id):
    """
      Returns a particular index endpoint given index endpoint id
      Args:
        index_endpoint_id - id of index endpoint
      Return:
        index_endpoint
    """
    index_endpoint_name = self.get_name_from_id(index_endpoint_id)
    index_endpoint_client = self.get_index_endpoint_client()
    index_endpoint = index_endpoint_client.get_index_endpoint(
      name = index_endpoint_name)
    index_endpoint = proto.Message.to_dict(index_endpoint)
    index_endpoint["index_endpoint_id"] = index_endpoint["name"].split("/")[-1]
    index_endpoint.pop("name",None)
    return index_endpoint

  def create_index_endpoint(self, index_endpoint_display_name: str):
    """
      Triggers an operation to create index endpoint
      Args:
        index_endpoint_display_name - display name of index endpoint
      Returns:
        long running operation
    """
    index_endpoint = {
      "display_name": index_endpoint_display_name,
      "network": VPC_NETWORK_NAME,
    }
    index_endpoint_client = self.get_index_endpoint_client()
    operation = index_endpoint_client.create_index_endpoint(
      parent=PARENT, index_endpoint=index_endpoint).operation
    return OperationService().parse_to_dict(operation, metadata_required=False)

  def delete_index_endpoint(self, index_endpoint_id):
    """
      Triggers an operation to delete index endpoint
      Args:
        index_endpoint_id - id of index endpoint
      Returns:
        long running operation
    """
    index_endpoint_client = self.get_index_endpoint_client()
    index_endpoint_name = self.get_name_from_id(index_endpoint_id)
    operation = index_endpoint_client.delete_index_endpoint(
      name = index_endpoint_name).operation
    return OperationService().parse_to_dict(operation, metadata_required=False)


  def get_index_endpoint_operation(self, name):
    """
      Returns status of index endpoint operation
      Args:
        name - operation name
      Returns:
        long running operation
    """
    grpc_channel = self.get_index_endpoint_client().transport.grpc_channel
    return OperationService().get_operation(name, grpc_channel, False)


