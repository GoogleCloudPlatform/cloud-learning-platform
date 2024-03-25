"""Map skill to skill"""
from common.models import Skill
from common.utils.errors import ValidationError, ResourceNotFoundException
from sentence_transformers import CrossEncoder
from torch import nn

# pylint: disable = invalid-name

class SkillSimilarity():
  """Class for skill similarity"""

  cross_encoder = CrossEncoder(
      "cross-encoder/ms-marco-MiniLM-L-12-v2",
      default_activation_function=nn.Sigmoid())

  def get_skill_data(self, skill_id_1, skill_id_2, source):
    skill_data_1 = Skill.find_by_id(skill_id_1)
    skill_data_2 = Skill.find_by_id(skill_id_2)

    if skill_data_1 is None or skill_data_2 is None:
      raise ResourceNotFoundException("Skill with the given id does not exist")

    if skill_data_1.source_name == source and \
      skill_data_2.source_name == source:
      text1 = skill_data_1.name + ". " + skill_data_1.description
      text2 = skill_data_2.name + ". " + skill_data_2.description
    else:
      raise ValidationError("Data source does not match for both the skills")
    return text1, text2

  def get_skill_similarity(self, text1, text2):
    try:
      similarity_score = self.cross_encoder.predict([text1, text2])
    except Exception("Couldn't retieve similarity score") as Failed_Retrieval:
      raise Failed_Retrieval

    similarity_score = similarity_score.item()
    return round(similarity_score, 3)
