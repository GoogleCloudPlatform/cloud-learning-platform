"""Search at any level in  Skill Graph"""
from common.models import (Skill, SkillServiceCompetency, Category, SubDomain,
  Domain, Concept, SubConcept, KnowledgeServiceLearningContent,
  KnowledgeServiceLearningUnit, KnowledgeServiceLearningObjective)
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError
from services.embedding import Embedding
from config import (BI_ENCODER_MODELS, CROSS_ENCODER_MODELS)

# pylint: disable=raise-missing-from,broad-exception-raised,consider-using-f-string,invalid-name

class SearchSkillGraph(Embedding):
  """Class for Search at any level in Skill Graph"""

  BI_ENCODER_MODEL_NAME = BI_ENCODER_MODELS["SEARCH"]
  CROSS_ENCODER_MODEL_NAME = CROSS_ENCODER_MODELS["SEARCH"]
  BI_ENCODER_TOP_K = 15

  def __init__(self, level, source=None) -> None:
    super().__init__(
      self.BI_ENCODER_MODEL_NAME, self.CROSS_ENCODER_MODEL_NAME)
    self.level = level
    self.source_name = source
    if self.source_name:
      self.DB_INDEX = level + "_" + source
      self.index_description = f"Embeddings for {source} in {level}"
    else:
      self.DB_INDEX = level
      self.index_description = f"Embeddings for {level}"

  def prepare_text_for_embedding(self, name=None, description=None):
    """
    Prepares text for embedding. If Both name and
    description are present. They are combined.

    Args:
      name (str): name value
      description (str): Description text

    Returns:
      text (str): Combined text if both name and description are present.
    """
    if name and description:
      text = name + ". " + description
    elif name:
      text = name
    elif description:
      text = description
    else:
      raise Exception("For embedding input alteast one out of "
      "name and description should be present.")
    return text

  def prepare_and_save_embeddings(self, documents):
    """Prepares input text from given documents and save the
      embeddings

      Args:
        documents: list(FireoModels)
    """
    texts = []
    doc_ids = []
    filtered_documents = []
    Logger.info("Len of documents: {}".format(len(documents)))
    if self.source_name:
      for doc in documents:
        if doc.source_name == self.source_name:
          filtered_documents.append(doc)
    else:
      filtered_documents = documents
    for doc in filtered_documents:
      if self.level == "competency":
        texts.append(self.prepare_text_for_embedding(
          doc.name, doc.description))
      else:
        texts.append(self.prepare_text_for_embedding(
          doc.name, doc.description))
      doc_ids.append(doc.id)
    Logger.info("Len texts: {}".format(len(texts)))
    Logger.info("Len ids: {}".format(len(doc_ids)))
    if doc_ids:
      gcs_path = self.export_embedding_csv(
        texts, doc_ids, self.DB_INDEX , self.DB_INDEX)
      self.populate_embedding_db(
        gcs_path, self.DB_INDEX, self.index_description, self.level)
    else:
      print("No documents found to generate embeddings.")

  def populate_level_embeddings_in_db(self):
    """Populates Embedding database index for a given level
    in Skill Graph
    """
    level_obj = self.get_level_obj()
    documents = level_obj.fetch_all_documents()
    if not documents:
      return
    else:
      Logger.info("No of {} : {} ".format(self.level, len(documents)))

    self.prepare_and_save_embeddings(documents)

  def get_level_obj(self):
    """Return Fireo Class for particular level

    Args: None
    Returns: Fireo Class
    """
    if self.level == "skill":
      level_obj = Skill
    elif self.level == "competency":
      level_obj = SkillServiceCompetency
    elif self.level == "category":
      level_obj = Category
    elif self.level == "sub_domain":
      level_obj = SubDomain
    elif self.level == "domain":
      level_obj = Domain
    else:
      raise Exception("Level not defined in Skill Graph")
    return level_obj

  def align_query(self, query, top_k):
    """Given query and top_k, this function return top_k
       documents from database for a given level

      Args:
        query: str - query to search
      Returns:
        response_list: List[dict] - List of top_k aligned documents
        for given query
    """
    document_ids = self.search_docs([query], self.BI_ENCODER_TOP_K)
    document_ids = [doc_ids["id"] for _, doc_ids in document_ids[0].items()]
    docs = []
    level_obj = self.get_level_obj()
    for doc_id in document_ids:
      doc_obj = level_obj.find_by_id(doc_id)
      docs.append(doc_obj)
    matched = []
    reranker_input = [[query, self.prepare_text_for_embedding(
      doc.name, doc.description)] for doc in docs]
    scores_passages = self.rerank_docs(reranker_input)
    for i, score in enumerate(scores_passages):
      name = docs[i].name
      if not name:
        name = ""
      matched.append({
        "id": document_ids[i],
        "name": name,
        "score": score
      })
    matched = sorted(matched,
    key = lambda x: x["score"], reverse = True)[:top_k]
    return matched

  def get_search_results(self, query = "", top_k=5):
    """
    Given the query, search all related documents

    Args:
      request_body:
        query: search query
        top_k: number of candidates to be returned
    Returns:
      response_list: List[dict] - List of top_k alignmed documents
      for a given level
    """
    if query:
      query = self.prepare_text_for_embedding(query)
    else:
      raise ValidationError("Query should be present to search")
    index_exists, _ = self.check_index_exist(self.level, True)
    Logger.info(f"INDEX EXIST FOR SEARCH at {self.level} : {index_exists}")
    if not index_exists:
      raise Exception("Index not found for {0}. Please use {1} to create "
        "index.".format(self.level, "skill-service/api/v1/skill/embeddings"))
    result = self.align_query(query, top_k)
    return result

