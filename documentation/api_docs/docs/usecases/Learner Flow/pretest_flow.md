---
sidebar_label: Skipping a Pretest Module or Submitting an Pretest Assessment
sidebar_position: 4
---

# Skipping a Pretest Module and Submitting an Pretest Assessment

The following steps are to create the flow for skipping a pretest module or submitting a pretest assessment

:::note

Assumptions:
- Learner has logged in and has a valid `user_id`, `learner_id` and `session_id`
- Learner is interacting with an `pretest-module`/`pretest-assessment` node and has the `node_id` for that node

:::

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)


### Skipping a Pretest Module

When a learner successfully skips a pretest module the `skipped` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule will perform the following operations:
1. Update progress in student's learner profile with the `pretest-module` status as `skipped`.
2. Unlock `unit-overview` module in the same learning experience and update it's status in progress of student's learner profile.

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_objects",
    "node_id": "pretest_module_id",
    "session_id": "sample_login_session_id",
    "verb": "skipped"
  }
]
```

After the `skipped` rule successfully executes following response is returned:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": []
}
```
