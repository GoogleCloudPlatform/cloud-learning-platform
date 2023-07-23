"""Utils Microservice Entry Point"""
import uvicorn
from fastapi import FastAPI, Depends

from routes import (activity_handler, feedback_handler,
gethelp_handler, gettopics_handler, inlinefeedback_handler)
from config import PORT, API_BASE_URL, SERVICE_NAME, IS_DEVELOPMENT
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

app = FastAPI()
BASE_URL = f"/{SERVICE_NAME}/{API_BASE_URL}"


@app.get("/ping")
def health_check():
  return {
      "success": True,
      "message": "Successfully reached utils microservice",
      "data": {}
  }

api = FastAPI(
    title="Utils APIs",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)])

api.include_router(activity_handler.router)
api.include_router(feedback_handler.router)
api.include_router(gethelp_handler.router)
api.include_router(gettopics_handler.router)
api.include_router(inlinefeedback_handler.router)
add_exception_handlers(app)
add_exception_handlers(api)

app.mount(BASE_URL, api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(PORT),
      log_level="debug",
      reload=IS_DEVELOPMENT)
