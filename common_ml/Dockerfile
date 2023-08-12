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

ARG BASE_IMG
FROM ${BASE_IMG}

COPY requirements.txt service_requirements.txt

RUN apt-get install -y make g++ && \
    apt-get install -y --no-install-recommends curl wget zip unzip && \
    cat service_requirements.txt > requirements.txt && \
    pip install -r requirements.txt && \
    rm -Rf /root/.cache/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY src/ .
