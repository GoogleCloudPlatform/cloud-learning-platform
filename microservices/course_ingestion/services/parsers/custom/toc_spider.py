"""Crawler for the table of contents for the Foundations of Sociology"""

from parsel import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# pylint: disable=unspecified-encoding

class CustomTOCSpider():
  """A Selenium spider to crawl table of contents from custom."""
  url = None

  def __init__(self, url, output_filename):
    self.url = url
    self.driver = self.create_driver()
    self.toc = {}
    self.output_filename = output_filename

  def create_driver(self):
    """creates chrome web driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    return driver

  def get_toc(self):
    """returns toc"""
    self.driver.get(self.url)
    time.sleep(5)
    html = self.driver.page_source
    selector = Selector(html)
    toc = {}
    sections = selector.xpath("//nav/section")
    chapter_num = 1
    for sec in sections:
      comptency = sec.css("h3::text").get(default="")
      li_list = sec.css("li")
      for li in li_list:
        sub_comptency = li.css(".overview-list-item__title").css(
            "div::text").get(default="")
        toc[str(chapter_num)] = {
            "comptency": comptency,
            "sub_comptency": sub_comptency
        }
        chapter_num += 1
    if not os.path.exists(".tmp"):
      os.makedirs(".tmp")
    with open(self.output_filename, "w") as fp:
      json_string = json.dumps(toc, indent=2)
      fp.write(json_string)
    self.driver.quit()
