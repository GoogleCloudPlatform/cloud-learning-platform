"""Module for abstractive summarization utility"""
from transformers import T5Tokenizer, T5ForConditionalGeneration
from common_ml.config import MODEL_NAME_SUMMARY
from common_ml.utils import clean_text

summary_model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME_SUMMARY)
summary_tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME_SUMMARY)


def generate_summary(text):
  """
    Returns a summary for an input text.
    Args:
      text (str): input text
    Returns:
      summary (str): summary generated using T5-base
    """
  text = clean_text(text)
  input_ids = summary_tokenizer.encode(
      "summarize: " + text, return_tensors="pt", add_special_tokens=True)
  generated_ids = summary_model.generate(
      input_ids=input_ids,
      num_beams=2,
      max_length=150,
      repetition_penalty=2.5,
      length_penalty=1.0,
      early_stopping=True)
  preds = [
      summary_tokenizer.decode(
          g, skip_special_tokens=True, clean_up_tokenization_spaces=True)
      for g in generated_ids
  ]
  summary = preds[0]
  return summary
