import sys
sys.path.append("microservices/llm_service/src")
sys.path.append("common/src")
import logging
logging.basicConfig(level=logging.INFO, stream=sys.error)

from services.query_service import query_engine_build

if __name__ == "__main__":
  args = sys.argv[1:]
  
  doc_url = args[0]
  query_engine = args[1]
  user_id = args[2]
  
  print(f"*** building query index for {doc_url}, query_engine {query_engine}, for user id {user_id}")
  
  params = {}
  query_engine_build(doc_url, query_engine, user_id, params)
  