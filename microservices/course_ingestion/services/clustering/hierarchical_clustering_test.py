"""testing heirarchical clustering"""

# pylint: disable=invalid-overridden-method
#pylint: disable=wrong-import-position
#pylint: disable=redefined-outer-name
# pylint: disable=unspecified-encoding

import sys

sys.path.append("../../common/src")

import pytest
import json
import ast
from unittest.mock import MagicMock
from config import SERVICES
from services.clustering import hierarchical_clustering as hc

class AsyncMock(MagicMock):  #pylint: disable=invalid-overridden-method
  #pylint: disable=useless-super-delegation

  async def __call__(self, *args, **kwargs):
    return super(AsyncMock, self).__call__(*args, **kwargs)  #pylint: disable=super-with-arguments


@pytest.fixture
def get_topic_tree():
  with open("testing/sample_clustering_output.json") as f:
    topic_tree = ast.literal_eval(json.load(f))
  return topic_tree


@pytest.fixture(name="mocked_get_topics")
def fixture_mocked_get_topics():
  """mocks get_topics"""
  return [["sample_topic", 0.912334]]


dummy_titles = {
    "competency": [["competency title"]],
    "sub_competency": [["subcompetecy title"]],
    "learning_objective": [[
        "learning objective title 1", "learning objective title 2"
    ]]
}

get_titles_response = {
    "success": True,
    "message": "All good",
    "data": {
        "titles": [
            ["Science - The Cycle of Induction and Deduction"]
        ]
    }
}

get_blooms_titles_response = {
    "success": True,
    "message": "All good",
    "data": {
        "titles": [
            [
                "Describe the role of induction and deduction "
                "in the scientific method"
            ]
        ]
    }
}

get_summary_response = {
    "success": True,
    "message": "All good",
    "data": {
        "summary": "Science has played a significant role as a means of "
                   "generating new knowledge. Aristotle was probably one "
                   "of the first who formalized an approach to knowledge "
                   "generation that involved a process of inquiry and "
                   "analysis in which general principles can be formulated "
                   "from what is observed (induction), and from these general "
                   "principles, hypotheses can be derived that can be used "
                   "to test those principles (deduction)."
    }
}

text_data = [
    "Science has played a significant role as a means of "
    "generating new knowledge. Historians of science can trace "
    "the origins of a scientific method to the time of Aristotle "
    "and earlier. Aristotle was probably one of the first who "
    "formalized an approach to knowledge generation that involved "
    "a process of inquiry and analysis in which general principles "
    "can be formulated from what is observed (induction), and from these "
    "general principles, hypotheses can be derived that can be used to"
    "test those principles (deduction). The results of the tests of the "
    "hypotheses can then be used to inform theory. The cycle of induction "
    "and deduction is what is responsible for the creation of new knowledge "
    "(Gauch, 2003). In the 18th and 19th centuries, rationalism, defined as "
    "the belief that knowledge can be created through internal reflection "
    "and logic, was superseded by empiricism, the belief that what is known "
    "is that which is discoverable by the senses and ultimately measurable."
]


def mocked_requests_post(**kwargs):
  """Function mock post requests"""

  class MockResponse:
    """Class to get mock responses"""

    def __init__(self, json_data, status_code):
      self.content = json.dumps(json_data)
      self.status_code = status_code

    def json(self):
      return self.json_data

  if kwargs[
      "url"] == "http://{}:{}/title-generation/api/v1/title-generation".format(
          SERVICES["title-generation"]["host"],
          SERVICES["title-generation"]["port"],
      ):
    return MockResponse(get_titles_response, 200)

  elif kwargs[
      "url"] == "http://{}:{}/title-generation/api/v1/blooms-title-generation".\
          format(
          SERVICES["title-generation"]["host"],
          SERVICES["title-generation"]["port"],
      ):
    return MockResponse(get_blooms_titles_response, 200)
  elif kwargs[
      "url"] == "http://{}:{}/extractive-summarization/api/v1/summarize".\
          format(
          SERVICES["extractive-summarization"]["host"],
          SERVICES["extractive-summarization"]["port"]):
    return MockResponse(get_summary_response, 200)
  return MockResponse(None, 404)


