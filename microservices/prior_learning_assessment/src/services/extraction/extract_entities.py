# pylint: disable=broad-except
"""
This is the main file for extraction framework, based on \
doc type specialized parser or form parser functions will be called
"""

import traceback
import os
import re
import shutil
import random
import string
from collections import ChainMap
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from services.extraction.post_process import data_transformation
from services.extraction.utils_functions import (extract_form_fields,
    del_gcs_folder, form_parser_entities_mapping, clean_form_parser_keys,
    standard_entity_mapping, strip_value, get_doc_type,
    get_json_format_for_processing)
from services.extraction.config import (DOCAI_OUTPUT_FILE_NAME, PARSER_CONFIG,
                          DOCAI_ENTITY_MAPPING, PROCESS_TIMEOUT_SECONDS)


def form_parser_extraction(parser_details: dict, gcs_doc_path: str,
                           doc_class: str, context: str, timeout: int):
  """
  This is form parser extraction main function. It will send
  request to parser and retrieve response and call
    default and derived entities functions

  Parameters
    ----------
    parser_details: It has parser info like parser id, name, location, and etc
    gcs_doc_path: Document gcs path
    doc_class: Document class - transcript, certificate, badges, etc
    context: context name- set to generic for now; going down it can be used
    for extracting more context
    timeout: Max time given for extraction entities using async form parser API

  Returns: Form parser response - list of dicts having entity, value,
    confidence and manual_extraction information.
    -------
  """

  location = parser_details["location"]
  processor_id = parser_details["processor_id"]
  opts = {}

  # Location can be 'us' or 'eu'
  if location == "eu":
    opts = {"api_endpoint": "eu-documentai.googleapis.com"}

  client = documentai.DocumentProcessorServiceClient(client_options=opts)
  # create a temp folder to store parser op, delete folder once processing done
  # call create gcs bucket function to create bucket,
  # folder will be created automatically not the bucket
  gcs_output_uri = f"gs://{DOCAI_OUTPUT_FILE_NAME}"
  letters = string.ascii_lowercase
  temp_folder = "".join(random.choice(letters) for i in range(10))
  gcs_output_uri_prefix = "temp_" + temp_folder
  # temp folder location
  destination_uri = f"{gcs_output_uri}/{gcs_output_uri_prefix}/"
  print("Destination folder")
  print(destination_uri)
  gcs_documents = documentai.GcsDocuments(documents=[{
      "gcs_uri": gcs_doc_path,
      "mime_type": "application/pdf"
  }])
  input_config = documentai.BatchDocumentsInputConfig(
    gcs_documents=gcs_documents)
  # Temp op folder location
  output_config = documentai.DocumentOutputConfig(
      gcs_output_config={"gcs_uri": destination_uri})

  print(f"input_config = {input_config}")
  print(f"output_config = {output_config}")
  print(f"processor_id = {processor_id}")

  # request for Doc AI
  request = documentai.types.document_processor_service.BatchProcessRequest(
      name=processor_id,
      input_documents=input_config,
      document_output_config=output_config,
  )
  operation = client.batch_process_documents(request)
  # Wait for the operation to finish
  operation.result(timeout=timeout)

  # Results are written to GCS. Use a regex to find
  # output files
  match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
  output_bucket = match.group(1)
  prefix = match.group(2)

  print(f"output_bucket: {output_bucket}")
  print(f"prefix: {prefix}")

  storage_client = storage.Client()
  bucket = storage_client.get_bucket(output_bucket)
  blob_list = list(bucket.list_blobs(prefix=prefix))
  extracted_entity_list = []
  form_parser_text = ""
  # saving form parser json, this can be removed from pipeline
  if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
  # browse through output jsons
  for i, blob in enumerate(blob_list):
    # If JSON file, download the contents of this blob as a bytes object.
    if ".json" in blob.name:
      blob_as_bytes = blob.download_as_bytes()
      # saving the parser response to the folder, remove this while integration
      # parser_json_fname = "temp.json"
      parser_json_fname = os.path.join(temp_folder, f"res_{i}.json")
      with open(parser_json_fname, "wb") as file_obj:
        blob.download_to_file(file_obj)

      document = documentai.types.Document.from_json(blob_as_bytes)
      form_parser_text += document.text
      # Read the text recognition output from the processor
      # pylint: disable=not-an-iterable
      for page in document.pages:
        for field in page.form_fields:
          field_name, field_name_confidence, field_coordinates = \
              extract_form_fields(field.field_name, document)
          field_value, field_value_confidence, value_coordinates = \
              extract_form_fields(field.field_value, document)
          # noise removal from keys and values
          field_name = clean_form_parser_keys(field_name)
          field_value = strip_value(field_value)
          temp_dict = {
              "key": field_name,
              "key_coordinates": field_coordinates,
              "value": field_value,
              "value_coordinates": value_coordinates,
              "key_confidence": round(field_name_confidence, 2),
              "value_confidence": round(field_value_confidence, 2),
              "page_no": int(page.page_number),
              "page_width": int(page.dimension.width),
              "page_height": int(page.dimension.height)
          }

          print(temp_dict)
          extracted_entity_list.append(temp_dict)

      print("Extraction completed")
    else:
      print(f"Skipping non-supported file type {blob.name}")

  # Get corresponding mapping dict, for specific context or fallback to "all"
  mapping_dict = DOCAI_ENTITY_MAPPING.get(context).get(doc_class)

  print(f"context = {context}")
  print(f"doc_class = {doc_class}")
  print(f"mapping_dict = {mapping_dict}")

  # Extract desired entites from form parser
  try:
    form_parser_entities_list, _ = form_parser_entities_mapping(
        extracted_entity_list, mapping_dict, form_parser_text, temp_folder)
    print("Form parser list of entities extracted")

    # delete temp folder
    if os.path.exists(temp_folder):
      shutil.rmtree(temp_folder)
    fold = DOCAI_OUTPUT_FILE_NAME + gcs_output_uri_prefix
    del_gcs_folder(gcs_output_uri.split("//")[1].split("/")[0], fold)

    print("Required entities created from Form parser response")
    return form_parser_entities_list

  except Exception as e:
    print(e)
    print(traceback.print_exc())
    if os.path.exists(temp_folder):
      shutil.rmtree(temp_folder)


