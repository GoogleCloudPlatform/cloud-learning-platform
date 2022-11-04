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
  Pytest Fixture for getting testclient from fastapi
"""
import os
import signal
import subprocess
import time
import requests
import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi.testclient import TestClient
from main import app
import platform
# recreate the emulator each module - could consider changing to session
# pylint: disable = consider-using-with, subprocess-popen-preexec-fn
@pytest.fixture
def firestore_emulator():

  Windows = True if platform.system() == "Windows" else False
  if Windows:
    emulator = subprocess.Popen(
      "firebase emulators:start --only firestore --project fake-project",
      shell=True)
  else:
    emulator = subprocess.Popen(
        "firebase emulators:start --only firestore --project fake-project",
        shell=True,
        preexec_fn=os.setsid)
  time.sleep(15)

  os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
  os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
  os.environ["PROJECT_ID"] = "fake-project"

  # yield so emulator isn't recreated each test
  yield emulator
  if Windows:
    os.kill(emulator.pid, signal.CTRL_BREAK_EVENT)
  else:
    os.killpg(os.getpgid(emulator.pid), signal.SIGTERM)
  # delete debug files
  # some get deleted, not all

  try:
    os.remove("firestore-debug.log")
    os.remove("ui-debug.log")
  except OSError:
    pass

  # TODO: script to unset / reset the environmental variables
  # instead of just delete

# pylint: disable = line-too-long
@pytest.fixture
def clean_firestore(firestore_emulator):
  requests.delete(
      "http://localhost:8080/emulator/v1/projects/fake-project/databases/(default)/documents"
  )

@pytest.fixture
def client_with_emulator(clean_firestore, scope="module"):
  test_client = TestClient(app)
  yield test_client
