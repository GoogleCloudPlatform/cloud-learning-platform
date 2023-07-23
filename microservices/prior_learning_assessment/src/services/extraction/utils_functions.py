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
# pylint: disable=invalid-name
import os
import re
from datetime import datetime
import pandas as pd
import numpy as np
from copy import deepcopy
from functools import reduce
from fuzzywuzzy import process
from collections import ChainMap
from google.cloud import storage
from schemas.prior_experience_schema import PriorExperienceModel
from routes.prior_experience import create_prior_experience
from services.extraction.config import TABLE_ENTITY_MAPPING
from services.extraction.table_extractor import TableExtractor

# This script has all the common and re-usable functions
# required for extraction framework


def pattern_based_entities(parser_data, pattern):
  """
  Function return matched text as per pattern
  Parameters
  ----------
  parser_data: text in which pattern is applied
  pattern : pattern
  Returns: Extracted text by using pattern
  -------
  """
  text = parser_data["text"]
  pattern = re.compile(pattern, flags=re.DOTALL)
  # match as per pattern
  matched_text = re.search(pattern, text)
  if matched_text:
    op = matched_text.group(1)
  else:
    op = None
  return op


def update_confidence(dupp, without_noise):
  for key in dupp.keys():
    for i in without_noise:
      if i["key"] == key:
        i["value_confidence"] = 0.0
  return without_noise


def check_duplicate_keys(dictme, without_noise):
  """
  Function to check duplicate keys
  Args:
     dictme: string
     without_noise: dict
  Returns:
    bool

  """
  # dictme is the mapping dictionary
  # without_noise is the raw dictionary which comes from Form parser
  dupp = {}
  for k, v in dictme.items():
    if len(v) > 1:
      dupp[k] = len(v)
  for k, v in dupp.items():
    count = 0
    for i in without_noise:
      if i["key"] == k:
        count = count + 1
    #remove this later
    count = 0
    if count != v:
      without_noise = update_confidence(dupp, without_noise)
      return False
  return True


def default_entities_extraction(parser_entities, default_entities,doc_type):
  """
   This function extracted default entities
   Parameters
   ----------
   parser_entities: Specialized parser entities
   default_entities: Default entites that need to extract from parser entities
   Returns : Default entites dict
   -------
  """
  parser_entities_dict = {}

  # retrieve parser given entities
  for each_entity in parser_entities:
    key, val, confidence = each_entity.get("type", ""), \
                           each_entity.get("mentionText", ""), round(
      each_entity.get("confidence", 0), 2)
    val = strip_value(val)
    parser_entities_dict[key] = [val, confidence]

  entity_dict = {}

  # create default entities
  for key in default_entities:
    if key in parser_entities_dict:
      entity_dict[default_entities[key][0]] = {
                 "entity": default_entities[key][0],
                 "value": parser_entities_dict[key][0],
                 "extraction_confidence": parser_entities_dict[key][1],
                 "manual_extraction": False,
                 "corrected_value": None}
    else:
      entity_dict[default_entities[key][0]] = {
                 "entity": default_entities[key][0], "value": None,
                 "extraction_confidence": None,
                 "manual_extraction": False,
                 "corrected_value": None}
  if doc_type == "utility_bill":
    if "supplier_address" in parser_entities_dict:
      if parser_entities_dict["supplier_address"][0] == "":
        if "receiver_address" in parser_entities_dict \
        and parser_entities_dict["receiver_address"][0]!="":
          entity_dict["reciever address"]["value"] = \
          parser_entities_dict["receiver_address"][0]
        else:
          if "service_address" in parser_entities_dict:
            entity_dict["reciever address"]["value"] = \
            parser_entities_dict["service_address"][0]
  return entity_dict


