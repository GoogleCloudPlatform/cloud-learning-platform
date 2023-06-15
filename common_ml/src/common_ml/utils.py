""""Module containing utility functions that are common in many microservices"""
import re
import json
import nltk
import requests
import numpy as np
import spacy
import editdistance
from keybert import KeyBERT
import inflect
import logging
from nltk.corpus import stopwords, wordnet
from retrying import retry
from sentence_transformers import SentenceTransformer, util
from sklearn.linear_model import LogisticRegression
from common_ml.lexrank import degree_centrality_scores
from common_ml.config import (SERVICES, LONG_SENT_THRESHOLD, SPLIT_THRESHOLD,
                              FEEDBACK_FACT_KEYBERT_THRESHOLD, RETRY_EXCEPTIONS,
                              SPACY_MODEL_TYPES)
from common.models import LearningUnit
#pylint: disable=len-as-condition,bare-except,unnecessary-list-index-lookup,unrecognized-option

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

MODEL_SENTENCE_RANK = None
MODEL_ENTITY_RANK = None
MODEL_STS = None
INFLECT_ENGINE = None
SPACY_MODELS = {}


def retry_on_exception(exception):
  """Function to retry requests on Connection Errors"""
  return isinstance(exception, RETRY_EXCEPTIONS)

def parse_response(response):
  """Function to parse status code and response"""
  return response.status_code, json.loads(response.content)

def check_status_code(status_code):
  """Function to check if ConnectionError needs to be raised
  based on status code"""
  if status_code !=500 and 400<= status_code <= 511:
    raise ConnectionError

def load_utils_models(
    spacy_models=False,
    model_sentence_rank=False,
    model_entity_rank=False,
    model_sts=False,
    inflect_engine=False):
  """Loads Models as per the configurations"""

  global MODEL_ENTITY_RANK
  global MODEL_STS
  global MODEL_SENTENCE_RANK
  global INFLECT_ENGINE
  global SPACY_MODELS

  if spacy_models:
    for model_type, model_name in SPACY_MODEL_TYPES.items():
      try:
        SPACY_MODELS[model_type] = spacy.load(model_name)
      except:
        SPACY_MODELS[model_type] = spacy.load("en_core_web_sm")

  if model_entity_rank:
    MODEL_ENTITY_RANK = KeyBERT("distilbert-base-nli-stsb-mean-tokens")

  if model_sts:
    MODEL_STS = SentenceTransformer(
        "distilbert-base-nli-stsb-mean-tokens", device="cpu")

  if model_sentence_rank:
    MODEL_SENTENCE_RANK = SentenceTransformer(
        "paraphrase-distilroberta-base-v1", device="cpu")

  if inflect_engine:
    INFLECT_ENGINE = inflect.engine()
    INFLECT_ENGINE.classical(all=True)

  return (SPACY_MODELS, MODEL_SENTENCE_RANK, MODEL_ENTITY_RANK, MODEL_STS,
          INFLECT_ENGINE)


SENTENCE_RANK_THRESH = 0.8
ENTITY_RANK_THRESH = 0.12
valid_named_entity_pos = ["NOUN", "PROPN"]

quantitative_adjectives = [
    "Much", "Little", "No", "None", "Some", "Any", "Enough", "Sufficient",
    "Whole", "Half", "Few", "Most", "All", "A little", "A little bit", "A lot"
    "Abundant", "Couple", "Double", "Each", "Either", "Empty", "Enough",
    "Enough of", "Every", "Few", "Full", "Great", "Half", "Heavily", "Heavy",
    "Huge", "Hundred", "Hundreds", "Insufficient", "Light", "Little", "Lots of",
    "Many", "Most", "More", "Neither", "No", "Numerous", "Plenty of", "Several",
    "Significant", "Single", "So few", "Some", "Sparse", "Substantial",
    "Sufficient", "Too", "Whole", "Other", "Another"
]
quantitative_adjectives = [word.lower() for word in quantitative_adjectives] +\
 quantitative_adjectives

conjunctive_adverb_words = [
    "Accordingly", "Furthermore", "Moreover", "Similarly", "Also", "Hence",
    "Namely", "Still", "Anyway", "However", "Nevertheless", "Then", "Besides",
    "Incidentally", "Next", "Thereafter", "Certainly", "Indeed", "Nonetheless",
    "Therefore", "Consequently", "Instead", "Now", "Thus", "Finally", "But",
    "Likewise", "Otherwise", "Undoubtedly", "Further", "Meanwhile",
    "In other words", "Since"
]
conjunctive_adverb_words = conjunctive_adverb_words + \
                            [word.lower() for word in conjunctive_adverb_words]

question_words = ["who", "what", "where", "why", "when", "how", "which", "whom"]

demonstrative_words = ["this", "these", "those"]

context_lacking_words = ["next", "let", "find", "let's", "their", "such"]

low_context_objects = [
    "Image", "Slideshow", "Slide", "Text", "Page", "Section", "Question",
    "Table", "Picture", "Module", "Figure", "Diagram", "Illustration",
    "Paragraph", "Chapter", "Course", "Appendix", "Evidence", "Example"
]
low_context_objects = low_context_objects + \
                            [word.lower() for word in low_context_objects]

low_context_prepositions = ["next", "below", "following", "above"]

low_context_phrases = []
for preposition in low_context_prepositions:
  for objects in low_context_objects:
    low_context_phrase = preposition + " " + objects
    low_context_phrases.append(low_context_phrase)

introductory_phrases = [
    "For example", "For instance", "In contrast", "For e.g."
]

introductory_prepositional_phrases = [
    "let us", "for e.g.", "let's say", "suppose that", "as an example",
    "let's assume", "consider the example", "example being",
    "consider an example", "click to view", "click on", "click the"
] + [phrase.lower() for phrase in introductory_phrases]


def check_pronoun(sent, spacy_model_type="default"):
  """Checks if pronoun exists in sentence after doing coreference resolution on
    given sentence

      args:
        sent: (str) - sentence in which pronoun is checked
      returns:
        bool: True  - if pronoun exists in sentence
              False - if not
  """
  resolved_text = get_coref_text(
    sent, resolve_all_mentions=True, spacy_model_type=spacy_model_type)
  doc_resolved = SPACY_MODELS[spacy_model_type](resolved_text)
  if len([
      tok.text
      for tok in doc_resolved
      if (tok.pos_ == "PRON" and tok.text.lower() not in (
          ["it", "we", "us", "you"] + question_words))
  ]):
    return True
  return False


def check_valid_words(words, spacy_model_type="default"):
  """
        This function checks if given words exist in Wordnet corpus
        Args:
            words: String
        Returns:
            True / False
  """
  word_checklist = []
  for word in word_split(words, spacy_model_type):
    if wordnet.synsets(word):
      word_checklist.append(word)
  test = (word_checklist == word_split(words, spacy_model_type))
  return bool(test)


def lemma_ent(ent, spacy_model_type="default"):
  """Function to get tokenized list of lemmas for given entity
  after removing stop words
  Args:
    ent: string
  Returns:
    lemma_list: list of lemma entities in the input entity
  """
  lemma_list = []
  ans_lemma = ""
  for word in word_split(ent, spacy_model_type):
    word = word.lower()
    if word not in stopwords.words() and word.isalpha():
      doc = SPACY_MODELS[spacy_model_type](word)
      ans_lemma = doc[0].lemma_
      lemma_list.append(ans_lemma)
  return lemma_list


