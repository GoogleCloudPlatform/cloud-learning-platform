"""Launch Endpoints"""
import traceback
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from config import ERROR_RESPONSES, API_DOMAIN
from common.models import LTIAssignment
from common.utils.errors import ValidationError
from common.utils.http_exceptions import (InternalServerError, BadRequest)
from common.utils.logging_handler import Logger
from services.ext_service_handler import get_content_item
# pylint: disable=line-too-long, unused-variable, broad-exception-raised

templates = Jinja2Templates(directory="templates")

router = APIRouter(responses=ERROR_RESPONSES)


@router.get("/e2e-resource-launch")
def login(request: Request, lti_assignment_id: str):
  """This login endpoint will return the user to firebase login page
  Args:
      lti_assignment_id (str): unique id of the LTI Assignment
  Returns:
      Template response with the login page of the user
  """
  try:
    url = f"{API_DOMAIN}/classroom-shim/api/v1/launch-assignment?lti_assignment_id={lti_assignment_id}"

    lti_assignment = LTIAssignment.find_by_id(lti_assignment_id)
    lti_content_item = get_content_item(lti_assignment.lti_content_item_id)
    token = request.headers["Authorization"].split(" ")[1]
    return templates.TemplateResponse(
        "e2e_resuorce_launch.html", {
            "request":
                request,
            "redirect_url":
                url,
            "token":
                token,
            "htmlContent":
                f"""
  <!DOCTYPE html>
    <html lang="en">

    <head>
      <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    </head>

    <body>
      <p id="status" style="text-align: center; margin-bottom: 2rem; display: none;"></p>

      <div style="text-align: center; margin-bottom: 2rem" id="google-sign-in-btn-container">
      </div>
      <script>
        function initiateRedirection(token) {{
          displayRedirecting()
          let timezone = null
          if (Intl?.DateTimeFormat().resolvedOptions().timeZone) {{
            timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
          }}
          let redirectUrl = null
          if (timezone) {{
            redirectUrl = `{url}&timezone=${{timezone}}`
          }} else {{
            redirectUrl = `{url}`
          }}
          return axios
            .get(redirectUrl, {{
              headers: {{
                Authorization: `Bearer {token}`,
              }},
            }})
            .then((response1) => {{
              return axios.post(response1.data.url, response1.data.message_hint, {{
                headers: {{
                  Authorization: `Bearer {token}`,
                }},
              }}).then((response2) => {{
                window.open(response2.data.url, "_self").focus()
              }}).catch((err) => {{
                console.log("err", err)
                if (err?.response?.data) {{
                  displayError(err.response.data.message)
                }} else {{
                  err?.response?.status == 401 ? displayError("Access Denied") : displayError(err.message)
                }}
              }})
            }}).catch((err) => {{
              console.log("err", err)
              if (err?.response?.data) {{
                displayError(err.response.data.message)
              }} else {{
                err?.response?.status == 401 ? displayError("Access Denied") : displayError(err.message)
              }}
            }})
        }}

        function displayRedirecting(text) {{
          let displayText = "Redirecting..."
          if (text) {{
            displayText = text
          }}
          document.getElementById("status").style.display = "block";
          document.getElementById("status").style.color = "black";
          document.getElementById("status").innerText = displayText;
        }}

        function displayError(text) {{
          let displayText = "There was a error while redirecting! Please try again."
          if (text) {{
            displayText = text
          }}
          document.getElementById("status").style.display = "block";
          document.getElementById("status").style.color = "red";
          document.getElementById("status").innerText = displayText;
        }}
        initiateRedirection(`{token}`)
      </script>
    </body>

    </html>
"""
        },
        status_code=301)

  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
