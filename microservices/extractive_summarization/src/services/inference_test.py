"""Module for unit testing the inference script"""
import pytest

from summarizer.coreference_handler import CoreferenceHandler  #pylint: disable=unused-import
from summarizer.model_processors import Summarizer, TransformerSummarizer  #pylint: disable=unused-import
from services import inference


@pytest.fixture()
def get_summarizer():
  """Function to return the summarizer model"""
  return Summarizer(
      model="distilbert-base-uncased", hidden=-2, reduce_option="mean")

@pytest.fixture(name="get_parser")
def fixture_get_parser():
  """Function to return the object of class parser"""
  Parser_obj = inference.Parser
  return Parser_obj


@pytest.mark.parametrize("inputs, output", [
    ({
        "data": """The buyer is RFR Holding, a New York real estate company.""",
        "ratio": 1,
        "min_length": 5,
        "max_length": 500
    }, {
        "summary":
            """The buyer is RFR Holding, a New York real estate company."""
    }),
    ({
        "data": """Apple""",
        "ratio": 1,
        "min_length": 5,
        "max_length": 500
    }, {
        "summary":
            "Apple"
    }),
    ({
        "data": """Apple""",
        "ratio": 0.5,
        "min_length": 5,
        "max_length": 500
    }, {
        "summary":
            ""
    }),
    ])
def test_summarize_text(inputs, output, get_summarizer):  #pylint: disable=redefined-outer-name
  """Unit testing for summarize function"""
  result = inference.summarize_text(inputs, get_summarizer)
  assert output == result

@pytest.mark.parametrize("inputs, outputs", [(
  "Plastic is a non-biodegradable synthetic material which is toxic. \
  This consumption of the disposed of plastic leads to various health \
problems.",
    [
  " Plastic is a non-biodegradable synthetic material which is toxic.",
  "This consumption of the disposed of plastic leads to various health \
problems."
    ])])
def test_run(get_parser, inputs, outputs):
  """Unit testing for function run part of class Parser"""
  result = get_parser(inputs).run()
  assert result == outputs

@pytest.mark.parametrize("inputs, outputs", [
    ("Plastic is a non-biodegradable synthetic material which is toxic. \
This consumption of the disposed of plastic leads to various health \
problems.",
    ("Plastic is a non-biodegradable synthetic material which is toxic. \
This consumption of the disposed of plastic leads to various health \
problems.", True))
])
def test_convert_to_paragraphs(get_parser, inputs, outputs):
  """Unit testing of function convert_to_paragraphs part of class Parser"""
  result = get_parser(inputs).convert_to_paragraphs()
  assert result == outputs