def sentence_selection(lu_sentences, sent_len_thresh=5,
spacy_model_type="default"):
  """Function to select good sentences to create questions out of them
  Args:
    lu_sentences: list of sentences
    [<text1>,<text2>]
  Returns:
    list of good sentences
    [<text1>]
  """
  try:
    # Remove sentences that are absolute questions:
    non_question_sents = [
      sent for sent in lu_sentences if not (
      (word_split(sent, spacy_model_type)[0].lower() in question_words and \
      SPACY_MODELS[spacy_model_type](sent)[1].pos_ in ["VERB", "ADP"]) or \
      (word_split(sent, spacy_model_type)[-1] == "?"))
    ]
    # Remove sentences starting with Bloom's taxonomy verbs:
    sentences = [
        sents for sents in non_question_sents
        if SPACY_MODELS[spacy_model_type](sents)[0].tag_  != "VB"
        ]
    # Remove sentences having refererence to objects which are not present:
    # eg: "below image" or "following table" or "next diagram"
    sentences = [
        sents for sents in sentences
        if not any(phrase in sents.lower() for phrase in low_context_phrases)
    ]

    # Remove sentences having refererence to objects which are not present:
    # eg: "Image 2" or "Table 3a" or "Slideshow 1"
    valid_sentences = []
    for sent in sentences:
      doc = SPACY_MODELS[spacy_model_type](sent)
      discard_sent = False
      for i, tok in enumerate(doc):
        if tok.text.lower() in low_context_objects and i < (len(doc) - 1):
          if doc[i + 1].pos_ == "NUM" or doc[i + 1].text == ":":
            discard_sent = True
            break
      if not discard_sent:
        valid_sentences.append(sent)

    # Remove sentences with phrases like "provided above/below":
    filtered_sentences = []
    for sentence in valid_sentences:
      if any(word in sentence.lower() for word in ["above", "below"]):
        doc = SPACY_MODELS[spacy_model_type](sentence)
        for token in doc:
          if token.text in ["above", "below"]:
            word_position = token.i
            if doc[word_position - 1].tag_ not in ["VBD", "VBN"]:
              filtered_sentences.append(sentence)
      else:
        filtered_sentences.append(sentence)
    # Modify sentences to improve quality:
    transformed_sentences = sentence_transformations(
      filtered_sentences, spacy_model_type)

    # Remove sentences having introductory prepositional phrases:
    sentences = [
        sents for sents in transformed_sentences
        if not any(phrase in sents.lower() for phrase in \
          introductory_prepositional_phrases)
        ]
    # Remove shorter sentences:
    sentences =[
        sents for sents in sentences
        if len([word for word in word_split(
          sents, spacy_model_type) if word not in \
        stopwords.words()]) > sent_len_thresh
    ]
    # Remove sentences begining with words that lack context:
    sentences = [
        sent for sent in sentences
        if word_split(
          sent, spacy_model_type)[0].lower() not in context_lacking_words
    ]
    # Removing sentences with specific Pronouns after Coref Resolution:
    sentences = [sent for sent in sentences if not check_pronoun(
      sent, spacy_model_type)]
    # Remove sentences having demostrative words as they lack context:
    selected_sentences = []
    for sent in sentences:
      if len(nltk.sent_tokenize(sent)) > 1:
        selected_sentences.append(sent)
      else:
        if not list(set(demonstrative_words) & \
                   set(word_split(sent.lower(), spacy_model_type))):
          selected_sentences.append(sent)
    # Remove sentences having URL links:
    sentences = [
        sent for sent in selected_sentences if not len(
            re.findall(
                r"(\S*@\S*\s?)|(https\S+|\(https\S+\))|"
                r"(http\S+|\(http\S+\))|(\(www\S+\))", sent))
    ]
    # Remove sentences where phrases like "Chapter 2" or "Example:" exist.
    # Also remove sentences begining with low context words:
    valid_sentences = []
    for sentence in sentences:
      discard_sent = False
      doc = SPACY_MODELS[spacy_model_type](sentence)
      if doc[0].text.lower() in low_context_objects + ["that"]:
        discard_sent = True
      else:
        for token in doc:
          if token.text in low_context_objects and token.i < (len(doc) - 1):
            if doc[token.i + 1].pos_ == "NUM" or doc[token.i + 1].text == ":":
              discard_sent = True
              break
      if not discard_sent:
        valid_sentences.append(sentence)
    # Return the 1st 2 sentences from LU even if no good sentences exist:
    if len(valid_sentences) < 2:
      valid_sentences = non_question_sents[:(2 - len(valid_sentences))] + \
                                                              valid_sentences
    # Remove duplicate sentences without changing order of sentences:
    sentences = list(dict.fromkeys(valid_sentences))
    # Final step: captialise 1st letter of each sentence
    sentences = [sent[0].upper() + sent[1:] for sent in sentences]
  except IndexError as e:
    logging.error("No sentences selected: %s", e)
  return sentences


def sentence_transformations(sentences, spacy_model_type="default"):
  """Function to get list of sentences modified to improve quality by
      stripping off conjunctive_adverb_words that exist in begining of sentence
      and replace the word "another" either with "a/an" or "one of the"
      whenever it is the first word of sentence
  Args:
    sentences: list of sentences

  Returns:
    list of modified sentences
  """
  # Strip conjunctive_adverb_words that exist in begining of sentence:
  sentences = [
      sent.strip(conjunctive_adverb_words[conjunctive_adverb_words.index(
          word_split(sent, spacy_model_type)[0])])
      if word_split(
        sent, spacy_model_type)[0] in conjunctive_adverb_words else sent
      for sent in sentences
  ]
  # Strip introductory phrases in beginning of sentence:
  transformed_sentences = []
  for sent in sentences:
    transformed_sentences.append(sent)
    for phrase in introductory_phrases:
      if phrase in sent:
        masked_sent = sent.replace(phrase, "MASKEDWORD")
        if SPACY_MODELS[spacy_model_type](masked_sent)[0].text == "MASKEDWORD":
          transformed_sent = masked_sent.replace("MASKEDWORD", "")
          transformed_sentences.append(transformed_sent)
  # When 1st word, replace "another"/"other" with either "a/an" when followed
  # by ADJ, or with "one of the" when followed by NOUN:
  valid_sentences = []
  for sent in transformed_sentences:
    if word_split(
      sent, spacy_model_type)[0].lower() in ["another", "other"] and \
      SPACY_MODELS[spacy_model_type](sent)[1].pos_ in ["NOUN", "ADJ"]:
      second_word = word_split(sent, spacy_model_type)[1]
      if SPACY_MODELS[spacy_model_type](sent)[1].pos_ == "ADJ":
        sent = INFLECT_ENGINE.an(sent.replace(
                                  word_split(
                                    sent, spacy_model_type)[0], "", 1).strip())
        valid_sentences.append(sent)
      elif SPACY_MODELS[spacy_model_type](
        sent)[1].pos_ == "NOUN" and SPACY_MODELS[spacy_model_type](
          sent)[2].pos_ == "NOUN":
        sent = INFLECT_ENGINE.an(sent.replace(
                                  word_split(
                                    sent, spacy_model_type)[0], "", 1).strip())
        valid_sentences.append(sent)
      elif SPACY_MODELS[spacy_model_type](sent)[1].pos_ == "NOUN":
        if INFLECT_ENGINE.singular_noun(second_word) is False:
          plural_noun = INFLECT_ENGINE.plural(second_word)
          if check_valid_words(plural_noun):
            sent = sent.replace(second_word, plural_noun, 1)
            sent = sent.replace(word_split(
              sent, spacy_model_type)[0], "One of the", 1)
            valid_sentences.append(sent)
          else:
            sent = INFLECT_ENGINE.an(
                sent.replace(word_split(
                  sent, spacy_model_type)[0], "", 1).strip())
            valid_sentences.append(sent)
        else:
          sent = sent.replace(
            word_split(sent, spacy_model_type)[0], "One of the", 1)
          valid_sentences.append(sent)
    else:
      valid_sentences.append(sent)
  # Remove redundant "," or whitespace present in sentences:
  sentences = [sent.strip(",").strip(" ") for sent in valid_sentences]
  return sentences


def bad_sentence_is_true(sentences):
  """Find if a list of sentence has atleast one bad sentence.
     Check if any sentence ends or starts with bad symbols

      args:
        sentences: (list) - input sentences to check if bad
      returns:
        bool: True  - if any sentence is bad
              False - if none of the sentences are bad
  """
  flag = False
  for sent in sentences:
    if sent[0] in ["—", "-", ")", "(", "\n", ",", "’"] or sent[-1]\
        in ["—", "-", ")", "(", "\n", ",", "’"] or\
            sent[0].isdigit() or sent[-1].isdigit():
      flag = True
      break
  return flag


def word_split(text, spacy_model_type="default"):
  """Splits a text into its constituent words and
  gives the output as a list of words
  Args:
    text: string
  Returns:
    list of words
    [<text1>, <text2>]
    """
  doc = SPACY_MODELS[spacy_model_type](text)
  return [tok.text for tok in doc]


def join_next_sentence(sentences, idx):
  """
  Function to join incorrectly splitted sentences with the next sentence.
  Args:
    sentences: List of sentences(str)
    idx: List of indexes that needs to be merged
  Returns:
    sentences: List of sentences(str)
  """
  for id_ in idx[::-1]:
    if id_ + 1 < len(sentences):
      final_sent = sentences[id_] + " " + sentences[id_ + 1]
      del sentences[id_ + 1]
      del sentences[id_]
      sentences.insert(id_, final_sent)
  return sentences

def join_previous_sentence(sentences, idx):
  """
  Function to join incorrectly splitted sentences with the previous sentence.
  Args:
    sentences: List of sentences(str)
    idx: List of indexes that needs to be merged
  Returns:
    sentences: List of sentences(str)
  """
  for id_ in idx[::-1]:
    if id_ != 0:
      final_sent = sentences[id_ - 1] + " " + sentences[id_]
      del sentences[id_]
      del sentences[id_ - 1]
      sentences.insert(id_ - 1, final_sent)
  return sentences

