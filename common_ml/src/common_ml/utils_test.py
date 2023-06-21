""""Module containing utility functions that are common in many microservices"""
#pylint: disable=wrong-import-position,line-too-long,global-variable-not-assigned
import nltk
nltk.download("stopwords")
nltk.download("wordnet")
from keybert import KeyBERT
import pytest
import numpy as np
import json
import mock
from common_ml import utils

SPACY_MODELS, MODEL_SENTENCE_RANK, MODEL_ENTITY_RANK, MODEL_STS, INFLECT_ENGINE = utils.load_utils_models(
    spacy_models=True,
    model_sentence_rank=True,
    model_entity_rank=True,
    model_sts=True,
    inflect_engine=True)

SPACY_MODEL_TYPE = "default"

@pytest.mark.parametrize(
    "text, expected_result",
    [(
      "Sociologists make use of tried and true methods of research such as "
      "experiments, surveys, and field research. They follow the scientific "
      "method. It’s true that humans and their social interactions are so "
      "diverse that they can seem impossible to chart or explain. It might "
      "seem that science is only about physical phenomena, such as chemical "
      "reactions, or about proving ideas right or wrong rather than about "
      "exploring the nuances of human behavior. However, sociologists are "
      "social scientists. They use a scientific process of research that "
      "establishes parameters to help make sure results are objective and "
      "accurate. Scientific methods provide limitations and boundaries that "
      "focus a study and organize its results. The scientific method involves "
      "developing and testing theories about the world based on empirical "
      "evidence. The basis of definition is its commitment to systematic "
      "observation of the empirical world and strives to be objective, "
      "critical, skeptical, and logical. It involves a series of prescribed "
      "steps established over centuries of scholarship. Sociologists follow "
      "the scientific method to conduct reliable, valid studies. The "
      "scientific method is a six-step process. A researcher begins by "
      "formulating a specific question about a topic. She then reads all "
      "the available published research on the subject. This collecting and "
      "reading of previous research are called a literature review. Next, the"
      " researcher develops a hypothesis, with the information collected. A "
      "hypothesis is a testable prediction of a relationship between two or "
      "more variables. It states that if a specific condition exists, then a "
      "certain effect results. A hypothesis is a causal statement, meaning "
      "that it indicates what causes something. For example, the "
      "statement “If I eat nothing but McDonald’s food for thirty days "
      "then I will gain weight” is a testable prediction regarding the impact "
      "of consuming a certain kind of food to a specific period. The "
      "researcher then carefully designs a study to test whether the "
      "hypothesis is correct. Next, she conducts that study, analyzes the "
      "data gathered, and draws conclusions based on the data. Finally, "
      "the researcher writes an article or report discussing the study, "
      "the data, and the outcomes. The material is published to share the "
      "new information. Other researchers can then analyze the research "
      "process. They may try to replicate the study. Together, all of these "
      "steps comprise the scientific method. Sociological topics do not "
      "merely reduce to right or wrong facts. In this field, results of "
      "studies tend to provide people with access to knowledge they did "
      "not have before—knowledge of other cultures, understanding of rituals "
      "and beliefs, knowledge of trends and attitudes. The scientific method "
      "relies on consistency of steps, all of which are intended to produce "
      "valid and testable results. The steps include \"Ask a "
      "question\",\"Research existing studies\",\"Formulate a "
      "hypothesis\",\"Design & conduct a study\",\"Draw "
      "conclusions\",\"Report results\".",
      ["Sociologists make use of tried and true methods of research such "
      "as experiments, surveys, and field research.",
      "It's true that humans and Sociologists social interactions are so "
      "diverse that they can seem impossible to chart or explain.",
      "It might seem that science is only about physical phenomena, such as "
      "chemical reactions, or about proving ideas right or wrong rather than "
      "about exploring the nuances of human behavior.",
      "Sociologists are social scientists.", "Sociologists use a scientific "
      "process of research that establishes parameters to help make sure "
      "results are objective and accurate.", "Scientific methods provide "
      "limitations and boundaries that focus a study and organize its "
      "results.", "The scientific method involves developing and testing "
      "theories about the world based on empirical evidence.", "The basis of "
      "definition is its commitment to systematic observation of the empirical"
      " world and strives to be objective, critical, skeptical, and logical.",
      "The basis of definition involves a series of prescribed steps "
      "established over centuries of scholarship.", "Sociologists follow the "
      "scientific method to conduct reliable, valid studies.", "A researcher "
      "begins by formulating a specific question about a topic.",
      "A researcher then reads all the available published research on the "
      "subject.", "A researcher develops a hypothesis, with the information "
      "collected.", "A hypothesis is a testable prediction of a relationship "
      "between two or more variables.", "A hypothesis states that if a "
      "specific condition exists, then a certain effect results.",
      "A hypothesis is a causal statement, meaning that it indicates what "
      "causes something.", "A researcher then carefully designs a study to "
      "test whether the hypothesis is correct.", "A researcher conducts a "
      "study , analyzes the data gathered, and draws conclusions based on "
      "the data.", "A researcher writes an article or report discussing the "
      "study, the data, and the outcomes.", "The material is published to "
      "share the new information.", "Other researchers can then analyze the "
      "research process.", "Other researchers may try to replicate a study .",
      "Sociological topics do not merely reduce to right or wrong facts.",
      "The scientific method relies on consistency of steps, all of which are "
      "intended to produce valid and testable results.", "The steps "
      "include \"Ask a question\",\"Research existing studies\",\"Formulate a "
      "hypothesis\",\"Design & conduct a study\",\"Draw "
      "conclusions\",\"Report results\"."]

      )])
