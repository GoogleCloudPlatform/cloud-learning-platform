"""Crawler for the table of contents for the Bio101 course on openstax.org."""

import scrapy
import os
import json

# pylint: disable=unspecified-encoding

class TocSpider(scrapy.Spider):
  """A scrapy spider to crawl the Table of Contents from openstax.

  Attributes:
    start_urls:
  """
  name = "toc"

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    url = kwargs.get("url")
    self.start_urls = [url]

  def start_requests(self):
    """begins parsing of single url"""
    for url in self.start_urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    """custom parser"""
    elements = [
        r.xpath("string()").get()
        for r in response.xpath("//span[contains(@class, 'styled__Summary')]")
    ]
    toc = {}
    last_unit = ""
    has_units = False
    for e in elements:
      if e[0].isdigit():
        chapter = e.split(" ")
        chapter_number = chapter[0]
        chapter_title = " ".join(chapter[1:])
        toc[chapter_number] = {"unit": last_unit, "chapter": chapter_title}
      else:
        last_unit = e
        has_units = True
    if not has_units:
      if not os.path.exists(".tmp"):
        os.makedirs(".tmp")
      elements = list(map(lambda x: " ".join(x.split()[1:]), elements))
      mapping_dict = {
          "units": [],
          "unit_chapter_mapping": [],
          "chapter_names": elements
      }
      with open(".tmp/mapping_data.json", "w") as fp:
        json_string = json.dumps(mapping_dict, indent=2)
        fp.write(json_string)
    yield toc

  @classmethod
  def from_url(cls, url):
    return cls(url)  # pylint: disable=too-many-function-args
