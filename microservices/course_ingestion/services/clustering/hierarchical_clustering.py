"""hierarchical clustering"""
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer
import numpy as np
import requests
from umap import UMAP
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import json
from config import SERVICES, TITLE_SIMILARITY_CER_THRESHOLD, TITLE_GENERATION_BATCH_SIZE
import tornado.ioloop
from string import punctuation
from tornado.gen import multi
from transformers import T5Tokenizer
from textacy.extract import keyterms
from services.triple_inference import TripleService
import spacy
import editdistance
nlp = spacy.load("en_core_web_sm")
triple_service = TripleService()

tokenizer = T5Tokenizer.from_pretrained("t5-base")

#pylint: disable=consider-using-with,broad-exception-raised
title_generation_executor = ThreadPoolExecutor(max_workers=1)
summarization_executor = ThreadPoolExecutor(max_workers=8)

hierarchical_clustering = AgglomerativeClustering(
    affinity="cosine", linkage="complete")
umap_model = UMAP(random_state=42,
    n_neighbors=5,
    n_components=20,
    min_dist=0.0,
    metric="cosine",
    verbose=False)
sentence_model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")


def is_nan(num):
  """Check if num is empty."""
  return num == ""

def cer(original, result):
  r"""The CER is defined as the editing/Levenshtein distance.

      character level Levenshtein distance divided by the amount of
      characters in the original text.
      In case of the original having more charactes (N) than the result
      and both being totally different (all N characters resulting in 1
      edit operation each), the CER will always be 1 (N / N = 1).
      """
  # The WER ist calculated on word (and NOT on character) level.
  # Therefore we split the strings into words first:
  if is_nan(result):
    result = ""
  original = list(original)
  result = list(result)
  return editdistance.eval(original, result) / float(len(original))

def get_blooms_titles(texts, max_title_length, n_titles=1):
  try:
    prediction = json.loads(
        requests.post(
            url="http://{}:{}/title-generation/api/v1/blooms-title-generation"
            .format(
                SERVICES["title-generation"]["host"],
                # "0.0.0.0",
                SERVICES["title-generation"]["port"],
            ),
            json={
                "texts": texts,
                "max_title_length": max_title_length,
                "n_titles": n_titles
            },
        ).content)["data"]
    preds = prediction["titles"]
    return preds
  except ConnectionError as e:
    raise Exception("Failed to connect with title \
       generation microservice") from e
  except (TypeError, KeyError) as e:
    raise Exception("Internal server error") from e


def get_titles(texts, max_title_length, n_titles=1):
  try:
    prediction = json.loads(
        requests.post(
            url="http://{}:{}/title-generation/api/v1/title-generation".format(
                SERVICES["title-generation"]["host"],
                # "0.0.0.0",
                SERVICES["title-generation"]["port"],
            ),
            json={
                "texts": texts,
                "max_title_length": max_title_length,
                "n_titles": n_titles
            },
        ).content)["data"]
    preds = prediction["titles"]
    return preds
  except ConnectionError as e:
    raise Exception("failed to connect with \
      title generation microservice") from e
  except (TypeError, KeyError) as e:
    raise Exception("Internal server error") from e


def get_summary(text, ratio=0.3):
  try:
    prediction = json.loads(
        requests.post(
            url="http://{}:{}/extractive-summarization/api/v1/summarize"
            .format(
                SERVICES["extractive-summarization"]["host"],
                # "0.0.0.0",
                SERVICES["extractive-summarization"]["port"],
            ),
            json={
                "data": text,
                "ratio": ratio
            },
        ).content)["data"]
    return prediction["summary"]
  except ConnectionError as e:
    raise Exception("failed to connect with extractive \
      summarization microservice") from e
  except (TypeError, KeyError) as e:
    raise Exception("Internal server error") from e


def join_texts(texts):
  if texts:
    joined_text = texts[0].strip()
    for text in texts[1:]:
      if (len(joined_text) > 0) and (joined_text[-1] not in punctuation):
        joined_text = joined_text + ". " + text
      else:
        joined_text = joined_text + " " + text
  else:
    joined_text = ""
  return joined_text


