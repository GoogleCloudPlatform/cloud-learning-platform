---
sidebar_label: Training Deep Knowledge Tracing Model
sidebar_position: 3
---

# Training Deep Knowledge Tracing Model

The following steps are to train the Deep Knowledge Tracing Model


### Step 1:

Ensure that the data required to train the Deep Knowledge Tracing Model is available in the database as part of the user_events collection. If not, please ingest user_events according to the steps described in the earlier section.

### Step 2:

Training the Deep Knowledge Tracing Model at a course level can be initiated by sending a **POST** request using 
the API **`<APP_URL>/deep-knowledge-tracing/api/v1/train`** where the request body will contain information about the course and job_title as below

```json
{
  "course_id": "test_course",
  "title": "sampe-job-title"
}
```

On successful hit, an async experiment (batch job) will be created in the background which will train DKT model. And the response will contain this experiment (job) information similar to the below json

```json
{
  "success": true,
  "message": "Successfully initiated the experiment with type 'deep-knowledge-tracing'. Please use the experiment id to track status",
  "data": {
    "experiment_id": "34176209-39a3-42e0-bbc5-5135a525fbcb",
    "status": "active"
  }
}
```

### Step 3:

(approx time taken for this step: 5 minute)

We can check the status of the experiment using the experiment id that we get in the response.
For that, we can hit the **GET** request using the API **`<APP_URL>/deep-knowledge-tracing/api/v1/experiments/{experiment_id}`** where we pass the experiment_id as path param(in this case, the API url will look like <{base_url}/deep-knowledge-tracing/api/v1/experiments/34176209-39a3-42e0-bbc5-5135a525fbcb)

The response will look like this:

```json
{
  "success": true,
  "message": "Successfully fetched experiment details",
  "data": {
    "experiment_id": "34176209-39a3-42e0-bbc5-5135a525fbcb",
    "created_by": "",
    "created_time": "2022-12-26 11:53:49.900549+00:00",
    "last_modified_by": "",
    "last_modified_time": "2022-12-26 11:55:12.094668+00:00",
    "input_data": {
        "course_id": "test_course",
        "title": "sampe-job-title"
      },
    "status": "succeeded",
    "metadata": {"history":{
      "auc":[0.953,0.956,0.96],
      "binary_accuracy":[0.88,0.881,889],
      "loss" : [0.258,0.253,0.244],
      "precision": [0.85,0.866,0.87],
      "recall": [0.80,789,0.805],
      "val_auc":[0.97,0.974,0.974],
      "val_binary_accuracy":[0.903,0.915,0.91],
      "val_loss" : [0.22,0.20,019],
      "val_precision": [0.90,0.945,0.918],
      "val_recall": [0.817,0.816,0.825],
      },
    "evaluation_score":{
      "auc":0.976,
      "binary_accuracy" : 0.9176,
      "loss" : 0.185,
      "precision" : 0.928,
      "recall" : 0.836
}}
    "errors": {},
    "type": "deep-knowledge-tracing"
  }
}
```

Here, the **`status`** in the **`data`** key shows the success status of the job which in this case is "succeeded".

For successful experiments, field metadata contains the train, validation and test scores for the experiment. The field history contains the train and validation scores for every epoch in the experiment and the field evaluation_score holds the test score.(Note: Currently, the DKT model is configured to train for 10 Epochs)

If it fails for some reason, we will have **`status`** as "failed" with the explanation/data available in the **`errors`** key.
