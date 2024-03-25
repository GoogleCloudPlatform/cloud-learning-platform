"""Maps skill to lu nodes of learning resource."""

# pylint: disable=invalid-name

from config import RERANKER_THRESHOLD, RATIO_THRESHOLD
from services.skill_to_knowledge.skill_to_node_data.skill_to_passage import Skill_Passage


class Skill_LU(Skill_Passage):
  """Skill to LU node alignment"""

  def calculate_length(self, metadata) -> None:
    """Calculates the number of words in the LU text
      Args:
        metadata: list - list of Skill_Passage objects
      Returns:
        node_length: returns the number of words in the knowledge node text
    """
    node_length = sum(lower_level_node.length for lower_level_node in metadata)
    return node_length

  def calculate_score(self, metadata) -> float:
    """Calculates the similarity score between LU and skill
      Args:
        metadata: list - list of Skill_Passage objects
      Returns:
        score: returns the weighted semantic similarity score
    """
    score = sum(
        lower_level_node.length * lower_level_node.score
        for lower_level_node in metadata
    )
    try:
      result = score / self.length
    except ZeroDivisionError:
      result = 0.0
    return round(result, 3)

  def check_mapping(self, metadata) -> bool:
    """Checks if the LU node can be mapped to the skill
      Args:
        metadata: list - list of Skill_Passage objects
      Returns:
        (boolean) True (if mapped)
                  False (otherwise)
    """
    count_lower_mapped_nodes = sum(
        1 for lower_level_node in metadata if lower_level_node.mapped)
    try:
      return count_lower_mapped_nodes / len(
        metadata) >= RATIO_THRESHOLD or self.score >= RERANKER_THRESHOLD
    except ZeroDivisionError:
      return False