def name_entity_creation(entity_dict, name_list):
  """
    This function is to create name from Fname and Gname.
    Can be re-used if it helps
    Parameters
    ----------
    entity_dict: extracted entities dict
    name_list: list of varibles required to create name
    Returns : derived name entitity dict
    -------
  """
  name = ""
  confidence = 0
  # loop through all the name variables used for name creation
  for each_name in name_list:
    parser_extracted_name = entity_dict[each_name]["value"]
    if parser_extracted_name:
      name += parser_extracted_name
      confidence += entity_dict[each_name]["extraction_confidence"]

  if name.strip():
    name = name.strip()
    confidence = round(confidence / len(name_list), 2)
  else:
    name = None
    confidence = None

  name_dict = {
      "entity": "Name", "value": name,
       "extraction_confidence": confidence,
       "manual_extraction": False,
        "corrected_value": None}

  return name_dict


def derived_entities_extraction(parser_data, derived_entities):
  """
    This function extract/create derived entities based on config
    derived entity section
    Parameters
    ----------
    parser_data: text in which pattern is applied
    derived_entities: derived entities dict and pattern
    Returns: derived entities dict
    -------
  """
  derived_entities_extracted_dict = {}

  # loop through derived entities
  for key, val in derived_entities.items():
    pattern = val["rule"]
    pattern_op = pattern_based_entities(parser_data, pattern)
    pattern_op = strip_value(pattern_op)
    derived_entities_extracted_dict[key] = \
        {"entity": key, "value": pattern_op,
            "extraction_confidence": None,
            "manual_extraction": True,
            "corrected_value": None,
            "value_coordinates": None,
            "key_coordinates": None,
            "page_no": None,
            "page_width": None,
            "page_height": None
            }
  return derived_entities_extracted_dict


def entities_extraction(parser_data, required_entities, doc_type):
  """
    This function reads information of default and derived entities
    Parameters
    ----------
    parser_data: specialzed parser result
    required_entities: required extracted entities
    doc_type: Document type
    Returns: Required entities dict
    -------
  """
  # Read the entities from the processor
  parser_entities = parser_data["entities"]
  default_entities = required_entities["default_entities"]
  derived_entities = required_entities.get("derived_entities")
  # Extract default entities
  entity_dict = default_entities_extraction(parser_entities,
                                            default_entities,doc_type)
  print("Default entities created from Specialized parser response")
  # if any derived entities then extract them
  if derived_entities:
    # this function can be used for all docs, if derived entities
    # are extracted by using regex pattern
    derived_entities_extracted_dict = derived_entities_extraction\
        (parser_data, derived_entities)
    entity_dict.update(derived_entities_extracted_dict)
    print("Derived entities created from Specialized parser response")
  return entity_dict


def check_int(d):
  """
    This function check given string is integer
    Parameters
    ----------
    d: input string
    Returns: True/False
    -------
  """
  count = 0
  date_val = ""
  for i in d:
    if i and (i.strip()).isdigit():
      count = count + 1
      date_val += str(i.strip())
  flag = ((count >= 2) and (len(date_val) < 17))
  return flag


def consolidate_coordinates(d):
  """
    This function create co-ordinates for groupby entities
    Parameters
    ----------
    d: entity co-ordinates list

    Returns: List of co-ordinates
    -------
  """
  entities_cooridnates = []
  if len(d)>1:
    for i in d:
      if i:
        entities_cooridnates.append(i)
    if entities_cooridnates:
      entity_coordinates = [entities_cooridnates[0][0],
                           entities_cooridnates[0][1],
                           entities_cooridnates[-1][6],
                             entities_cooridnates[0][1],
                           entities_cooridnates[0][0],
                           entities_cooridnates[-1][7],
                             entities_cooridnates[-1][6],
                           entities_cooridnates[-1][7]]
      final_coordinates = [float(i) for i in entity_coordinates]
    else:
      final_coordinates = None

    return final_coordinates
  else:
    if d.values[0]:
      return [float(i) for i in d.values[0]]
    else:
      return None


