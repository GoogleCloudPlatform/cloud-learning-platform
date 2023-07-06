"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# This script is for postprocessing the extracted OCR output.
# The configuration file for the script is config.py

# The post processing script handles the following:
# 1. Cleans any noise in the extracted value.
# 2. Converts a value to its upper case
# 3. Converts a value to its lower case.
# 3. Change date format.
# 4. Removes extra spaces in extracted value.
# 5. Corrects extracted value to string.
# 6. Corrects extracted value to number.

# For date formats user can use below symbols:
# %d Day of the month as a zero-padded decimal number eg.01, 02, …, 31
# %b Month as locale’s abbreviated name eg.Jan, Feb, …, Dec (en_US);
# %B Month as locale’s full name eg.January, February, …, December (en_US);
# %m Month as a zero-padded decimal number eg:01, 02, …, 12
# %y Year without century as a zero-padded decimal number eg:00, 01, …, 99
# %Y Year with century as a decimal number eg:0001, 0002, …,
# 2013, 2014, …, 9998, 9999
# eg: 03/04/2022 is '%m/%d/%y'

import re
import datetime
from datetime import datetime
from services.extraction.config import (STR_TO_NUM_DICT, NUM_TO_STR_DICT,
  CLEAN_VALUE_DICT, LOWER_TO_UPPER_LIST, UPPER_TO_LOWER_LIST, CLEAN_SPACE_LIST,
  DATE_FORMAT_DICT, CONVERT_TO_STRING, CONVERT_TO_NUMBER)


def list_to_string(string_list):
  """
  Function to join a list of string characters to a single string
  Input:
   string_list: list of string characters
  Output:
   str1: concatenated string
  """
  # initialize an empty string
  # traverse in the string
  return "".join(string_list)


def string_to_number(value):
  """
  Function to correct a extracted integer value
  Input:
    value: Input string
  Output:
    value: Returns corrected string
  """
  if value is None:
    pass
  else:
    # convert input string to list
    string = list(value)
    # traverse through the list
    for index, i in enumerate(string):
      # check for the match character in str_to_num template
      for k, v in STR_TO_NUM_DICT.items():
        # check if upper case match
        if i == k:
          # check if input is in lower case
          if i.islower():
            # correct the value
            string[index] = v.lower()
          else:
            # check if input is in upper case
            # correct the value
            string[index] = v.upper()

    # concatenate list to string
    value = list_to_string(string)
  return value


def number_to_string(value):
  """
  Function to correct a extracted string value
    Input:
     value: Input string
    Output:
     value: Returns corrected string
  """
  if value is None:
    pass
  else:
    # convert input string to list
    string = list(value)

    # traverse through the list
    for index, i in enumerate(string):
      # check for the match character in num_to_str template
      for k, v in NUM_TO_STR_DICT.items():
        # check if the key values match
        if i == k:
          # check if input string is in lower case
          if i.islower():
            # correct the value
            string[index] = v.lower()
          else:
            # check if input string is in upper case
            # correct the value
            string[index] = v.upper()
    # concatenate list to string
    value = list_to_string(string)
  return value


def upper_to_lower(value):
  """
  Function to convert to lower case
    Input:
      value: Input string
    Output:
      value: converted string
  """
  if value is None:
    return value
  else:
    return value.lower()


def lower_to_upper(value):
  """
  Function to convert to upper case
    Input:
      value: Input string
    Output:
      value: converted string
  """
  if value is None:
    return value
  else:
    return value.upper()


def clean_value(value, noise):
  """
  Function to clean a extracted value
   Input:
     value: Input string
       noise: Noise in the input string
    Output:
       corrected_value: corrected string without noise
  """
  if value is None:
    return value
  else:
    return value.replace(noise, "")


def clean_multiple_space(value):
  """
  Function to remove extra spaces in extracted value
  Input:
    value: Input string
  Output:
    corrected_value: corrected string removing extra spaces
  """
  if value is None:
    return value
  else:
    # create a pattern for extra space
    pattern = re.compile(r"\s{2,}")
    # replace the pattern with single space in the string
    return re.sub(pattern, " ", value)