def check_unbalanced_brackets(sentence):
  """
  Function to check if the sentence has unbalanced paranthesis or not
  """
  open_tup = tuple("({[")
  close_tup = tuple(")}]")
  mapping = dict(zip(open_tup, close_tup))
  queue = []

  for i in sentence:
    if i in open_tup:
      queue.append(mapping[i])
    elif i in close_tup:
      if not queue or i != queue.pop():
        return True
  if not queue:
    return False
  else:
    return True


def sentence_split(text):
  """Splits a text into its constituent sentences and
  gives the output as a list of sentences
  Args:
    text: string
  Returns:
    list of sentences splitted into individual sentences
    [<text1>, <text2>]
    """
  sentences = nltk.sent_tokenize(text)
  idx = []
  skip = False
  special_chars = ["(", "[", "{", "<"]
  #code to identify if the last word of splitted sentence is an acronym
  for i, sent in enumerate(sentences):
    acronym = re.findall(r"(?:[A-Z]\.)+", sent)
    if skip:
      skip = False
      continue
    else:
      if len(acronym) > 0 and len(sent) > 2:
        for acr in acronym:  # checking if acronym is the last word
          index = sent.find(acr)
          if index + len(acr) == len(sent) and sent[index - 1] in [" ", "."]:
            idx.append(i)
            skip = True
      elif (sent.strip()[0] in special_chars) and len(sent) > 2:
        idx.append(i)
      elif  sent[0].islower() and i-1 > 0 and \
        sentences[i-1][-1].strip() not in [".", "?", "!"]:
        idx.append(i)
  # code to merge the bad splitted sentences

  sentences = join_previous_sentence(sentences, idx)
  # code to merge sentences that have points in them like 1. sen1 2. sen2
  # with the next sentence
  idx = []
  for i, sent in enumerate(sentences):
    if len(sent) > 1:
      if (sent[-2].isnumeric() and sent[-1] == ".") or \
          (sent[0].isnumeric() and sent[1] == "."):
        idx.append(i)

  sentences = join_next_sentence(sentences, idx)
  # code to merge sentences with points in them with the next sentence
  # Example: 1. This is first sentence. 2. This is second sentence.
  idx = []
  for i, sent in enumerate(sentences):
    if len(sent) > 1:
      if (sent[0].isnumeric() and sent[1] == ".") or \
          (sent[0].isnumeric() and sent[1] == "."):
        idx.append(i)

  sentences = join_previous_sentence(sentences, idx)

  # code to merge sentences starting with number, this is to handle very edge
  # cases. Example: Merging the following into a single sentence as it should be
  # original  sentence : With t(15;17), a fragment of chr. 17 that contains RARA
  # gene migrates to chr. 15 with following fusion of RARA and PML genes.

  # nltk.sent_tokenize tokenizes as shown below
  # sent1: With t(15;17), a fragment of chr.
  # sent2: 17 that contains RARA gene migrates to chr.
  # sent3: 15 with following fusion of RARA and PML genes.

  # With the below code line 462 - 473 the bad sentence split as show above will
  # be fixed.
  idx = []
  for i, sent in enumerate(sentences):
    if len(sent) > 1:
      if sent.strip()[0].isnumeric() or sent.strip()[0].islower():
        idx.append(i)

  sentences = join_previous_sentence(sentences, idx)

  # code to merge sentences with unbalanced paranthesis
  # Original sentence: Two out of four receptors seem contribute the most to
  # cancer development in humans ERBB1 (syn. : HER1) is activated by EGF ERBB2
  # (syn. : HER2 ).
  # Example:
  # sen1 : Two out of four receptors seem contribute the most to cancer
  # development in humans ERBB1 (syn.
  # sen2 : HER1) is activated by EGF ERBB2 (syn. : HER2 ).
  idx = []
  for i, sent in enumerate(sentences):
    if len(sent) > 1:
      if check_unbalanced_brackets(sent):
        idx.append(i)

  sentences = join_next_sentence(sentences, idx)

  return sentences


def get_ranked_sentences(model, sent_text):
  """Function to get ranked sentences from KeyBERT
  Args:
    model: KeyBERT model
    sent_text: text of type string
  Returns:
    A list of tuples in the format [(idx, sentence, sentence_score)]
  """
  sent_text = sentence_split(sent_text)
  embeddings = model.encode(sent_text, convert_to_tensor=True)
  cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
  cosine_scores = cosine_scores * 0.5 + 0.5
  cosine_scores[cosine_scores > 1.0] = 1.0
  cosine_scores[cosine_scores < 0.0] = 0.0
  centrality_scores = degree_centrality_scores(
      cosine_scores.cpu().numpy(), threshold=None)
  sorted_centrality_scores = np.sort(centrality_scores)[::-1]
  most_central_sentence_indices = np.argsort(-centrality_scores)
  sentence_scores = [(i, sent_text[i], sorted_centrality_scores[i])
                     for i in most_central_sentence_indices
                     if len(sent_text[i]) > 20]
  return sentence_scores


def softmax(x):
  """Compute softmax values for each sets of scores in x.
        args:
          x: (float)
      returns:
        (float): softmax calulated for given input
  """
  return np.exp(x) / np.sum(np.exp(x), axis=0)


def get_ranked_entities(entity_list,
                        lu_text,
                        pos_required=True,
                        model=MODEL_ENTITY_RANK):
  """Function to get ranked entites from text
  args:
    model: model to be used for entity ranking
    entity_list: (list) - of entities to be ranked
    lu_text: (str) - input string to provide context
  returns:
    entity_scores: (list) - of entities & thier scores with respect to
                            given context
  """
  if pos_required:
    answer = [ent[0] for ent in entity_list["answer"]]
    entity_scores = model.extract_keywords(lu_text, candidates=answer)
    entity_scores = [[ent, score, entity_list["answer"][answer.index(ent)][1]]
                     for ent, score in entity_scores if ent in answer]
  else:
    answer = entity_list
    entity_scores = model.extract_keywords(lu_text, candidates=answer)
    entity_scores = [[ent, score] for ent, score in entity_scores]

  return entity_scores


def convert_cluster_to_entity_list(filtered_cluster,
  tokenized_text_list, sentence_start_end, resolve_all_mentions = False):
  """
    Return a dictionary containing sentence-wise list of representative
    entity with their mentions.

  Args:
    filtered_clusters(list of list of indexes) -
                [[[0, 4], [18, 18], [56, 59], [78, 78]], [[22, 22]]]
                This example shows the start position, end position of the
                entity mention
    tokenized_text_list (list of list of strings) - list of sentences
                tokenized into words on which coreference resolution
                is to be donee
    sentence_start_end: dictionary of start index(relative to text)
                and end index (relative to text) for each sentence
                of the text.
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

  Returns:
    sentence_wise_entities(list of 3 element tuples) -
                First element - start position of entity
                Second element - end position of entity
                Third element - Entity(String)(Here the first element of
                the cluster) with which to replace the text in between
                positions (First element, Second element)
  """
  tokenized_text = [tok for tokenized_sent in tokenized_text_list \
    for tok in tokenized_sent]
  entity_list = []
  for cluster in filtered_cluster:
    if not cluster == []:
      rep_ent = "".join(tokenized_text[cluster[0][0]:(cluster[0][1] + 1)])
      for i in range(1, len(cluster)):
        entity_list.append((cluster[i][0], cluster[i][1], rep_ent))

  if not resolve_all_mentions:
    entity_list.sort(key=lambda x: x[0])
    if len(entity_list) > 1:
      filtered_entity_list = []
      for n in range(len(entity_list)):
        if n < len(entity_list)-1 and entity_list[n][0] >= entity_list[n+1][0] \
          and entity_list[n][1] <= entity_list[n+1][1]:
          continue
        else:
          filtered_entity_list.append(entity_list[n])
      entity_list = filtered_entity_list

  sentence_wise_entities = {}
  for i in range(len(tokenized_text_list)):
    sent_start_idx = sentence_start_end[i]["start"]
    sent_end_idx = sentence_start_end[i]["end"]
    sentence_wise_entities[i] = []
    for j in range(len(entity_list)):
      if entity_list[j][0] <= sent_end_idx:
        if entity_list[j][0] >= sent_start_idx:
          sentence_wise_entities[i].append(
              (entity_list[j][0] - sent_start_idx,
               entity_list[j][1] - sent_start_idx, entity_list[j][2]))
  return sentence_wise_entities


