---
sidebar_label: CRUD APIs for Statement
sidebar_position: 5
---

# CRUD APIs for Statement

The following steps are regarding the CRUD APIs for Statements

### Create a Statement

To create one or more Statements, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/statement`** .

The request body for the API is as follows:

```json
[
  {
    "actor": {
      "uuid": "2ivy523v5y6ynefn7a",
      "object_type": "agent",
      "name": "Learner1",
      "mbox": "mailto:test_agent@example.org",
      "mbox_sha1sum": "",
      "open_id": "",
      "account_homepage": "",
      "account_name": "",
      "members": [],
      "user_id": ""
    },
    "verb": {
      "uuid": "v1bv9an0sf1n2u08na",
      "name": "Verb1",
      "url": "http://example.com/xapi/verbs#verb1",
      "canonical_data": {}
    },
    "object": {
      "uuid": "1bcv1629rbcayb8gs",
      "name": "Activity1",
      "authority": "Sample Authority",
      "canonical_data": {
        "name": "Learning Object 1",
        "type": "learning_objects",
        "uuid": "Hboh8qf4aw3bgBooDQ"
      }
    },
    "object_type": "activities",
    "timestamp": "",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": []
  }
]
```

In the input payload, **`actor`** refers to an Agent (Agent data model) or Group, **`verb`** is the action (Verb data model) and **`object`** can be an Activity (Activity data model) or another statement as well.

Before adding a statement, the firestore collection must have the valid Agent, Verb, and Activity data that are passed in the payload of the statement otherwise **`ResourceNotFoundException`** exception is raised.

The **`type`** field in the object's canonical data must be either of these - `learning_experiences`
, `curriculum_pathways`, `assessment_items`, `learning_resources` or `learning_objects`. And the id referenced in the canonical data must already exist in the firestore collection before creating a statement.

:::note

The standard types of the object's canonical data can be further improved upon request.

:::

After successfully adding new Statements document to the Big Query, you will get the list of statement ids, similar to the below json:

```json
{
  "success": true,
  "message": "Successfully added the given statement/s",
  "data": ["98c60a1f-28f2-46a8-a3b5-35ed8e22d3d3"]
}
```

### Get all Statements

When we need to fetch all the Statements available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/statement`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Statement array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Statements.

```json
{
  "success": true,
  "message": "Successfully fetched the statements",
  "data": {
    "records": [
    {
      "actor": {
        "uuid": "2ivy523v5y6ynefn7a",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:test_agent@example.org",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": ""
      },
      "verb": {
        "uuid": "v1bv9an0sf1n2u08na",
        "name": "Verb1",
        "url": "http://example.com/xapi/verbs#verb1",
        "canonical_data": {}
      },
      "object": {
        "uuid": "1bcv1629rbcayb8gs",
        "name": "Activity1",
        "authority": "Sample Authority",
        "canonical_data": {}
      },
      "object_type": "activities",
      "result": {},
      "context": {},
      "timestamp": "2022-09-01 09:45:19 +0000",
      "authority": {},
      "attachments": [],
      "uuid": "98c60a1f-28f2-46a8-a3b5-35ed8e22d3d3",
      "stored": "2022-09-01 09:45:19 +0000"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific Statement

When we need to fetch the details of a specific Statement then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/statement/{uuid}`** where **`uuid`** is the unique ID of the statement.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the statement",
  "data": {
    "actor": {
      "uuid": "2ivy523v5y6ynefn7a",
      "object_type": "agent",
      "name": "Learner1",
      "mbox": "mailto:test_agent@example.org",
      "mbox_sha1sum": "",
      "open_id": "",
      "account_homepage": "",
      "account_name": "",
      "members": [],
      "user_id": ""
    },
    "verb": {
      "uuid": "v1bv9an0sf1n2u08na",
      "name": "Verb1",
      "url": "http://example.com/xapi/verbs#verb1",
      "canonical_data": {}
    },
    "object": {
      "uuid": "1bcv1629rbcayb8gs",
      "name": "Activity1",
      "authority": "Sample Authority",
      "canonical_data": {}
    },
    "object_type": "activities",
    "result": {},
    "context": {},
    "timestamp": "2022-09-01 09:45:19 +0000",
    "authority": {},
    "attachments": [],
    "uuid": "98c60a1f-28f2-46a8-a3b5-35ed8e22d3d3",
    "stored": "2022-09-01 09:45:19 +0000"
  }
}
```

If the Statement is not present for a given uuid - **`98c60a1f-28f2-46a8-a3b5-8e22`** then the response would be as follows:

```json
{
  "success": false,
  "message": "xAPI Statement with '98c60a1f-28f2-46a8-a3b5-8e22' not found",
  "data": null
}
```
