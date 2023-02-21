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
BQ JSON helper Service
"""

import json

def convert_to_json(dict_object, key):
  """_summary_

  Args:
    dict_object (_type_): _description_
    key (_type_): _description_

  Returns:
    _type_: _description_
  """
  if key in dict_object.keys():
    return json.dumps(dict_object[key])
  return None


def convert_dict_array_to_json(dict_object, key):
  """_summary_

  Args:
    dict_object (_type_): _description_
    key (_type_): _description_

  Returns:
    _type_: _description_
  """
  if key in dict_object.keys():
    return [json.dumps(i) for i in dict_object[key]]
  else:
    return None
