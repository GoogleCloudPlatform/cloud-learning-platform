"""learning_content inference"""

import os
import json
import shutil
from typing import Union, Any

from common.utils.gcs_adapter import download_file_from_gcs
from common.utils.logging_handler import Logger
from .parsers.custom.custom_spider import CustomSpider
from .parsers.custom.toc_spider import CustomTOCSpider
from common.models import LearningContentItem, Competency
from common.utils.errors import ResourceNotFoundException
from .parsers.openstax.openstax_spider import parse_content
from .parsers.custom.custom_pdf_parser import CustomPdfParser
from .import_learning_content import create_learning_content_collections, \
  create_clustering_learning_content_collections
from .parsers.custom.custom_html_paragraph_parser import CustomHtmlParser
from .clustering.hierarchical_clustering import create_recursive_topic_tree
from .parsers.custom.custom_pdf_paragraph_parser import CustomPdfParagraphParser
from utils.paginator import pagination
from utils.exception_handlers import LearningContentNotFound


# pylint: disable=protected-access
# pylint: disable=redefined-builtin
# pylint: disable=raise-missing-from
# pylint: disable=unspecified-encoding
# pylint: disable=broad-exception-raised


def clean_temp_folders():
  """deletes all tmp files"""
  try:
    shutil.rmtree(".tmp")
  except FileNotFoundError:
    pass
  try:
    shutil.rmtree("data")
  except FileNotFoundError:
    pass


async def create_learning_content_using_clustering(request_body):
  """creates learning_content using clustering"""
  learning_content_url = request_body["gcs_path"]
  learning_content_title = request_body["title"]
  start_page = request_body.get("start_page", 1)
  end_page = request_body.get("end_page", None)
  description = request_body.get("description", "")
  created_by = request_body.get("created_by", "")
  last_modified_by = request_body.get("last_modified_by", "")
  doc_format = request_body["format"]
  create_learning_units = request_body.get("create_learning_units", True)
  create_triples = request_body.get("create_triples", False)
  course_category = request_body.get("course_category", "")
  if doc_format.lower() in ["pdf", "epub"]:
    file_path = download_file_from_gcs(gcs_path=learning_content_url)
    paragraphs = parse_pdf_paragraph(
      file_path=file_path, start_page=start_page, end_page=end_page)
  elif doc_format.lower() == "html":
    paragraphs = parse_html_paragraphs(learning_content_url)
  else:
    raise Exception("Unsupported document format")
  titles_flag = request_body.get("titles_needed", True)
  course = await create_recursive_topic_tree(
    paragraphs, node_level="course", titles_flag=titles_flag,
    create_learning_units=create_learning_units,
    create_triples=create_triples)
  if not os.path.exists(".tmp"):
    os.makedirs(".tmp")
  with open(".tmp/topic_modelling_output_reduced_dim.json", "w") as fp:
    json_string = json.dumps(str(course), indent=2)
    fp.write(json_string)
  created_learning_content_id = create_clustering_learning_content_collections(
    learning_content_title, description, learning_content_url,
    start_page, end_page,
    doc_format.lower(),
    ".tmp/topic_modelling_output_reduced_dim.json", last_modified_by,
    created_by, create_learning_units, create_triples, course_category)
  clean_temp_folders()
  return get_learning_content(created_learning_content_id)


async def create_learning_content(request_body):
  """root function which integrates parser and content tree creation"""
  using_parser = request_body.get("using_parser", False)
  try:
    if using_parser:
      return create_learning_content_using_parser(request_body)
    else:
      return await create_learning_content_using_clustering(request_body)
  finally:
    clean_temp_folders()