def preprocess_text_for_qg(text=None, model_type="spanbert", lu_id=None,
    spacy_model_type="default"):
  """Function to preprocess text to make it ready for qg"""
  if lu_id or text:
    if lu_id:
      coref_text = get_corefed_lu_text(
        lu_id, model_type, spacy_model_type=spacy_model_type)
    elif text:
      coref_text = get_coref_text(
        text, model_type, spacy_model_type=spacy_model_type)
    coref_text = clean_text(coref_text, False)
    coref_text = coref_text.replace(" 's", "'s")
    sentences = sentence_split(coref_text)
    selected_sentences = sentence_selection(
      sentences, spacy_model_type=spacy_model_type)
    return coref_text, sentences, selected_sentences
  else:
    raise Exception("Either of the text or learning unit id"
                    "should be present as parameter")


def resolve_text(filtered_clusters, doc_list,
  sentence_start_end, resolve_all_mentions = False):
  """
  Return the resolved text.

  Args:
    filtered_clusters(list of list of indexes) -
                [[[0, 4], [18, 18], [56, 59], [78, 78]], [[22, 22]]]
                This example shows the start position, end position of the
                entity mention
    doc_list (list of list of spacy Doc) - list of doc of sentences
                on which coreference resolution is to be done
    sentence_start_end: dictionary of start index(relative to text)
                and end index (relative to text) for each sentence
                of the text.
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

  Returns:
    corefed_sents(list(string)) - list of sentences on which coreference
                resolution done was performed such that each sentence in
                the text has only actual mention (cluster head) of the entity
  """
  tokenized_text_list = [[tok.text_with_ws for tok in doc] for doc in doc_list]
  sentence_wise_entities = convert_cluster_to_entity_list(filtered_clusters,
                                tokenized_text_list, sentence_start_end,
                                resolve_all_mentions)
  corefed_sents = []
  for sent_idx, resolved_entities in sentence_wise_entities.items():
    document = doc_list[sent_idx]
    tokenized_text = list(tok.text_with_ws for tok in document)
    for start, end, ent_text in resolved_entities:
      ent_text = ent_text.strip()
      # In both of the following cases, the first token in the coreference
      # is replaced with the main mention, while all subsequent tokens
      # are masked out with "", so that they can be eliminated from
      # the returned document during "".join(resolved).

      # The first case attempts to correctly handle possessive coreferences
      # by inserting "'s" between the mention and the final whitespace
      # These include my, his, her, their, our, etc.

      # Disclaimer: Grammar errors can occur when the main mention is plural,
      # e.g. "zebras" becomes "zebras's" because this case isn't
      # being explictly checked and handled.
      if document[end].tag_ in ["PRP$", "POS"]:
        tokenized_text[start] = ent_text + "'s" + document[end].whitespace_
      else:
        # If not possessive, then replace first token with main mention directly
        tokenized_text[start] = ent_text + document[end].whitespace_
      # Mask out remaining tokens
      for i in range(start + 1, end + 1):
        tokenized_text[i] = ""
    refined_text = "".join(tokenized_text)
    refined_text = refined_text.strip(" ")
    # For removing all space/new-line characters
    refined_text = " ".join(refined_text.split())
    refined_text = first_letter_to_upper_case(refined_text)
    corefed_sents.append(refined_text)
  return corefed_sents

@retry(retry_on_exception=retry_on_exception, wait_exponential_multiplier=1000,
wait_exponential_max=10000, stop_max_delay=600000)
def get_coref_clusters(text_list, model_type="spanbert",
    spacy_model_type="default"):
  """Return the cluster in allennlp coref resolution clusters.

  Format [[[start_idx, end_idx],[start_idx, end_idx], [[start_idx,
  end_idx]]]
  Ex: [[[0, 4], [18, 18], [56, 59], [78, 78]], [[22, 22]]]

  Args:
      text_list: (list of texts on which coref resolution will be performed)

  Returns:
    all_clusters - list of list of list of cluster mention positions
    [[[[0, 2], [7, 7], [27, 27], [30, 30], [35, 35], [104, 104], [108,
    108]], [[77, 77], [82, 82]], [[89, 89], [93, 93]], [[110, 124], [134,
    134], [148, 148]]]]
  """
  try:
    all_clusters = []
    if model_type == "spanbert":
      url = "http://{}:{}/coref-resolution/api/v1/predict".format(
          SERVICES["coref-resolution"]["host"],
          SERVICES["coref-resolution"]["port"])
      input_json = {"documents": text_list,
        "spacy_model_type": spacy_model_type}
      response = json.loads(requests.post(url=url,
                                            json=input_json).content)["data"]
      for prediction in response["prediction"]:
        all_clusters.append(prediction["clusters"])
    else:
      for text in text_list:
        doc = SPACY_MODELS[spacy_model_type](text)
        clusters = doc._.coref_clusters
        new_clusters = []
        for cluster in clusters:
          inside_list = []
          for coref in cluster:
            inside_list.append([coref.start, coref.end - 1])
          new_clusters.append(inside_list)
        all_clusters.append(new_clusters)
    return all_clusters
  except (TypeError, KeyError) as e:
    logging.error("Failed to get coref clusters. Error: %s", e)
    return [[]]


def get_resolved_sents(sentences, clusters, resolve_all_mentions = False,
    spacy_model_type="default"):
  """Return the list of coref-resolved sentences of the given text.

  By replacing every coref mention only once for each sentence.

  Args:
    sentences(list of string) - list of input sentences
    clusters (list of lists) - coref clusters for each entity mention
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

  Returns:
    resolved_sents (list of strings) - list of sentences of the text
              on which coreference resolution was performed and
              resolved such that each sentence in the text has only
              actual mention (cluster head) of the entity
  """
  sentence_docs = []
  sentence_start_end = {}
  for i, sent in enumerate(sentences):
    doc = SPACY_MODELS[spacy_model_type](sent)
    if i == 0:
      sentence_start_end[i] = {"start": 0, "end": len(doc) - 1}
    else:
      sentence_start_end[i] = {
          "start": sentence_start_end[i - 1]["end"] + 1,
          "end": len(doc) + sentence_start_end[i - 1]["end"]
      }
    sentence_docs.append(doc)

  if resolve_all_mentions:
    new_predictions_cluster = clusters
  else:
    new_predictions_cluster = []
    for cluster in clusters:
      last_cluster_index = 0
      sent_cluster = []
      cluster_length = len(cluster)
      for i in range(len(sentences)):
        sent_start_idx = sentence_start_end[i]["start"]
        sent_end_idx = sentence_start_end[i]["end"]
        for j in range(last_cluster_index, cluster_length):
          if isinstance(cluster[j][0], int):
            if cluster[j][0] < sent_end_idx:
              if cluster[j][0] >= sent_start_idx:
                last_cluster_index = j + 1
                sent_cluster.append([cluster[j][0], cluster[j][1]])
                break
            elif cluster[j][0] > sent_end_idx:
              last_cluster_index = j
              break
      new_predictions_cluster.append(sent_cluster)
  resolved_sents = resolve_text(
    new_predictions_cluster, sentence_docs,
    sentence_start_end, resolve_all_mentions)
  return resolved_sents


### evaluation functions
def is_nan(num):
  """Check if num is empty."""
  return num == ""


def wer(original, result, spacy_model_type="default"):
  r"""The WER is defined as the editing/Levenshtein distance.

      Word level Levenshtein distance divided by the amount of words in
      the original text.
      In case of the original having more words (N) than the result and both
      being totally different (all N words resulting in 1 edit operation
      each), the WER will always be 1 (N / N = 1).
      """
  # The WER is calculated on word (and NOT on character) level.
  # Therefore we split the strings into words first:
  if is_nan(result):
    result = ""
  original = word_split(original, spacy_model_type)
  result = word_split(result, spacy_model_type)
  return editdistance.eval(original, result) / float(len(original))


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


def ngram_wer(text_a, text_b, ngram_val=1):
  """Calculate n gram WER between two texts.
        args:
          text_a: (str) - 1st string
          text_b: (str) - 2nd string
          ngram_val: (num) - default value: 1
      returns:
        (float): ngram word error rate between a and b inputs
  """
  bi_a = text_a.lower().split()
  bi_b = text_b.lower().split()

  if ngram_val == 2:
    bi_a = list(nltk.bigrams(bi_a))
    bi_b = list(nltk.bigrams(bi_b))
  if len(bi_b) > len(bi_a):
    bi_b, bi_a = bi_a, bi_b
  count = 0
  for element in bi_b:
    if element in bi_a:
      count += 1
  return (count) / (len(bi_b) + 0.00001)