async def compress_text_for_title_generation(texts):
  tokens_count = [len(tokenizer.tokenize(text)) for text in texts]
  total_tokens = sum(tokens_count)
  text = ""
  if total_tokens > 0:
    sentence_ratios = [(512 / total_tokens) * (n_token / total_tokens)
                       for n_token in tokens_count]
    if total_tokens > 512:
      summarised_docs = await multi([
          tornado.ioloop.IOLoop.current().run_in_executor(
              summarization_executor, get_summary, text, ratio)
          for text, ratio in zip(texts, sentence_ratios)
      ])
      text = join_texts(summarised_docs)
    else:
      text = join_texts(texts)
  return text


def get_batches(iterable, n=1):
  batches = []
  l = len(iterable)
  for ndx in range(0, l, n):
    batches.append(iterable[ndx:min(ndx + n, l)])
  return batches


async def get_all_titles(combined_text_list,
                         max_title_length,
                         batch_size=32,
                         blooms_title=False,
                         n_titles=5):
  #combined_text_list = [item for sublist in texts_list for item in sublist]
  if blooms_title:
    all_titles = await multi([
        tornado.ioloop.IOLoop.current().run_in_executor(
            title_generation_executor, get_blooms_titles, batch,
            max_title_length, n_titles)
        for batch in get_batches(combined_text_list, batch_size)
    ])
  else:
    all_titles = await multi([
        tornado.ioloop.IOLoop.current().run_in_executor(
            title_generation_executor, get_titles, batch,
            max_title_length, n_titles)
        for batch in get_batches(combined_text_list, batch_size)
    ])
  all_titles = [item for sublist in all_titles for item in sublist]
  return all_titles


def update_titles(topic_tree, titles_dict, level, next_indices):
  try:
    if level == "course":
      for competency, title in zip(topic_tree, titles_dict["competency"][0]):
        competency["title"] = title
      for i, competency in enumerate(topic_tree):
        new_node = update_titles(competency["sub_competencies"], titles_dict,
                                 "competency", next_indices)
        topic_tree[i]["sub_competencies"] = new_node
        next_indices["comp_ind"] += 1
    elif level == "competency":
      for sub_competency, title in zip(
          topic_tree, titles_dict["sub_competency"][next_indices["comp_ind"]]):
        sub_competency["title"] = title
      for i, sub_comp in enumerate(topic_tree):
        new_node = update_titles(sub_comp["learning_objectives"], titles_dict,
                                 "sub_competency", next_indices)
        topic_tree[i]["learning_objectives"] = new_node
        next_indices["subcomp_ind"] += 1
    elif level == "sub_competency":
      for learning_objective, title in zip(
          topic_tree,
          titles_dict["learning_objective"][next_indices["subcomp_ind"]]):
        learning_objective["title"] = title
    elif level == "learning_objective":
      for learning_unit, title in zip(
          topic_tree, titles_dict["learning_unit"][next_indices["lo_ind"]]):
        learning_unit["title"] = title
    else:
      raise Exception("Undefined topic tree level - {}".format(level))
    return topic_tree
  except (KeyError, IndexError) as e:
    raise Exception("Internal server Error") from e


def get_optimum_clusters(model, data, level):
  sil_score_max = -1
  level_map = {
      "competency": 20,
      "sub_competency": 10,
      "learning_objective": 3,
      "learning_unit": 1
  }
  possible_cluster_count = len(data) // level_map[level]
  if possible_cluster_count < 2:
    return [0 for i in range(len(data))]
  elif possible_cluster_count == 2:
    model.n_clusters = 2
    labels = model.fit_predict(data)
    return labels
  else:
    for n_clusters in range(2, possible_cluster_count):
      model.n_clusters = n_clusters
      labels = model.fit_predict(data)
      sil_score = silhouette_score(data, labels)
      if sil_score > sil_score_max:
        sil_score_max = sil_score
        best_n_clusters = n_clusters
    model.n_clusters = best_n_clusters
    clusters = model.fit_predict(data)
    return clusters


