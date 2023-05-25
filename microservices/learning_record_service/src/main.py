"""
  Learning Record Service Microservice
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
from fastapi.middleware.cors import CORSMiddleware
from routes import activity_state, agent, activity, statement, verb
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def health_check():
  """Health Check API

  Returns:
      dict: Status object with success message
  """
  return {
      "success": True,
      "message": "Successfully reached Learning Record Service",
      "data": {}
  }


api = FastAPI(
    title="Learning Record Service API",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)]
    )

api.include_router(statement.router)
api.include_router(activity_state.router)
api.include_router(activity.router)
api.include_router(verb.router)
api.include_router(agent.router)

add_exception_handlers(api)
add_exception_handlers(app)

app.mount("/learning-record-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