def extract_entities(gcs_doc_path_list: list, doc_class: str, context: str):
  """
  This function calls specialed parser or form parser depending on document type

  Parameters
  ----------
  gcs_doc_path: Document gcs path
  doc_class: Type of documents. Ex: unemployment_form, driver_license, and etc
  context: context

  Returns
  -------
    List of dicts having entity, value, confidence and
           manual_extraction information.
    Extraction accuracy
  """
  # read parser details from configuration json file
  output = []
  doc_type_list = get_doc_type(gcs_doc_path_list)
  for index, doc_type in enumerate(doc_type_list):
    gcs_doc_path = gcs_doc_path_list[index]
    parsers_info = PARSER_CONFIG
    parser_information = parsers_info.get(doc_type).get(doc_class)
    # if parser present then do extraction else update the status
    if parser_information:
      parser_name = parser_information["parser_name"]
      parser_type = parser_information["parser_type"]

      if parser_type == "FORM_PARSER_PROCESSOR":
        print(f"Form parser extraction started for this document: {doc_class}")
        desired_entities_list = form_parser_extraction(parser_information,
          gcs_doc_path, doc_class, context, PROCESS_TIMEOUT_SECONDS)
      else:
        print("Specialized parser extraction needed for this doc")

      # calling standard entity mapping function to standardize the entities
      final_extracted_entities = []
      for entities in desired_entities_list:
        mapped_entities = standard_entity_mapping(entities, parser_name)
        # calling post processing utility function
        # input json is the extracted json file after your mapping script
        result_dict = get_json_format_for_processing(mapped_entities)
        result_dict, _ = data_transformation(result_dict)
        final_extracted_entities.append(dict(ChainMap(*result_dict)))

      print(final_extracted_entities)

      print(f"Extraction completed for this document: {doc_class}")
      for res in final_extracted_entities:
        output.append(res)
    else:
      # Parser not available
      print(f"Parser not available for this document: {doc_class}")
      output = None
  return output