def remove_low_context_brackets(text):
  """Function to remove brackets which contains words like "Image", "Chapter"
     etc.
        args:
          text: (str) - input sentence from which bracket has to be removed
          Example: text = "Amplification, in _______, can be detected as
                Homogeneously Stained Regions or Double minutes [ Image 19 ]."
              outout = "'Amplification, in _______, can be detected as
                  Homogeneously Stained Regions or Double minutes .'"

      returns:
        text: (str) - bracket removed version of text

  """
  low_context_words = list(set(item.lower() for item in low_context_objects))
  processed_text = text
  bracket_regex = re.compile(r"\[(.*?)\]|\([^()]*\)|\{[^{}]*\}")
  for b_occurence in reversed(list(bracket_regex.finditer(text))):
    for low_c_obj in low_context_words:
      if re.search(r"\b" + low_c_obj + r"\b",
                   text[b_occurence.start():b_occurence.end()].strip("{([])}"),
                   re.IGNORECASE):
        processed_text = processed_text[:b_occurence.start(
        )] + processed_text[b_occurence.end():]
  return processed_text


def remove_char_at_index(text, index):
  """
  Function to remove character at "index", from input text.
  """
  text = text[:index] + text[index + 1:]
  return text


def remove_unbalanced_brackets(text: str) -> str:
  """
  Function to remove unbalanced brackets from input text.
  Example:
    input text: Some neurofibromas transform to malignant tumor {(MPNST)).
    output text: Some neurofibromas transform to malignant tumor (MPNST).
  """
  remove_square = set()
  remove_curly = set()
  remove_parenthesis = set()
  stack_square = []
  stack_curly = []
  stack_parenthesis = []
  for ind, char in enumerate(text):
    if char in "()":
      if char == "(":
        stack_parenthesis.append(ind)
      elif not stack_parenthesis:
        remove_parenthesis.add(ind)
      else:
        stack_parenthesis.pop()
    elif char in "{}":
      if char == "{":
        stack_curly.append(ind)
      elif not stack_curly:
        remove_curly.add(ind)
      else:
        stack_curly.pop()
    elif char in "[]":
      if char == "[":
        stack_square.append(ind)
      elif not stack_square:
        remove_square.add(ind)
      else:
        stack_square.pop()
    else:
      continue
  remove_ind = list(remove_parenthesis.union(set(
    stack_parenthesis))) + list(remove_curly.union(set(
    stack_curly))) + list(remove_square.union(set(stack_square)))
  output = ""
  for ind, char in enumerate(text):
    if ind in remove_ind:
      continue
    output += char
  return output


def clean_text(text, lstrip_nonalpha=True):
  """Function to clean text in proper format so that non-ascii chars, other
      symbols, invalid whitespace characters are removed
        args:
          text: (str) - input sentence to be cleaned
          lstrip_nonalpha (bool) - indicates if left stripping of
                                  non-alphabetic characters from start of
                                  the text is needed to be performed.
                                  If set to "True", non-alphabetic characters
                                  from the start of the text will be removed.
                                  If set to "False", this operation will NOT
                                  be performed.
      returns:
        text: (str) - cleaned version of input text
  """
  # pylint: disable=inconsistent-quotes
  text = text.replace("’", "'")
  text = text.replace('”', '"')
  text = text.replace('“', '"')
  #Transliterate non-ASCII characters
  # text = unidecode(text)
  text = re.sub("--", "-", text)
  # text = re.sub(r" \([^)]*\)", " ", text)
  text = re.sub(r" {1,}\.", ".", text)
  text = re.sub(r" \t", " ", text)
  text = re.sub(r" +", " ", text)
  # remove empty parenthesis
  text = text.replace("()", " ")
  text = remove_unbalanced_brackets(text)
  # remove brackets which has low context words in them
  text = remove_low_context_brackets(text)
  # remove non-alphabet characters from start of paragraph
  if lstrip_nonalpha:
    text = re.sub(r"^[^a-zA-Z_____]*", "", text)
  # replacing more than one space by single space
  text = re.sub(" {2,}", " ", text)
  text = text.replace(" ’", "’")
  text = text.replace(" - ", "-")
  text = text.replace(" ,", ",")
  text = text.replace(" .", ".")
  #remove extra underscores. Example: _________LO 22. Explain the term kinship.
  text = re.sub(r"_{2,}", "", text)
  text = re.sub(r"\s+$", "", text, 0, re.MULTILINE)
  return text.strip()


def first_letter_to_upper_case(text):
  """Converts first letter of the text to upper case
  and retains original casing
  Args:
      text (str): input text
  Returns:
      text (str): string with 1st character as capital
  """
  text = text[:1].upper() + text[1:]
  return text


def make_title_case(text):
  """Convert text to title case."""
  text = text.title()
  return text


def rank_entities(text, candidates):
  """Function to rank candidates using keybert
  Args:
    text (string): LU text.
    Example: Gold rings dangled from cow's nose.
    candidates (list of dictionary): Contains entities and their starting index
    as keys. Example:
    [{"text": Gold, "start_idx": 0},
     {"text": rings, "start_idx": 1}]
  """
  entities = [item["text"] for item in candidates]
  keywords = MODEL_ENTITY_RANK.extract_keywords(
      text, candidates=entities, top_n=len(candidates))
  result = []
  added_index = []
  for entity, score in keywords:
    if entity in entities:
      item_index = entities.index(entity)
      if item_index in added_index and entity in entities[item_index + 1:]:
        item_index = entities.index(entity, item_index + 1)
      added_index.append(item_index)
      candidates[item_index]["score"] = score
      result.append(candidates[item_index])
  return result


def clean_candidates(candidates):
  """Function to clean text of candidates
  Args:
      candidates (list): candidates that need to be cleaned
  Returns:
      candidates (list): cleaned candidates
  """
  for i in range(len(candidates)):
    candidates[i]["text"] = re.sub(r" - ", "-", candidates[i]["text"])
    candidates[i]["text"] = re.sub(r"\b\s+'\b", r"'", candidates[i]["text"])
    candidates[i]["text"] = re.sub(r"\(\w$", "", candidates[i]["text"])
  return candidates


def remove_overlapping(entities):
  """Remove overlapping entities
  Args:
      entities (list): entities that are to be checked
  Returns:
      result (list): Entities which are non-overlapping
  """
  result = []
  for i, item in enumerate(entities):
    start = item["start_idx"]
    end = start + len(item["text"])
    flag = False
    for j, item_2 in enumerate(entities):
      if j == i:
        continue
      start_item_2 = item_2["start_idx"]
      end_item_2 = start_item_2 + len(item_2["text"])
      if start >= start_item_2 and end <= end_item_2:
        flag = True
        break
    if not flag:
      result.append(item)
  return result


def get_bracket_array(sentence):
  """Creates an array of tuples containing the position index where brackets
  are found in a sentence
  Args:
    sentences (string): text
  Returns:
    List of tuples in the format [(idx1, idx2)]  where,
    idx1 = start index of the bracket
    idx2 = end index of the bracket
  """
  bracket_array = []
  start = None
  count = 0
  for i, character in enumerate(sentence):
    if character == "(" and count == 0:
      start = i
      count += 1
    elif character == "(":
      count += 1
    elif character == ")":
      if start and count == 1:
        bracket_array.append((start, i))
        start = None
        count = 0
      else:
        count -= 1
  return bracket_array


def remove_bracket_entities(entities, sentence):
  """Removes entities in a sentence which are inside brackets
  Args:
    sentence(string): Text. Example
                      My car is in the drive (with the window open).
    entities (list): List of dictionaries. Example-
    [{"text": "car", "start_idx": 3}]
    text - Entity in the sentence,
    start_idx - starting index of the entity
  Returns:
    list of dictionaries after removing the entities inside brackets. Example
    [{"text": "car", "start_idx": 3}]
  """
  bracket_array = get_bracket_array(sentence)
  result = []
  for i, item in enumerate(entities):
    start = item["start_idx"]
    end = start + len(item["text"]) - 1
    text = item["text"]
    flag = False
    for b_start, b_end in bracket_array:
      if ((b_start < start and b_end > end) or ("(" in text or ")" in text)):
        flag = True
        break
    if not flag:
      result.append(entities[i])
  return result


