"""Updates item difficulty and discrimination in firestore"""

from common.models import ChooseTheFactItem, AnswerAQuestionItem, ParaphrasingPracticeItem, CreateKnowledgeNotesItem
import fireo

def update_assessment_items(
    item_difficulty, item_discrimination, item_type_dict, model_type):
  """Updates item discimination and difficulty of Assessment items"""
  print("Updating Assessment parameters")
  batch = fireo.batch()
  count = 0
  for assessment_id, _ in item_difficulty.items():
    if count >450:
      batch.commit()
      count = 0
    count += 1
    item_type = item_type_dict[assessment_id]
    if item_type == "choose_the_fact":
      ctf_item = ChooseTheFactItem.find_by_id(assessment_id)
      if ctf_item:
        ctf_item.difficulty_score = float(item_difficulty[assessment_id])
        if model_type=="2pl":
          ctf_item.discrimination = float(item_discrimination[assessment_id])
        ctf_item.learning_unit = ctf_item.learning_unit.get()
        ctf_item.update(batch=batch)
    elif item_type=="answer_a_question":
      aaq_item = AnswerAQuestionItem.find_by_id(assessment_id)
      if aaq_item:
        aaq_item.difficulty_score = float(item_difficulty[assessment_id])
        if model_type=="2pl":
          aaq_item.discrimination = float(item_discrimination[assessment_id])
        aaq_item.learning_unit = aaq_item.learning_unit.get()
        aaq_item.update(batch=batch)
    elif item_type=="paraphrasing_practice":
      paraphrase_item = ParaphrasingPracticeItem.find_by_id(assessment_id)
      if paraphrase_item:
        paraphrase_item.difficulty_score = float(item_difficulty[assessment_id])
        if model_type=="2pl":
          paraphrase_item.discrimination = float(
            item_discrimination[assessment_id])
        paraphrase_item.learning_unit = paraphrase_item.learning_unit.get()
        paraphrase_item.update(batch=batch)
    elif item_type=="create_knowledge_notes":
      create_knowledge_notes_item = CreateKnowledgeNotesItem.\
        find_by_id(assessment_id)
      if create_knowledge_notes_item:
        create_knowledge_notes_item.difficulty_score = \
          float(item_difficulty[assessment_id])
        if model_type=="2pl":
          create_knowledge_notes_item.discrimination = float(
            item_discrimination[assessment_id])
        create_knowledge_notes_item.learning_unit = \
          create_knowledge_notes_item.learning_unit.get()
        create_knowledge_notes_item.update(batch=batch)
  batch.commit()


