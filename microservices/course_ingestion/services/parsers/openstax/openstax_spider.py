"""Crawler for the openstax courses."""
from twisted.internet import defer, reactor
import json
import re
import scrapy
import html2text
from scrapy.crawler import CrawlerRunner
from .toc_spider import TocSpider

# pylint: disable=unspecified-encoding

class OpenStaxSpider(scrapy.Spider):
  """A scrapy spider to crawl an HTML course from openstax.

  Attributes:
    start_urls:
    toc:
  """
  name = "openstax"

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    url = kwargs.get("url")
    toc_file = kwargs.get("toc_file")
    self.start_urls = [url]
    with open(toc_file) as json_file:
      self.toc = json.load(json_file)[0]

  def start_requests(self):
    """to start scraping a given url"""
    for url in self.start_urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    """parses content of a given url"""
    title = response.css("h1 span::text").getall()
    if title[0].startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
      x = title[0]
      chapter = str(int(float(x))) if "." in x else str(int(x))
      sub_response = response.xpath('//*[contains(text(),"the end of this \
            section, you will be able to:")]')
      if len(sub_response) != 0:
        learn_obj = sub_response[0].css("ul > li").getall()
        if len(learn_obj) != 0:
          learning_objectives = "\n".join([
              html2text.html2text(i).replace("*", "").strip() for i in learn_obj
          ])
        else:
          content = response.xpath('//div[@id="main-content"]')[0].xpath(
              '//*[contains(@class, "learning-objectives")]').css(
                  "ul > li").getall()
          if len(content) != 0:
            learning_objectives = "\n".join([
                html2text.html2text(i).replace("*", "").strip() for i in content
            ])
          else:
            learning_objectives = ""
      else:
        learning_objectives = ""

      headings = response.xpath("(//h4 | //h3)")
      learning_units = []
      for heading in headings:
        clean_paragraph = []
        paragraphs = heading.xpath("(following-sibling::p)").getall()
        str_heading = heading.xpath("string(.)").get()
        for p in paragraphs:
          clean = re.compile("<.*?>")
          clean_text = re.sub(clean, "", p)
          clean_paragraph.append(clean_text)
        if len(clean_paragraph) > 0:  # pylint: disable=g-explicit-length-test
          learning_units.append({
              "title": str_heading,
              "text": str.join("", clean_paragraph),
              "pdfTitle": "test.pdf"
          })
      if len(learning_units) > 0:  # pylint: disable=g-explicit-length-test
        clean_title = title[-1]
        unit = {
            "competency": self.toc[chapter]["unit"],
            "chapter": chapter,
            "subChapter": title[0],
            "subCompetency": {
                "title": self.toc[chapter]["chapter"],
                "display_type": "Sub Competency",
                "label": self.toc[chapter]["chapter"],
                "learningResourcePath": "test/data",
                "learningObjectives": {
                    "title": clean_title,
                    "learningUnits": learning_units,
                    "learningObjectives": learning_objectives
                }
            }
        }

        yield unit

    resp = response.xpath("//a[@aria-label='Next Page']")
    if "href" in resp.attrib:
      next_page = resp.attrib["href"]
      if next_page is not None:
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)


def parse_content(url, toc_file, output_file):
  """triggers runners in a series to parse toc and main content"""
  runner_1 = CrawlerRunner(settings={"FEEDS": {toc_file: {"format": "json"}}})
  runner_2 = CrawlerRunner(
      settings={"FEEDS": {
          output_file: {
              "format": "json"
          }
      }})

  @defer.inlineCallbacks
  def crawl():
    """serial crawler"""
    yield runner_1.crawl(TocSpider, url=url)
    yield runner_2.crawl(OpenStaxSpider, url=url, toc_file=toc_file)
    reactor.stop()

  crawl()
  reactor.run()