def standard_entity_mapping(desired_entities_list, parser_name):
  """
    This function changes entity name to standard names and also
                create consolidated entities like name and date
    Parameters
    ----------
    desired_entities_list: List of default and derived entities
    parser_name: name of the parser

    Returns: Standard entities list
    -------
  """
  # convert extracted json to pandas dataframe
  df_json = pd.DataFrame.from_dict(desired_entities_list)
  # read entity standardization csv
  entity_standardization = os.path.join(
        os.path.dirname(__file__), ".", "entity-standardization.csv")
  entities_standardization_csv = pd.read_csv(entity_standardization)
  entities_standardization_csv.dropna(how="all", inplace=True)

  # Keep first record incase of duplicate entities
  entities_standardization_csv.drop_duplicates(subset=["entity"]
                                               , keep="first", inplace=True)
  entities_standardization_csv.reset_index(drop=True)

  # Create a dictionary from the look up dataframe/excel which has
  # the key col and the value col
  dict_lookup = dict(
        zip(entities_standardization_csv["entity"],
            entities_standardization_csv["standard_entity_name"]))
  # Get( all the entity (key column) from the json as a list
  key_list = list(df_json["entity"])
  # Replace the value by creating a list by looking up the value and assign
  # to json entity
  for index,item in enumerate(key_list):
    if item in dict_lookup:
      df_json["entity"][index]=dict_lookup[item]
    else:
      df_json = df_json.drop(index)
      df_json.reset_index(inplace=True, drop=True)
  # convert datatype from object to int for column "extraction_confidence"
  df_json["extraction_confidence"] = pd.to_numeric\
      (df_json["extraction_confidence"],errors="coerce")
  group_by_columns = ["value", "extraction_confidence", "manual_extraction",
                      "corrected_value", "page_no",
                        "page_width", "page_height", "key_coordinates",
                      "value_coordinates"]
  df_conc = df_json.groupby("entity")[group_by_columns[0]].apply(
        lambda x: "/".join([v.strip() for v in x if v]) if check_int(x)
        else " ".join([v.strip() for v in x if v])).reset_index()

  df_av = df_json.groupby(["entity"])[group_by_columns[1]].mean().\
      reset_index().round(2)
  # taking mode for categorical variables
  df_manual_extraction = df_json.groupby(["entity"])[group_by_columns[2]]\
      .agg(pd.Series.mode).reset_index()
  df_corrected_value = df_json.groupby(["entity"])[group_by_columns[3]]\
      .mean().reset_index().round(2)
  if parser_name == "FormParser":
    df_page_no = df_json.groupby(["entity"])[group_by_columns[4]].mean()\
        .reset_index().round(2)
    df_page_width = df_json.groupby(["entity"])[group_by_columns[5]].mean()\
        .reset_index().round(2)
    df_page_height = df_json.groupby(["entity"])[group_by_columns[6]].mean()\
        .reset_index().round(2)
    # co-ordinate consolidation
    df_key_coordinates = df_json.groupby("entity")[group_by_columns[7]].apply(
      consolidate_coordinates).reset_index()
    df_value_coordinates = df_json.groupby("entity")[group_by_columns[8]].apply(
      consolidate_coordinates).reset_index()
    dfs = [df_conc, df_av, df_manual_extraction, df_corrected_value,
           df_page_no, df_page_width, df_page_height,
       df_key_coordinates, df_value_coordinates]
  else:
    dfs = [df_conc, df_av, df_manual_extraction, df_corrected_value]

  df_final = reduce(lambda left, right: pd.merge(left, right, on="entity"), dfs)
  df_final = df_final.replace(r"^\s*$", np.nan, regex=True)
  df_final = df_final.replace({np.nan: None})
  extracted_entities_final_json = df_final.to_dict("records")
  print("Entities standardization completed")
  return extracted_entities_final_json