def generate_entities(doc, assessment_type=None):
  """Function to get candidates using spacy
  Args:
    doc: Spacy object fitted on input sentence
    assessment_type: "external_distractors" - for CTF Type 0
                   OR "None" - For others
    discard_ner_types: Types of named entities to discard
  Returns:
    named_entities, non_named_entities:
    list of dictionaries after removing the entities inside brackets.
  """
  named_entities = []
  for ent in doc.ents:
    if ent[-1].pos_ in valid_named_entity_pos:
      named_entities.append({
      "text": ent.text,
      "start_idx": ent.start_char,
      "label": ent.label_
    })
  doc_ents = [i.text for i in doc.ents]
  non_named_entities = []
  for ind, _ in enumerate(doc):
    if doc[ind].pos_ == "ADJ":
      if not (assessment_type == "external_distractors" and \
      doc[ind].text in quantitative_adjectives):
        curr = ind
        flag = False
        text = doc[curr].text_with_ws
        if doc[curr].text in quantitative_adjectives:
          text = ""
        while ((curr < len(doc) - 1) and
               ((doc[curr + 1].pos_ == "NOUN") or
                (doc[curr + 1].text.strip() == "-"))) or (
                    (curr > 0) and (doc[curr].text.strip() == "-")):
          flag = True
          text += "" + str(doc[curr + 1].text_with_ws)
          curr += 1
          if doc[curr].pos_ in ["PART", "PUNCT"
                               ] and doc[curr].text in ["'s", "-"]:
            text += "" + str(doc[curr + 1].text_with_ws)
            curr += 1
        if flag:
          non_named_entities.append({
              "text": text.rstrip(),
              "start_idx": doc[ind].idx
          })
    elif (ind == 0 and doc[ind].pos_ == "NOUN") or (
        doc[ind].pos_ == "NOUN" and doc[ind - 1].pos_ != "NOUN" and
        doc[ind - 1].pos_ != "ADJ" and doc[ind - 1].text not in ["'s", "-"]):
      curr = ind
      text = doc[curr].text_with_ws
      while (curr < len(doc) - 1 and
             (doc[curr + 1].pos_ == "NOUN" or
              (doc[curr + 1].pos_ in ["PART", "PUNCT"]) and
              doc[curr + 1].text in ["'s", "-"])) or doc[curr].text == "-":
        text += "" + str(doc[curr + 1].text_with_ws)
        curr += 1
        if doc[curr-1].pos_ == "NOUN" and doc[curr-1].text in doc_ents and\
            doc[curr].pos_ == "PART":
          text = ""
      non_named_entities.append({
          "text": text.rstrip(),
          "start_idx": doc[ind].idx
      })
  non_named_entities = clean_candidates(non_named_entities)
  non_named_entities = remove_overlapping(non_named_entities)
  non_named_entities = remove_bracket_entities(non_named_entities, doc.text)
  named_entities = remove_bracket_entities(named_entities, doc.text)
  return (named_entities, non_named_entities)


def extract_entities(text, assessment_type=None, spacy_model_type="default"):
  """Function to extract entities and return their score
  Args:
    text (string)
  Returns:
    result (list): List of dictionaries. Example
    [{"sentence": "<text>", "named_entities": "<text>",
    "non_named_entities": "<text>"}]
  """
  sentences = sentence_split(text)
  result = []
  for sentence in sentences:
    entities = {}
    doc = SPACY_MODELS[spacy_model_type](sentence)
    named_entities, non_named_entities = generate_entities(doc, assessment_type)
    non_named_entities = rank_entities(text, non_named_entities)
    entities["sentence"] = sentence
    entities["named_entities"] = named_entities
    entities["non_named_entities"] = non_named_entities
    result.append(entities)
  return result


def answer_in_question(question, answer, spacy_model_type="default"):
  """Function to identify QA pairs where answer lies in question
  Args:
      question (str): sentence that is to be checked
      answer (str): answer to be checked
  Returns:
      (bool): True - if answer lies in question
              Flase - if not
  """
  answer_doc = SPACY_MODELS[spacy_model_type](answer)
  count = 0
  question_doc = SPACY_MODELS[spacy_model_type](question)
  answer_lemmas = [token.lemma_ for token in answer_doc]
  question_lemmas = [token.lemma_ for token in question_doc]
  for word in answer_lemmas:
    if word in question_lemmas:
      count = count + 1
  score = 100 * (count / len(answer_lemmas))
  if score >= 95:
    return True
  return False


def entity_in_topn(entity, context, top_n=7):
  """
  Method to check if the "entity" is present in "top_n" entities of the
  "context" using keyBERT scores.
  Args:
    entity (str): an entity which is to be checked.
    context (str): document in which the check is to be performed.
    top_n (int): default value 7.
  Returns:
    bool: True if "entity" is in "top_n" entities of the "context", else False.
  """
  entity_len = len(entity.split())
  top_entities = MODEL_ENTITY_RANK.extract_keywords(context,
      keyphrase_ngram_range=(entity_len, entity_len), top_n=top_n)
  for item in top_entities:
    if item[0].lower() == entity.lower():
      return True
  return False


def get_facts_for_correct_incorrect_feedback(candidate_sentences, answer,
                                          context, spacy_model_type="default"):
  """
  Method to extract facts/sentences from list of sentences, which can
  be used as feedback in case of correct/incorrect response by the user.
  There is a two-step filtering done based on "use_two_filter".
  First, check if the "answer" entity is in the top_n (default=7) entities
  in the candidate sentence. Second, check if the keyBERT score of the answer
  entity in the context is in the threshold.
  Courses like Bio, where entities are specific to the course, the filtering
  need not be strict as the most of the sentences that has entity's mention
  can be used as feedback fact. Whereas, Courses with more general entities
  like Research Design, Sociology, it requires a stricter filtering
  (two filters).
  Args:
    candidate_sentences (list): list of sentences from which facts for
                                feedback are to be searched.
    answer (str): answer for the assessment item.
    context (str or list): sentence(s) from which the question is generated.
                            CTF and single hop AAQ questions are generated
                            from single sentence (str). Whereas, Multihop
                            questions are generated from two sentences (list).
    Returns:
      facts_for_correct_feedback (list): list of facts/sentences for feedback
                                          in case of correct response.
      facts_for_incorrect_feedback (list): list of facts/sentences for feedback
                                          in case of incorrect response.
  """
  facts_for_correct_feedback = []
  facts_for_incorrect_feedback = []
  BLANK = "_"*7
  use_two_filter = bool(spacy_model_type == "default")
  if isinstance(context, list):
    context = [i.lower() for i in context]
  else:
    context = context.lower()
  for sent in candidate_sentences:
    if len(sent.split()) < LONG_SENT_THRESHOLD:
      if (re.search(r"\b" + answer.strip(".,") + r"\b", sent, re.IGNORECASE))\
          and sent.lower() not in context:
        answer_sent_keybert_score = MODEL_ENTITY_RANK.extract_keywords(
          sent, candidates=[answer])[0][1]
        if use_two_filter:
          if entity_in_topn(answer, sent):
            if answer_sent_keybert_score >= \
                FEEDBACK_FACT_KEYBERT_THRESHOLD["high"]:
              replacer = re.compile(r"\b" + answer + r"\s", re.IGNORECASE)
              sent_with_blank = replacer.sub(f"{BLANK} ", sent)
              if BLANK in sent_with_blank:
                facts_for_incorrect_feedback.append(
                    first_letter_to_upper_case(sent_with_blank))
            elif answer_sent_keybert_score >= \
                FEEDBACK_FACT_KEYBERT_THRESHOLD["low"]:
              facts_for_correct_feedback.append(
                first_letter_to_upper_case(sent))
        else:
          if answer_sent_keybert_score >= \
              FEEDBACK_FACT_KEYBERT_THRESHOLD["high"]:
            replacer = re.compile(r"\b" + answer + r"\s", re.IGNORECASE)
            sent_with_blank = replacer.sub(f"{BLANK} ", sent)
            if BLANK in sent_with_blank:
              facts_for_incorrect_feedback.append(
                  first_letter_to_upper_case(sent_with_blank))
          elif answer_sent_keybert_score >= \
              FEEDBACK_FACT_KEYBERT_THRESHOLD["low"]:
            facts_for_correct_feedback.append(
              first_letter_to_upper_case(sent))
  facts_for_correct_feedback = list(set(facts_for_correct_feedback))
  facts_for_incorrect_feedback = list(set(facts_for_incorrect_feedback))
  return facts_for_correct_feedback, facts_for_incorrect_feedback


def get_similarity_score(sent1, sent2):
  """
  Takes two sentences and returns cosine similarity between the two using
  sentence-transformer - distilbert-base-nli-stsb-mean-tokens.
  Args:
      sent1 (str): first sentence
      sent2 (str): second sentence
  Returns:
      consine_sim (float): cosine similarity between "sent1" and "sent2"
  Examples:
  >>> question = "What are considered delicacies?"
  >>> lu_title = "Define the fungi in your diet"
  >>> question_lu_sim_score = get_similarity_score(question, lu_title)
  >>> question_lu_sim_score
  >>> 0.32670873403549194
  """
  sent1_embd = MODEL_STS.encode(sent1.lower())
  sent2_embd = MODEL_STS.encode(sent2.lower())
  cosine_sim = util.pytorch_cos_sim(sent1_embd, sent2_embd)[0][0].item()
  return cosine_sim