@pytest.mark.parametrize("texts, max_title_length, actual_output", [
  (text_data, 32,
  [["Describe the role of induction and deduction in the scientific method"]])
])
def test_get_blooms_titles(mocker, texts, max_title_length, actual_output):
  mocker.patch(
      "services.clustering.hierarchical_clustering.requests.post",
      side_effect=mocked_requests_post)
  response = hc.get_blooms_titles(texts, max_title_length, n_titles=1)
  assert response == actual_output


@pytest.mark.parametrize(
    "texts, max_title_length, actual_output",
    [(text_data, 32, [["Science - The Cycle of Induction and Deduction"]])])
def test_get_titles(mocker, texts, max_title_length, actual_output):
  mocker.patch(
      "services.clustering.hierarchical_clustering.requests.post",
      side_effect=mocked_requests_post)
  response = hc.get_titles(texts, max_title_length, n_titles=1)
  assert response == actual_output


@pytest.mark.parametrize(
    "data, ratio, actual_output",
    [(text_data[0], 0.3, "Science has played a significant role as a means of "
      "generating new knowledge. Aristotle was probably one "
      "of the first who formalized an approach to knowledge "
      "generation that involved a process of inquiry and analysis "
      "in which general principles can be formulated from what "
      "is observed (induction), and from these general principles, "
      "hypotheses can be derived that can be used to test those "
      "principles (deduction).")])
def test_get_summary(mocker, data, ratio, actual_output):
  mocker.patch(
      "services.clustering.hierarchical_clustering.requests.post",
      side_effect=mocked_requests_post)
  response = hc.get_summary(data, ratio)
  assert response == actual_output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "texts, token_lengths, join_texts, expected_ouput",
    [(["This is a sample text 1", "This is the sample text 2"
      ], [524, 561], "This is a sample text 1. This is the sample text 2",
      "This is a sample text 1. This is the sample text 2"),
     (["This is a sample text 3", "This is the sample text 4"
      ], [50, 51], "This is a sample text 3. This is the sample text 4",
      "This is a sample text 3. This is the sample text 4")])
async def test_compress_text_for_title_generation(texts, token_lengths,
                                                  join_texts, expected_ouput,
                                                  mocker):
  mocker.patch(
      "services.clustering.hierarchical_clustering.len",
      side_effect=token_lengths)
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_summary",
      side_effect=lambda x, y: x)
  mocker.patch(
      "services.clustering.hierarchical_clustering.join_texts",
      return_value=join_texts)
  output = await hc.compress_text_for_title_generation(texts)
  assert isinstance(output, str)
  assert output == expected_ouput


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "texts_list, max_title_length, blooms_title, expected_ouput",
    [(["This is a sample text 1", "This is the sample text 2"
      ], 32, True, [["blooms title 1"], ["blooms title 2"]]),
     (["This is a sample text 3", "This is the sample text 4"
      ], 32, False, [["title 1"], ["title 2"]])])
async def test_get_all_titles(texts_list, max_title_length, blooms_title,
                              expected_ouput, mocker):
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_batches",
      side_effect=lambda x, y: [x])
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_blooms_titles",
      return_value=[["blooms title 1"], ["blooms title 2"]])
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_titles",
      return_value=[["title 1"], ["title 2"]])
  output = await hc.get_all_titles(
      texts_list, max_title_length, blooms_title=blooms_title)
  assert isinstance(output, list)
  assert len(texts_list) == len(output)
  assert output == expected_ouput


@pytest.mark.parametrize("iterable, n, expected_output",
                         [(["text"] * 20, 5, [["text"] * 5] * 4),
                          (["text"] * 2, 5, [["text"] * 2] * 1),
                          (["text"] * 10, 10, [["text"] * 10] * 1)])
def test_get_batches(iterable, n, expected_output):
  batches = hc.get_batches(iterable, n)
  assert isinstance(batches, list)
  assert batches == expected_output


@pytest.mark.parametrize("texts, expected_output",
                         [(["This is sample text. ", "This is sample text 2"
                           ], "This is sample text. This is sample text 2"),
                          (["This is sample text ", "This is sample text 2"
                           ], "This is sample text. This is sample text 2")])
def test_join_texts(texts, expected_output):
  output = hc.join_texts(texts)
  assert isinstance(output, str)
  assert output == expected_output