def get_recursive_tree(clustering_model, embeddings, node_level, documents,
                       doc_ids, text_list, create_learning_units,
                       create_triples):
  if node_level == "course":
    clusters = get_optimum_clusters(
        clustering_model, embeddings[doc_ids], level="competency")
    comps = []
    for comp_cluster in set(clusters):
      comp = {}
      comp["competency"] = comp_cluster
      comp["document_ids"] = [
          doc_id for doc_id, cluster_id in zip(doc_ids, clusters)
          if cluster_id == comp_cluster
      ]
      comp["text"] = join_texts([documents[i] for i in comp["document_ids"]])
      comp["title"] = len(text_list)
      text_list.append({
          "docs": [documents[i] for i in comp["document_ids"]],
          "blooms_title": False
      })
      comp["sub_competencies"], text_list = get_recursive_tree(
          clustering_model, embeddings, "competency", documents,
          comp["document_ids"], text_list, create_learning_units,
          create_triples)
      comps.append(comp)
    return comps, text_list
  elif node_level == "competency":
    clusters = get_optimum_clusters(
        clustering_model, embeddings[doc_ids], level="sub_competency")
    scs = []
    for sc_cluster in set(clusters):
      sc = {}
      sc["sub_competency"] = sc_cluster
      sc["document_ids"] = [
          doc_id for doc_id, cluster_id in zip(doc_ids, clusters)
          if cluster_id == sc_cluster
      ]
      sc["text"] = join_texts([documents[i] for i in sc["document_ids"]])
      sc["title"] = len(text_list)
      text_list.append({
          "docs": [documents[i] for i in sc["document_ids"]],
          "blooms_title": False
      })
      sc["learning_objectives"], text_list = get_recursive_tree(
          clustering_model, embeddings, "sub_competency", documents,
          sc["document_ids"], text_list, create_learning_units,
          create_triples)
      scs.append(sc)
    return scs, text_list
  elif node_level == "sub_competency":
    clusters = get_optimum_clusters(
        clustering_model, embeddings[doc_ids], level="learning_objective")
    los = []
    for lo_cluster in set(clusters):
      lo = {}
      lo["learning_objective"] = lo_cluster
      lo["document_ids"] = [
          doc_id for doc_id, cluster_id in zip(doc_ids, clusters)
          if cluster_id == lo_cluster
      ]
      lo["text"] = "<p>".join([documents[i] for i in lo["document_ids"]])
      lo["title"] = len(text_list)
      text_list.append({
          "docs": [documents[i] for i in lo["document_ids"]],
          "blooms_title": True
      })
      if create_learning_units:
        lo["learning_units"], text_list = get_recursive_tree(
            clustering_model, embeddings, "learning_objective", documents,
            lo["document_ids"], text_list, False, create_triples)
      los.append(lo)
    return los, text_list
  elif node_level == "learning_objective":
    clusters = get_optimum_clusters(
        clustering_model, embeddings[doc_ids], level="learning_unit")
    lus = []
    for lu_cluster in set(clusters):
      lu = {}
      lu["learning_unit"] = lu_cluster
      lu["document_ids"] = [
          doc_id for doc_id, cluster_id in zip(doc_ids, clusters)
          if cluster_id == lu_cluster
      ]
      lu["text"] = "<p>".join([documents[i] for i in lu["document_ids"]])
      lu["topics"] = get_topics(lu["text"].replace("<p>", " "))
      lu["title"] = len(text_list)
      text_list.append({
          "docs": [documents[i] for i in lu["document_ids"]],
          "blooms_title": True
      })
      if create_triples:
        lu["triples"], text_list = get_recursive_tree(
            clustering_model, embeddings, "learning_unit", documents,
            lu["document_ids"], text_list, False, create_triples)
      lus.append(lu)
    return lus, text_list
  elif node_level == "learning_unit":
    triples = []
    lu_text_list = [" ".join([documents[i] for i in doc_ids])]
    triples = triple_service.generate_triples(lu_text_list)[0]
    return triples, text_list


