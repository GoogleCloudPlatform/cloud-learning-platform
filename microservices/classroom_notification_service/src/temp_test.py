"""
Dummy unit test script
"""
import os

def test_env():
  project_id=os.getenv("PROJECT_ID")
  assert  project_id is not None
