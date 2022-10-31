"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from flask import Flask, jsonify, current_app, request, render_template
from classroom import get_courses, enroll_student

ADMIN_EMAIL = "<INSERT_ADMIN_EMAIL>"
STUDENT_EMAIL = "<INSERT_STUDENT_EMAIL>"
COURSE_ID = "<INSERT_COURSE_ID"
ENROLLMENT_CODE = "<INSERT_ENROLLMENT_CODE>"

app = Flask(__name__, static_folder='static', static_url_path='/static')
# app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
  return current_app.send_static_file('view.html')


@app.route("/studyhall")
def studyhall():
  return current_app.send_static_file('studyhall.html')


# @app.route("/bg.png")
# def image():
#     return current_app.render_template('bg.png')


@app.route("/courses")
def courses():
  courses = get_courses()
  return jsonify(courses)


@app.route("/enroll", methods=["GET", "POST"])
def enroll():
  if request.method == 'POST':
    print(request.json)
    content = request.json
    result = enroll_student(content["email"], COURSE_ID, ENROLLMENT_CODE)
    return jsonify(result)
  else:
    return jsonify("Post requests only")


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
