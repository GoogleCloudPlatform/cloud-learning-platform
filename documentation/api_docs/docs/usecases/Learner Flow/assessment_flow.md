---
sidebar_label: Starting, Resuming and Submitting an Assessment
sidebar_position: 3
---

# Starting, Resuming and Submitting an Assessment

The following steps are to create the flow for starting, resuming and submitting an Assessments

:::note

Assumptions:
- Learner has logged in and has a valid `user_id`, `learner_id` and `session_id`
- Learner is interacting with an `assessments` node and has the `node_id` for that node

:::

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)


### Starting an Assessment

When a learner starts an assessment the `started` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule creates a new sub-session within the current `session_id` and return that session. It also marks the current node and its parent nodes as `in_progress`.

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "assessments",
    "node_id": "sample_assessment_id",
    "session_id": "sample_login_session_id",
    "verb": "started"
  }
]
```

After the `started` rule successfully executes following response is returned:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    {
      "user_id": "sample_user_id",
      "parent_session_id": "sample_login_session_id",
      "session_data": {
        "learnosity_session_id": "cf71bcf0-516f-4156-8ca9-d65115045a1e",
        "node_id": "sample_assessment_id",
        "node_type": "assessments"
      },
      "session_id": "sample_session_id",
      "created_time": "2023-01-17 16:49:54.203242+00:00",
      "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
    }
  ]
}
```

The response for this rule contains a `Session` object. The `learnosity_session_id` along with `user_id` and `activity_template_id` can be used to call Learnosity Items API in order to render the assessment.

### Resuming an Assessment

When a learner resumes an assessment the `resumed` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule tries to find the latest session for the given `user_id` and `node_id` and copies the `session_data` from that session.

:::note

To use `resumed` rule, the learner should have previously attempted that node. If there are no previous session found the API would return `404 ResourceNotFound` with message `No session found`.

:::

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "assessments",
    "node_id": "sample_assessment_id",
    "session_id": "sample_login_session_id",
    "verb": "resumed"
  }
]
```

After the `resumed` rule successfully executes following response is returned:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    {
      "user_id": "sample_user_id",
      "parent_session_id": "sample_login_session_id",
      "session_data": {
        "learnosity_session_id": "cf71bcf0-516f-4156-8ca9-d65115045a1e",
        "node_id": "sample_assessment_id",
        "node_type": "assessments"
      },
      "session_id": "sample_session_id",
      "created_time": "2023-01-17 16:49:54.203242+00:00",
      "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
    }
  ]
}
```

The response for this rule contains a `Session` object. The `learnosity_session_id` along with `user_id` and `activity_template_id` can be used to call Learnosity Items API in order to render the assessment.

### Submitting a Manual Graded or Autograded Assessment

When a learner successfully submits an assessment the `submitted` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule will perform the following operations:
1. Create a new `SubmittedAssessment` for the submission and return that as response.
2. Fetch responses and scores from Learnosity and evaluate the assessment in case the assessment is of `autograded` tag.
    - If the learner has passed the evaluation, then check all unlocked learning hierarchy nodes, mark all completed nodes, fetch the achievements and skills awarded and update the student's learner profile with progress.
    - If the learner has failed the evaluation, then update the progress in student's learner profile with the assessment's status as "evaluated".
3. If the assessment is of `manually graded` tag, then update the progress in student's learner profile with the assessment's status as "evaluation_pending".

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "assessments",
    "node_id": "sample_assessment_id",
    "session_id": "sample_login_session_id",
    "verb": "submitted"
  }
]
```

After the `submitted` rule successfully executes following response is returned for an autograde assessment where learner has passed the assessment:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    {
      "assessment_id": "sample_assessment_id",
      "learner_id": "sample_learner_id",
      "assessor_id": null,
      "type": "practice",
      "plagiarism_score": null,
      "plagiarism_report_path": null,
      "submission_gcs_paths": [],
      "result": null,
      "pass_status": true,
      "status": "completed",
      "is_flagged": false,
      "comments": null,
      "timer_start_time": "2023-01-18 07:23:36.029225+00:00",
      "attempt_no": 3,
      "learner_session_id": "cf71bcf0-516f-4156-8ca9-d65115045a1e",
      "learner_session_data": {
        "subscores": [
          {
            "num_questions": 20,
            "attempted_max_score": 20,
            "title": "biochem",
            "score": 19,
            "num_attempted": 20,
            "items": [
              "293486384",
              "293481468",
              "293475858",
              "293475234",
              "292922805"
            ],
            "max_score": 20,
            "id": "subscore-1"
          },
          {
            "attempted_max_score": 20,
            "items": [
              "293486384",
              "293481468",
              "293475858",
              "293475234",
              "292922805"
            ],
            "title": "inorganics",
            "num_attempted": 20,
            "max_score": 20,
            "score": 20,
            "id": "subscore-2",
            "num_questions": 20
          }
        ],
        "activity_id": "chemistry_classtest1",
        "score": 39,
        "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
        "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
        "responses": [
          {
            "score": 1,
            "dt_score_updated": "2017-06-19T02:03:19Z",
            "item_reference": "293486384",
            "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
            "max_score": 1
          }
        ],
        "max_score": 40,
        "status": "Completed"
      },
      "assessor_session_id": null,
      "submitted_rubrics": null,
      "overall_feedback": null,
      "uuid": "4xgZOWEPA8rGorz6bka9",
      "created_time": "2023-01-18 07:23:36.029225+00:00",
      "last_modified_time": "2023-01-18 07:23:36.242996+00:00",
      "created_by": "",
      "last_modified_by": ""
    }
  ]
}
```

As shown above the response contains the `SubmittedAssessment` created for the learner's submission. Also because the assessment was of tag `autograded` we also get the `learner_session_data` which contains responses from Learnosity.
