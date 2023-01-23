"""Tool Registration Endpoints"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from config import ERROR_RESPONSES

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Login Template"], responses=ERROR_RESPONSES)


@router.get("/launch")
def login(request: Request):
  return templates.TemplateResponse("login.html", {
      "request": request,
  })
