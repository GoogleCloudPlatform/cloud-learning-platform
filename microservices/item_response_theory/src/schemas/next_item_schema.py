"""Schema for next assessment item"""

from enum import Enum

# pylint: disable=invalid-name
class ActivityType(str, Enum):
  choose_the_fact= "choose_the_fact"
  answer_a_question= "answer_a_question"
  paraphrase_practice= "paraphrasing_practice"
  create_knowledge_notes= "create_knowledge_notes"