# pylint: disable=broad-except
async def create_recursive_topic_tree(documents,
                                      node_level="course",
                                      titles_flag=True,
                                      create_learning_units=True,
                                      create_triples=True):
  embeddings = np.array(
      sentence_model.encode(documents, show_progress_bar=True))
  try:
    reduced_embeddings = umap_model.fit_transform(embeddings)
  except Exception:
    try:
      umap_model_modified = UMAP(random_state=42,
          n_neighbors=2, n_components=10, min_dist=0.0, metric="cosine")
      reduced_embeddings = umap_model_modified.fit_transform(embeddings)
    except Exception:
      reduced_embeddings = embeddings
  topic_tree, text_list = get_recursive_tree(
      hierarchical_clustering,
      reduced_embeddings,
      node_level,
      documents,
      range(len(documents)),
      text_list=[],
      create_learning_units=create_learning_units,
      create_triples=create_triples)
  if titles_flag:
    text_list_with_summaries = await get_summarized_texts(text_list)
    titles_list = await generate_titles(text_list_with_summaries, max_length=32)
    topic_tree = add_titles_to_tree(
        topic_tree, titles_list, node_level=node_level,
        create_learning_units=create_learning_units)
    topic_tree = check_for_duplicate_titles(
      topic_tree, node_level, create_learning_units)
  return topic_tree

def handle_duplicate_titles_sub_comp(sub_competency):
  """Check if duplicate titles exist inside a sub competency and
    if they exist add Part-{X} at the end"""
  learning_objectives = sub_competency["learning_objectives"]
  title_mapping = {}
  for lo_index, learning_objective in enumerate(learning_objectives):
    learning_units = learning_objective["learning_units"]
    for lu_index, learning_unit in enumerate(learning_units):
      lu_title = learning_unit["title"]
      if lu_title in title_mapping:
        prev_lo_index, prev_lu_index, count = title_mapping[lu_title]
        if count > 1:
          title_mapping[lu_title][-1] += 1
          learning_unit["title"] = lu_title + " Part-" + str(count+1)
        else:
          title_mapping[lu_title][-1] += 1
          learning_objectives[prev_lo_index]["learning_units"]\
            [prev_lu_index]["title"] += " Part-" + str(count)
          learning_unit["title"] += " Part-" + str(count+1)
      else:
        title_mapping[lu_title] = [lo_index, lu_index, 1]
  return sub_competency

def check_for_duplicate_titles(topic_tree, node_level,
    create_learning_units, is_list=True):
  """Merges the nodes at particular level with same title"""
  if node_level == "course":
    updated_topic_tree = []
    for competency in topic_tree:
      competency = check_for_duplicate_titles(
        competency, "competency", create_learning_units,
        is_list=False)
      updated_topic_tree.append(competency)
    return updated_topic_tree
  elif node_level == "competency":
    updated_topic_tree = []
    if is_list:
      sub_competencies = topic_tree
    else:
      sub_competencies = topic_tree["sub_competencies"]
    for sub_competency in sub_competencies:
      sub_competency = check_for_duplicate_titles(
        sub_competency, "sub_competency", create_learning_units,
        is_list=False)
      sub_competency = handle_duplicate_titles_sub_comp(sub_competency)
      updated_topic_tree.append(sub_competency)
    if is_list:
      return updated_topic_tree
    else:
      topic_tree["sub_competencies"] = updated_topic_tree
      return topic_tree
  elif node_level == "sub_competency":
    updated_topic_tree = []
    titles_dict = {}
    if is_list:
      learning_objectives = topic_tree
    else:
      learning_objectives = topic_tree["learning_objectives"]
    for i, learning_objective in enumerate(learning_objectives):
      title = learning_objective["title"]
      if title not in titles_dict:
        titles_dict[title] = i
      else:
        prev_index = titles_dict[title]
        prev_lo = learning_objectives[prev_index]
        prev_lo["document_ids"].extend(
          learning_objective["document_ids"])
        prev_lo["text"] = "<p>".join([
          prev_lo["text"], learning_objective["text"]])
        if "learning_units" in prev_lo:
          prev_lo["learning_units"].extend(
            learning_objective["learning_units"]
          )
    for _, value in titles_dict.items():
      updated_topic_tree.append(learning_objectives[value])
    final_tree = []
    if create_learning_units:
      for learning_objective in updated_topic_tree:
        learning_objective = check_for_duplicate_titles(
          learning_objective, "learning_objective",
          create_learning_units, is_list=False)
        final_tree.append(learning_objective)
        updated_topic_tree = final_tree

    if is_list:
      return updated_topic_tree
    else:
      topic_tree["learning_objectives"] = updated_topic_tree
      return topic_tree

  elif node_level == "learning_objective":
    updated_topic_tree = []
    titles_dict = {}
    if is_list:
      learning_units = topic_tree
    else:
      learning_units = topic_tree["learning_units"]
    for i, learning_unit in enumerate(learning_units):
      title = learning_unit["title"]
      if title not in titles_dict:
        titles_dict[title] = i
      else:
        prev_index = titles_dict[title]
        prev_lu = learning_units[prev_index]
        prev_lu["document_ids"].extend(
          learning_unit["document_ids"])
        prev_lu["text"] = "<p>".join([prev_lu["text"], learning_unit["text"]])
        if "triples" in prev_lu:
          prev_lu["triples"].extend(
            learning_unit["triples"]
          )
    for _, value in titles_dict.items():
      updated_topic_tree.append(learning_units[value])
    if is_list:
      return updated_topic_tree
    else:
      topic_tree["learning_units"] = updated_topic_tree
      return topic_tree