def preprocess_text_for_qg(text, expected_result):
  result = utils.preprocess_text_with_coref_resolution(text)
  assert result == expected_result


@pytest.mark.parametrize("sentences,output", [([
    "The earliest leaders in the kindergarten movement transplanted "
    "Froebel’s ideas directly. ",
    "The first kindergarten in the United States was founded by Margarethe"
    " Schurz (1833–1876) in Wisconsin in 1856 (Snyder, 1972). ",
    "Schurz had studied with Froebel and, upon immigrating to the United "
    "States, started a German-speaking school to teach her own and"
    " neighbors’ children. ",
    "Later, Schurz met Elizabeth Palmer Peabody (1804–1894) and their "
    "encounter was the impetus for the American kindergarten movement. ",
    "Elizabeth Peabody was part of a well-known family of social reformers. ",
    "Her sister, Mary, was married to Horace Mann, considered to be the "
    "father of public education in the United States. ",
    "In Boston, Elizabeth Peabody organized the first English-speaking"
    " kindergarten in 1860, and soon after wrote the first American "
    "kindergarten textbook for teachers (Snyder, 1972). ",
    "She understood that teachers needed to be trained in Froebel’s"
    " philosophy to ensure the quality and integrity of the expanding "
    "kindergarten movement. ",
    "She also traveled widely and became an outspoken advocate for the"
    " cause, inspiring new generations of leaders, the most influential "
    "of whom was Susan Blow. ",
    "Susan Blow (1843–1916) was the major voice in expanding the kindergarten"
    " movement and in fighting to keep it true to Froebel’s original vision. ",
    "Inspired by Elizabeth Peabody’s promotion of kindergarten, Blow visited"
    " Froebelian kindergartens in the United States and Germany and became "
    "the leading interpreter of the approach at home. ",
    "In 1873, with the support of William Harris, a reform-minded school "
    "superintendent in St. Louis, Susan Blow founded the first public "
    "school kindergarten (Snyder, 1972) in response to Harris’s concern "
    "that schooling did not begin until age 7. ",
    "Blow was ambivalent about connecting kindergarten to public school, "
    "fearing that “the formality of the grades would seize kindergarten in "
    "its grip” ", "(Snyder, 1972, p. 66). "
], True)])
def test_bad_sentence_is_true(sentences, output):
  model_result = utils.bad_sentence_is_true(sentences)
  assert isinstance(model_result, bool)
  assert model_result == output


@pytest.mark.parametrize("words, expected_result", [("researc study", False)])
def test_check_valid_words(words, expected_result):
  result = utils.check_valid_words(words)
  assert result == expected_result


@pytest.mark.parametrize(
    "ent, expected_result",
    [("Sociological studies, surveys", ["sociological", "study", "survey"])])