def generate_overall_score(assessment_item):
  """
  Takes assessment specific dictionary in which the 'activity' key has the
  name of the assessment item, and rest of the key-value pairs are name of
  the score and the corresponding score. Returns an Overall Score for that
  assessment item calculated using pre-trained Logistic Regression.
  Args:
      assessment_item (dict): A dictionary for an assessment item
          containing assessment type in 'activity' key.
          For Answer a question, keys are:
          activity, question_generation_score, answer_extraction_score,
          sentence_ranking_score, answer_ranking_score,
          question_lu_sim_score, question_lu_text_sim_score
  Returns:
      overall_score (float): Overall score for that assessment item.
  Examples:
  "assessment_item" for Answer a Question activity.
  >>> assessment_item = {'activity': 'answer_a_question',
                      'question_generation_score': -0.26,
                      'answer_extraction_score': -0.31,
                      'sentence_ranking_score': 0.99,
                      'answer_ranking_score': 0.4,
                      'question_lu_sim_score': 0.28280574083328247,
                      'question_lu_text_sim_score': 0.4390767216682434}
  >>> overall_score = generate_overall_score(assessment_item)
  >>> overall_score
  >>> 0.4021665325996465
  """
  activity = assessment_item["activity"]
  model_lr = LogisticRegression()
  model_lr.classes_ = np.array([0, 1])
  if activity == "answer_a_question":
    qa_datapoint = np.array([
        assessment_item["question_generation_score"],
        assessment_item["answer_extraction_score"],
        assessment_item["sentence_ranking_score"],
        assessment_item["answer_ranking_score"],
        assessment_item["question_lu_sim_score"],
        assessment_item["question_lu_text_sim_score"]
    ])
    model_lr.coef_ = np.array([[
        2.50690793, 1.27226922, -0.93287293, 0.73962861, 1.70755687, 1.30233887
    ]])  # trained coefs
    model_lr.intercept_ = np.array([0.22271274])  # trained intercept
    overall_score = model_lr.predict_proba([qa_datapoint])[0][1]
  return overall_score


def update_learning_unit(lu, data):
  """Function to update learning unit values"""
  lu = LearningUnit.find_by_id(lu)
  try:
    lu_fields = lu.get_fields()
    lu_fields["parent_node"] = lu.parent_node.ref.path
    for key, value in data.items():
      lu_fields[key] = value
    for key, value in lu_fields.items():
      if key == "parent_node":
        parent = lu.parent_node.get().__class__.collection.get(value)
        if parent:
          setattr(lu, key, parent)
        else:
          raise Exception("Learning objective with this ID does not exist")
      else:
        setattr(lu, key, value)
    lu.update()
  except (TypeError, KeyError) as e:
    raise Exception("Failed to update learning_unit") from e


def get_coref_text(text, model_type="spanbert",
    resolve_all_mentions = False, spacy_model_type="default"):
  """Return the resolved text from AllenNLP Coref Resolution.

    By replacing every coref mention only once for each sentence.

    Args:
    text(string) - a string (text of learning unit in this case)
    model_type - Type of model to use when doing coref resolution, can be
                  neuralcoref or spanbert
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence
    Returns:
    resolved_text(string) - coreference resolution done on text and
                resolved such that each sentence in the text has only
                actual mention (cluster head) of the entity
  """
  return batch_get_coref_text(
    [text], model_type, resolve_all_mentions, spacy_model_type)[0]


def get_coref_sentences(text, model_type="spanbert",
    spacy_model_type="default"):
  return batch_get_coref_sentences([text], model_type,
    spacy_model_type=spacy_model_type)[0]

def split_large_paragraphs(text):
  """Function to split very large texts above a certain threshold
  Args:
    text (str): Paragarph which needs to be split
  Returns:
    [text]: List of text after split
    split_flag (bool): Flag to show whether paragraph split took place or not"""

  split_flag = False
  if len(text) > SPLIT_THRESHOLD:
    split_flag = True
    indexes = [i for i, c in enumerate(text) if c == "."]
    req_indexes = [i for i in indexes if i < SPLIT_THRESHOLD]
    if req_indexes:
      req_index = req_indexes[-1]
      para1 = text[:req_index+1]
      para2 = text[req_index+1:]
      result, _ = split_large_paragraphs(para2)
      final_result = [para1] + result
      return final_result, split_flag
    else:
      return [text], False
  else:
    return [text], split_flag

def merge_split_paragraphs(sentences, merge_index):
  """Function to merge text that was split due to it being very large
  Args:
    sentences: list(list(text)) List of sentences in each split paragraph
    merge_index: list(orig_index (before split), initial_index (after_split),
    final_index (after_split), split_occurred(bool))
  Returns:
    final_sentences: list(list(text))) List of sentences in each original
    paragraph"""
  final_sentences = []
  try:
    for tup in merge_index:
      if tup[-1]:
        final_sentences.append(sentences[tup[1]] + sentences[tup[2]])
      else:
        final_sentences.append(sentences[tup[2]])
  except IndexError as e:
    logging.error("Index Error during merging split paragraphs: %s", e)
    return sentences
  return final_sentences

def batch_get_coref_sentences(
  text_batch, model_type="spanbert", resolve_all_mentions = False,
  spacy_model_type="default"):
  """Returns list of corefed sentences for each text in the given text
    list.

    Args:
      text_batch: list of texts to be corefed.
      mocel_type: "spanbert" or "neuralcoref"
      resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

    Returns:
      all_resolved_sents (list of lists): list of corefed sentences
      for each text present in text_batch

    """
  all_resolved_sents = []
  all_sentences = []
  new_text_batch = []
  batch = []
  merge_index = []
  prev_len = 0
  for i, text in enumerate(text_batch):
    split_text, split_flag = split_large_paragraphs(text)
    batch += split_text
    merge_index.append([i, prev_len, len(batch)-1, split_flag])
    prev_len = len(batch)

  for text in batch:
    sentences = sentence_split(text)
    new_text_batch.append(" ".join(sentences))
    all_sentences.append(sentences)

  clusters = get_coref_clusters(new_text_batch, model_type, spacy_model_type)

  for sentences, cluster in zip(all_sentences, clusters):
    resolved_sents = get_resolved_sents(sentences, cluster,
                resolve_all_mentions, spacy_model_type)
    all_resolved_sents.append(resolved_sents)

  all_resolved_sents = merge_split_paragraphs(all_resolved_sents, merge_index)
  return all_resolved_sents

def batch_get_coref_text(
  text_batch, model_type = "spanbert", resolve_all_mentions = False,
  spacy_model_type="default"):
  """Return the resolved text from AllenNLP Coref Resolution.

    By replacing every coref mention only once for each sentence.

    Args:
    text_batch(list) - a list of strings (text of learning unit in this case)
    model_type - Type of model to use when doing coref resolution, can be
                  neuralcoref or spanbert
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

    Returns:
    resolved_texts(list) - list of coreference resolved text such that
                  each sentence in the text has only actual mention
                  (cluster head) of the entity
  """
  resolved_texts = []
  all_corefed_sents = batch_get_coref_sentences(
    text_batch, model_type, resolve_all_mentions, spacy_model_type)
  for corefed_sents in all_corefed_sents:
    text = " ".join(corefed_sents)
    resolved_texts.append(text)
  return resolved_texts

def get_corefed_lu_text(
  lu_id, model_type="spanbert", resolve_all_mentions = False,
  spacy_model_type="default"):
  """
    Returns text of learning unnit after doing corefence resolution

    Args:
    lu_id(string) - learning unnit id
    model_type - Type of model to use when doing coref resolution, can be
                  neuralcoref or spanbert
    resolve_all_mentions (boolen): resolves all metions in the text if true
                else every coref mention only once for each sentence

    Returns:
    corefed_text - Resolved text of learning unit
  """
  lu = LearningUnit.find_by_id(lu_id)
  text_batch = lu.text.split("<p>")
  if lu.coref_text:
    return lu.coref_text
  else:
    corefed_text_list = batch_get_coref_text(
      text_batch, model_type, resolve_all_mentions, spacy_model_type)
    corefed_text = " ".join(corefed_text_list)
    data = {"coref_text": corefed_text}
    update_learning_unit(lu_id, data)
  return corefed_text


def get_important_sents_from_text_for_CKN(
    text, coref_model_type="spanbert", spacy_model_type="default"):
  """Returns list of important sentence from the given text"""
  imp_sent_indices = []
  corefed_sents = get_coref_sentences(
    text, model_type=coref_model_type, spacy_model_type=spacy_model_type)
  cleaned_corefed_sents = []
  for sent in corefed_sents:
    cleaned_sent = clean_text(sent)
    if cleaned_sent:
      cleaned_corefed_sents.append(cleaned_sent)
  selected_sents = sentence_selection(
    cleaned_corefed_sents, spacy_model_type=spacy_model_type)
  for sent in selected_sents:
    for i, corefed_sent in enumerate(cleaned_corefed_sents):
      if cer(sent, corefed_sent) <= 0.1:
        imp_sent_indices.append(i)
  return imp_sent_indices


