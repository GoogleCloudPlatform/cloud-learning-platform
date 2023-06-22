import requests
import webbrowser
import tempfile

token = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY3YmFiYWFiYTEwNWFkZDZiM2ZiYjlmZjNmZjVmZTNkY2E0Y2VkYTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFtIENoYXVkaGFyaSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BRWRGVHA0d0l4Um53NTBoVzdfYmppcVlPTWdkaHB0MEd6OWR3MUQ2THBPQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb3JlLWxlYXJuaW5nLXNlcnZpY2VzLWRldiIsImF1ZCI6ImNvcmUtbGVhcm5pbmctc2VydmljZXMtZGV2IiwiYXV0aF90aW1lIjoxNjg2NjYyNzE0LCJ1c2VyX2lkIjoiTkh2cEJBZTVFTFJ4aVZJWDdDR0VsUHRwck5qMiIsInN1YiI6Ik5IdnBCQWU1RUxSeGlWSVg3Q0dFbFB0cHJOajIiLCJpYXQiOjE2ODY2NjI3MTQsImV4cCI6MTY4NjY2NjMxNCwiZW1haWwiOiJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTExMzc3MTk1MzUxNTAyMTQyMiJdLCJlbWFpbCI6WyJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.WjxGMwabsLLr11i_zl6U3Ru4pCafmic8Di9lUZjf981LVEKvr7UpqAedkI1a7DOrn83X2MbpPUKx3_vnWHOQH75bkHJI_-2xa_zA7NUKh_eKUKm8H5eXp4RgGCZ4maj43_uKBa-QB244Mglkb0DU-9_lxzuzQ49BsJUBSOYmBmQ8-OLoNgV3lWzS6g0BpiK2aAtpR_6sM9y6b1ROOerN9IZruX2s54OSXVQAp7OUGwoWKfIvGztInHVu85Oh0h9wR6VyBnwYsAZO0XTh2dl7dBZy0FmQ1EFEDItwBBEm3BiphU6-g6EomfMpmN74Q8jQeyH6W67_Z-gtOTQD2CBO8g"
url = "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/content-selection-launch-init?tool_id=xwsBdJzPESMQWiQw7Plh&user_id=vcmt4ZemmyFm59rDzl1U&context_id=MxO1PHDujyv7wYbpOOoN&context_type=section"
url_req = requests.get(
    url, headers={"Authorization": token}, timeout=60, verify=False)

print("initial req status", url_req.status_code)

second_url_req = requests.get(
    url_req.json().get("url"),
    headers={"Authorization": token},
    allow_redirects=True,
    timeout=60,
    verify=False)

print(second_url_req.status_code)
print(second_url_req.text)
# webbrowser.open_new_tab(f"data:text/html,{second_url_req.text}")

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
  temp_file.write(second_url_req.content)
  temp_file.flush()

  # Open the temporary file in a web browser
  webbrowser.open(f"file://{temp_file.name}")