def create_learning_content_using_parser(request_body):
  """creates learning content using only parser"""
  learning_content_url = request_body["gcs_path"]
  learning_content_title = request_body["title"]
  doc_format = request_body["format"]
  start_page = request_body.get("start_page", 1)
  end_page = request_body.get("end_page", None)
  created_by = request_body.get("created_by", "")
  last_modified_by = request_body.get("last_modified_by", "")
  toc_output_json = ".tmp/toc.jl"
  competency_output_json = ".tmp/output.json"
  doc_type = request_body.get("doc_type", "custom")
  course_category = request_body.get("course_category", "")
  if doc_format.lower() == "pdf":
    file_path = download_file_from_gcs(gcs_path=learning_content_url)
    parse_pdf(
      url=file_path, output_file=competency_output_json, doc_type=doc_type)

  elif doc_format.lower() == "html":
    ## TODO download files from gcs. Do we need to download an URL from GCS?
    parse_html(
      url=learning_content_url,
      output_file=competency_output_json,
      output_toc_file=toc_output_json,
      doc_type=doc_type)
  else:
    raise Exception("Unsupported document format")

  content_id = create_learning_content_collections(learning_content_title,
                                                   learning_content_url,
                                                   doc_format.lower(),
                                                   start_page, end_page,
                                                   competency_output_json,
                                                   last_modified_by, created_by,
                                                   course_category)
  clean_temp_folders()
  return get_learning_content(content_id)


def parse_pdf_paragraph(file_path, start_page=1, end_page=None):
  """extracts all paragraphs for a pdf file"""
  paragraph_parser = CustomPdfParagraphParser(
    path=file_path, start_page=start_page, end_page=end_page)
  return paragraph_parser.get_paragraphs()


def parse_html_paragraphs(url):
  """extracts all paragraphs for a html file"""
  paragraph_parser = CustomHtmlParser(url)
  return paragraph_parser.get_paragraphs()


def parse_pdf(url, output_file, doc_type):
  """handles parsing of pdf doc - used in parser alone content creation"""
  if doc_type == "custom":

    pdf_parser = CustomPdfParser(path=url, output_filename=output_file)
    pdf_parser.get_result()
  else:
    raise Exception("Pdf parser for Openstax will be released in next release")


def parse_html(url, output_file, output_toc_file, doc_type):
  """handles parsing of static and dynamic html files
  - used in parser alone content creation"""
  if doc_type == "custom":
    toc_parser = CustomTOCSpider(url=url, output_filename=output_toc_file)
    toc_parser.get_toc()
    content_parser = CustomSpider(
      url=url, toc_file=output_toc_file, output_filename=output_file)
    content_parser.parse_homepage()

  else:
    parse_content(url, output_toc_file, output_file)


def get_all_learning_contents():
  """returns all the learning_contents"""
  learning_content_list = []
  learning_contents = LearningContentItem.collection.fetch()
  if learning_contents:
    try:
      for learning_content in learning_contents:
        learning_content_dict = (
          learning_content.get_fields(reformat_datetime=True))
        learning_content_dict["id"] = learning_content.id
        competency_list = []
        learning_content.load_children()
        for competency in learning_content.competencies:
          competency_item = competency.get_fields(reformat_datetime=True)
          competency_item["id"] = competency.id
          competency_list.append(competency_item)
        learning_content_dict["competencies"] = competency_list
        learning_content_dict.pop("competency_ids", None)
        learning_content_list.append(learning_content_dict)
      return learning_content_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all learning_contents") from e
  else:
    raise ResourceNotFoundException("No learning_contents found")


def get_learning_contents(skip: int, limit: int, sort_by: str,
                          order_by: str, search_query: str) -> Union[Any, str]:
  """
  Function for get all learning contents
  :param skip: int
  :param limit: int
  :param sort_by: str
  :param order_by: str
  :param search_query: str
  :return: dict
  """
  l_contents = []
  ord_by = order_by
  if sort_by == "ascending" and order_by != "title":
    ord_by = order_by
  elif sort_by == "descending" and order_by != "title":
    ord_by = "-{}".format(order_by)

  try:
    contents = LearningContentItem.collection.order(ord_by).fetch()
    if contents:
      for content in contents:
        data = content.get_fields(reformat_datetime=True)
        data["content_id"] = content.id
        l_contents.append(data)

      if search_query is not None:
        l_contents = [content for content in l_contents if
                      search_query.lower() in content["title"].lower()]

      if sort_by == "ascending" and order_by == "title":
        l_contents = sorted(l_contents, key=lambda i: i["title"].lower())
      elif sort_by == "descending" and order_by == "title":
        l_contents = sorted(l_contents, key=lambda i: i["title"].lower(),
                            reverse=True)

      if skip >= 0 and limit > 0:
        result = pagination(payload=l_contents, skip=skip, limit=limit)
        res = {
          "data": result,
          "total_rec": len(l_contents)
        }
      elif skip < 0 or limit < 0:
        raise Exception("The skip and limit value should be a positive number")
      elif skip == 0 and limit == 0:
        return l_contents
      else:
        res = {
          "data": l_contents,
          "total_rec": len(l_contents)
        }
      return res
    else:
      raise ResourceNotFoundException("No learning_contents found")
  except Exception as e:
    Logger.error("No Learning content found: {}".format(e))
    return False


