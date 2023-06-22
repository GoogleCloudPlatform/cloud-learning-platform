# FROM python:3.7
FROM huggingface/transformers-pytorch-gpu:3.3.1

WORKDIR /opt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

RUN python3 -m spacy download en_core_web_md
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en

RUN ["python3", "-c", "from transformers import DistilBertModel; model = DistilBertModel.from_pretrained('distilbert-base-uncased')"]

COPY src/ .

EXPOSE 8888
ENTRYPOINT ["python3", "main.py"]