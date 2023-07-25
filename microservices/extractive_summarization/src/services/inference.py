"""Module to get output response from Summarizer API"""
from typing import List
import nltk
from summarizer import Summarizer

summarizer_model = Summarizer(
        model="distilbert-base-uncased", hidden=-2, reduce_option="mean")

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

class Parser(object):  #pylint: disable=useless-object-inheritance
  """Class to parse text"""

  def __init__(self, raw_text: bytes):
    self.all_data = str(raw_text).split("\n")

  def __isint(self, v) -> bool:  #pylint: disable=invalid-name,no-self-use
    try:
      int(v)
      return True
    except:  #pylint: disable=bare-except
      return False

  def __should_skip(self, v) -> bool:  #pylint: disable=invalid-name
    return self.__isint(v) or v == "\n" or "-->" in v

  def __process_sentences(self, v) -> List[str]:  #pylint: disable=invalid-name,no-self-use
    sentence = nltk.tokenize.sent_tokenize(v)
    return sentence

  def run(self) -> List[str]:
    """Function to return cleaned list of sentences"""
    total: str = ""
    for data in self.all_data:
      if not self.__should_skip(data):
        cleaned = data.replace("&gt;", "").replace("\n", "").strip()
        if cleaned:
          total += " " + cleaned
    sentences = self.__process_sentences(total)
    return sentences

  def convert_to_paragraphs(self) -> str:
    """Function to convert the cleaned list of sentences into a paragraph"""
    sentences: List[str] = self.run()
    perform_summarization = True
    if len(sentences) <=1:
      perform_summarization = False
    text = " ".join([sentence.strip() for sentence in sentences]).strip()
    return (text, perform_summarization)

def summarize_text(request_body, model=summarizer_model):
  """
    Inference method
    Args:
        response_body(dictionary) - Request body for post request
        "data" - text data that needs to be summarized
        "ratio" - Ratio of sentences to summarize to from the original body
        "min_length" - The minimum length to accept as a sentence.
        "max_length" -  The maximum length to accept as a sentence.

    """
  text = request_body["data"]
  ratio = request_body.get("ratio", 0.2)
  parsed, perform_summarization = Parser(text).convert_to_paragraphs()
  if perform_summarization:
    summary = model(parsed,
                    ratio=ratio,
                    min_length=request_body.get("min_length", 25),
                    max_length=request_body.get("max_length", 500))

    response_body = {"summary": summary}
  elif ratio >= 1:
    response_body = {"summary": parsed}
  else:
    response_body = {"summary": ""}
  return response_body
