"""config file for parser"""

import os
import json

# ========= DocAI Parsers =======================

# To add parsers, edit /terraform/enviroments/dev/main.tf
def load_config(filename):
  with open(os.path.join(
    os.path.dirname(__file__), ".", filename), encoding="utf-8") as json_file:
    return json.load(json_file)

PARSER_CONFIG = load_config("parser_config.json")
assert PARSER_CONFIG, "Unable to locate \"parser_config.json\""

PROCESS_TIMEOUT_SECONDS = 600

# GCS temp folder to store async form parser output
DOCAI_OUTPUT_FILE_NAME = "aitutor-dev/pla/docai-output"

# Attributes not required from specialized parser raw json
DOCAI_ATTRIBUTES_TO_IGNORE = [
    "textStyles", "textChanges", "revisions", "pages.image"
]

TABLE_ENTITY_MAPPING = {
    "experience_title": ["Course", "Curriculum", "Program", "Syllabus",
        "Semester", "Subject"],
    "credits_earned": ["Credits"]
}

# Full mapping of entityes and column names, grouped by document class.
DOCAI_ENTITY_MAPPING = {
    # State or program specific docs
    "generic": {
        "transcripts": {
            "default_entities": {
                "Name": ["Name"],
                "Organization": ["Organization", "University"],
                "Experience Title": ["Experience Title"],
                "Date Graduated": ["Date Graduated"],
                "Credits Earned": ["Credits Earned"],
                "Description": ["Description"],
                "URL": ["URL"],
                "Competencies": ["Competencies"],
                "Skills": ["Skills"]
            },
            "table_entities": {
                "header_list": ["Courses", "Curriculum", "Program",
                "Syllabus", "Semester", "Subject", "Credits"],
                "req_entities" : ["Course", "Course_code", "Credit",
                "Course_Description"]
            },
            # "derived_entities": {
            #     "What is your graduation date?": {
            #         "rule":
            #         r"What is your graduation date\?\n\d\.(.*?)\((mm/dd/yyyy)"
            #     },
            #     "What is your gender?": {
            #         "rule":
            #         r"What is your gender\?\n\d\.(.*?)\n\d"
            #     }
            # }
        }
    }
}

# Post-processing related Variables
# Template to be used to convert to string(based on observation).
# The dictionary keys are the OCR extracted characters and
# dictionary values are the actual values to be populated.
NUM_TO_STR_DICT = {"8": "B", "0": "0", "1": "I", "4": "A", "5": "S"}

# Template to be used to convert to number(based on observation).
# The dictionary keys are the OCR extracted characters and
# dictionary values are the actual values to be populated.
STR_TO_NUM_DICT = {"B": "8", "O": "0", "I": "1", "A": "4", "S": "5"}

# dictionary to clean extracted values.
# eg: if input_dict={"dob":"2021-12-04\n"} then we have noise="\n"
# So we pass CLEAN_VALUE_DICT={"dob":"\n"}
# In case dob key has different noise for different document create
# CLEAN_VALUE_DICT={"dob":["noise1","noise2"]}
CLEAN_VALUE_DICT = {"dob": ["\n", "IM"], "application_apply_date": ["\n"],
                    "effective_date": ["\n"],
                    "employer_address": ["\n"], "employer_county": ["\n"],
                    "employer_name": ["\n"]}

# list for extracted values to be in upper case.
# The list items are the key names.
LOWER_TO_UPPER_LIST = ["name"]

# list for extracted values to be in lower case.
# The list items are the key names.
UPPER_TO_LOWER_LIST = ["address"]

# list to remove extra spaces in extracted values.
# The list items are the key names.
CLEAN_SPACE_LIST = ["name"]

# dictionary to update date format.
# The dictionary key values are the key field names and the
# dictionary values
# are list of two input items. first item is input_date_format and
# second item is output date format.
# DATE_FORMAT_DICT = {"dob": ["%Y-%m-%d", "%y/%m/%d"]}
DATE_FORMAT_DICT = {"dob": ["%Y-%m-%d", "%Y-%m-%d"]}
# list of key fields for which extracted values are needed to be
# corrected to string
# will be based on NUM_TO_STR_DICT
CONVERT_TO_STRING = ["name"]

# list of key fields for which extracted values are needed to be
# corrected to integer
# will be based on STR_TO_NUM_DICT.
CONVERT_TO_NUMBER = ["phone_no"]
