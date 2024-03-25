"""Maps skill to passage nodes of learning resource."""

# pylint: disable=invalid-name

from services.embedding import Embedding

from config import RERANKER_THRESHOLD

# pylint: disable=redefined-builtin
class Skill_Passage:
  """Skill to passage node alignment"""
  model = Embedding.cross_encoders["cross-encoder/ms-marco-MiniLM-L-12-v2"]


  def __init__(self, id, title, metadata) -> None:
    """Initialize all the instance variables with the necessary attributes
       for the knowledge data."""

    self.id = id
    self.title = title
    self.length = self.calculate_length(metadata)
    self.score = self.calculate_score(metadata)
    self.mapped = self.check_mapping(metadata)

  def calculate_length(self, metadata) -> int:
    """Calculates the number of words in the Passage text
      Args:
        metadata: dictionary containing
                passage_text: text of the passage
                skill_description: skill description
      Returns:
        node_length: returns the number of words in the knowledge node text
    """
    node_length = len(metadata["passage_text"].split(" "))
    return node_length

  def calculate_score(self, metadata) -> float:
    """Calculates the similarity score between Passage and skill
      Args:
        metadata: dictionary containing
                passage_text: text of the passage
                skill_description: skill description
      Returns:
        score: returns the weighted semantic similarity score
    """
    score = Skill_Passage.model.predict(
        [metadata["skill_description"], metadata["passage_text"]]).tolist()
    return round(score, 3)

  def check_mapping(self, metadata): # pylint: disable=unused-argument
    """Checks if the Passage node can be mapped to the skill
      Args:
        metadata: list - list of Skill_Passage objects
      Returns:
        (boolean) True (if mapped)
                  False (otherwise)
    """
    return self.score >= RERANKER_THRESHOLD

  def get_item_dict(self) -> dict:
    """returns dictionary with all the important values"""
    accepted_keys = ["id", "title", "score"]
    item_dict = {key: val for key, val in \
      self.__dict__.items() if key in accepted_keys}
    return item_dict
