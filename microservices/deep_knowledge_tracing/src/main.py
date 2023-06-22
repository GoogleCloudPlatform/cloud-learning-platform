"""Deep Knowledge Tracing microservice"""
import uvicorn
import config
from fastapi import FastAPI,Depends
from routes import dkt_routes, job_status, user_events
from common.utils.gcs_adapter import download_blob
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

#pylint: disable=pointless-string-statement
""" For local Development
import sys
sys.path.append("../../../common/src")
import os
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
"""

app = FastAPI()

download_blob(config.MODEL_WEIGHTS_PATH, config.MODEL_PARAMS_DIR)


@app.get("/ping")
def health_check():
  return {
      "success": True,
      "message": "Successfully reached DKT microservice",
      "data": {}
  }

api = FastAPI(
    title="Deep Knowledge Tracing APIs",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)])

api.include_router(dkt_routes.router)
api.include_router(job_status.router)
api.include_router(user_events.router)

app.mount("/deep-knowledge-tracing/api/v1", api)
add_exception_handlers(app)
add_exception_handlers(api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="info",
      reload=config.IS_DEVELOPMENT)
