# pylint: disable=unnecessary-comprehension
"""Crawler for the custom courses."""

from parsel import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import html2text
import spacy

nlp = spacy.load("en_core_web_sm")

# pylint: disable=unspecified-encoding

class CustomHtmlParser():
  """A Selenium spider to crawl an HTML course from custom."""
  url = None

  def __init__(self, url, output_filename="output.json"):
    self.url = url
    self.driver = self.create_driver()
    self.output_filename = output_filename
    self.paragraphs = []

  def create_driver(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    return driver

  def remove_heading(self, text):
    sentences = [sent for sent in nlp(text).sents]
    if len(sentences) == 1:
      return ""
    else:
      return text

  def clean_paragraphs(self, item):
    text = html2text.html2text(item)
    text = text.replace("**", "").strip("\n")
    text = text.replace("\n", " ")
    text = self.remove_heading(text)
    return text

  def get_paragraphs(self, write_to_file=True):
    self.driver.get(self.url)
    time.sleep(5)
    html = self.driver.page_source
    selector = Selector(html)
    p_list = selector.xpath("//p").getall()
    for i in p_list:
      text = self.clean_paragraphs(i)
      if text != "":
        self.paragraphs.append(text)
    if write_to_file:
      with open(self.output_filename, "w") as fp:
        json_string = json.dumps({
            "paragraphs": self.paragraphs,
        }, indent=2)
        fp.write(json_string)
    return self.paragraphs
