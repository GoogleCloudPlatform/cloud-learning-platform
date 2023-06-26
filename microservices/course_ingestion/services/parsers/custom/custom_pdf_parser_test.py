"""Test file for custom_pdf_parser.py"""
# pylint: disable=super-init-not-called

import pytest
import fitz
from services.parsers.custom.custom_pdf_parser import CustomPdfParser
from services.parsers.custom.test_data.pdf_parser_mock_data import actual_elemets_list, \
  actual_font_counts_granularity_false, actual_styles_granularity_false, \
  actual_font_counts_granularity_true, actual_styles_granularity_true, \
  actual_size_tag_dict

# pylint: disable=unspecified-encoding


sample_path = "services/parsers/custom/test_data/Biology_test.pdf"
sample_output_filename = "output_json_biology_test"


class CustomPdfParserTest(CustomPdfParser):
  """Class def for all the CustomPdfParser functionalities."""

  def __init__(self, path, output_filename):
    self.path = path
    self.output_filename = output_filename
    self.doc = fitz.open(self.path)

@pytest.fixture(name="get_custom_pdf_parser")
def fixture_get_custom_pdf_parser():
  #returns CustomPdfParser object
  custom_parser_obj = CustomPdfParserTest(sample_path, sample_output_filename)
  return custom_parser_obj


@pytest.mark.parametrize("granularity, actual_font_counts, actual_styles", [
    (False, actual_font_counts_granularity_false,
     actual_styles_granularity_false),
    (True, actual_font_counts_granularity_true, actual_styles_granularity_true)
])
def test_fonts_usage(get_custom_pdf_parser, granularity, actual_font_counts,
                     actual_styles):
  font_counts, styles = get_custom_pdf_parser.fonts_usage(
      get_custom_pdf_parser.doc, granularity)
  assert isinstance(font_counts, list)
  assert isinstance(styles, dict)
  assert font_counts == actual_font_counts
  assert styles == actual_styles


@pytest.mark.parametrize(
    "actual_size_tag, font_counts, styles",
    [(actual_size_tag_dict, actual_font_counts_granularity_false,
      actual_styles_granularity_false)])
def test_font_tags(get_custom_pdf_parser, actual_size_tag, font_counts, styles):
  size_tag = get_custom_pdf_parser.font_tags(font_counts, styles)
  assert isinstance(size_tag, dict)
  assert size_tag == actual_size_tag


@pytest.mark.parametrize("actual_elements, size_tag",
                         [(actual_elemets_list, actual_size_tag_dict)])
def test_headers_para(get_custom_pdf_parser, actual_elements, size_tag):
  elements = get_custom_pdf_parser.headers_para(
    get_custom_pdf_parser.doc, size_tag)
  assert isinstance(elements, list)
  assert elements == actual_elements


@pytest.mark.parametrize("actual_ckg_structure", [({
    "competency": "",
    "chapter": "",
    "subChapter": "",
    "sub_competency": {
        "title": "",
        "display_type": "Sub Competency",
        "label": "",
        "learningResourcePath": "",
        "learning_objectives": {
            "title": "",
            "learning_units": []
        }
    }
})])
def test_get_structure(get_custom_pdf_parser, actual_ckg_structure):
  ckg_structure = get_custom_pdf_parser.get_structure()
  assert isinstance(ckg_structure, dict)
  assert ckg_structure == actual_ckg_structure


@pytest.mark.parametrize(
    "element, actual_element",
    [("<h7>By the end of this section, you will be able to do the following:|-",
      "By the end of this section, you will be able to do the following:")])
def test_postprocess_element(get_custom_pdf_parser, element, actual_element):
  postprocessed_element = get_custom_pdf_parser.postprocess_element(element)
  assert isinstance(postprocessed_element, str)
  assert postprocessed_element == actual_element