def test_lemma_ent(ent, expected_result):
  result = utils.lemma_ent(ent)
  assert result == expected_result


@pytest.mark.parametrize(
    "input_1,output",
    [("The impact of Hart and Risley's Meaningful Differences in the Everyday "
      "Experiences of Young American Children on the early childhood field. The"
      " impact of the Economic Opportunity Act and the Founding of Head Start"
      " on the early childhood field. The impact of the Works Progress "
      "Administration Nurseries on the early childhood field", [
          "The impact of Hart and Risley's Meaningful Differences in the "
          "Everyday Experiences of Young American Children on the early "
          "childhood field.",
          "The impact of the Economic Opportunity Act and the Founding "
          "of Head Start on the early childhood field.",
          "The impact of the Works Progress Administration Nurseries on "
          "the early childhood field"
      ]), ("Hello_", ["Hello_"]), ("Hello.\n Hi ", ["Hello.", "Hi"]),
     ("Hello. \n", ["Hello."])])
def test_sentence_split(input_1, output):
  model_result = utils.sentence_split(input_1)
  assert isinstance(model_result, list)
  assert model_result == output


#pylint: disable=redefined-outer-name
@pytest.mark.parametrize("text, expected_result", [(
    "A conflict perspective theorist would view a social institution, such as "
    "the economy, as inherently unfair or exploitative. Inherently unfair or "
    "exploitative would examine the social institution to see how the social "
    "institution provides an advantage to some while disadvantaging, or "
    "exploiting,"
    " a different group of people. For example, a theorist working within the "
    "conflict perspective might interpret the social institution of "
    "'government' as creating laws that favor the wealthy at the expense of "
    "the impoverished.",
    [(0, "A conflict perspective theorist would view a social institution, "
      "such as the economy, as inherently unfair or exploitative.",
      1.0263695801215726),
     (2,
      "For example, a theorist working within the conflict perspective might "
      "interpret the social institution of 'government' as creating laws that "
      "favor the wealthy at the expense of the impoverished.",
      0.9835343996753529),
     (1, "Inherently unfair or exploitative would examine "
      "the social institution to see how the social institution provides an "
      "advantage to some while disadvantaging, or exploiting, a different group "
      "of people.", 0.990096344698385)])])
def test_get_ranked_sentences(text, expected_result):
  global MODEL_SENTENCE_RANK
  result = utils.get_ranked_sentences(MODEL_SENTENCE_RANK, text)
  for _, (res, exp_res) in enumerate(zip(result, expected_result)):
    assert res[0] == exp_res[0]
    assert res[1] == exp_res[1]
    np.testing.assert_almost_equal(
        res[2], exp_res[2], decimal=2, err_msg="", verbose=True)


@pytest.fixture(name="get_model")
def fixture_get_model():
  """Function to get ChooseTheFactController"""
  return KeyBERT("distilbert-base-nli-stsb-mean-tokens")


@pytest.mark.parametrize(
    "entity_list, lu_text, pos_required, expected_result",
    [({
        "sentence":
            "According to this sociological viewpoint, "
            "the elements of society are interdependent.",
        "answer": [["elements", 0], ["society", 1],
                   ["sociological viewpoint", 2]]
    },
      "A further explanation of the functionalist perspective is as the perspective"
      " that views society as a structure with interrelated parts designed to meet "
      "the biological and social needs of individuals who make up that society. "
      "According to this sociological viewpoint, the elements of society are "
      "interdependent. This means each part influences the others.A theorist "
      "working within the functionalist perspective would focus on how a "
      "particular social institution contributes to the stability of society as a "
      "whole. For example, a functionalist might interpret the social institution "
      "of \u201ceducation\u201d as promoting social stability by teaching students "
      "basic knowledge. They might also suggest that the social institution of "
      "education is crucial for teaching students how to interact with others, "
      "learn the limits of their abilities, and provide additional role models to "
      "show them their place in society. All these things will provide continuity "
      "from one generation to the next, ensuring that those capable of performing "
      "fill essential tasks.", True, [["sociological viewpoint", 0.3995, 2],
                                      ["society", 0.2727, 1],
                                      ["elements", 0.1008, 0]])])
