"""Item Response Theory microservice"""

import uvicorn
import config
from fastapi import FastAPI
from routes import train_irt, fake_data, ability, next_item, job_status
from common.utils.http_exceptions import add_exception_handlers

# pylint: disable=pointless-string-statement
# pylint: disable=wrong-import-position
""" For Local Development
import sys
sys.path.append("../../../common/src")
import os
# os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "gcp-classroom-dev"
"""

app = FastAPI()


@app.get("/ping")
def health_check():
  return True


api = FastAPI(
    title="Item Response Theory APIs",
    version="latest",
    docs_url=None,
    redoc_url=None
)

api.include_router(train_irt.router)
api.include_router(fake_data.router)
api.include_router(ability.router)
api.include_router(next_item.router)
api.include_router(job_status.router)
add_exception_handlers(app)
add_exception_handlers(api)

app.mount("/item-response-theory/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      debug=True,
      reload=config.IS_DEVELOPMENT)
