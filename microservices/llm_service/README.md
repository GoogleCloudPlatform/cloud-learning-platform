## Installation

### Set OpenAI key
```echo $OPENAI_API_KEY | gcloud secrets create "openai-api-key" --data-file=-```


## Build a Query Engine

### Using util script

This process can take a few hours. Best done in a tmux or screen session.

The userid is the user that created the query engine.  You can get that from the Cloud Firestore console.

```python utils/build_query_engine.py gs://<bucket> <engine-name> <userid>```