def test_get_ranked_entities(get_model, entity_list, lu_text, pos_required,
                             expected_result):
  result = utils.get_ranked_entities(entity_list, lu_text,
                                     pos_required, get_model)
  assert result == expected_result


@pytest.mark.parametrize("filtered_clusters,tokenized_text_list,sentence_start_end,output",
  [
    ([], [
        ["Winona ", "Sample ", "(", "1917–2008", ")", ", ", "another ",
        "important ", "role ", "model ", "and ", "national ", "leader", "."],
        ["In ", "her ", "own ", "words", ", ", "“", "The ", "highlight ", "of ",
        "my ", "life ", "was ", "being ", "selected ", "as ", "the ", "vice ",
        "chair ", "of ", "the ", "International ", "Year ", "of ", "the ",
        "Child ", "(", "1979–1980", ")", "” ", "(", "Neugebauer", ", ", "1995",
        ", ", "p. ", "57", ")", "."]
    ],{0:{"start": 0, "end": 13}, 1:{"start": 14, "end": 51}}, {0:[], 1:[]}),
    ([[[0, 0], [4, 4]]], [
        ["John ", "is ", "travelling", ". "], ["He ", "likes ", "it", "."]
    ],{0:{"start": 0, "end": 3}, 1:{"start": 4, "end": 7}}, {0: [], 1: [(0, 0, "John ")]})
])
def test_convert_cluster_to_entity_list(filtered_clusters, tokenized_text_list,
                                        sentence_start_end, output):
  model_result = utils.convert_cluster_to_entity_list(filtered_clusters,
                                  tokenized_text_list, sentence_start_end)
  assert isinstance(model_result, dict)
  assert model_result == output


@pytest.mark.parametrize("filtered_clusters,text_list,sentence_start_end,output",
  [
    ([], ["Winona Sample (1917\u20132008), another important role model and "
      "national leader.", "In her own words, \u201cThe highlight of my life was"
      " being selected as the vice chair of the International Year of the "
      "Child (1979\u20131980)\u201d (Neugebauer, 1995, p. 57)."],
      {0:{"start": 0, "end": 13}, 1:{"start": 14, "end": 51}},
     ["Winona Sample (1917–2008), another important role model and national "
     "leader.", "In her own words, “The highlight of my life was being selected "
     "as the vice chair of the International Year of the Child (1979–1980)” "
     "(Neugebauer, 1995, p. 57)."]),
    ([[[0, 0], [4, 4]]],
        ["John is travelling.", "He likes it."],
      {0:{"start": 0, "end": 3}, 1:{"start": 4, "end": 7}},
      ["John is travelling.", "John likes it."]),
    ([[[0, 0], [4, 4]]],
        ["John ", "He likes it."],
      {0:{"start": 0, "end": 1}, 1:{"start": 4, "end": 7}},
    ["John", "John likes it."])
])
def test_resolve_text(filtered_clusters, text_list,
                  sentence_start_end, output):
  docs = [SPACY_MODELS[SPACY_MODEL_TYPE](text) for text in text_list]
  model_result = utils.resolve_text(filtered_clusters,
                  docs, sentence_start_end)
  assert isinstance(model_result, list)
  assert model_result == output

#pylint: disable= unused-argument
def mocked_requests_post(**kwargs):

  class MockResponse:

    def __init__(self, json_data, status_code):
      self.content = json.dumps(json_data)
      self.status_code = status_code

    def json(self):
      return self.json_data
  coref_clusters = {
    "success": True,
    "message": "All good",
    "data": {
        "prediction": [
            {
                "top_spans": [
                    [
                        0,
                        0
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        6,
                        6
                    ]
                ],
                "antecedent_indices": [
                    [
                        0,
                        1,
                        2
                    ],
                    [
                        0,
                        1,
                        2
                    ],
                    [
                        0,
                        1,
                        2
                    ]
                ],
                "predicted_antecedents": [
                    -1,
                    0,
                    -1
                ],
                "document": [
                    "John",
                    "is",
                    "travelling",
                    ".",
                    "He",
                    "likes",
                    "it",
                    "."
                ],
                "clusters": [
                    [
                        [
                            0,
                            0
                        ],
                        [
                            4,
                            4
                        ]
                    ]
                ]
            }
        ]
    }
}
  return MockResponse(coref_clusters, 200)

