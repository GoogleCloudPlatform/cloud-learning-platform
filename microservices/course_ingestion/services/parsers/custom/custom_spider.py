"""Crawler for the custom courses."""

from parsel import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import html2text

# pylint: disable=unspecified-encoding
class CustomSpider():
  """A Selenium spider to crawl an HTML course from custom."""
  url = None

  def __init__(self, url, toc_file, output_filename):
    self.url = url
    with open(toc_file) as json_file:
      self.toc = json.load(json_file)
    self.driver = self.create_driver()
    self.output = []
    self.output_filename = output_filename

  def create_driver(self):
    """creates web driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    return driver

  def parse_homepage(self):
    """parses homepage"""
    self.driver.get(self.url)
    time.sleep(5)
    html = self.driver.page_source
    selector = Selector(html)
    resp = selector.xpath("//a[contains(@class, 'overview-list-item__link')]")
    i = 1
    for anchor in resp:
      next_page = anchor.attrib["href"]
      if next_page is not None:
        next_page = self.url + next_page.lstrip("#/")
        self.parse_content(next_page, self.toc[str(i)]["comptency"],
                           self.toc[str(i)]["sub_comptency"], i)
        i += 1

    self.driver.quit()
    with open(self.output_filename, "w") as fp:
      json_string = json.dumps(self.output, indent=2)
      fp.write(json_string)

  def parse_content(self, url, competency, sub_competency, chapter_num):
    """parses content"""
    self.driver.get(url)
    time.sleep(5)
    html = self.driver.page_source
    selector = Selector(html)
    learning_units = []
    current_lu = {"text": "", "pdfTitle": "test.pdf", "title": ""}
    learn_obj_list = selector.xpath(
        "//div[@class='block-image__paragraph brand--head "
        "brand--linkColor brand--linkColor']")
    if len(learn_obj_list) == 1:
      text = html2text.html2text(learn_obj_list[0].get())

      learn_obj = text.split("**")[-1].strip()
    else:
      learn_obj = ""
    resp = selector.xpath(
        "//div[contains(@class, 'page__content')]/section/div")
    for div in resp:
      block_process_css = div.css(".block-process")
      if block_process_css:
        continue
      impact = div.css(".block-impact")
      if impact and impact.xpath(".//text()").get() == "Did I Get This? ":
        break
      elif impact:
        continue
      heading = div.xpath(".//h2 | .//h3").xpath(".//text()").get()
      if heading:
        if len(current_lu["text"]) != 0:
          learning_units.append(current_lu)
          current_lu = {"text": "", "title": heading, "pdfTitle": "test.pdf"}
        else:
          current_lu["title"] = heading
      pargraphs = div.xpath(".//div/div/div/div/div/div/p")
      for p in pargraphs:
        if current_lu["text"] == "":
          current_lu["text"] += " ".join(p.xpath(".//text()").getall())
        else:
          current_lu["text"] += " " + " ".join(p.xpath(".//text()").getall())
    if len(current_lu["text"]) != 0:
      learning_units.append(current_lu)

    if len(learning_units) > 0:
      unit = {
          "competency": competency,
          "chapter": chapter_num,
          "subChapter": "",
          "subCompetency": {
              "title": sub_competency,
              "display_type": "Sub Competency",
              "label": sub_competency,
              "learningResourcePath": "test/data",
              "learningObjectives": {
                  "title": learn_obj,
                  "learningUnits": learning_units
              }
          }
      }
      self.output.append(unit)
