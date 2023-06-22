ARG BASE_IMG
FROM ${BASE_IMG}
WORKDIR /opt

RUN apt-get install tesseract-ocr -y
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -c "from sentence_transformers import SentenceTransformer;SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')"
RUN python -m spacy download en
RUN python -c "import nltk;nltk.download('punkt')"
COPY . .

EXPOSE 8888

ENTRYPOINT [ "python", "main.py" ]