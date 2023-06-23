"""Pdf parser for custom pdf resource"""

import operator
import json
import fitz
import os

# pylint: disable=unspecified-encoding

class CustomPdfParser():
  """A pdf parser to get output in a sturctured json ."""
  path = None

  def __init__(self, path, output_filename):
    self.path = path
    self.output_filename = output_filename
    self.output_json_list = self.create_elements()
    if not os.path.exists(".tmp"):
      os.makedirs(".tmp")
    with open(self.output_filename, "w") as fp:
      json_string = json.dumps(self.output_json_list, indent=2)
      fp.write(json_string)

  def get_result(self):
    """returns result"""
    return self.output_json_list

  def create_elements(self):
    """extracts elements from the parsed output"""
    doc = fitz.open(self.path)
    font_counts, styles = self.fonts_usage(doc, granularity=False)
    size_tag = self.font_tags(font_counts, styles)
    elements = self.headers_para(doc, size_tag)
    output_json_list = self.process_elements_pdf(elements)
    return output_json_list

  def fonts_usage(self, doc, granularity=False):
    """Extracts fonts and their usage in PDF documents.
    Args:
      doc: PDF document to iterate through
      type doc: <class "fitz.fitz.Document">
      granularity: also use "font", "flags" and "color" to discriminate text
      type granularity: bool
    Return:
      most used fonts sorted by count, font style information
      rtype: [(font_size, count), (font_size, count}], dict
    """
    styles = {}
    font_counts = {}

    for page in doc:
      blocks = page.getText("dict")["blocks"]
      for block in blocks:
        if block["type"] == 0:
          for line in block["lines"]:
            for line_span in line["spans"]:
              if granularity:
                identifier = "{0}_{1}_{2}_{3}".format(line_span["size"],
                                                      line_span["flags"],
                                                      line_span["font"],
                                                      line_span["color"])
                styles[identifier] = {
                    "size": line_span["size"],
                    "flags": line_span["flags"],
                    "font": line_span["font"],
                    "color": line_span["color"]
                }
              else:
                identifier = "{0}".format(line_span["size"])
                styles[identifier] = {
                    "size": line_span["size"],
                    "font": line_span["font"]
                }

              font_counts[identifier] = font_counts.get(identifier, 0) + 1

    font_counts = sorted(
        font_counts.items(), key=operator.itemgetter(1), reverse=True)

    if len(font_counts) < 1:
      raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles

  def font_tags(self, font_counts, styles):
    """Returns dictionary with font sizes as keys and tags as value.
      Args:
        font_counts: (font_size, count) for all fonts occuring in document
        type font_counts: list
        styles: all styles found in the document
        type styles: dict
      Return:
        a dict of all element tags based on font-sizes
      """
    para_style = styles[font_counts[0][0]]
    para_size = para_style["size"]
    font_sizes = []
    for (font_size, _) in font_counts:
      font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)

    idx = 0
    size_tag = {}
    for size in font_sizes:
      idx += 1
      if size == para_size:
        idx = 0
        size_tag[size] = "<p>"
      if size > para_size:
        size_tag[size] = "<h{0}>".format(idx)
      elif size < para_size:
        size_tag[size] = "<s{0}>".format(idx)

    return size_tag

  def headers_para(self, doc, size_tag):
    """Scrapes headers & paragraphs from PDF and return texts with element tags.
      Args:
        doc: PDF document to iterate through
        type doc: <class "fitz.fitz.Document">
        size_tag: textual element tags for each size
        type size_tag: dict
      Return:
        list of texts with pre-prended element tags
      """
    header_para = []
    first = True
    previous_span = {}
    for page in doc:
      blocks = page.getText("dict")["blocks"]
      sorted_blocks = sorted(blocks, key=lambda i: i["bbox"][1])
      for block in sorted_blocks:
        if block["type"] == 0:
          block_string = ""
          for line in block["lines"]:
            for line_span in line["spans"]:
              if line_span["text"].strip():
                if first:
                  previous_span = line_span
                  first = False
                  block_string = size_tag[line_span["size"]] + line_span["text"]
                else:
                  if line_span["size"] == previous_span["size"]:

                    if block_string and all((c == "|") for c in block_string):
                      block_string = size_tag[
                          line_span["size"]] + line_span["text"]
                    if block_string == "":
                      block_string = size_tag[
                          line_span["size"]] + line_span["text"]
                    else:
                      block_string += " " + line_span["text"]

                  else:
                    header_para.append(block_string)
                    block_string = size_tag[
                        line_span["size"]] + line_span["text"]

                  previous_span = line_span

            block_string += "|"

          header_para.append(block_string)

    return header_para

  def get_structure(self):
    """Method to return structure as dictionary"""
    return {
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
    }

  def postprocess_element(self, element):
    """Method to postprocess the element
    Args:
      element: element to postprocess
      type: string
    Returns:
      postprocessed element"""
    replace_in_element = [
        "<p>", "<s1>", "<s2>", "<s3>", "<h2>", "<h3>", "<h4>", "<h7>", "-| ",
        "- ", "|"
    ]
    for str_to_replace in replace_in_element:
      element = element.replace(str_to_replace, "")
    if element[-1] == "-":
      element = element[:-1]
    return element

  def find_competency(self, toc, element):
    """Method to find to name of
      competency for the element(subcompetency)
      Args:
        toc: table of content
        type: list of dictionary[{"competency1":[subcomp_1, subcomp_2]},
                                {"competency2":[subcomp_1, subcomp_2]}]
        element: element containing name of subcompetency
        type: string
      Returns:
        name of competency found from toc"""

    for comp_dict in toc:
      for sub_comps in comp_dict.values():
        for sub_comp in sub_comps:
          if sub_comp in element:
            return list(comp_dict.keys())[0]
    return ""

  def process_elements_pdf(self, elements):
    """Method to process elements obtained from pdf
      Args:
        elements: elements obtained from headers_para method
        type: list
      Returns:
        list which contains the output structure for json"""

    output_json_list = []
    subcompetencies = []
    toc = []
    on_subcom_level = False
    word_incomp = False
    for i, element in enumerate(elements):
      element = element.replace("|", "")
      element = element.replace("   ", " ")
      element = element.replace("  ", " ")
      if "<h2>" in element:
        if "Content" in element:
          count = 0
          for count_element in elements[i + 1:]:
            count += 1
            if "<h2>" in count_element:
              break
          for toc_element in elements[i:i + count + 1]:
            if "<h7>" in toc_element:
              toc_element = self.postprocess_element(toc_element)
              toc_element = toc_element.split(":")[1].strip()
              toc.append({toc_element: []})
            elif "<s1>" in toc_element and "Chapter" in toc_element:
              toc_element = toc_element.split(":")[1].strip()
              toc_element = self.postprocess_element(toc_element)
              toc[-1][list(toc[-1].keys())[0]].append(toc_element)

          for j in toc:
            subcompetencies.append(list(j.values())[0])
          subcompetencies = [j for i in subcompetencies for j in i]

        elif any(x in element for x in subcompetencies):
          structure = self.get_structure()
          competency = self.find_competency(toc, element)
          structure["competency"] = competency
          structure["sub_competency"]["title"] = self.postprocess_element(
              element)
          structure["sub_competency"]["label"] = self.postprocess_element(
              element)
          on_subcom_level = True
          output_json_list.append(structure)
      elif (("<h3>" in element) or ("<h4>" in element)) and on_subcom_level:
        lu_dict = {"text": "", "title": ""}
        lu_dict["title"] = self.postprocess_element(element)
        output_json_list[-1]["sub_competency"]["learning_objectives"][
            "learning_units"].append(lu_dict)
      elif ("<p>" in element) or ("<s3>" in element):
        element = element.strip()
        try:
          prev = output_json_list[-1]["sub_competency"]["learning_objectives"][
              "learning_units"][-1]["text"]
          if ("." in prev[-5:]) or ("?" in prev[-5:]) or (":" in prev[-5:]):
            append_to_text = "\n"
          else:
            if word_incomp:
              append_to_text = ""
            else:
              append_to_text = " "
          word_incomp = bool("-" in element[-5:])
          element = self.postprocess_element(element)
          output_json_list[-1]["sub_competency"]["learning_objectives"][
              "learning_units"][-1]["text"] = output_json_list[-1][
                "sub_competency"]["learning_objectives"]["learning_units"][-1][
                      "text"] + append_to_text + element
        except:  # pylint: disable=bare-except
          pass
    return output_json_list
