"""Module containing unit tests for summary_items script"""
import pytest
from transformers import AlbertTokenizer, AlbertModel

from summarizer.model_processors import Summarizer
from summarizer.sentence_handler import SentenceHandler


@pytest.fixture()
def custom_summarizer():
  """Function to return ALBERT summarizer model"""
  albert_model = AlbertModel.from_pretrained(
      "albert-base-v2", output_hidden_states=True)
  albert_tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")
  return Summarizer(
      custom_model=albert_model, custom_tokenizer=albert_tokenizer)


@pytest.fixture()
def summarizer():
  """Function to return distillbert summarizer"""
  return Summarizer("distilbert-base-uncased")


@pytest.fixture()
def summarizer_multi_hidden():
  """Function to return distillbert summarizer with changed hidden states"""
  return Summarizer("distilbert-base-uncased", hidden=[-1, -2])


@pytest.fixture()
def passage():
  """Function to return test case"""
  return """
    The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.
    The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.
    Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008.
    Real estate firm Tishman Speyer had owned the other 10%.
    The buyer is RFR Holding, a New York real estate company.
    Officials with Tishman and RFR did not immediately respond to a request for comments.
    It's unclear when the deal will close.
    The building sold fairly quickly after being publicly placed on the market only two months ago.
    The sale was handled by CBRE Group.
    The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.
    The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028.
    Meantime, rents in the building itself are not rising nearly that fast.
    While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities.
    Still the building is among the best known in the city, even to people who have never been to New York.
    It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top.
    It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day.
    The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices.
    Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest.
    Blackstone Group (BX) bought it for $1.3 billion 2015.
    The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself.
    Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete.
    Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.
    """


def test_elbow_calculation(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test elbow_calculation"""
  res = summarizer.calculate_elbow(passage, k_max=5)
  assert len(res) == 4


def test_optimal_elbow_calculation(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test optimal_elbow_calculation"""
  res = summarizer.calculate_optimal_k(passage, k_max=6)
  assert isinstance(res, int)


def test_list_handling(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test list_handling"""
  res = summarizer(passage, num_sentences=3, return_as_list=True)
  assert isinstance(res, list)
  assert len(res) == 3


def test_multi_hidden(summarizer_multi_hidden, passage):  #pylint: disable=redefined-outer-name
  """Function to test multi_hidden"""
  res = summarizer_multi_hidden(
      passage, num_sentences=5, min_length=40, max_length=500)
  assert len(res) > 10


def test_multi_hidden_concat(summarizer_multi_hidden: Summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test multi_hidden_concat"""
  summarizer_multi_hidden.hidden_concat = True
  res = summarizer_multi_hidden(
      passage, num_sentences=5, min_length=40, max_length=500)
  assert len(res) > 10


def test_summary_creation(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test summary_creation"""
  res = summarizer(passage, ratio=0.15, min_length=40, max_length=500)
  assert len(res) > 10


def test_summary_embeddings(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test summary_embeddings"""
  embeddings = summarizer.run_embeddings(
      passage, ratio=0.15, min_length=25, max_length=500)
  assert embeddings.shape[1] == 768
  assert embeddings.shape[0] > 1


def test_summary_larger_ratio(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test summary_larger_ratio"""
  res = summarizer(passage, ratio=0.5)
  assert len(res) > 10


def test_cluster_algorithm(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test cluster_algorithm"""
  res = summarizer(passage, algorithm="gmm")
  assert len(res) > 10


def test_do_not_use_first(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test do_not_use_first"""
  res = summarizer(passage, ratio=0.1, use_first=False)
  assert res is not None


def test_albert(custom_summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test albert"""
  res = custom_summarizer(passage)
  assert len(res) > 10


def test_num_sentences(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test num_sentences"""
  result = summarizer(passage, num_sentences=3)
  result_sents = SentenceHandler().process(result)
  assert len(result_sents) == 3


def test_num_sentences_embeddings(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test num_sentences_embeddings"""
  result = summarizer.run_embeddings(passage, num_sentences=4)
  assert result.shape == (4, 768)


def test_aggregate_embeddings(summarizer, passage):  #pylint: disable=redefined-outer-name
  """Function to test aggregate_embeddings"""
  result = summarizer.run_embeddings(passage, num_sentences=4, aggregate="mean")
  assert result.shape == (768,)
