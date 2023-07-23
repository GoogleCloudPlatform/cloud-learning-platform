"""
  Credential Pathway Service
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
from fastapi import FastAPI
from routes import badge, assertion, issuer

app = FastAPI()


@app.get("/ping")
def health_check():
  """Health Check API

  Returns:
      dict: Status object with success message
  """
  return {
      "success": True,
      "message": "Successfully reached Credentials And Pathway Service",
      "data": {}
  }


api = FastAPI(title="Credentials And Pathway Service API's", version="latest")

api.include_router(badge.router)
api.include_router(assertion.router)
api.include_router(issuer.router)

app.mount("/credential-pathway-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
