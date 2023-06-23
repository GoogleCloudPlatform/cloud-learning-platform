"""Base class to inherit from for custom pdf parser"""

import operator
import json
import re
import fitz
import string
import pytesseract
from PIL import Image
import io

import spacy

nlp = spacy.load("en_core_web_sm")
mat = fitz.Matrix(5, 5)  # high resolution matrix

# pylint: disable=unspecified-encoding,broad-exception-raised,simplifiable-if-statement


class CustomPdfParagraphParser():
  """Parser for extracting paragraphs from a pdf file.
    """

  def __init__(self, path, output_filename=None, start_page=1, end_page=None):
    self.path = path
    self.output_filename = output_filename
    self.doc = fitz.open(self.path)
    self.paragraphs = []
    self.start = start_page - 1
    self.end = end_page
    self.step = 1
    self.elements = []
    if (not self.end) or (self.end > self.doc.page_count):
      self.end = self.doc.page_count

  def create_json_from_pdf(self, write_to_file=False):
    """parses paragraphs from pdf and dumps content to a json"""
    font_counts, styles = self.fonts_usage(granularity=False)
    size_tag = self.font_tags(font_counts, styles)
    elements = self.get_all_elements()
    self.elements = elements[:]
    elements = self.generate_paragraph_elements(elements, size_tag)
    self.paragraphs = self.paragraphs_from_pdf(elements)
    if write_to_file:
      with open(self.output_filename, "w") as fp:
        json_string = json.dumps({
            "paragraphs": self.paragraphs,
        }, indent=2)
        fp.write(json_string)

  def get_paragraphs(self):
    """returns paragraphs"""
    self.create_json_from_pdf()
    return self.paragraphs

  def fonts_usage(self, granularity=False):
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
    for page in self.doc:
      blocks = page.getText("dict")["blocks"]
      for block in blocks:  # iterate through the text blocks
        if block["type"] == 0:  # block contains text
          for line in block["lines"]:  # iterate through the text lines
            # iterate through the text spans
            for line_span in line["spans"]:
              if granularity:
                identifier = "{0}#*#{1}#*#{2}#*#{3}".format(
                    line_span["size"], line_span["flags"], line_span["font"],
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
              font_counts[identifier] = font_counts.get(
                  identifier, 0) + 1  # count the fonts usage
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
    para_style = styles[
        font_counts[0][0]]  # get style for most used font by count (paragraph)
    para_size = para_style["size"]  # get the paragraph"s size
    # sorting the font sizes high to low,
    # so that we can append the right integer to each tag
    font_sizes = []
    for (font_size, _) in font_counts:
      font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)
    # aggregating the tags for each font size
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

  def get_ocred_text(self, page, bbox):
    """Return OCR-ed span text using Tesseract.
    Args:
        page: fitz.Page
        bbox: fitz.Rect or its tuple
    Returns:
        The OCR-ed text of the bbox.
    """
    global mat
    try:
      # Step 1: Make a high-resolution image of the bbox.
      pix = page.get_pixmap(
          colorspace=fitz.csGRAY,  # we need no color
          matrix=mat,
          clip=bbox,
      )
      image = pix.getImageData("png")  # make a PNG image
      # Step 2: Invoke Tesseract to OCR the image. Text is stored in stdout.
      text = pytesseract.image_to_string(
          Image.open(io.BytesIO(image)), config="--psm 7", lang="eng")
      text = text.strip(string.whitespace)  # remove line end characters
      return text
    except Exception as e:
      raise Exception("unable to apply OCR the image") from e

  def get_text_from_span(self, page, span):
    """Method to extract text from the line span of the page"""
    text = span["text"]
    try:
      if chr(65533) in text:  # invalid characters encountered!
        # invoke OCR
        text1 = text.lstrip()
        spaces_before = " " * (len(text) - len(text1))  # leading spaces
        text1 = text.rstrip()
        spaces_after = " " * (len(text) - len(text1))  # trailing spaces
        text = spaces_before + self.get_ocred_text(page, span["bbox"]) + \
          spaces_after
      return text
    except Exception:
      return text

  def check_is_bold_span(self, span):
    """Checks True if span contains bold text"""
    if span["flags"] > 15:
      return True
    return False

  def get_all_elements(self):
    """Iterates over all the pages in the pdf and stores all
    blocks in a single list"""
    elements = []
    for page in self.doc.pages(self.start, self.end, self.step):
      blocks = page.getText("dict")["blocks"]
      sorted_blocks = sorted(blocks, key=lambda i: i["bbox"][1])
      for block in sorted_blocks:
        if block["type"] == 0:
          block["page"] = page
          elements.append(block)
    return elements

  def get_prev_block_index(self, curr_block_index):
    """Return index of previous block if it exist"""
    if curr_block_index > 0:
      return curr_block_index - 1
    else:
      return -1

  def get_prev_line_index(self, curr_line_index):
    """Returns index of previous line if it exist"""
    if curr_line_index > 0:
      return curr_line_index - 1
    else:
      return -1

  def get_prev_span_index(self, curr_span_index):
    """Returns index of prev span if it exist"""
    if curr_span_index > 0:
      return curr_span_index - 1
    else:
      return -1

  def get_next_span(self, line, curr_span_index):
    """Return next span if it exist for a given line"""
    no_of_spans = len(line["spans"])
    if no_of_spans > curr_span_index + 1:
      if line["spans"][curr_span_index + 1].get("text","").strip():
        return line["spans"][curr_span_index + 1]
      else:
        return self.get_next_span(line, curr_span_index+1)
    else:
      return None

  def get_line_text(self, line):
    """Return text of a given line after iterating
    over all the spans"""
    line_text = ""
    for span in line["spans"]:
      span_text = span["text"]
      span_text = span_text.strip().strip("\n").strip().strip("-")
      if span_text:
        line_text += span_text
    return line_text

  def check_if_header(self, elements, b, l, ls, size_tag):
    """Checks if a line span is header text or not"""
    line_span = elements[b]["lines"][l]["spans"][ls]
    font_tag = size_tag[line_span["size"]]
    if font_tag != "<p>":
      return True
    is_span_bold = self.check_is_bold_span(line_span)
    if is_span_bold:
      prev_line_index = self.get_prev_line_index(l)
      if prev_line_index == -1:
        prev_span_index = self.get_prev_span_index(ls)
        if prev_span_index != -1:
          prev_span = elements[b]["lines"][l]["spans"][prev_span_index]
          if prev_span["is_header"]:
            return True
          else:
            return False
        else:
          next_span = self.get_next_span(elements[b]["lines"][l], ls)
          if next_span:
            is_next_span_bold = self.check_is_bold_span(next_span)
            if is_next_span_bold:
              return True
            else:
              return False
          else:
            return True
      else:
        next_span = self.get_next_span(elements[b]["lines"][l], ls)
        span_text = ""
        if next_span:
          span_text = next_span.get("text","").strip()
        if span_text:
          is_next_span_bold = self.check_is_bold_span(next_span)
          if is_next_span_bold:
            return True
          else:
            return False
        else:
          prev_line = elements[b]["lines"][prev_line_index]
          line_text = self.get_line_text(prev_line)
          if not line_text or prev_line["is_header"]:
            return True
          else:
            return False
    else:
      return False

  def generate_paragraph_elements(self, elements, size_tag):
    """Scrapes paragraphs from PDF and return texts with element tags.
          Return:
            list of texts with pre-prended element tags
          """
    raw_paragraphs = []
    prev_span = {}
    previous_origin = None
    for b, block in enumerate(elements):
      page = block["page"]
      block_string = ""
      for l, line in enumerate(block["lines"]):
        for ls, line_span in enumerate(line["spans"]):
          if ls == 0:
            line_origin = line_origin = round(line_span["origin"][0], 2)
          is_header = self.check_if_header(elements, b, l, ls, size_tag)
          ## adding info to blocks:
          elements[b]["is_header"] = is_header
          block["lines"][l]["is_header"] = is_header
          line["spans"][ls]["is_header"] = is_header

          if not is_header:
            span_text = self.get_text_from_span(page, line_span)
            if not prev_span:
              if not block_string:
                block_string = size_tag[line_span["size"]] + span_text
              elif block_string and all((c == "#") for c in block_string):
                block_string = size_tag[line_span["size"]] + span_text
              else:
                block_string += span_text
            elif prev_span and line_span["size"] == prev_span["size"]:
              if block_string and all((c == "#") for c in block_string):
                # block_string only contains pipes
                block_string = size_tag[line_span["size"]] + span_text
              elif block_string == "":
                # new block has started, so append size tag
                block_string = size_tag[line_span["size"]] + span_text
              elif previous_origin and (previous_origin < line_origin):
                raw_paragraphs.append(block_string)
                block_string = size_tag[line_span["size"]] + span_text
                previous_origin = line_origin
              else:  # in the same block, so concatenate strings
                block_string += " " + \
                    span_text
            else:
              raw_paragraphs.append(block_string)
              block_string = size_tag[line_span["size"]] + span_text
            prev_span = line_span
        previous_origin = line_origin
        block_string += "##"
      raw_paragraphs.append(block_string)
    return raw_paragraphs

  def postprocess_element(self, element):
    """Method to postprocess the element
        Args:
        element: element to postprocess
        type: string
        Returns:
        postprocessed element"""
    rx = re.compile(r"_{2,}")
    element = rx.sub("", element)
    replace_in_element = [
        "<p>", "<s1>", "<s2>", "<s3>", "<h2>", "<h3>", "<h4>", "<h7>", "-| ",
        "|", "<h5>"
    ]
    for str_to_replace in replace_in_element:
      element = element.replace(str_to_replace, "")
    return element

  def postprocess_paragraph_text(self, text):
    """post processes extracted paragraphs"""
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")
    text = text.replace("’", "'")
    text = text.replace(" ,", ",")
    rx = re.compile(r"_{2,}")
    text = rx.sub("", text)
    return text

  def is_bullet_point(self, element):
    """
        Method to check if the element is only a bullet point.
        Args:
            element: element generated by generate_paragraph_elements function
        returns:
            Boolean value
    """
    only_bullet_regex = re.compile(r"^(\d+\.|[a-z]\.|[A-Z]\.|\u2022)+")
    if re.match(only_bullet_regex, element):
      return True
    return False

  def is_bullet_sentence(self, element):
    """
        Method to check if the element has a bullet point and some text.
        Args:
            element: element generated by generate_paragraph_elements function
        returns:
            Boolean value
    """
    bullet_and_text_regex = re.compile(
        r"^(\d+\.|[a-z]\.|[A-Z]\.|\u2022)+\s*\w+")
    if re.match(bullet_and_text_regex, element):
      return True
    return False

  def refine_paragraphs(self, paragraphs):
    """
        Method to refine paragraphs
        by postprocessing and merging small paragraphs
        Args:
            paragraphs: list of
            paragraphs generated by paragraphs_from_pdf function
        returns:
            list of refined paragraphs
    """
    refined_paragraphs = []
    if paragraphs:
      refined_paragraphs = [self.postprocess_paragraph_text(paragraphs[0])]
      for i in range(1, len(paragraphs)):
        para = self.postprocess_paragraph_text(paragraphs[i])
        if len([sent.text for sent in nlp(refined_paragraphs[-1]).sents]) < 1:
          refined_paragraphs[-1] = (refined_paragraphs[-1] + " " + para).strip()
        else:
          refined_paragraphs.append(para.strip())
    return refined_paragraphs

  def paragraphs_from_pdf(self, elements):
    """Method to process elements obtained from pdf
        Args:
        elements: elements obtained from generate_paragraph_elements method
        type: list
        Returns:
        list which contains the output structure for json"""
    paragraphs = [""]
    incomplete = False
    bullet_text = False
    for _, element in enumerate(elements):
      element = element.replace("##", "")
      element = element.replace("   ", " ")
      element = element.replace("  ", " ")
      if "<p>" in element:
        element = self.postprocess_element(element)
        if not element.strip():
          continue
        try:
          if self.is_bullet_sentence(element):
            # if pymupdf detected bullet point + text as a single element
            incomplete = False
            paragraphs[-1] = paragraphs[-1] + " " + element
          elif self.is_bullet_point(element):
            # if pymupdf detected bullet point and text as seperate elements
            incomplete = False
            paragraphs[-1] = paragraphs[-1] + " " + element
            bullet_text = True
          elif bullet_text:
            paragraphs[-1] = paragraphs[-1] + " " + element
            bullet_text = False
          elif (incomplete or (not element.strip()[0].isupper())):
            if paragraphs:
              paragraphs[-1] = paragraphs[-1] + " " + element
            else:
              paragraphs.append(element)
            if element.strip()[-1] in (".", "?", "!"):
              incomplete = False
              paragraphs[-1] += "\n"
          elif element.strip()[-1] in (".", "?", "!"):
            # if current text is complete
            element += "\n"
            paragraphs.append(element)
          else:
            incomplete = True
            paragraphs.append(element)
        except Exception as e:
          print(e)
          raise Exception("parser failed in parsing the document") from e
    paragraphs = self.refine_paragraphs(paragraphs)
    return paragraphs
