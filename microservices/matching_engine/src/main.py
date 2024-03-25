"""
  matching-engine microservice
"""

# pylint: disable=pointless-string-statement
# pylint: disable=wrong-import-position
""" For Local Development
import sys
sys.path.append("../../../common/src")
import os
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
"""
import uvicorn
from fastapi import FastAPI
from routes import index,index_endpoint,query,deploy
from config import SERVICE_NAME, API_BASE_URL, PORT
from utils.http_exceptions import add_exception_handlers

app = FastAPI()
BASE_URL = f"/{SERVICE_NAME}/{API_BASE_URL}"



@app.get("/ping")
def health_check():
  return {
      "success": True,
      "message": "Successfully reached matching-engine microservice",
      "data": {}
  }

api = FastAPI(title="Matching Engine API", version="latest")

api.include_router(index.router)
api.include_router(index_endpoint.router)
api.include_router(query.router)
api.include_router(deploy.router)

add_exception_handlers(app)
add_exception_handlers(api)
app.mount("/matching-engine/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(PORT),
      log_level="debug",
      reload=True)
