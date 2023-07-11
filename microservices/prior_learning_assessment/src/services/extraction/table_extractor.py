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

import json
from copy import deepcopy
from fuzzywuzzy import fuzz

# pylint: disable=broad-except

# Extract data from a table present in a form


class TableExtractor:
  """
  Extract data from a table present in the form
  """
  def __init__(self, json_path):
    self.json_path = json_path
    # master_dict --> page_num > tables > table_num > table data
    self.master_dict = {}
    self.table_list = []

    with open(json_path, encoding="utf-8") as f_obj:
      self.data = json.load(f_obj)
    self.table_attributes()

  def table_attributes(self):
    """
    This function obtains information regarding all the tables.
    For ex. total tables, table header info, table row wise data
		in dataframe format
    """
    if "pages" in self.data.keys():
      # Iterate over pages
      for pg_num, page in enumerate(self.data["pages"]):

        page_data = {}
        if "tables" in page.keys():

          # Iterate over tables
          for table_num, table in enumerate(page["tables"]):

            # extract header(columns)
            if "bodyRows" in table and "headerRows" in table:
              for _, hrow in enumerate(table["headerRows"]):
                header_row = [
                  TableExtractor.get_text(
                    cell["layout"], self.data) for cell in hrow["cells"]
                ]
                columns = []
                for val, conf in header_row:
                  if val is None:
                    tup = (val, conf)
                    columns.append(tup)
                  else:
                    tup = (" ".join(val.split()), conf)
                    columns.append(tup)
                table_data = {"headers": columns}
                table_data["page_num"] = pg_num
                col_data = {}
                try:
                  for row_num, row in enumerate(table["bodyRows"]):
                    row_data = [
                        TableExtractor.get_text(
                          cell["layout"], self.data) for cell in row["cells"]
                    ]
                    for i_col in range(len(header_row)):
                      entity_val, conf = row_data[i_col]
                      col_data[i_col] = {
                        "value": entity_val,
                        "extraction_confidence": conf
                      }
                    table_data[row_num] = {"rows": deepcopy(col_data)}

                except ValueError as e:
                  print(e)
                  return "Table Empty !!!"

              page_data[table_num] = table_data
              # page_data["height"] = page["dimension"]["height"]
              # page_data["width"] = page["dimension"]["width"]
          self.master_dict[pg_num] = page_data

          print("Checking the tabel extractor")

          #This code converts the  dict to a simpler list format
          final = []
          for pg_num,page in self.master_dict.items():
            for table_num, table in page.items():
              obj = {}
              obj["table_id"] = table_num
              obj["header_data"] = table["headers"]
              obj["row_data"] = []
              for key, rows in table.items():
                if(key not in ["headers","page_num"]):
                  row_arr = []
                  for _ , cell in rows.items():
                    print("Inside the final loop")
                    for _ , row_val in cell.items():
                      value= row_val["value"]
                      confidence = row_val["extraction_confidence"]
                      tup= (value,confidence)
                      row_arr.append(tup)
                    print("Appending the row_arr")
                    obj["row_data"].append(row_arr)
              final.append(obj)
          print(final)
          self.table_list = final
    else:
      print("no data found in table")
      return None

  @staticmethod
  def get_text(el, data):
    """Convert text offset indexes into text snippets."""
    text = ""
    # Span over the textSegments
    if "textAnchor" in el.keys():
      if "textSegments" in el["textAnchor"].keys():
        for segment in el["textAnchor"]["textSegments"]:
          # Check for startIndex. If not present = 0
          if "startIndex" in segment.keys():
            start_index = segment["startIndex"]
          else:
            start_index = 0
          # Check for endIndex. If not present = 0
          if "endIndex" in segment.keys():
            end_index = segment["endIndex"]
          else:
            end_index = 0
          text += data["text"][int(start_index) : int(end_index)]
          text= text.strip().replace("\n", " ")
          cell_conf = el["confidence"]
          cell_coordinates = el["boundingPoly"]["normalizedVertices"]
          coordinates = []
          for bb_cord in cell_coordinates:
            coordinates.append(deepcopy(bb_cord["x"]))
            coordinates.append(deepcopy(bb_cord["y"]))

    if text in ("", None):
      text = cell_conf = coordinates = None
    return (text, cell_conf)

  @staticmethod
  def compare_lists(master_list, sub_list):
    """Compare two list and return the avg match percentage

    Args:
        list1 (list): list with items
        list2 (list): list with items
    """
    def x(l):
      return l in master_list

    matched = list(filter(x, sub_list))
    return len(matched)/len(master_list)

  @staticmethod
  def get_table_using_header(page, inp_header):
    """uses the page info to extract the table

    Args:
        page (dict): dict that contains a table info
        inp_header (list): list of column names to
				 match with the header of a table
    """
    for pg_num in page:
      for table_num in page[pg_num]:
        if isinstance(table_num, int):
          table_dict = page[pg_num][table_num]
          table_header = [val[0] for val in table_dict["headers"]]
          if TableExtractor.compare_lists(table_header, inp_header) >= 0.70:
            return table_dict, table_header
          else:
            continue
    print("Input headers does not match up to 70% with any table.")
    return None

  def filter_table(self, table_entities):
    """
    Filter our the required prior learning tables from the larger list
    Args: Table_entities: table ehaders and sub_headers to choose the tables
    Return: List of filtered tables
    """
    req_tables = []
    for table in self.table_list:
      header_flag = 0
      sub_header_flag = 0
      for _,head in enumerate(table["header_data"]):
        for header in table_entities["header_list"]:
          #rule 1
          if fuzz.ratio(header, head[0]) > 50:
            header_flag = header_flag + 1
      if header_flag == 0 :
        for _, sub_tab in enumerate(table["row_data"][0]):
          for sub_header in table_entities["header_list"]:
            #rule 2
            if fuzz.ratio(sub_header, sub_tab[0]) > 50:
              sub_header_flag = sub_header_flag +1

      if header_flag>0 or sub_header_flag >0:
        req_tables.append(table)
    return req_tables

  def course_extract(self,final_tables_list,table_entities):
    """
    Extract prior experiene data from the filtered tables
    Args: fitlered lsit of tables, and req entitites to be extracted from table
    Return: List of prior experiences
    """
    all_data = []
    for table in final_tables_list:
      data = {}
      data["keys"] = []
      data["values"] = []
      data["confidence"] = []
      for header in table["header_data"]:
        for entity in table_entities["req_entities"]:
          if fuzz.ratio(entity, header[0]) > 90:
            index = table["header_data"].index(header)
            data["keys"].append(header[0])
            key_value = []
            conf_value = []
            for val in table["row_data"]:
              key_value.append(val[0])
              conf_value.append(val[1])
            data["values"].append(key_value)
            data["confidence"].append(conf_value)

      #if no headers have the req entities- possibly the sub-headers might have
      if len(data["keys"]) == 0:
        for sub_header in table["row_data"][0]:
          for entity in table_entities["req_entities"]:
            if fuzz.ratio(entity, sub_header[0]) > 90:
              index = table["row_data"][0].index(sub_header)
              data["keys"].append(sub_header[0])
              key_value = []
              conf_value = []
              for val in table["row_data"][1:]:
                key_value.append(val[index][0])
                conf_value.append(val[index][1])
              data["values"].append(key_value)
              data["confidence"].append(conf_value)

      all_data.append(data)
    return all_data
