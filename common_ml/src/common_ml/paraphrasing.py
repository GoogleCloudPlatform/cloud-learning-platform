"""Module for paraphrasing"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from common_ml.config import MODEL_NAME_PARAPHRASE

tokenizer_paraphrase = AutoTokenizer.from_pretrained(MODEL_NAME_PARAPHRASE)
model_paraphrase = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_PARAPHRASE)


def get_paraphrase_text(text, num_return_sequences=1):
  """
  Method to paraphrase an input text using T5 model fine-tuned on
  Google PAWS dataset.
  Args:
    text (str): input text to be paraphrased.
    num_return_sequences (int): number of paraphrased sentences
                                to be returned from the model.
  Returns:
    paraphrased_texts (list): list of paraphrased text of the input text, where
                              len(paraphrased_texts) = num_return_sequences.
  """
  paraphrased_texts = []
  text =  "paraphrase: " + text + " </s>"

  encoding = tokenizer_paraphrase.encode_plus(
      text, pad_to_max_length=True, return_tensors="pt")
  input_ids = encoding["input_ids"]
  attention_masks = encoding["attention_mask"]

  outputs = model_paraphrase.generate(
    input_ids=input_ids, attention_mask=attention_masks,
    max_length=256,
    do_sample=True,
    top_k=120,
    top_p=0.95,
    early_stopping=True,
    num_return_sequences=num_return_sequences
  )

  for output in outputs:
    decoded_output = tokenizer_paraphrase.decode(output,
        skip_special_tokens=True, clean_up_tokenization_spaces=True)
    paraphrased_texts.append(decoded_output)
  return paraphrased_texts
