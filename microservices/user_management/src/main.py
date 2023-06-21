"""
  User Management Service
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
import config
from fastapi import FastAPI, Depends

from routes import (user_event, user, permission, action, user_group, staff,
                    module, session, application, association_group,
                    learner_association_group,
                    discipline_association_group)
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

app = FastAPI()


@app.get("/ping")
def health_check() -> dict:
  """
  Endpoint to check the microservice health
  Params
  ------
  None
  Returns
  -------
  dict
  """
  return {
    "success": True,
    "message": "Successfully reached User Management Service",
    "data": {}
  }


add_exception_handlers(app)

api = FastAPI(title="User Access Management Service APIs",
              version="latest",
              # docs_url=None,
              # redoc_url=None,
              # dependencies=[Depends(validate_token)]
              )

api.include_router(user.router)
api.include_router(user_group.router)
api.include_router(permission.router)
api.include_router(action.router)
api.include_router(module.router)
api.include_router(application.router)
api.include_router(session.router)
api.include_router(staff.router)
api.include_router(association_group.router)
api.include_router(learner_association_group.router)
api.include_router(discipline_association_group.router)
add_exception_handlers(api)

api_v2 = FastAPI(title="User Access Management Service APIs",
                 version="latest",
                 docs_url=None,
                 redoc_url=None,
                 dependencies=[Depends(validate_token)]
                 )

api_v2.include_router(user.router)
api_v2.include_router(user_event.router)

app.mount("/user-management/api/v1", api)

if __name__ == "__main__":
  uvicorn.run("main:app",
              host="0.0.0.0",
              port=int(config.PORT),
              log_level="debug",
              reload=True)