@mock.patch(
    "common_ml.utils.requests.post",
     mock.MagicMock(side_effect=mocked_requests_post))
@pytest.mark.parametrize(
    "text_list,output",
    [(["John is travelling. He likes it."],[[[[0, 0], [4, 4]]]])
     ])
def test_get_coref_clusters(text_list, output):
  result = utils.get_coref_clusters(text_list, "spanbert")
  assert isinstance(result, list)
  assert result == output


@pytest.mark.parametrize(
    "text,output",
    [("The impact of the Perry/High Scope Preschool Project on the early "
      "childhood field", False)])
def test_isnan(text, output):
  model_result = utils.is_nan(text)
  assert isinstance(model_result, bool)
  assert model_result == output


@pytest.mark.parametrize("lu_sentences, sent_len_thresh, output",
    [(
      ["Kindergartners who live in New York are often concerned about their "
      "body image.", "SQ3R Revisted in the next Chapter: you need to read the "
      "SQ3R reading strategy.", "SQ3R Revisted in Chapter 2, you read the "
      "SQ3R reading strategy.", "The evidence provided above is a more "
      "logical extension of the main topic.", "The For example the way in "
      "which counties operate is extremely complicated and cannot be "
      "determined by simple ways.", "In contrast, the idea of sociology is "
      "very inert and will not always make sense.", "The purpose of a "
      "narrative is to tell a story.", "These stories can be personal, "
      "creative, emotionally moving, or amusing.", "Narratives often are "
      "enjoyable to read and write because they tap into our innate ability "
      "to tell stories.", "We are all storytellers, after all, and our "
      "stories connect us to others by providing a window into a larger, "
      "universal set of experiences.", "They help us to form our identities "
      "and to make meaning of the events around us by attaching language to "
      "experience.", "To that end, a narrative may use more artistic and "
      "figurative language and provide details that are more descriptive.",
      "A narrative strives to connect directly with the reader."],
      5,
      ["Kindergartners who live in New York are often concerned about their "
      "body image.",
      "Narratives often are enjoyable to read and write because they tap into "
      "our innate ability to tell stories.", "We are all storytellers, after "
      "all, and our stories connect us to others by providing a window into a "
      "larger, universal set of experiences.",
      "They help us to form our identities and to make meaning of the events "
      "around us by attaching language to experience.",
      "To that end, a narrative may use more artistic and figurative language "
      "and provide details that are more descriptive.",
      "A narrative strives to connect directly with the reader."]
      )])
def test_sentence_selection(mocker, lu_sentences, sent_len_thresh, output):
  mocker.patch("common_ml.utils.check_pronoun", return_value=False)
  model_result = utils.sentence_selection(lu_sentences, sent_len_thresh)
  assert model_result == output



@pytest.mark.parametrize(
    "sentence_a, sentence_b, actual_result",
    [("The impact of the Perry/High Scope Preschool Project on the "
      "early childhood field",
      "The impact of the Perry Scope Preschool Project on the early "
      "childhood field", 0.9230762130182977)])
def test_ngram_wer(sentence_a, sentence_b, actual_result):
  model_result = utils.ngram_wer(sentence_a, sentence_b)
  assert isinstance(model_result, float)
  assert model_result == actual_result


@pytest.mark.parametrize(
    "original, result, output",
    [("The impact of the Perry/High Scope Preschool Project on the "
      "early childhood field",
      "The impact of the Perry Scope Preschool Project on the early "
      "childhood field", 0.06172839506172839)])
def test_cer(mocker, original, result, output):
  mocker.patch("common_ml.utils.editdistance.eval", return_value=5)
  mocker.patch("common_ml.utils.is_nan", return_value=False)
  model_result = utils.cer(original, result)
  assert isinstance(model_result, float)
  assert model_result == output


@pytest.mark.parametrize(
    "original, result, output",
    [("The impact of the Perry/High Scope Preschool Project on the "
      "early childhood field",
      "The impact of the Perry Scope Preschool Project on the early "
      "childhood field", 0.13333333333333333)])