def form_parser_entities_mapping(form_parser_entity_list, mapping_dict,
                                 form_parser_text, json_folder):
  """
    Form parser entity mapping function

    Parameters
    ----------
    form_parser_entity_list: Extracted form parser entities before mapping
    mapping_dict: Mapping dictionary have info of default, derived entities
            along with desired keys

    Returns: required entities - list of dicts having entity, value, confidence
            and manual_extraction information
    -------
  """
  # extract entities information from config files
  default_entities = mapping_dict.get("default_entities")
  derived_entities = mapping_dict.get("derived_entities")
  table_entities = mapping_dict.get("table_entities")
  flag = check_duplicate_keys(default_entities, form_parser_entity_list)

  df = pd.DataFrame(form_parser_entity_list)
  key_list = df["key"].tolist()
  required_entities_list = []
  # loop through one by one default entities mentioned in the config file
  for each_ocr_key, each_ocr_val in default_entities.items():
    idx_list = []
    for val in each_ocr_val:
      extracted_one = process.extractOne(val, key_list)
      if extracted_one[1] >= 90:
        idx_list = df.index[df["key"] == extracted_one[0]].tolist()
        break

    if idx_list:
      temp_dict = {
          "entity": each_ocr_key, "value": df["value"][idx_list[0]],
          "extraction_confidence": float(df["value_confidence"]
                                        [idx_list[0]]),
          "manual_extraction": False,
          "corrected_value": None,
          "value_coordinates": [float(i) for i in df["value_coordinates"]
                                          [idx_list[0]]],
          "key_coordinates": [float(i) for i in df["key_coordinates"]
                                        [idx_list[0]]],
          "page_no": int(df["page_no"][idx_list[0]]),
          "page_width": int(df["page_width"][idx_list[0]]),
          "page_height": int(df["page_height"][idx_list[0]])
        }
    else:
      # filling null value if parser didn't extract
      temp_dict = {
        "entity": each_ocr_key,
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      }
    required_entities_list.append(temp_dict)
  print("Default entities created from Form parser response")
  if derived_entities:
    # this function can be used for all docs, if derived entities
    # are extracted by using regex pattern
    parser_data = {}
    parser_data["text"] = form_parser_text
    derived_entities_op_dict = derived_entities_extraction(parser_data,
                                                           derived_entities)
    required_entities_list.extend(list(derived_entities_op_dict.values()))
    print("Derived entities created from Form parser response")

  #Print statements mentioned in this section needs to be removed after
  #integration of the tabel extracted values into the function's return value
  if table_entities:
    table_response = None
    files = os.listdir(json_folder)
    for json_file in files:
      json_path = os.path.join(json_folder, json_file)
      table_extract_obj = TableExtractor(json_path)
      final_table_list = table_extract_obj.filter_table(table_entities)
      print("Filtered list of tables")
      print(final_table_list)
      table_response = table_extract_obj.course_extract(final_table_list,\
        table_entities)
      print("Extracted course details")
      print(table_response)
      #validating if there is atleast one prior experinece that was extracted
      if table_response and table_response[0]["keys"]:
        extracted_entities = extract_entities_from_table_response(
          table_response)
        if extracted_entities:
          required_entities_list.extend(extracted_entities)
          required_entities_list = separate_out_PE(required_entities_list)
          break
      else:
        print("No experience data found from tables")

  if not all(isinstance(item, list) for item in required_entities_list):
    required_entities_list = [required_entities_list]
  print("Checking final entity list after addition of table data")
  print(required_entities_list)
  return required_entities_list, flag


def separate_out_PE(extracted_entities):
  """
  Method to separate PE (Prior Experiences) based on Experience Title,
  Credits Earned

  Args:
    extracted_entities (list): List of entities extracted from PDF.

  Returns:
    separated_entities (list of dict): List of individual PEs
  """
  experience_titles = []
  credits_earned = []
  separated_entities = []
  entities = deepcopy(extracted_entities)
  for item in extracted_entities:
    if item["entity"] == "experience_title" and item["value"]:
      experience_titles = list(
        zip(item["value"], item["extraction_confidence"]))
      entities.remove(item)
    if item["entity"] == "credits_earned" and item["value"]:
      credits_earned = list(zip(item["value"], item["extraction_confidence"]))
      entities.remove(item)
  for index, experience_title in enumerate(experience_titles):
    entities_temp = deepcopy(entities)
    for entity in entities_temp:
      if entity["entity"] == "Experience Title":
        entity["value"] = experience_title[0]
        entity["extraction_confidence"] = experience_title[1]
      if entity["entity"] == "Credits Earned":
        entity["value"] = credits_earned[index][0]
        entity["extraction_confidence"] = credits_earned[index][1]
    separated_entities.append(entities_temp)
  return separated_entities