@pytest.mark.parametrize(
    "text, mock_entities, expected_output",
    [("This is sentence1. This is sentence2", [("entity1", 1), ("entity2", 0.5),
                                               ("entity3", 1),
                                               ("entity4", 0.5)], [{
                                                   "entity": "entity1",
                                                   "salience": 1
                                               }, {
                                                   "entity": "entity2",
                                                   "salience": 0.5
                                               }, {
                                                   "entity": "entity3",
                                                   "salience": 1
                                               }, {
                                                   "entity": "entity4",
                                                   "salience": 0.5
                                               }])])
def test_get_topics(text, mock_entities, expected_output, mocker):
  mocker.patch(
      "services.clustering.hierarchical_clustering.keyterms.textrank",
      return_value=mock_entities)
  output = hc.get_topics(text)
  assert isinstance(output, list)
  assert isinstance(output[0], dict)
  assert len(output) == len(expected_output)


@pytest.mark.asyncio
@pytest.mark.parametrize("docs, mocked_compressed_text, expected_output", [([{
    "docs": "test_paragraph"
}], "summarised_text", [{
    "docs": "test_paragraph",
    "summarised_text": "summarised_text"
}])])
async def test_get_summarized_texts(docs, mocked_compressed_text,
                                    expected_output, mocker):
  mocker.patch(
      "services.clustering.hierarchical_clustering."
      "compress_text_for_title_generation",
      new_callable=AsyncMock,
      return_value=mocked_compressed_text)
  output = await hc.get_summarized_texts(docs)
  assert isinstance(output, list)
  assert output == expected_output


@pytest.mark.parametrize(
    "titles", ["comp_title", "subcomp_title", "lo_title", "lu_title"])
def test_update_titles(titles):
  topic_tree = [{
      "competency": 1,
      "title": 0,
      "sub_competencies": [{
          "title": 1,
          "learning_objectives": [{
              "title": 2,
              "learning_units":[
                  {
                      "title": 3
                  }
              ]
          }]
      }]
  }]
  output_tree = hc.add_titles_to_tree(topic_tree, titles, node_level="course")
  assert isinstance(output_tree, list)
  assert output_tree[0]["title"] == titles[0]
  assert output_tree[0]["sub_competencies"][0]["title"] == titles[1]
  assert output_tree[0]["sub_competencies"][0]["learning_objectives"][0][
      "title"] == titles[2]
  assert output_tree[0]["sub_competencies"][0]["learning_objectives"][0][
      "learning_units"][0]["title"] == titles[3]


@pytest.mark.asyncio
@pytest.mark.parametrize("docs, expected_output", [([{
    "summarised_text": "test_paragraph 1",
    "blooms_title": True
}, {
    "summarised_text": "test_paragraph 2",
    "blooms_title": False
}], ["generated_title", "generated_title"])])
async def test_generate_titles(docs, expected_output, mocker):
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_all_titles",
      new_callable=AsyncMock,
      return_value=["generated_title"])
  output = await hc.generate_titles(docs, 48)
  assert isinstance(output, list)
  assert output == expected_output


@pytest.mark.asyncio
async def test_create_recursive_topic_tree(mocker, mocked_get_topics):
  """tests create_recursive_topic_tree"""
  mocker.patch(
      "services.clustering.hierarchical_clustering.get_topics",
      return_value=mocked_get_topics)
  clustering_test_docs = [
      "Science has played a significant role as a means of "
      "generating new knowledge. Historians of science can trace "
      "the origins of a scientific method to the time of Aristotle "
      "and earlier.", "Aristotle was probably one of the first who "
      "formalized an approach to knowledge generation that involved "
      "a process of inquiry and analysis in which general principles "
      "can be formulated from what is observed (induction), and from these "
      "general principles, hypotheses can be derived that can be used to"
      "test those principles (deduction).", "The results of the tests of the "
      "hypotheses can then be used to inform theory.",
      " The cycle of induction "
      "and deduction is what is responsible for the creation of new knowledge "
      "(Gauch, 2003). In the 18th and 19th centuries, rationalism, defined as "
      "the belief that knowledge can be created through internal reflection "
      "and logic, was superseded by empiricism, the belief that what is known "
      "is that which is discoverable by the senses and ultimately measurable."
  ]
  response = await hc.create_recursive_topic_tree(
      clustering_test_docs, node_level="course", titles_flag=False)
  assert isinstance(response, list)