def test_wer(original, result, output):

  model_result = utils.wer(original, result)
  assert isinstance(model_result, float)
  assert model_result == output


@pytest.mark.parametrize(
    "text, output",
    [("International Journal of Multicultural Education (IJME) is a "
      "peer-reviewed open-access journal for scholars, practitioners, "
      "and students of multicultural education.",
      "International Journal of Multicultural Education (IJME) is a "
      "peer-reviewed open-access journal for scholars, practitioners, "
      "and students of multicultural education.")])
def test_clean_text(text, output):
  model_result = utils.clean_text(text)
  assert isinstance(model_result, str)
  assert model_result == output


@pytest.mark.parametrize(
    "text,output",
    [("The earliest leaders in the kindergarten movement transplanted "
      "Froebel’s ideas directly.",
      "The Earliest Leaders In The Kindergarten Movement Transplanted "
      "Froebel’S Ideas Directly.")])
def test_make_title_case(text, output):
  model_result = utils.make_title_case(text)
  assert isinstance(model_result, str)
  assert model_result == output


@pytest.mark.parametrize("text, output",
                         [("this is a book.", "This is a book.")])
def test_first_letter_to_upper_case(text, output):
  result = utils.first_letter_to_upper_case(text)
  assert result == output


@pytest.mark.parametrize("candidates, output", [([{
    "text": "Gold rings",
    "start_idx": 0
}, {
    "text": "cow 's nose",
    "start_idx": 24
}], [{
    "text": "Gold rings",
    "start_idx": 0
}, {
    "text": "cow's nose",
    "start_idx": 24
}])])
def test_clean_candidates(candidates, output):
  function_result = utils.clean_candidates(candidates)
  assert function_result == output


@pytest.mark.parametrize("text, candidates, output",
                         [("Gold rings dangled from cow's nose.", [{
                             "text": "Gold rings",
                             "start_idx": 0
                         }, {
                             "text": "cow's nose",
                             "start_idx": 24
                         }], [{
                             "score": 0.496,
                             "start_idx": 0,
                             "text": "Gold rings"
                         }, {
                             "score": 0.6488,
                             "start_idx": 24,
                             "text": "cow's nose"
                         }])])
def test_rank_entities(text, candidates, output):
  function_result = utils.rank_entities(text, candidates)
  assert all((item in function_result for item in output))


@pytest.mark.parametrize("doc, output, mocked_output",
                         [(SPACY_MODELS[SPACY_MODEL_TYPE]("Gold rings dangled from cow's nose."), ([], [{
                             "text": "Gold rings",
                             "start_idx": 0
                         }, {
                             "text": "cow's nose",
                             "start_idx": 24
                         }]), [{
                             "text": "Gold rings",
                             "start_idx": 0
                         }, {
                             "text": "cow's nose",
                             "start_idx": 24
                         }])])
def test_generate_entities(mocker, doc, output, mocked_output):
  mocker.patch("common_ml.utils.clean_candidates", return_value=mocked_output)
  mocker.patch(
      "common_ml.utils.remove_overlapping",
      return_value=[{
          "text": "Gold rings",
          "start_idx": 0
      }, {
          "text": "cow's nose",
          "start_idx": 24
      }])
  mocker.patch(
      "common_ml.utils.remove_bracket_entities",
      side_effect=[[{
          "text": "Gold rings",
          "start_idx": 0
      }, {
          "text": "cow's nose",
          "start_idx": 24
      }], []])
  function_result = utils.generate_entities(doc)
  assert function_result == output


@pytest.mark.parametrize("text, output",
                         [("Gold rings dangled from cow's nose.", [{
                             "named_entities": [],
                             "non_named_entities": [{
                                 "score": 0.496,
                                 "start_idx": 0,
                                 "text": "Gold rings"
                             }, {
                                 "score": 0.6488,
                                 "start_idx": 24,
                                 "text": "cow's nose"
                             }],
                             "sentence": "Gold rings dangled from cow's nose."
                         }])])
