---
sidebar_label: CRUD APIs for Achievement
sidebar_position: 3
---

# CRUD APIs for Achievement

The following steps are regarding the CRUD APIs for achievements


### Create an achievement

To create an achievement, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/achievement`**

The request body for the API is as follows:

```json
{
  "type": "course equate",
  "name": "ML Professional",
  "description": "",
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "associations": {
    "exact_match_of": [],
    "exemplar": [],
    "has_skill_level": [],
    "is_child_of": [],
    "is_parent_of": [],
    "is_part_of": [],
    "is_peer_of": [],
    "is_related_to": [],
    "precedes": [],
    "replaced_by": []
  },
  "tags": ["ML"],
  "credits_available": 0,
  "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
  "image": "",
  "result_descriptions": [],
  "timestamp": ""
}
```

The achievement would then be created and the response message would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the achievement",
  "data": {
    "uuid": "U2DDBkl3Ayg0PWudzhI",
    "type": "course equate",
    "name": "ML Professional",
    "description": "",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "associations": {
      "exact_match_of": [],
      "exemplar": [],
      "has_skill_level": [],
      "is_child_of": [],
      "is_parent_of": [],
      "is_part_of": [],
      "is_peer_of": [],
      "is_related_to": [],
      "precedes": [],
      "replaced_by": []
    },
    "tags": ["ML"],
    "credits_available": 0,
    "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
    "image": "",
    "result_descriptions": [],
    "timestamp": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Get all achievements

When we need to fetch all available achievements then we would make a **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/achievements`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of achievement array to be returned which takes a default value **`10`** if not provided. This will fetch the list of available achievements.

```json
{
  "success": true,
  "message": "Successfully fetched the achievements",
  "data": {
    "records": [
      {
        "uuid": "U2DDBkl3Ayg0PWudzhI",
        "type": "course equate",
        "name": "ML Professional",
        "description": "",
        "alignments": {
          "competency_alignments": [],
          "skill_alignments": []
        },
        "associations": {
          "exact_match_of": [],
          "exemplar": [],
          "has_skill_level": [],
          "is_child_of": [],
          "is_parent_of": [],
          "is_part_of": [],
          "is_peer_of": [],
          "is_related_to": [],
          "precedes": [],
          "replaced_by": []
        },
        "tags": ["ML"],
        "credits_available": 0,
        "field_of_study": "",
        "metadata": {"design_config" : {
                                  "shape" : "",
                                  "theme": "",
                                  "illustration": ""
        }},
        "image": "",
        "result_descriptions": [],
        "timestamp": "",
        "is_archived": false,
        "created_time": "2022-03-03 09:22:49.843674+00:00",
        "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
      }
    ],
    "total_count": 10000
  }
}
```

### Get a specific achievement

When we need to fetch the details of a specific achievement then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/achievement/{uuid}`** where **`uuid`** is the unique ID of the achievement.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the achievement",
  "data": {
    "uuid": "U2DDBkl3Ayg0PWudzhI",
    "type": "course equate",
    "name": "ML Professional",
    "description": "",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "associations": {
      "exact_match_of": [],
      "exemplar": [],
      "has_skill_level": [],
      "is_child_of": [],
      "is_parent_of": [],
      "is_part_of": [],
      "is_peer_of": [],
      "is_related_to": [],
      "precedes": [],
      "replaced_by": []
    },
    "tags": ["ML"],
    "credits_available": 0,
    "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
    "image": "",
    "result_descriptions": [],
    "timestamp": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

If the achievement is not present for a given uuid - **`random_id`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Achievement with uuid random_id not found",
    "data": null
}
```

### Update a specific achievement

When we need to update the details of a specific achievement then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/achievement/{uuid}`** where **`uuid`** is the unique ID of the achievement.
The request body would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the achievement",
  "data": {
    "type": "competency",
    "name": "ML Professional",
    "description": "Updated description",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "associations": {
      "exact_match_of": [],
      "exemplar": [],
      "has_skill_level": [],
      "is_child_of": [],
      "is_parent_of": [],
      "is_part_of": [],
      "is_peer_of": [],
      "is_related_to": [],
      "precedes": [],
      "replaced_by": []
    },
    "tags": ["ML"],
    "credits_available": 0,
    "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
    "image": "",
    "result_descriptions": [],
    "timestamp": "",
    "is_archived": false
  }
}
```

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully updated the achievement",
  "data": {
    "uuid": "U2DDBkl3Ayg0PWudzhI",
    "type": "competency",
    "name": "ML Professional",
    "description": "Updated description",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "associations": {
      "exact_match_of": [],
      "exemplar": [],
      "has_skill_level": [],
      "is_child_of": [],
      "is_parent_of": [],
      "is_part_of": [],
      "is_peer_of": [],
      "is_related_to": [],
      "precedes": [],
      "replaced_by": []
    },
    "tags": ["ML"],
    "credits_available": 0,
    "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
    "image": "",
    "result_descriptions": [],
    "timestamp": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

If the achievement is not present for a given uuid - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Achievement with uuid WPXbWYopqpoTbyl9 not found",
    "data": null
}
```

### Delete a specific achievement

When we need to delete a specific achievement then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/achievement/{uuid}`** where **`uuid`** is the unique ID of the achievement.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the achievement"
}
```

If the achievement is not present for a given uuid - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Achievement with uuid WPXbWYopqpoTbyl9 not found",
    "data": null
}
```
