"""Module for unit testing fixtures"""
import os
import signal
import subprocess
import time

import requests

import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,consider-using-with,subprocess-popen-preexec-fn


@pytest.fixture(scope="module")
def firestore_emulator():
  emulator = subprocess.Popen(
      "firebase emulators:start --only firestore --project fake-project",
      shell=True,
      preexec_fn=os.setsid)
  time.sleep(10)

  os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
  os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

  yield emulator

  os.killpg(os.getpgid(emulator.pid), signal.SIGTERM)
  try:
    os.remove("firestore-debug.log")
    os.remove("ui-debug.log")
  except OSError:
    pass

  # TODO: script to unset / reset the environmental variables instead of


@pytest.fixture
def clean_firestore(firestore_emulator):
  requests.delete("http://localhost:8080/emulator/v1/projects/fake-project/"\
    "databases/(default)/documents"
                 )
