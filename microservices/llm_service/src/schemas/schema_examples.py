""" Schema examples and test objects for unit tests """
# pylint: disable = line-too-long

LLM_GENERATE_EXAMPLE = {
  "llm_type": "",
  "prompt": "",
  "context": "",
  "primer":  "",
}

CHAT_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "user_id": "dhjgkjsdfhasd98798as7",
  "title": "Test chat",
  "llm_type": "VertexAI-Text-alpha",
  "history": [
    "test input 1",
    "test response 1",
    "test input 2",
    "test response 2"
  ],
  "created_time": "2023-05-05 09:22:49.843674+00:00",
  "last_modified_time": "2023-05-05 09:22:49.843674+00:00"
}
