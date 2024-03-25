ARG BASE_IMG
FROM ${BASE_IMG}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .
EXPOSE 8888
ENTRYPOINT [ "python", "main.py" ]
