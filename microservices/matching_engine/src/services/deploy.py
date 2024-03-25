"""Module for index deployments """
from services.index_endpoint import IndexEndpointService
from services.operation import OperationService
from google.cloud import aiplatform
from config import (PROJECT_NUMBER,REGION,DEFAULT_MACHINE_TYPE,
DEFAULT_MIN_REPLICA,DEFAULT_MAX_REPLICA)

class DeployIndexService():
  """class to deploy, check status and undeploy indexes to index endpoints"""
  def deploy_index(self,input_params):
    """
      Deploys given index to a given index_endpoint
      Args:
        input_params - Dict with the following keys
          deployed_index_display_name - name to be given to deployed_index
          index_id - id of index to be deployed
          index_endpoint_id - id of the index endpoint
      Returns:
        long running operation
    """
    deployed_index_display_name = input_params.get(
      "deployed_index_display_name")
    index_id = input_params.get("index_id")
    index_endpoint_id = input_params.get("index_endpoint_id")
    machine_type = input_params.get("machine_type",DEFAULT_MACHINE_TYPE)
    min_replica_count = input_params.get("min_replica_count",
    DEFAULT_MIN_REPLICA)
    max_replica_count = input_params.get("max_replica_count",
    DEFAULT_MAX_REPLICA)
    deployed_index_id = deployed_index_display_name+"_"+index_id
    index_to_deploy = aiplatform.MatchingEngineIndex(project=PROJECT_NUMBER,
      location=REGION, index_name=index_id)
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        project = PROJECT_NUMBER, location = REGION,
        index_endpoint_name = index_endpoint_id)
    #pylint: disable=protected-access
    deployed_index = index_endpoint._build_deployed_index(
            deployed_index_id=deployed_index_id,
            index_resource_name=index_to_deploy.resource_name,
            display_name=deployed_index_display_name,
            machine_type=machine_type,
            min_replica_count=min_replica_count,
            max_replica_count=max_replica_count)
    lro = index_endpoint.api_client.deploy_index(
            index_endpoint=index_endpoint.resource_name,
            deployed_index=deployed_index
        )

    return OperationService().parse_to_dict(lro.operation, False)



  def undeploy_index(self, input_params):
    """
      Undeploys deployed index from index_endpoint
      Args:
        input_params - Dict with the following keys
          deployed_index_id - id of the deployed_index
          index_endpoint_id - id of the index endpoint
      Returns:
        long running operation
    """
    deployed_index_id = input_params.get("deployed_index_id")
    index_endpoint_id = input_params.get("index_endpoint_id")
    index_endpoint_name = IndexEndpointService().get_name_from_id(
      index_endpoint_id)
    client = IndexEndpointService().get_index_endpoint_client()
    operation = client.undeploy_index(index_endpoint = index_endpoint_name,
    deployed_index_id = deployed_index_id).operation
    return OperationService().parse_to_dict(operation, False)

  def get_index_deployment_operation(self, name):
    """
      Returns status of index deployment operation
      Args:
        name - operation name
      Returns:
        long running operation
    """
    return IndexEndpointService().get_index_endpoint_operation(name)

