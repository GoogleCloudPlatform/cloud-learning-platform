---
sidebar_label: Inference using Deep Knowledge Tracing
sidebar_position: 4
---

# Inference using Deep Knowledge Tracing

The following steps are to get predictions using the Deep Knowledge Tracing Model


### Step 1:

Ensure that the model is trained for the course for which predictions are required. If not, please train DKT model according to the steps described in the earlier section.

### Step 2:

To get predictions of the Deep Knowledge Tracing Model at a course level for a given user we need to hit a **POST** request using 
the API **`<APP_URL>/deep-knowledge-tracing/api/v1/predict`** where the request body will be as below

```json
{
  "course_id": "test_course",
  "user_id": "sampe-user",
  "user_events": [{"learning_unit":"sample learning Unit 1", "is_correct": 0},
                  {"learning_unit":"sample learning Unit 2", "is_correct": 1},
                  {"learning_unit":"sample learning Unit 1", "is_correct": 1}
                  {"learning_unit":"sample learning Unit 1", "is_correct": 1}]
}
```
Here course_id is the course for which predictions are required and user_id is the identity of the user for whom DKT will predict mastery scores based on the recent activity captured through user events. The learning units in this API are expected to belong to the same course for which predictions are required.

On successful hit, the DKT model returns mastery score for all learning units (topics) that constitute the given course
as below

```json
{
"success": true,
"message": "Successfully generated predictions from dkt model",
"data": {
    "sample learning Unit 1":0.94,
    "sample learning Unit 2":0.77,
    "sample learning Unit 3":0.42,
    "sample learning Unit 4":0.12,
}
}
```