---
sidebar_label: Unlocking, Starting and completing a SRL Module
sidebar_position: 2
---

# Unlocking, Starting and completing a SRL Module

The following steps are to create the flow for unlocking, starting and completing a SRL Module

:::note

Assumptions:
- Learner has logged in and has a valid `user_id`, `learner_id` and `session_id`
- Learner is interacting with a learning hierarchy that has atleast a `learning_object` that acts as a unit overview and acts as prerequisite for the srl module
- Additionally, the learning hierarchy should also have a `learning_experience` node as a parent node to the unit overview and srl module
- Further, a learning_resource must be created and set as the child_node for the SRL learning object module
- The SRL module in the learning hierarchy is a `learning_object` node of `type` set as `srl`
- The user has access to the `node_id` of the unit overview module as well as the srl module

:::

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)

### Unlocking a srl module

When a learner completes the unit overview module. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule creates a new sub-session within the current `session_id` and return that session. It also marks the status of unit overview as `completed` and the parent `learning experience` will be marked as `in_porgress`. Further it will also unlock the dependent srl module; the status of the srl module will be markd as `not_started` but will be unlocked, `is_locked` flag will also be marked as `False` for the srl module.
To check the progres and updates on the learning_modules for the learner, the user needs to access the SLP endpoints to fetch the user specific hierarchy.

The `node_id` here is the uuid of the unit overview node

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_objects",
    "node_id": "sample_learning_object_id",
    "session_id": "sample_login_session_id",
    "verb": "completed"
  }
]
```
After the rule is eectued successfullym the folliwing response would be seen
```json
{
  "success": true,
  "message": "Successfully executed the rules",
  "data": [
    null
  ]
}
```
Once the `completed` rule is executed for the learning_object, the srl module is marked as unlocked, and is_hidden is set to False and the corresposning parent_node is also stored.
However, the is_hidden adn is_locked flags in the progress are applicable only for the specific parent_node i.e the srl module is visible and unlocked only in the heirarchy for the parent_node.
This can be checked using the slp endpoints to fetch the learner's progress.

### Starting a SRL Learning Resource

When a learner starts a srl learning resource the `started` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule tries to find the latest session for the given `user_id` and `node_id` and copies the `session_data` from that session.

:::note

To use `started` rule, the learner should have previously unlocked the parent node of the srl learning resource.
:::

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

### Completing a SRL Learning Resource

When a learner successfully completes a SRL learning resource the `completed` rule should be executed. A **POST** request has to be made to the API endpoint - **`<APP_URL>/rules-engine/api/v1/execute-rule`**

This rule marks the current node as completed and checks if its parent nodes can also be completed or unlocked recursively.

Sample request body is as follows:
```json
[
  {
    "user_id": "sample_user_id",
    "node_type": "learning_resources",
    "node_id": "srl_learning_resource_id",
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