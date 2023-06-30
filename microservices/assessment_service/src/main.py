"""
  Assessment Microservice
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
from routes import (assessment_item, assessment, submitted_assessment, rubric,
                    rubric_criterion, assessment_content)
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
      "message": "Successfully reached Assessment Service",
      "data": {}
  }


api = FastAPI(
    title="Assessment Service API's",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)]
    )

api.include_router(assessment.router)
api.include_router(assessment_item.router)
api.include_router(submitted_assessment.router)
api.include_router(assessment_content.router)
api.include_router(rubric.router)
api.include_router(rubric_criterion.router)

add_exception_handlers(app)
add_exception_handlers(api)
app.mount("/assessment-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