def convert_to_truecase(text, spacy_model_type="default"):
  """Function for ensuring proper capitalization
   of words in the given text"""
  truecased_sents = []
  for sentence in sentence_split(text):
    truecased_sentence = ""
    for tok in SPACY_MODELS[spacy_model_type](sentence):
      tok_text = tok.text_with_ws
      if tok.pos_ != "PROPN":
        tok_text = tok_text.lower()
      truecased_sentence += tok_text
    truecased_sentence = truecased_sentence[0].upper() + \
       truecased_sentence[1:]
    truecased_sents.append(truecased_sentence)
  return " ".join(truecased_sents)

def get_constituency_parse_tree(sentence):
  """Perform  constituency parsing on a sentence."""
  prediction = json.loads(
      requests.post(
          url="http://{}:{}/const-parsing/api/v1/predict".format(
              SERVICES["const-parsing"]["host"],
              SERVICES["const-parsing"]["port"]),
          json={
              "sentence": sentence
          }).content)["data"]
  return prediction["trees"]


def get_bracket_array_with_np(bracket_array, tree):
  """Creates an array of tuples
    Args:
    bracket_array - output of function : get_bracket_array()
    tree - a string which contains the constituency parsing of the text
        Example : (S (NP (NNP Patty) (NNP Smith) (NNP Hill)) (VP (VBZ founds)
        (NP (NP (NP (DT the) (NNP National) (NNP Committee)) (PP (IN on)
        (NP (NNP Nursery) (NNPS Schools)))) (PRN (-LRB- -LRB-)
        (VP (ADVP (RB later)) (NNP NANE)) (-RRB- -RRB-))) (S (VP (TO to)
        (VP (VB establish) (NP (NP (DT a) (JJ professional)
        (NN organization)) (PP (IN for) (NP (NN nursery) (NN school)
        (NNS educators)))) (PP (IN in) (NP (CD 1926))))))))

    Returns a list of tuples where each element is (op_idx , close_idx,
    position, 1) for noun phrase in tree and (op_idx, close_idx, 0) for not
    noun phrase. Here, (op_idx) refers to the index of opening bracket and
    (close_idx) refers to index of closing bracket
    """
  new_bracket_array = []
  for i, ele in enumerate(bracket_array):
    if ele[1] == -1:
      continue
    count = 0
    for j in range(i, len(bracket_array)):
      count = count + bracket_array[j][1]
      if count == 0:
        break
    if tree[ele[0] + 1:ele[0] + 4] == "NP ":
      new_bracket_array.append((ele[0], bracket_array[j][0], 1))
    else:
      new_bracket_array.append((ele[0], bracket_array[j][0], 0))
  return new_bracket_array


def get_nn_end_start_end(bracket_array_with_np):
  """Returns the element from bracket_array_with_np which has the longest
    noun phrase till the end of the sentence
    Args:
    bracket_array_with_np - output of function : get_bracket_array_with_np()

    Returns an element from bracket_array_with_np which is the longest noun
    phrase and goes till the end of the sentence
    """
  end_lim = bracket_array_with_np[0][1]
  for i in range(1, len(bracket_array_with_np)):
    if bracket_array_with_np[i][1] == end_lim - 1:
      end_lim = bracket_array_with_np[i][1]
      if bracket_array_with_np[i][2] == 1:
        return bracket_array_with_np[i][0],\
            bracket_array_with_np[i][1], True
      end_lim = bracket_array_with_np[i][1]
  return -1, -1, False


def get_nn_mid_start_end(bracket_array_with_np):
  """Returns the element from bracket_array_with_np which has the longest
    noun phrase anywhere in the sentence
    Args:
    bracket_array_with_np - output of function : get_bracket_array_with_np()

    Returns an element from bracket_array_with_np which is the longest noun
    phrase anywhere in the sentence
    """
  max_len_nn_phrase = 0
  # end_lim = bracket_array_with_np[0][1]
  max_nn_phrase = bracket_array_with_np[0]
  for ele in bracket_array_with_np:
    if (ele[1] - ele[0]) > max_len_nn_phrase:
      if ele[2] == 1:
        max_len_nn_phrase = (ele[1] - ele[0])
        max_nn_phrase = ele
  if max_nn_phrase[2] == 1:
    return max_nn_phrase[0], max_nn_phrase[1], True
  return -1, -1, False


def get_text_from_tree(tree, start_idx, end_idx):
  """Returns the noun_phrase from the tree based on the opening and closing
    bracket index given by the function : get_nn_start_end()
    Args:
    tree - a string which contains the constituency parsing of the text
        Example : (S (NP (NNP Patty) (NNP Smith) (NNP Hill)) (VP (VBZ founds)
        (NP (NP (NP (DT the) (NNP National) (NNP Committee)) (PP (IN on)
        (NP (NNP Nursery) (NNPS Schools)))) (PRN (-LRB- -LRB-)
        (VP (ADVP (RB later)) (NNP NANE)) (-RRB- -RRB-))) (S (VP (TO to)
        (VP (VB establish) (NP (NP (DT a) (JJ professional)
        (NN organization)) (PP (IN for) (NP (NN nursery) (NN school)
        (NNS educators)))) (PP (IN in) (NP (CD 1926))))))))
    start_idx - index of opening bracket of longest noun phrase
    end_idx - index of closing bracket of longest noun phrase

    Returns the text from the tree string by removing the brackets
    """
  mytext = tree[start_idx:end_idx]
  mytext = re.sub(r"\(\S+", "", mytext)
  mytext = re.sub(r"\){1,}", "", mytext)
  mytext = re.sub(r" {2,}", " ", mytext)
  mytext = mytext.replace("-LRB-", "(")
  mytext = mytext.replace("-RRB-", ")")
  mytext = mytext.replace("-LCB-", "{")
  mytext = mytext.replace("-RCB-", "}")
  mytext = mytext.replace("-LSB-", "[")
  mytext = mytext.replace("-RSB-", "]")
  return mytext.strip()


def get_longest_nn_phrase(sentence):
  """Returns the longest noun phrase of a sentence
    Args:
    sentence - a sentence to get the longest noun phrase from

    Returns the longest noun phrase of the sentence
    """
  tree = get_constituency_parse_tree(sentence)
  bracket_array = []
  for i, node in enumerate(tree):
    if node == "(":
      bracket_array.append((i, 1))
    elif node == ")":
      bracket_array.append((i, -1))
  bracket_array_with_np = get_bracket_array_with_np(bracket_array, tree)

  start_idx_end, end_idx_end, nn_end_exists = get_nn_end_start_end(
      bracket_array_with_np)
  start_idx_mid, end_idx_mid, nn_mid_exists = get_nn_mid_start_end(
      bracket_array_with_np)
  refined_nn_end = ""
  refined_nn_mid = ""
  if nn_end_exists:
    refined_nn_end = get_text_from_tree(tree, start_idx_end, end_idx_end)
  if nn_mid_exists:
    refined_nn_mid = get_text_from_tree(tree, start_idx_mid, end_idx_mid)
  if refined_nn_end:
    return refined_nn_end, True
  if refined_nn_mid:
    return refined_nn_mid, True
  return "", False


def drop_blooms_verb(sentence, spacy_model_type="default"):
  """returns noun phrase by fropping blooms verb
   or converting the sentence to how based question"""
  phrase = ""
  sentence = sentence.strip()
  doc = SPACY_MODELS[spacy_model_type](sentence)
  flag = False
  for tok in doc:
    if tok.tag_ == "WP":
      flag = True
      phrase = doc[tok.i:].text
      break
    elif tok.text == "apply":
      flag = True
      phrase = "how to {}".format(doc[tok.i:].text)
      break
  if not flag:
    phrase, _ = get_longest_nn_phrase(sentence)
  phrase = clean_text(phrase)
  return phrase


def is_long(text, spacy_model_type="default"):
  """
  Function to get hint when the sentence is long/contains conjunctions for
  the given text input.
  Return: hint (string)
  """
  doc = SPACY_MODELS[spacy_model_type](text)
  conj_tags = ["CCONJ", "CONJ", "SCONJ", "CC"]
  flag = False
  for token in doc:
    if token.pos_ in conj_tags:
      flag = True
  return bool(len(nltk.word_tokenize(text)) > 20 or flag)


def postprocess_text_for_frontend(text):
  """Function to post-process text before sending to frontend"""
  text = re.sub(r"\s+$", "", text, 0, re.MULTILINE)
  if re.findall(r"\n+", text):
    text = text.replace("\n", "<br>")
  return text