def test_extract_entities(mocker, text, output):
  mocker.patch(
      "common_ml.utils.sentence_split",
      return_value=["Gold rings dangled from cow's nose."])
  mocker.patch(
      "common_ml.utils.generate_entities",
      return_value=([], [{
          "text": "Gold rings",
          "start_idx": 0
      }, {
          "text": "cow's nose",
          "start_idx": 24
      }]))
  mocker.patch(
      "common_ml.utils.rank_entities",
      return_value=[{
          "text": "Gold rings",
          "start_idx": 0,
          "score": 0.496
      }, {
          "text": "cow's nose",
          "start_idx": 24,
          "score": 0.6488
      }])
  function_result = utils.extract_entities(text)
  assert function_result == output


@pytest.mark.parametrize("entities, output", [([{
    "score": 0.3588,
    "start_idx": 56,
    "text": "anti-miscegenation law"
}, {
    "score": 0.3249,
    "start_idx": 60,
    "text": "-miscegenation law"
}, {
    "score": 0.3145,
    "start_idx": 61,
    "text": "miscegenation law"
}, {
    "score": 0.1345,
    "start_idx": 99,
    "text": "books"
}, {
    "score": 0.2873,
    "start_idx": 119,
    "text": "laws"
}], [{
    "score": 0.3588,
    "start_idx": 56,
    "text": "anti-miscegenation law"
}, {
    "score": 0.1345,
    "start_idx": 99,
    "text": "books"
}, {
    "score": 0.2873,
    "start_idx": 119,
    "text": "laws"
}])])
def test_remove_overlapping(entities, output):
  function_result = utils.remove_overlapping(entities)
  assert function_result == output


@pytest.mark.parametrize(
    "sentence, actual_output",
    [("My car is in the drive (with the window open).", [(23, 44)])])
def test_get_bracket_array(sentence, actual_output):
  function_result = utils.get_bracket_array(sentence)
  assert function_result == actual_output


@pytest.mark.parametrize(
    "question, answer, output",
    [("What type of nematodes are present in all habitats?", "Nematodes", True),
     ("What Greek word is Nematoda derived from?", "Nemos", False)])
def test_answer_in_question(question, answer, output):
  result = utils.answer_in_question(question, answer)
  assert result == output


@pytest.mark.parametrize("entities, sentence, output", [([{
    "text": "car",
    "start_idx": 3
}, {
    "text": "drive",
    "start_idx": 17
}, {
    "text": "window",
    "start_idx": 33
}], "My car is in the drive (with the window open).", [{
    "text": "car",
    "start_idx": 3
}, {
    "text": "drive",
    "start_idx": 17
}])])
def test_remove_bracket_entities(mocker, entities, sentence, output):
  mocker.patch("common_ml.utils.get_bracket_array", return_value=[(23, 44)])
  function_result = utils.remove_bracket_entities(entities, sentence)
  assert function_result == output

@pytest.mark.parametrize("text, expected_output", [(
  ["Developing writers can often benefit from examining an essay, a paragraph, "
  "or even a sentence to determine what makes it effective. On the following "
  "pages are several paragraphs for you to evaluate on your own, along with "
  "the Writing Center's explanation."],
  ([["Developing writers can often benefit from examining an essay, a paragraph, "
  "or even a sentence to determine what makes it effective. On the following "
  "pages are several paragraphs for you to evaluate on your own, along with "
  "the Writing Center's explanation."]], False)
)])
def test_split_large_paragraphs(text, expected_output):
  result = utils.split_large_paragraphs(text)
  assert result == expected_output


@pytest.mark.parametrize("text_list, merge_index, expected_output", [(
[["Developing writers can often benefit from examining an essay, a paragraph, "
  "or even a sentence to determine what makes it effective."],
  ["On the following "
  "pages are several paragraphs for you to evaluate on your own, along with "
  "the Writing Center's explanation."]],
  [[0, 0, 1, True]],
  [["Developing writers can often benefit from examining an essay, a paragraph,"
  " or even a sentence to determine what makes it effective.",
  "On the following "
  "pages are several paragraphs for you to evaluate on your own, along with "
  "the Writing Center's explanation."]]
)])
def test_merge_split_paragraphs(text_list, merge_index, expected_output):
  result = utils.merge_split_paragraphs(text_list, merge_index)
  assert result == expected_output
