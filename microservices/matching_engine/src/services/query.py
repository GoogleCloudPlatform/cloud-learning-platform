"""module to query deployed indexes"""


from google.cloud import aiplatform
from config import PROJECT_NUMBER,REGION


class IndexQueryService():
  """class for querying index service"""
  def parse_response(self, responses):
    """
      Converts MatchResponse object to nested dict
    """
    parsed_responses = []
    for response in responses:
      neighbors = []
      response_dict = {}
      for neighbor in response:
        neighbor_dict = {}
        neighbor_dict["id"] = neighbor.id
        neighbor_dict["distance"] = neighbor.distance
        neighbors.append(neighbor_dict)
      for i in range(len(neighbors)):
        response_dict[str(i)] = neighbors[i]
      parsed_responses.append(response_dict)
    return parsed_responses

  def match(self,input_params: dict):
    """returns a list of nearest neighbors for a given list of queries

    Args:
        input_params (dict): Dict with the following keys
          deployed_index_id - id of deployed_index
          index_endpoint_id - id of the index endpoint
          queries - List of query embeddings

    Returns:
        List of nearest neighbors for a given list of queries
    """
    index_endpoint_id = input_params.get("index_endpoint_id")
    deployed_index_id = input_params.get("deployed_index_id")
    num_neighbors = input_params.get("num_neighbors",10)
    filters = input_params.get("filters",[])
    queries = input_params.get("queries")
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
          project = PROJECT_NUMBER, location = REGION,
          index_endpoint_name = index_endpoint_id)
    if not filters:
      filters = []
    nearest_neighbors = index_endpoint.match(deployed_index_id,
      queries, num_neighbors, filters)
    return self.parse_response(nearest_neighbors)
