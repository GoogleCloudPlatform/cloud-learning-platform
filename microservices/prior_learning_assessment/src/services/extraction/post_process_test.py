"""Unit Test for Post Process Script"""
from services.extraction import post_process


def test_list_to_string():
  expected_result = "sample_text_1sample_text_2"
  string_list = ["sample_text_1", "sample_text_2"]
  result = post_process.list_to_string(string_list)
  assert result == expected_result


def test_string_to_number():
  expected_result = "808581"
  test_string = "BO8S8I"
  result = post_process.string_to_number(test_string)
  assert result == expected_result


def test_number_to_string():
  expected_result = "STRING"
  test_string = "5TR1NG"
  result = post_process.number_to_string(test_string)
  assert result == expected_result


def test_upper_to_lower():
  expected_result = "string"
  test_string = "STRING"
  result = post_process.upper_to_lower(test_string)
  assert result == expected_result


def test_lower_to_upper():
  expected_result = "STRING"
  test_string = "string"
  result = post_process.lower_to_upper(test_string)
  assert result == expected_result


def test_clean_value():
  expected_result = "This is a test "
  test_string = "This is a test string"
  noise = "string"
  result = post_process.clean_value(test_string, noise)
  assert result == expected_result


def test_clean_multiple_space():
  expected_result = "test string"
  test_string = "test     string"
  result = post_process.clean_multiple_space(test_string)
  assert result == expected_result


def test_get_date_in_format():
  expected_result = "2000-01-01"
  test_string = "2000-01-01"
  output_date_format = "%Y-%m-%d"
  input_date_format = "%Y-%m-%d"
  result = post_process.get_date_in_format(input_date_format,
                                          output_date_format, test_string)
  assert result == expected_result



def test_correction_script():
  expected_result = {
    "url":{"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": "textscore",
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}}

  corrected_dict = {
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": {"text": "John Smith", "score": 0.9},
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}}

  template = "convert_to_string"

  result = post_process.correction_script(corrected_dict, template)
  assert result == expected_result



def test_data_transformation():
  expected_input_dict = [{
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": {"text": "John Smith", "score": 0.9},
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}}]

  expected_temp_dict = [{
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": "TEXTSCORE",
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}
    }]

  input_dict = [{
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": {"text": "John Smith", "score": 0.9},
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}
    }]

  input_dict, temp_dict = post_process.data_transformation(input_dict)
  assert input_dict == expected_input_dict
  assert temp_dict == expected_temp_dict