def batch_populate_skill_embeddings(request_body):
  """Starts a batch job to populate Embedding for
    Semantic Search
  Args:
    request_body: dict - containing:
      level: List[str] - skill graph level
        for which embedding has to be created
      source_name: List[str] - skill source name
        for which embedding has to be created
  Returns:
    None"""
  try:
    Logger.info(f"Populating embeddings from: {request_body}")
    level = request_body.get("level")
    source_name = request_body.get("source_name", None)
    search_obj = SearchSkillGraph(level, source_name)
    search_obj.populate_level_embeddings_in_db()
  except Exception as e:
    raise Exception(f"Failed to populate embeddings. Error: {e}")


class KnowledgeGraph(Embedding):
  """Class for creating embeddings of any level(s) in Knowledge Graph"""

  BI_ENCODER_MODEL_NAME = BI_ENCODER_MODELS["SEARCH"]
  CROSS_ENCODER_MODEL_NAME = CROSS_ENCODER_MODELS["SEARCH"]
  BI_ENCODER_TOP_K = 15

  def __init__(self, level) -> None:
    super().__init__(
      self.BI_ENCODER_MODEL_NAME, self.CROSS_ENCODER_MODEL_NAME)
    self.level = level
    self.DB_INDEX = level
    self.index_description = f"Embeddings for {self.level}"

  def prepare_text_for_embedding(self, name=None, description=None):
    """Prepares text for embedding. If Both name and
    description are present. They are combined.

    Args:
      name str: name value
      description str: Description text

    Returns str : Combined text if both name and
      description are present
      """
    if name and description:
      text = name + ". " + description
    elif name:
      text = name
    elif description:
      text = description
    else:
      raise Exception("For embedding input alteast one out of "
      "name and description should be present.")
    return text

  def prepare_and_save_embeddings(self, documents):
    """Prepares input text from given documents and save the
      embeddings

      Args:
        documents: list(FireoModels)
    """
    texts = []
    doc_ids = []
    Logger.info("Len of documents: {}".format(len(documents)))
    for doc in documents:
      if self.level in ["learning_units", "e2e_test_LU"]:
        texts.append(self.prepare_text_for_embedding(doc.title))
      else:
        texts.append(self.prepare_text_for_embedding(
            doc.title, doc.description))
      doc_ids.append(doc.id)
    Logger.info("Len texts: {}".format(len(texts)))
    Logger.info("Len ids: {}".format(len(doc_ids)))
    gcs_path = self.export_embedding_csv(
            texts, doc_ids, self.level , self.level)
    self.populate_embedding_db(
          gcs_path, self.level, self.index_description, object_type="knowledge")

  def populate_level_embeddings_in_db(self):
    """Populates Embedding database index for a given level
    in Knowledge Graph
    """
    level_obj = self.get_level_obj()
    documents = level_obj.fetch_all_documents()
    if not documents:
      Logger.info("No docs found for {}".format(self.level))
      return
    else:
      Logger.info("No of {} : {} ".format(self.level, len(documents)))

    self.prepare_and_save_embeddings(documents)

  def get_level_obj(self):
    """Return Fireo Class for particular level

    Args: None
    Returns: Fireo Class
    """
    if self.level == "concepts":
      level_obj = Concept
    elif self.level == "sub_concepts":
      level_obj = SubConcept
    elif self.level == "learning_objectives":
      level_obj = KnowledgeServiceLearningObjective
    elif self.level in ["learning_units", "test_LU", "e2e_test_LU"]:
      level_obj = KnowledgeServiceLearningUnit
    elif self.level == "learning_resources":
      level_obj = KnowledgeServiceLearningContent
    else:
      raise Exception("Level not defined in Knowledge Graph")
    return level_obj


def batch_populate_kg_embeddings(request_body):
  """Starts a batch job to populate Embedding for given levels of
    Knowledge Graph
  Args:
    request_body: dict - containing:
      level: List[str] - Knowledge graph level
          for which embedding has to be created
  Returns:
    None"""
  try:
    level = request_body.get("level")
    Logger.info(f"Populating embeddings for: {level}")
    search_obj = KnowledgeGraph(level)
    search_obj.populate_level_embeddings_in_db()
  except Exception as e:
    raise Exception(f"Failed to populate embeddings. Error: {e}")
