"""
  Learning Object Service
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
import config
import uvicorn
from fastapi import FastAPI, Depends
from routes import (curriculum_pathway,
                    learning_experience,
                    learning_object,
                    learning_resource,
                    content_serving,
                    batch_job,
                    faq_content)
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

app = FastAPI()


@app.get("/ping")
def health_check():
  """Health Check API

  Returns:
      dict: Status object with success message
  """
  return {
      "success": True,
      "message": "Successfully reached Learning Object Service",
      "data": {}
  }


api = FastAPI(
    title="Learning Object Service API's",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)]
  )

api.include_router(curriculum_pathway.router)
api.include_router(learning_experience.router)
api.include_router(learning_object.router)
api.include_router(learning_resource.router)
api.include_router(content_serving.router)
api.include_router(batch_job.router)
api.include_router(faq_content.router)

add_exception_handlers(app)
add_exception_handlers(api)

app.mount("/learning-object-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