#pylint: disable=consider-using-set-comprehension
def get_topics(text):
  all_entities = keyterms.textrank(
      nlp(text),
      position_bias=False,
      topn=10,
      window_size=3,
      include_pos=("NOUN", "ADJ"))
  all_entities = [{
      "entity": ent[0],
      "salience": round(ent[1], 3)
  } for ent in all_entities]
  return all_entities


async def get_summarized_texts(text_list):
  for i in text_list:
    i["summarised_text"] = await compress_text_for_title_generation(i["docs"])
  return text_list


async def generate_titles(text_list_with_summaries, max_length):
  blooms_indices = []
  non_blooms_indices = []
  for i in range(len(text_list_with_summaries)):
    if text_list_with_summaries[i]["blooms_title"]:
      blooms_indices.append(i)
    else:
      non_blooms_indices.append(i)
  blooms_text_list = [
      i["summarised_text"]
      for i in [text_list_with_summaries[j] for j in blooms_indices]
  ]
  non_blooms_text_list = [
      i["summarised_text"]
      for i in [text_list_with_summaries[j] for j in non_blooms_indices]
  ]
  blooms_titles = await get_all_titles(
      blooms_text_list,
      max_title_length=max_length,
      batch_size=TITLE_GENERATION_BATCH_SIZE,
      blooms_title=True,
      n_titles=5)
  non_blooms_titles = await get_all_titles(
      non_blooms_text_list,
      max_title_length=max_length,
      batch_size=TITLE_GENERATION_BATCH_SIZE,
      blooms_title=False,
      n_titles=5)
  for i, j in zip(blooms_indices, blooms_titles):
    text_list_with_summaries[i]["title"] = j
  for i, j in zip(non_blooms_indices, non_blooms_titles):
    text_list_with_summaries[i]["title"] = j
  return [i["title"] for i in text_list_with_summaries]

def get_filtered_title(parent_title, candidate_titles):
  if parent_title:
    cers = [cer(parent_title, candidate_title) \
      for candidate_title in candidate_titles]
    for i, cer_value in enumerate(cers):
      if cer_value > TITLE_SIMILARITY_CER_THRESHOLD:
        return candidate_titles[i]
    return candidate_titles[np.argmax(cers)]
  else:
    return candidate_titles[0]

def add_titles_to_tree(topic_tree, titles_list, parent_title = None,
  node_level="course", create_learning_units=True):
  if node_level == "course":
    for i in topic_tree:
      i["title"] = titles_list[i["title"]][0]
      i["sub_competencies"] = add_titles_to_tree(
          i["sub_competencies"], titles_list, parent_title = i["title"],
          node_level="competency", create_learning_units=create_learning_units)
    return topic_tree
  elif node_level == "competency":
    for i in topic_tree:
      i["title"] = get_filtered_title(parent_title, titles_list[i["title"]])
      i["learning_objectives"] = add_titles_to_tree(
          i["learning_objectives"], titles_list, node_level="sub_competency",
          create_learning_units=create_learning_units)
    return topic_tree
  elif node_level == "sub_competency":
    for i in topic_tree:
      i["title"] = titles_list[i["title"]][0]
      if create_learning_units:
        i["learning_units"] = add_titles_to_tree(
            i["learning_units"], titles_list, parent_title = i["title"],
            node_level="learning_objective")
    return topic_tree
  elif node_level == "learning_objective":
    for i in topic_tree:
      i["title"] = get_filtered_title(parent_title, titles_list[i["title"]])
    return topic_tree
