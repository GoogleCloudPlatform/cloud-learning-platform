"""
  Student Learner Profile Microservice
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
import time
import config
import uvicorn

from fastapi import FastAPI, Depends, Request

from common.utils.logging_handler import Logger
from common.utils.auth_service import validate_token
from common.utils.http_exceptions import add_exception_handlers

from routes import (learner, learner_profile, mastery, goal, achievement,
                    ingestion, education_fields, progress, learner_achievements)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  """
  Add process time header to every request
  """
  method = request.method
  path = request.scope.get("path")
  start_time = time.time()
  response = await call_next(request)
  if path != "/ping":
    process_time = time.time() - start_time
    time_elapsed = round(process_time * 1000)
    Logger.info(f"{method} {path} Time elapsed: {str(time_elapsed)} ms")
  return response


@app.get("/ping")
def health_check():
  """
  Health Check
  """
  return {
    "success": True,
    "message": "Successfully reached student learner profile microservice",
    "data": {}
  }


api = FastAPI(
  title="Student Learner Profile Service API",
  version="latest",
  docs_url=None,
  redoc_url=None,
  dependencies=[Depends(validate_token)]
)

api.include_router(learner.router)
api.include_router(learner_profile.router)
api.include_router(mastery.router)
api.include_router(goal.router)
api.include_router(achievement.router)
api.include_router(ingestion.router)
api.include_router(education_fields.router)
api.include_router(progress.router)
api.include_router(learner_achievements.router)

add_exception_handlers(app)
add_exception_handlers(api)
app.mount("/learner-profile-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=int(config.PORT),
    log_level="debug",
    reload=config.IS_DEVELOPMENT)
