---
sidebar_label: Execute Rules Engine EndPoint
sidebar_position: 5
---

# Execute Rules Engine EndPoint

The following steps are regarding the execute Rules Engine EndPoint


### Execute a Rule

To execute one or more rules, a **POST** request has to be made to he API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`** .

Sample request body for the API is as follows:

```json
[
  {
    "verb": "started",
    "user_id": "",
    "node_id": "",
    "node_type": "",
    "session_id": "",
    "data": {}
  }
]
```
In the input payload, 
**`verb`** refers to the action (Verb data model) which has been accomplished. Currently, it must be either of these - `started` and `completed`.
**`user_id`** refers to the UUID of the user who has performed the action.
**`node_id`** refers to the UUID from the Learning Hierarchy on which the action has been completed.
**`node_type`** refers to the type of Learning Hierarchy. It must be either of these - `learning_experiences`
, `curriculum_pathways`, `assessments`, `learning_resources` or `learning_objects`
**`session_id`** refers to the session UUID during the which action was completed.
**`data`** optional dict to send additional data for the rule, for e.g. comments.

::: note
More rules for verbs like `submitted`, `non-eval`, `evaluated`, etc. will be added and updated in the doc here.
:::

Before adding a statement, the firestore collection must have the user_id, node_id, session_id and Verb name data that are passed in the payload of the statement otherwise **`ResourceNotFoundException`** exception is raised.


After successfully executing the rule, you will get the list of responses returned after executing the rules in the response as shown below:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    {
      "user_id": "sample_user_id",
      "parent_session_id": "sample_login_session_id",
      "session_data": null,
      "session_id": "sample_session_id",
      "created_time": "2023-01-17 16:49:54.203242+00:00",
      "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
    }
  ]
}
```

If multiple rules are executed, a list of responses from each rule is returned. For rules which don't return a response `null` is returned. A sample response for multiple rules getting executed is shown below:

```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    {"sample response from rule 1"},
    null,  // sample response from rule 2
    {"sample response from rule 3"}
  ]
}
```