def extract_entities_from_table_response(table_response):
  """
  Method to extract entities (experience_title, credits_earned) from
  table_response.

  Args:
    table_response (dict): keys and values extracted from tables.

  Returns:
    res_list (list): list containing dict of "experience_title" and
                    "credits_earned".
  """
  experience_titles = {
    "entity": "experience_title",
    "value": [],
    "extraction_confidence": []
  }
  credits_earned = {
    "entity": "credits_earned",
    "value": [],
    "extraction_confidence": []
  }
  res_list = []
  for response in table_response:
    for index, key in enumerate(response["keys"]):
      if key in TABLE_ENTITY_MAPPING["experience_title"]:
        experience_titles["value"].extend(response["values"][index])
        experience_titles["extraction_confidence"].extend(
          response["confidence"][index])
      if key in TABLE_ENTITY_MAPPING["credits_earned"]:
        credits_earned["value"].extend(response["values"][index])
        credits_earned["extraction_confidence"].extend(
          response["confidence"][index])
  if experience_titles["value"]:
    res_list.append(experience_titles)
  if credits_earned["value"]:
    res_list.append(credits_earned)
  return res_list


def download_pdf_gcs(bucket_name=None, gcs_uri=None, file_to_download=None,
                     output_filename=None) -> str:
  """
    Function takes a path of an object/file stored in GCS bucket and
            downloads the file in the current working directory

    Args:
        bucket_name (str): bucket name from where file to be downloaded
        gcs_uri (str): GCS object/file path
        output_filename (str): desired filename
        file_to_download (str): gcs file path excluding bucket name.
            Ex: if file is stored in X bucket under the folder Y with
            filename ABC.txt
            then file_to_download = Y/ABC.txt
    Return:
        pdf_path (str): pdf file path that is downloaded from the
                bucket and stored in local
  """
  if bucket_name is None:
    bucket_name = gcs_uri.split("/")[2]
  # if file to download is not provided it can be extracted from the GCS URI
  if file_to_download is None and gcs_uri is not None:
    file_to_download = "/".join(gcs_uri.split("/")[3:])
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(file_to_download)
  # save file, if output path provided
  if output_filename:
    with open(output_filename, "wb") as file_obj:
      blob.download_to_file(file_obj)
  return blob


def clean_form_parser_keys(text):
  """
    Cleaning form parser keys
    Parameters
    ----------
    text: original text before noise removal - removed spaces, newlines
    Returns: text after noise removal
    -------
  """
  # removing special characters from beginning and end of a string
  try:
    if len(text):
      text = text.strip()
      text = text.replace("\n", " ")
      text = re.sub(r"^\W+", "", text)
      last_word = text[-1]
      text = re.sub(r"\W+$", "", text)
      if last_word in [")", "]"]:
        text += last_word

  except: # pylint: disable=bare-except
    print("Exception occurred while cleaning keys")
  return text


def del_gcs_folder(bucket, folder):
  """
  This function is to delete folder from gcs bucket, this is used to
   delete temp folder from bucket
  Parameters
  ----------
  bucket: Bucket name
  folder: Folder name inside bucket
  Returns : None
  -------
  """
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket)
  blobs = bucket.list_blobs(prefix=folder)
  for blob in blobs:
    blob.delete()


def strip_value(value):
  """
  Function for default cleaning of values to remove space at end and begining
  and '\n' at end
  Input:
       value: Input string
  Output:
       corrected_value: corrected string without noise
  """
  if value is None:
    corrected_value = value
  else:
    corrected_value = value.strip()
    corrected_value = corrected_value.replace("\n", " ")
  return corrected_value


def extract_form_fields(doc_element: dict, document: dict):
  """
   # Extract form fields from form parser raw json
    Parameters
    ----------
    doc_element: Entitiy
    document: Extracted OCR Text

    Returns: Entity name and Confidence
    -------
  """
  response = ""
  list_of_coordidnates = []
  # If a text segment spans several lines, it will
  # be stored in different text segments.
  for segment in doc_element.text_anchor.text_segments:
    start_index = (
      int(segment.start_index)
      if segment in doc_element.text_anchor.text_segments
      else 0
    )
    end_index = int(segment.end_index)
    response += document.text[start_index:end_index]
  confidence = doc_element.confidence
  coordinate = list([doc_element.bounding_poly.normalized_vertices])
  for item in coordinate:
    for xy_coordinate in item:
      list_of_coordidnates.append(float(round(xy_coordinate.x, 4)))
      list_of_coordidnates.append(float(round(xy_coordinate.y, 4)))
  return response, confidence, list_of_coordidnates


