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
  Script to do portforwarding of different services.
"""
import yaml
import os
import subprocess
import argparse

# disabling for linting to pass
# pylint: disable = consider-using-with, subprocess-popen-preexec-fn

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--namespace", "-n")
  args = parser.parse_args()
  print("Setting up port-forward in namespace '%s'" % args.namespace)

  port_config_data = []
  with open("setup/port_config.yaml", "r", encoding="utf-8") as stream:
    port_config = yaml.safe_load(stream)
    port_config_data = port_config.get("data", [])

  for service in port_config_data:
    service_name = service.replace(".PORT", "")
    port = port_config_data[service]
    cmd = "kubectl port-forward service/%s %s:%s -n %s" % (service_name, port,
                                                           80, args.namespace)
    print(cmd)
    emulator = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