def get_date_in_format(input_date_format, output_date_format, value):
  """
  Function to change a date format
    Input:
     input_date_format: input format of date
     output_date_format: output format of date
     value: Input date string
    Output:
      new_date: date in new format
  """
  if value is None:
    new_date = value
  else:
    try:
      # convert existing date to new date format
      new_date = datetime.strptime(value, input_date_format)\
          .strftime(output_date_format)  # 2022-02-02
    except Exception:  # pylint: disable=broad-except
      # if any error in date format no change in input date
      print("Error occurred in the date format so keeping existed date only")
      new_date = value
  return new_date


def correction_script(corrected_dict, template):
  """
  Function for correction of extracted values
    Input:
      corrected_dict:input dictionary with key value pair
      template: type of correction requested
    Output:
    corrected_dict: output dictionary with key and corrected value
  """
  # traverse through the input dictionary
  for k, v in corrected_dict.items():
    # check for template type
    if template == "clean_value":
      # check for keys in template
      for key, noise in CLEAN_VALUE_DICT.items():
        # if keys are matched
        if k == key:
          # get the noise from the template for that key
          noise = CLEAN_VALUE_DICT.get(key)
          # copy input value
          input_value = v
          # iterate th
          for i in noise:
            # call clean_value function
            corrected_value = clean_value(input_value, i)
            input_value = corrected_value
            # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "lower_to_upper":
      # check for keys in template
      for item in LOWER_TO_UPPER_LIST:
        # if keys are matched
        if k == item:
          # call lower_to_upper function
          corrected_value = lower_to_upper(v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "upper_to_lower":
      # check for keys in template
      for item in UPPER_TO_LOWER_LIST:
        # if keys are matched
        if k == item:
          # call upper_to_lower function
          corrected_value = upper_to_lower(v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "clean_multiple_space":
      # check for keys in template
      for item in CLEAN_SPACE_LIST:
        # if keys are matched
        if k == item:
          # call clean_multiple_space function
          corrected_value = clean_multiple_space(v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "date_format":
      # check for keys in template
      for key,value in DATE_FORMAT_DICT.items():
        # if keys are matched
        if k == key:
          # get key values from template
          value = DATE_FORMAT_DICT.get(key)
          # call get_date_in_format function; value[0]=input date format;
          # value[1]=output date format
          corrected_value = get_date_in_format(value[0], value[1], v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "convert_to_string":
      # check for keys in template
      for item in CONVERT_TO_STRING:
        # if keys are matched
        if k == item:
          # call number_to_string function
          corrected_value = number_to_string(v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value

    # check for template type
    if template == "convert_to_number":
      # check for keys in template
      for item in CONVERT_TO_NUMBER:
        # if keys are matched
        if k == item:
          # call string_to_number function
          corrected_value = string_to_number(v)
          # modify the input dictionary to the corrected value
          corrected_dict[k] = corrected_value
  # return corrected_dict
  return corrected_dict


def data_transformation(input_dict):
  """
  Function for data transformation
  Input:
      input_dict: input dictionary of extraction
  Output:
      input_dict: original dictionary
      temp_dict: corrected dictionary
  """
  try:
    # get a copy of input dictionary
    temp_dict = input_dict.copy()
    # traverse through input_dict
    for index, input_item in enumerate(input_dict):
      # get input dictionary
      corrected_dict = input_item.copy()
      # check for string
      corrected_dict = correction_script(corrected_dict, "convert_to_string")
      # check for number
      corrected_dict = correction_script(corrected_dict, "convert_to_number")
      # check for noise
      corrected_dict = correction_script(corrected_dict, "clean_value")
      # check for upper to lower
      corrected_dict = correction_script(corrected_dict, "upper_to_lower")
      # check for lower to upper
      corrected_dict = correction_script(corrected_dict, "lower_to_upper")
      # check for multiple spaces
      corrected_dict = correction_script(corrected_dict, "clean_multiple_space")
      # check for date format
      corrected_dict = correction_script(corrected_dict, "date_format")
      # correct input dictionary
      temp_dict[index] = corrected_dict
    return input_dict, temp_dict
  except Exception as e:  # pylint: disable=broad-except
    print(f"Error in the date tranformation postprocessing {e}")
    return None, None