def get_doc_type(gcs_uri_list: list):
  """
  This is a modular function that is used to classify a doc into a particular
  type.
  Currently this is just classifying the document type, but downstream
  this function will be developed into a doc classifcation module
  """
  res = []
  for gcs_uri in gcs_uri_list:
    pos = gcs_uri.rfind(".")
    pos = pos + 1
    doc_type = gcs_uri[pos:len(gcs_uri)]
    res.append(doc_type)
  return res


  # Methods for formatting response

  # Input json format
  # json=[{
  #       "entity": "name",
  #       "value": "Kathr1n    marie",
  #       "key_confidence": 1.0,
  #       "value_confidence": 1.0
  #   },
  #   {
  #       "entity": "dob",
  #       "value": "2022-jan-09\n",
  #       "key_confidence": 1.0,
  #       "value_confidence": 1.0
  #   },
  #   {
  #       "entity": "phone_no",
  #       "value": "123A",
  #       "key_confidence": 1.0,
  #       "value_confidence": 1.0
  #   },
  #   {
  #       "entity": "address",
  #       "value": "XYZ",
  #       "key_confidence": 1.0,
  #       "value_confidence": 1.0
  #   },
  #   ]

def get_json_format_for_processing(input_json):
  """Function to change list of dictionary json format to key value mapping
        dictionary
  Input:
    input_json: input json with list of dictionary format
  Output:
    new_json: list of key value mapping dictionary"""

  a = input_json
  new_list = []
  # for dictionary in input json
  for i in a:
    # get list of keys for the dictionary
    a = {}
    # create a dictionary from input dictionary
    a[i.get("entity")] = {
      "text": i.get("value"),
      "score": i.get("extraction_confidence")
    }
    # append the new dictionary in a list
    new_list.append(a)
  res = {}
  # convert list to dictionary
  res = dict(ChainMap(*new_list))
  # get new_json as list of dictionary
  new_json = [res]
  return new_json


def correct_json_format_for_db(output_dict, input_json):
  """Function to add a list of dictionary for key value mapping
       to input list of dictionary json
  Input:
    output_dict: list of dictionary with key value mapping
    input_json: list of dictionary json
  Output:
    input_json: list of dictionary json"""
  # traverse input json
  for item in input_json:
    # traverse the keys in dictionary
    for entity in output_dict[0].keys():
      # if keys are matched
      if item.get("entity") == entity:
        # reassign input json value to new one
        item["value"] = output_dict[0][entity]
  return input_json


def save_prior_experience_items(extracted_items):
  """saves extracted prior experience items in Firestore collection"""
  for item in extracted_items:
    experience_title = item["experience_title"]["text"]
    description = item["description"]["text"]
    date_completed = item["date_completed"]["text"]
    credits_earned = item["credits_earned"]["text"]
    url = item["url"]["text"]
    organization = item["organization"]["text"]
    skills = item["skills"]["text"]
    competencies = item["competencies"]["text"]

    prior_experience_item = PriorExperienceModel()
    if experience_title:
      prior_experience_item.experience_title = experience_title
    if description:
      prior_experience_item.description = description
    if date_completed:
      try:
        date_completed = datetime.strptime(date_completed, "%b %d, %Y")
        prior_experience_item.date_completed = date_completed
      except ValueError:
        pass
    if credits_earned:
      prior_experience_item.credits_earned = float(credits_earned)
    if url:
      prior_experience_item.url = url
    if organization:
      prior_experience_item.organization = organization
    if skills:
      prior_experience_item.skills = skills
    if competencies:
      prior_experience_item.competencies = competencies

    _ = create_prior_experience(prior_experience_item)
