"""Prior Learning Assessment microservice entrypoint"""
import uvicorn
from routes import prior_experience, pla_record, upload, extraction, \
  approved_experience
from fastapi import FastAPI, Depends
from config import IS_DEVELOPMENT, SERVICE_NAME, API_BASE_URL, PORT
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_token

app = FastAPI()

BASE_URL = f"/{SERVICE_NAME}/{API_BASE_URL}"


@app.get("/ping")
def health_check():
  return {
    "success": True,
    "message": "Successfully reached to prior learning assessment microservice",
    "data": {}
  }

api = FastAPI(
  title="Prior Learning Assessment APIs",
  version="latest",
  docs_url=None,
  redoc_url=None,
  dependencies=[Depends(validate_token)]
)

api.include_router(prior_experience.router)
api.include_router(pla_record.router)
api.include_router(extraction.router)
api.include_router(upload.router)
api.include_router(approved_experience.router)

add_exception_handlers(app)
add_exception_handlers(api)

app.mount(BASE_URL, api)

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=int(PORT),
    log_level="info",
    reload=IS_DEVELOPMENT
  )
