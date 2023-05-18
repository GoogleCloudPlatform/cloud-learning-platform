"""
  Classroom Shim Microservice
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
from fastapi.templating import Jinja2Templates
from routes import launch, lti_assignment, grade, context, assignment_copy
from common.utils.http_exceptions import add_exception_handlers
from utils.helper import validate_user

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/ping")
def health_check():
  return {
      "success": True,
      "message": "Successfully reached Classroom Shim microservice",
      "data": {}
  }


api = FastAPI(title="Classroom Shim Service APIs", version="latest")

api.include_router(launch.router)
api.include_router(
    assignment_copy.router, dependencies=[Depends(validate_user)])
api.include_router(lti_assignment.router, dependencies=[Depends(validate_user)])
api.include_router(context.router, dependencies=[Depends(validate_user)])
api.include_router(grade.router, dependencies=[Depends(validate_user)])

add_exception_handlers(app)
add_exception_handlers(api)

app.mount("/classroom-shim/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
