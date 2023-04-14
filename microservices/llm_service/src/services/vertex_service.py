# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Classes for working with language models.

This module is *experimental* and can be changed in the future.
"""
# pylint: disable = bad-indentation,trailing-whitespace,unused-argument
# pylint: disable = missing-class-docstring,no-value-for-parameter

import dataclasses
import tempfile
from typing import Any, Dict, List, Optional, Sequence, Type, Union

from google.cloud import storage

from google.cloud import aiplatform
from google.cloud.aiplatform import base
from google.cloud.aiplatform import initializer as aiplatform_initializer
from google.cloud.aiplatform import utils as aiplatform_utils
from google.cloud.aiplatform.utils import gcs_utils

try:
    import pandas
except:
    pandas = None


_LOGGER = base.Logger(__name__)


class _LanguageModel:
    """_LanguageModel is a base class for all language models.

    This class is *experimental* and can be changed in the future.
    """

    _model_name_to_class_map: Dict[str, Type["_LanguageModel"]] = {}

    # These constants must be overridden in the derived classes
    _MODEL_NAME: Optional[str] = None
    _LLM_ENDPOINT_NAME = "projects/cloud-large-language-models/locations/us-central1/endpoints/text-bison-001"
    _TUNING_MODEL_ID: Optional[str] = None
    _TUNING_TRAINING_PARAMETERS: Optional[Dict[str, Any]] = None

    def __init__(self, endpoint_name: Optional[str] = None):
        """Creates a LanguageModel.

        This constructor should not be called directly.
        Use `LanguageModel.from_pretrained(model_name=...)` instead.

        Args:
            endpoint_name: Vertex Endpoint resource name for the model
        """
        endpoint_name = endpoint_name or self._LLM_ENDPOINT_NAME
        self._endpoint = aiplatform.Endpoint(endpoint_name)

    @classmethod
    def _register_model_class(cls: Type["_LanguageModel"]):
        assert cls._MODEL_NAME
        _LanguageModel._model_name_to_class_map[cls._MODEL_NAME] = cls

    @classmethod
    def from_pretrained(
        cls, model_name: str, **kwargs: Dict[str, Any]
    ) -> "_LanguageModel":
        """Loads a LanguageModel.

        Args:
            name: Name of the model.
            **kwargs: Keyword arguments for the specified model.

        Returns:
            An instance of `LanguageModel` class or a derived class.
        """
        if not model_name:
            raise ValueError(
                "Please specify model_name when calling `from_pretrained`. "
                f"Available model names are: {list(_LanguageModel._model_name_to_class_map.keys())}"
            )
        if model_name:
            if not model_name in _LanguageModel._model_name_to_class_map:
                raise ValueError(
                    f"Unknown model name '{model_name}'. "
                    f"Available model names are: {list(_LanguageModel._model_name_to_class_map.keys())}"
                )
            cls = _LanguageModel._model_name_to_class_map[model_name]

        return cls(
            **kwargs,
        )

    @classmethod
    def list_tuned_model_names(cls, model_name: Optional[str] = None) -> Sequence[str]:
        """Lists the names of tuned models.

        Args:
            model_name: Optional. Model name to get tuned models for.
                Model names are the same as used in `LanguageModel.from_pretrained()`

        Returns:
            A list of tuned models that can be used with the `get_tuned_model` method.
        """
        if cls == _LanguageModel and not model_name:
            raise RuntimeError("Specify 'model_name' or use a concrete model class.")
        if model_name:
            cls = _LanguageModel._model_name_to_class_map[model_name]
        if not cls._TUNING_MODEL_ID:
            raise RuntimeError(f"The {cls.__name__} model does not support tuning")
        return _list_tuned_model_names(cls._TUNING_MODEL_ID)

    @classmethod
    def get_tuned_model(
        cls, tuned_model_name: str, model_name: Optional[str] = None
    ) -> "_LanguageModel":
        """Loads the specified tuned language model."""
        if cls == _LanguageModel and not model_name:
            raise RuntimeError("Specify 'model_name' or use a concrete model class.")
        if model_name:
            cls = _LanguageModel._model_name_to_class_map[model_name]
        if not cls._TUNING_MODEL_ID:
            raise RuntimeError(f"The {cls.__name__} model does not support tuning")

        tuned_vertex_model = aiplatform.Model(tuned_model_name)
        tuned_model_deployments = tuned_vertex_model.gca_resource.deployed_models
        if len(tuned_model_deployments) == 0:
            # Deploying the model
            endpoint_name = tuned_vertex_model.deploy().resource_name
        else:
            endpoint_name = tuned_model_deployments[0].endpoint
        model = cls(endpoint_name=endpoint_name)
        return model

    def tune_model(
        self,
        training_data: Union[str, "pandas.core.frame.DataFrame"],
        train_steps: int = 1000,
        tuning_job_location: Optional[str] = None,
        tuned_model_location: Optional[str] = None,
    ):
        """Tunes a model based on training data.

        This method launches a model tuning job that can take some time.

        Args:
            training_data: A Pandas DataFrame of a URI pointing to data in JSON lines format.
                The dataset must have the "input_text" and "output_text" columns.
            train_steps: Number of training steps to perform.
            tuning_job_location: GCP location where the tuning job should be run. Only "europe-west4" is supported for now.
            tuned_model_location: GCP location where the tuned model should be deployed. Only "us-central1" is supported for now.

        Returns:
            A `LanguageModelTuningJob` object that represents the tuning job.
            Calling `job.result()` blocks until the tuning is complete and returns a `LanguageModel` object.
        """
        if tuning_job_location != _TUNING_LOCATION:
            raise ValueError(
                f'Tuning is only supported in the following locations: tuning_job_location="{_TUNING_LOCATION}"'
            )
        if tuned_model_location != _TUNED_MODEL_LOCATION:
            raise ValueError(
                f'Model deployment is only supported in the following locations: tuned_model_location="{_TUNED_MODEL_LOCATION}"'
            )

        if not self._TUNING_MODEL_ID:
            raise RuntimeError(
                f"The {type(self).__name__} model does not support tuning"
            )
        pipeline_job = _launch_tuning_job(
            training_data=training_data,
            train_steps=train_steps,
            model_id=self._TUNING_MODEL_ID,
        )

        job = _LanguageModelTuningJob(
            base_model=self,
            job=pipeline_job,
        )
        self._job = job
        tuned_model = job.result()
        # The UXR study attendees preferred to tune model in place
        self._endpoint = tuned_model._endpoint


@dataclasses.dataclass
class TextGenerationResponse:
    """TextGenerationResponse represents a response of a language model.

    This class is *experimental* and can be changed in the future.
    """

    text: str
    _prediction_response: Any

    def __repr__(self):
        return self.text


class TextGenerationModel(_LanguageModel):
    """TextGenerationModel represents a general language model.

    This class is *experimental* and can be changed in the future.

    Examples:

        # Getting answers:
        model = TextGenerationModel.from_pretrained("text-bison-001")
        model.predict("What is life?")
    """

    _MODEL_NAME = "text-bison-001"
    _LLM_ENDPOINT_NAME = "projects/cloud-large-language-models/locations/us-central1/endpoints/text-bison-001"
    # TODO: Put the correct information here when it's known
    _TUNING_MODEL_ID = "text-bison-001"

    _DEFAULT_TEMPERATURE = 0.0
    _DEFAULT_MAX_OUTPUT_TOKENS = 128
    _DEFAULT_TOP_P = 0.95
    _DEFAULT_TOP_K = 40

    def predict(
        self,
        prompt: str,
        max_output_tokens: int = _DEFAULT_MAX_OUTPUT_TOKENS,
        temperature: float = _DEFAULT_TEMPERATURE,
        top_k: int = _DEFAULT_TOP_K,
        top_p: float = _DEFAULT_TOP_P,
    ) -> "TextGenerationResponse":
        """Gets model response for a single prompt.

        Args:
            prompt: Question to ask the model.
            max_output_tokens: Max length of the output text in tokens.
            temperature: Controls the randomness of predictions. Range: [0, 1].
            top_k: The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p: The cumulative probability of parameter highest probability vocabulary tokens to keep for nucleus sampling. Range: [0, 1].

        Returns:
            A `TextGenerationResponse` object that contains the text produced by the model.
        """

        return self._batch_predict(
            prompts=[prompt],
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )[0]

    def _batch_predict(
        self,
        prompts: List[str],
        max_output_tokens: int = _DEFAULT_MAX_OUTPUT_TOKENS,
        temperature: float = _DEFAULT_TEMPERATURE,
        top_k: int = _DEFAULT_TOP_K,
        top_p: float = _DEFAULT_TOP_P,
    ) -> List["TextGenerationResponse"]:
        """Gets model response for a single prompt.

        Args:
            prompts: Questions to ask the model.
            max_output_tokens: Max length of the output text in tokens.
            temperature: Controls the randomness of predictions. Range: [0, 1].
            top_k: The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p: The cumulative probability of parameter highest probability vocabulary tokens to keep for nucleus sampling. Range: [0, 1].

        Returns:
            A list of `TextGenerationResponse` objects that contain the texts produced by the model.
        """
        instances = [{"content": str(prompt)} for prompt in prompts]
        prediction_parameters = {
            "temperature": temperature,
            "maxDecodeSteps": max_output_tokens,
            "topP": top_p,
            "topK": top_k,
        }

        prediction_response = self._endpoint.predict(
            instances=instances,
            parameters=prediction_parameters,
        )

        return [
            TextGenerationResponse(
                text=prediction["content"],
                _prediction_response=prediction_response,
            )
            for prediction in prediction_response.predictions
        ]


TextGenerationModel._register_model_class()


class ChatModel(TextGenerationModel):
    """ChatModel represents a language model that is capable of chat.

    This class is *experimental* and can be changed in the future.

    Examples:

        # Getting answers:
        model = ChatModel.from_pretrained("text-bison-alpha")
        model.predict("What is life?")

        # Chat:
        chat = model.start_chat()

        chat.send_message("Do you know any cool events this weekend?")
    """

    _MODEL_NAME = "text-bison-alpha"
    _LLM_ENDPOINT_NAME = "projects/cloud-large-language-models/locations/us-central1/endpoints/text-bison-alpha"
    # TODO: Put the correct information here when it's known
    _TUNING_MODEL_ID = None

    def start_chat(
        self,
        max_output_tokens: int = TextGenerationModel._DEFAULT_MAX_OUTPUT_TOKENS,
        temperature: float = TextGenerationModel._DEFAULT_TEMPERATURE,
        top_k: int = TextGenerationModel._DEFAULT_TOP_K,
        top_p: float = TextGenerationModel._DEFAULT_TOP_P,
    ) -> "ChatSession":
        """Starts a chat session with the model.

        Args:
            max_output_tokens: Max length of the output text in tokens.
            temperature: Controls the randomness of predictions. Range: [0, 1].
            top_k: The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p: The cumulative probability of parameter highest probability vocabulary tokens to keep for nucleus sampling. Range: [0, 1].

        Returns:
            A `ChatSession` object.
        """
        return ChatSession(
            model=self,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )


ChatModel._register_model_class()


class ChatSession:
    """ChatSession represents a chat session with a language model.

    Within a chat session, the model keeps context and remembers the previous conversation.

    This class is *experimental* and can be changed in the future.
    """

    def __init__(
        self,
        model: ChatModel,
        max_output_tokens: int = TextGenerationModel._DEFAULT_MAX_OUTPUT_TOKENS,
        temperature: float = TextGenerationModel._DEFAULT_TEMPERATURE,
        top_k: int = TextGenerationModel._DEFAULT_TOP_K,
        top_p: float = TextGenerationModel._DEFAULT_TOP_P,
    ):
        self._model = model
        self._history = []
        self._history_text = ""
        self._max_output_tokens = max_output_tokens
        self._temperature = temperature
        self._top_k = top_k
        self._top_p = top_p

    def send_message(
        self,
        message: str,
        *,
        max_output_tokens: int = TextGenerationModel._DEFAULT_MAX_OUTPUT_TOKENS,
        temperature: float = TextGenerationModel._DEFAULT_TEMPERATURE,
        top_k: int = TextGenerationModel._DEFAULT_TOP_K,
        top_p: float = TextGenerationModel._DEFAULT_TOP_P,
    ) -> "TextGenerationResponse":
        """Sends message to the language model and gets a response.

        Args:
            message: Message to send to the model
            max_output_tokens: Max length of the output text in tokens.
            temperature: Controls the randomness of predictions. Range: [0, 1].
            top_k: The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p: The cumulative probability of parameter highest probability vocabulary tokens to keep for nucleus sampling. Range: [0, 1].

        Returns:
            A `TextGenerationResponse` object that contains the text produced by the model.
        """
        new_history_text = ""
        if self._history_text:
            new_history_text = self._history_text.rstrip("\n") + "\n\n"
        new_history_text += message.rstrip("\n") + "\n"

        response_obj = self._model.predict(
            prompt=new_history_text,
            max_output_tokens=max_output_tokens or self._max_output_tokens,
            temperature=temperature or self._temperature,
            top_k=top_k or self._top_k,
            top_p=top_p or self._top_p,
        )
        response_text = response_obj.text

        self._history.append((message, response_text))
        new_history_text += response_text.rstrip("\n") + "\n"
        self._history_text = new_history_text
        return response_obj


class TextEmbeddingModel(_LanguageModel):
    """TextEmbeddingModel converts text into a vector of floating-point numbers.

    This class is *experimental* and can be changed in the future.

    Examples:

        # Getting embedding:
        model = TextEmbeddingModel.from_pretrained("embedding-gecko-001")
        embeddings = model.get_embeddings(["What is life?"])
        for embedding in embeddings:
            vector = embedding.values
            print(len(vector))
    """

    _MODEL_NAME = "embedding-gecko-001"
    _LLM_ENDPOINT_NAME = "projects/cloud-large-language-models/locations/us-central1/endpoints/embedding-gecko-001"

    def get_embeddings(self, texts: List[str]) -> List["TextEmbedding"]:
        instances = [{"content": str(text)} for text in texts]

        prediction_response = self._endpoint.predict(
            instances=instances,
        )

        return [
            TextEmbedding(
                values=prediction["embeddings"]["values"],
                _prediction_response=prediction_response,
            )
            for prediction in prediction_response.predictions
        ]


class TextEmbedding:
    """Contains text embedding vector."""

    def __init__(
        self,
        values: List[float],
        _prediction_response: Any = None,
    ):
        self.values = values
        self._prediction_response = _prediction_response


TextEmbeddingModel._register_model_class()


###### Model tuning

# Endpoint label/metadata key to preserve the base model ID information
_TUNING_BASE_MODEL_ID_LABEL_KEY = "google-vertex-llm-tuning-base-model-id"
# Currently, tuning can only work in this location
_TUNING_LOCATION = "europe-west4"
# Currently, deployment can only work in this location
_TUNED_MODEL_LOCATION = "us-central1"


class _LanguageModelTuningJob:
    """LanguageModelTuningJob represents a fine-tuning job."""

    def __init__(
        self,
        base_model: _LanguageModel,
        job: aiplatform.PipelineJob,
    ):
        self._base_model = base_model
        self._job = job
        self._model: Optional[_LanguageModel] = None

    def result(self) -> "_LanguageModel":
        """Blocks until the tuning is complete and returns a `LanguageModel` object."""
        if self._model:
            return self._model
        self._job.wait()
        upload_model_tasks = [
            task_info
            for task_info in self._job.gca_resource.job_detail.task_details
            if task_info.task_name == "upload-llm-model"
        ]
        if len(upload_model_tasks) != 1:
            raise RuntimeError(
                f"Failed to get the model name from the tuning pipeline: {self._job.name}"
            )
        upload_model_task = upload_model_tasks[0]

        # Trying to get model name from output parameter
        vertex_model_name = upload_model_task.execution.metadata[
            "output:model_resource_name"
        ].strip()
        _LOGGER.info(f"Tuning has completed. Created Vertex Model: {vertex_model_name}")
        self._model = type(self._base_model).get_tuned_model(
            tuned_model_name=vertex_model_name
        )
        return self._model

    @property
    def status(self):
        """Job status"""
        return self._job.state

    def cancel(self):
        self._job.cancel()


def _get_tuned_models_dir_uri(model_id: str) -> str:
    staging_gcs_bucket = (
        gcs_utils.create_gcs_bucket_for_pipeline_artifacts_if_it_does_not_exist()
    )
    return (
        staging_gcs_bucket.replace("/output_artifacts/", "/tuned_language_models/")
        + model_id
    )


def _list_tuned_model_names(model_id: str) -> List[str]:
    tuned_models = aiplatform.Model.list(
        filter=f'labels.{_TUNING_BASE_MODEL_ID_LABEL_KEY}="{model_id}"',
        # TODO(b/275444096): Remove the explicit location once models are deployed to the user's selected location
        location=_TUNED_MODEL_LOCATION,
    )
    model_names = [model.resource_name for model in tuned_models]
    return model_names


def _generate_tuned_model_dir_uri(model_id: str) -> str:
    tuned_model_id = "tuned_model_" + aiplatform_utils.timestamped_unique_name()
    tuned_models_dir_uri = _get_tuned_models_dir_uri(model_id=model_id)
    tuned_model_dir_uri = _uri_join(tuned_models_dir_uri, tuned_model_id)
    return tuned_model_dir_uri


def _launch_tuning_job(
    training_data: Union[str, "pandas.core.frame.DataFrame"],
    model_id: str,
    train_steps: Optional[int] = None,
) -> aiplatform.PipelineJob:
    output_dir_uri = _generate_tuned_model_dir_uri(model_id=model_id)
    if isinstance(training_data, str):
        dataset_uri = training_data
    elif pandas and isinstance(training_data, pandas.DataFrame):
        dataset_uri = _uri_join(output_dir_uri, "training_data.jsonl")

        with tempfile.NamedTemporaryFile() as temp_file:
            dataset_path = temp_file.name
            df = training_data
            df = df[["input_text", "output_text"]]
            df.to_json(path_or_buf=dataset_path, orient="records", lines=True)
            storage_client = storage.Client(
                credentials=aiplatform_initializer.global_config.credentials
            )
            storage.Blob.from_string(
                uri=dataset_uri, client=storage_client
            ).upload_from_filename(filename=dataset_path)
    else:
        raise TypeError(f"Unsupported training_data type: {type(training_data)}")

    job = _launch_tuning_job_on_jsonl_data(
        model_id=model_id,
        dataset_name_or_uri=dataset_uri,
        train_steps=train_steps,
    )
    return job


def _launch_tuning_job_on_jsonl_data(
    model_id: str,
    dataset_name_or_uri: str,
    train_steps: Optional[int] = None,
) -> aiplatform.PipelineJob:
    pipeline_arguments = {
        "train_steps": train_steps,
        "project": aiplatform_initializer.global_config.project,
        # TODO(b/275444096): Remove the explicit location once tuning can happen in all regions
        # "location": aiplatform_initializer.global_config.location,
        "location": _TUNED_MODEL_LOCATION,
        "large_model_reference": model_id,
        "model_display_name": model_id + "-tuned",
    }

    if dataset_name_or_uri.startswith("projects/"):
        pipeline_arguments["dataset_name"] = dataset_name_or_uri
    if dataset_name_or_uri.startswith("gs://"):
        pipeline_arguments["dataset_uri"] = dataset_name_or_uri
    job = aiplatform.PipelineJob(
        template_path="https://us-kfp.pkg.dev/vertex-ai/large-language-model-pipelines/tune-large-model/preview",
        display_name=None,
        parameter_values=pipeline_arguments,
        # TODO(b/275444101): Remove the explicit location once model can be deployed in all regions
        location=_TUNING_LOCATION,
    )
    job.submit()
    return job


def _uri_join(uri: str, path_fragment: str) -> str:
    """Appends path fragment to URI.

    urllib.parse.urljoin only works on URLs, not URIs
    """

    return uri.rstrip("/") + "/" + path_fragment.lstrip("/")
