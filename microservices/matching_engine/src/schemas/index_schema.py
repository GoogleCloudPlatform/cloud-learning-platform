"""
Pydantic Model for Index API's
"""
from typing import Optional
from pydantic import BaseModel

# pylint: disable=line-too-long

class CreateIndexModel(BaseModel):
  """Create Index Pydantic Model"""
  display_name: str
  description: Optional[str] = "Sample description to create an index model"
  embeddings_gcs_path: str
  embeddings_dimension: int
  approximate_neighbor_count: Optional[int] = 50
  distance_measure_type: str = "DOT_PRODUCT_DISTANCE"
  leaf_node_embedding_count: Optional[int] = 500
  leaf_nodes_to_search_percent: Optional[int] = 7
  shard_size: Optional[str] = "SHARD_SIZE_SMALL"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "display_name":
                "Sample Index",
            "description":
                "Index created on sample data",
            "embeddings_gcs_path": "gs://sample_bucket/path/",
            "embeddings_dimension": 768,
            "approximate_neighbor_count":
                50,
            "distance_measure_type":
                "DOT_PRODUCT_DISTANCE",
            "leaf_node_embedding_count": 500,
            "leaf_nodes_to_search_percent": 7,
            "shard_size": "SHARD_SIZE_SMALL"

        }
    }

class UpdateIndexModel(BaseModel):
  """Create Index Pydantic Model"""
  display_name: Optional[str]
  description: Optional[str]
  embeddings_gcs_path: Optional[str]
  embeddings_dimension: Optional[int]
  approximate_neighbor_count: Optional[int] = 50
  distance_measure_type: Optional[str] = "DOT_PRODUCT_DISTANCE"
  leaf_node_embedding_count: Optional[int] = 500
  leaf_nodes_to_search_percent: Optional[int] = 7

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "display_name":
                "Sample Index",
            "description":
                "Index created on sample data",
            "embeddings_gcs_path": "gs://sample_bucket/path/",
            "embeddings_dimension": 768,
            "approximate_neighbor_count":
                50,
            "distance_measure_type":
                "DOT_PRODUCT_DISTANCE",
            "leaf_node_embedding_count": 500,
            "leaf_nodes_to_search_percent": 7

        }
    }
