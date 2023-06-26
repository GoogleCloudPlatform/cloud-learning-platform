"""Test file for custom_pdf_paragraph_parser.py"""
import sys
import pytest
from services.parsers.custom.custom_pdf_paragraph_parser import CustomPdfParagraphParser
from services.parsers.custom.test_data.pdf_paragraph_parser_mock_data import actual_output_json_list, actual_elemets_list, \
  actual_font_counts_granularity_false, actual_styles_granularity_false, \
  actual_font_counts_granularity_true, actual_styles_granularity_true, \
  actual_size_tag_dict

sys.path.append("../../common/src/")
LOCAL_FOLDER = "test_data"
sample_path = "services/parsers/custom/test_data/Biology_test.pdf"
sample_output_filename = "output_json_biology_test"

# pylint: disable=unspecified-encoding


@pytest.fixture(name="get_custom_pdf_paragraph_parser")
def fixture_get_custom_pdf_paragraph_parser():
  #returns BasePdfParser object
  parser_obj = CustomPdfParagraphParser(sample_path, sample_output_filename)
  parser_obj.get_paragraphs()
  return parser_obj


@pytest.mark.parametrize("granularity, actual_font_counts, actual_styles", [
    (False, actual_font_counts_granularity_false,
     actual_styles_granularity_false),
    (True, actual_font_counts_granularity_true, actual_styles_granularity_true)
])
def test_fonts_usage(get_custom_pdf_paragraph_parser, granularity,
                     actual_font_counts, actual_styles):
  font_counts, styles = get_custom_pdf_paragraph_parser.fonts_usage(granularity)
  assert isinstance(font_counts, list)
  assert isinstance(styles, dict)
  assert font_counts == actual_font_counts
  assert styles == actual_styles


@pytest.mark.parametrize(
    "actual_size_tag, font_counts, styles",
    [(actual_size_tag_dict, actual_font_counts_granularity_false,
      actual_styles_granularity_false)])
def test_font_tags(get_custom_pdf_paragraph_parser, actual_size_tag,
                   font_counts, styles):
  size_tag = get_custom_pdf_paragraph_parser.font_tags(font_counts, styles)
  assert isinstance(size_tag, dict)
  assert size_tag == actual_size_tag


@pytest.mark.parametrize("actual_elements, size_tag",
                         [(actual_elemets_list, actual_size_tag_dict)])
def test_generate_paragraph_elements(get_custom_pdf_paragraph_parser,
                                     actual_elements, size_tag):
  elements = get_custom_pdf_paragraph_parser.generate_paragraph_elements(
      get_custom_pdf_paragraph_parser.elements, size_tag)
  assert isinstance(elements, list)
  assert elements == actual_elements


@pytest.mark.parametrize(
    "element, actual_element",
    [("<h5>By the end of this section, you will be able to do the following:|",
      "By the end of this section, you will be able to do the following:")])
def test_postprocess_element(get_custom_pdf_paragraph_parser, element,
                             actual_element):
  postprocessed_element = get_custom_pdf_paragraph_parser.postprocess_element(
      element)
  assert isinstance(postprocessed_element, str)
  assert postprocessed_element == actual_element


@pytest.mark.parametrize("actual_output_list, elements",
                         [(actual_output_json_list, actual_elemets_list)])
def test_paragraphs_from_pdf(get_custom_pdf_paragraph_parser,
                             actual_output_list, elements):
  output_json_list = get_custom_pdf_paragraph_parser.paragraphs_from_pdf(
      elements)
  assert isinstance(output_json_list, list)
  assert output_json_list == actual_output_list


@pytest.mark.parametrize(
    "element, actual_element",
    [("By the end of “this section”, you will be able to do the following",
      "By the end of \"this section\", you will be able to do the following")])
def test_postprocess_paragraph_text(get_custom_pdf_paragraph_parser, element,
                                    actual_element):
  postprocessed_element = \
    get_custom_pdf_paragraph_parser.postprocess_paragraph_text(
      element)
  assert isinstance(postprocessed_element, str)
  assert postprocessed_element == actual_element


@pytest.mark.parametrize("input_text, expected_output",
                         [("• ", True), ("Sample text", False)])
def test_is_bullet_point(get_custom_pdf_paragraph_parser, input_text,
                         expected_output):
  postprocessed_element = get_custom_pdf_paragraph_parser.is_bullet_point(
      input_text)
  assert isinstance(postprocessed_element, bool)
  assert postprocessed_element == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [("• ", False), ("Sample text", False),
     ("• Identify the shared characteristics of the natural sciences", True),
     ("1. Identify the shared characteristics of the natural sciences", True)])
def test_is_bullet_sentence(get_custom_pdf_paragraph_parser, input_text,
                            expected_output):
  postprocessed_element = get_custom_pdf_paragraph_parser.is_bullet_sentence(
      input_text)
  assert isinstance(postprocessed_element, bool)
  assert postprocessed_element == expected_output


@pytest.mark.parametrize(
    "input_text_list, expected_output",
    [(["This is a short paragraph.____", "This is a long paragraph."
      ], ["This is a short paragraph.", "This is a long paragraph."])])
def test_refine_paragraphs(get_custom_pdf_paragraph_parser, input_text_list,
                           expected_output):
  postprocessed_element = get_custom_pdf_paragraph_parser.refine_paragraphs(
      input_text_list)
  assert isinstance(postprocessed_element, list)
  assert postprocessed_element == expected_output
