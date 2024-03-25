"""module to check operation status"""
from google.api_core import operations_v1
from google.longrunning.operations_pb2 import Operation

class OperationService():
  """class for operation service"""
  def get_operation(self, operation_name,channel,
  metadata_required = False) :
    """
      Returns operation using operation name and client channel
      Args:
        operation_name - name of operation
        channel - client transport channel, \
        differs for index, index_endpoint clients
        metadata_required - Flag to include metadata of operation in response
      Returns:
        operation dict

    """
    operations_client = operations_v1.OperationsClient(channel = channel)
    operation = operations_client.get_operation(name = operation_name)
    op_response = self.parse_to_dict(operation, metadata_required)
    return op_response

  def parse_to_dict(self, operation: Operation, metadata_required: bool):
    """
      Reformats operation object to dict
      Args:
        Operation protobuff object
        metadata_required - Flag to include metadata of operation in response
      Returns:
        operation dict
    """
    operation_dict = {}
    operation_dict["name"] = operation.name
    operation_dict["status"] = "completed" if operation.done else "running"
    if operation.error.message:
      operation_dict["error_message"] = operation.error.message
      operation_dict["status"] = "failed"
    if metadata_required:
      operation_dict["metadata"] = operation.metadata
    return operation_dict
