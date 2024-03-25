"""
  Skill Microservice
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
from routes import (skill, competency, category, sub_domain, domain, ingestion,
                    batch_job, search, role_to_skills, embeddings,
                    curriculum_to_skills, skill_to_knowledge, skill_similarity,
                    skill_unified_alignment, assessment_to_skills, data_source,
                    syntactic_search)
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
      "message": "Successfully reached Skill microservice",
      "data": {}
  }


api = FastAPI(
    title="Skill Service API",
    version="latest",
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(validate_token)]
  )

api.include_router(skill.router)
api.include_router(competency.router)
api.include_router(category.router)
api.include_router(sub_domain.router)
api.include_router(domain.router)
api.include_router(search.router)
api.include_router(syntactic_search.router)
api.include_router(ingestion.router)
api.include_router(skill_to_knowledge.router)
api.include_router(skill_similarity.router)
api.include_router(batch_job.router)
api.include_router(skill_unified_alignment.router)
api.include_router(curriculum_to_skills.router)
api.include_router(role_to_skills.router)
api.include_router(assessment_to_skills.router)
api.include_router(data_source.router)
api.include_router(embeddings.router)

add_exception_handlers(app)
add_exception_handlers(api)
app.mount("/skill-service/api/v1", api)

if __name__ == "__main__":
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=int(config.PORT),
      log_level="debug",
      reload=True)
