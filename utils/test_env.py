"test file"
import os
import json
CREDS = os.getenv("account", None)
test_creds=json.loads(CREDS)
print("=========================")
print(CREDS)
print(test_creds)
print(type(CREDS))
print(type(test_creds))