def get_learning_content(id):
  """returns learning_content details for a given learning_content id"""
  learning_content = LearningContentItem.find_by_id(id)
  try:
    learning_content_dict = (
      learning_content.get_fields(reformat_datetime=True))
    learning_content_dict["id"] = learning_content.id
    learning_content.load_children()
    competency_list = []
    for competency in learning_content.competencies:
      competency_item = competency.get_fields(reformat_datetime=True)
      competency_item["id"] = competency.id
      competency_list.append(competency_item)
    learning_content_dict["competencies"] = competency_list
    learning_content_dict.pop("competency_ids", None)
    return learning_content_dict
  except (TypeError, KeyError) as e:
    raise Exception("Failed to fetch the learning_content") from e


def validate_new_competencies(competency_ids):
  """Validates competency ids if they exist or not
  from the competency ids list"""
  for id in competency_ids:
    Competency.find_by_id(id)


def update_learning_content(id, content_request):
  """updates a given learning_content"""
  learning_content = LearningContentItem.find_by_id(id)
  try:
    learning_content_fields = learning_content.get_fields()
    for key, value in content_request.items():
      if key != "competency_ids":
        learning_content_fields[key] = value
      elif key == "competency_ids":
        validate_new_competencies(value)
        learning_content_fields[key] = list(set(value))
    for key, value in learning_content_fields.items():
      setattr(learning_content, key, value)
    learning_content.update()
    return get_learning_content(id)
  except (TypeError, KeyError) as e:
    raise Exception("Failed to update learning_content") from e


def delete_learning_content(content_id: str) -> None:
  """
  Function to Unlink all competency from the LC and Delete that LC
  Parameters
  ----------
  content_id: str
  Return
  ------
  None
  """
  try:
    content = LearningContentItem.find_by_id(content_id)
    if len(content.competency_ids) != 0:
      for comp_id in content.competency_ids:
        content.competency_ids.remove(comp_id)
        content.save()
      content.delete_by_id(content_id)
    else:
      content.delete_by_id(content_id)
  except ResourceNotFoundException as e:
    Logger.error(f"Learning content not found: {e}")
    raise LearningContentNotFound("Learning Content Is Not Found")


def add_competencies(id, request_body):
  """Updates and adds new competencies ids to learning content"""
  learning_content = LearningContentItem.find_by_id(id)
  try:
    learning_content_fields = learning_content.get_fields()
    for key, value in request_body.items():
      if key != "competency_ids":
        learning_content_fields[key] = value
    for key, value in learning_content_fields.items():
      setattr(learning_content, key, value)
    new_competency_ids = request_body.get("competency_ids", [])
    if new_competency_ids:
      existing_comp_ids = learning_content_fields["competency_ids"]
      new_competency_ids = set(new_competency_ids) - set(existing_comp_ids)
      new_competency_ids = list(new_competency_ids)
      validate_new_competencies(new_competency_ids)
      learning_content_fields["competency_ids"].extend(new_competency_ids)
      setattr(learning_content, "competency_ids",
              learning_content_fields["competency_ids"])
    learning_content.update()
    return get_learning_content(id)
  except (TypeError, KeyError) as e:
    raise Exception("Failed to update the learning content") from e
