---
sidebar_label: Starting, Resuming and Completing a Learning Resource
sidebar_position: 2
---

# Starting, Resuming and Completing a Learning Resource

The following steps are to create the flow for starting, resuming and completing an Assessments

:::note

Assumptions:
- Learner has logged in and has a valid `user_id`, `learner_id` and `session_id`
- Learner is interacting with a `learning_resources` node and has the `node_id` for that node

:::

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)


### Starting a Learning Resource

When a learner starts a learning resource the `started` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule creates a new sub-session within the current `session_id` and return that session. It also marks the current node and its parent nodes as `in_progress`.

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_resources",
    "node_id": "sample_learning_resource_id",
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
        "learnosity_session_id": null,
        "node_id": "sample_learning_resource_id",
        "node_type": "learning_resources"
      },
      "session_id": "sample_session_id",
      "created_time": "2023-01-17 16:49:54.203242+00:00",
      "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
    }
  ]
}
```
The response for this rule contains a `Session` object.


### Resuming a Learning Resource

When a learner resumes a learning resource the `resumed` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule tries to find the latest session for the given `user_id` and `node_id` and copies the `session_data` from that session.

:::note

To use `resumed` rule, the learner should have previously attempted that node. If there are no previous session found the API would return `404 ResourceNotFound` with message `No session found`.

:::

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_resources",
    "node_id": "sample_learning_resource_id",
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
        "node_id": "sample_learning_resource_id",
        "node_type": "learning_resources"
      },
      "session_id": "sample_session_id",
      "created_time": "2023-01-17 16:49:54.203242+00:00",
      "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
    }
  ]
}
```
The response for this rule contains a `Session` object.

### Completing a Learning Resource

When a learner successfully completes a learning resource the `completed` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule marks the current node as completed and checks if its parent nodes can also be completed or unlocked recursively.

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_resources",
    "node_id": "sample_learning_resource_id",
    "session_id": "sample_login_session_id",
    "verb": "completed"
  }
]
```

After the `completed` rule successfully executes following response is returned:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    null
  ]
}
```

The response is `null` for the `completed` rule as no information is returned on execution of this rule.