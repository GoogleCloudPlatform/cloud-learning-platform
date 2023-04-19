# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  LMS Service Microservice
"""
from http.client import responses
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import uvicorn
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import add_exception_handlers
from fastapi import FastAPI, Request, Depends
import config
from routes import (
  section,student,
  course_template,cohort,classroom_courses
  # ,user
        )
from utils.helper import validate_user

app = FastAPI()


@app.on_event("startup")
def set_default_executor():
  loop = asyncio.get_running_loop()
  loop.set_default_executor(ThreadPoolExecutor(max_workers=1000))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  """Middleware

  Args:
      request (Request): _description_
      call_next (_type_): _description_

  Returns:
      _type_: _description_
  """
  method = request.method
  path = request.scope.get("path")
  start_time = time.time()
  response = await call_next(request)
  if path != "/ping":
    process_time = time.time() - start_time
    time_elapsed = round(process_time * 1000)
    status = f"{response.status_code} {responses[response.status_code]}"
    try:
      client_ip = request.headers.getlist("X-Forwarded-For")[0].split(",")[0]
    except IndexError:
      client_ip=f"{request.client.host}:{request.client.port}"
    Logger.info(
      f"{client_ip} - {method} {path}" +
      f" Time elapsed: {str(time_elapsed)} ms Status: {status}"
      )
  return response


@app.get("/ping")
def health_check():
  return True


@app.get("/")
def hello():
  return "Hello World."

api = FastAPI(title="LMS Service APIs",
              version="latest",
              # dependencies=[Depends(validate_user)]
              )


# api.include_router(user.router)
api.include_router(section.router)
api.include_router(student.router)
api.include_router(student.section_student_router)
api.include_router(student.cohort_student_router)
api.include_router(course_template.router)
api.include_router(classroom_courses.router)
api.include_router(cohort.router)

add_exception_handlers(app)
add_exception_handlers(api)
app.mount("/lms/api/v1", api)

if __name__ == "__main__":
  uvicorn.run("main:app",
              host="0.0.0.0",
              port=int(config.PORT),
              log_level="debug",
              reload=True,
              access_log=config.ENABLE_UVICORN_LOGS)
