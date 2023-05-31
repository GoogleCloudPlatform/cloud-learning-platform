---
sidebar_label: CRUD APIs for Discipline Association Groups
sidebar_position: 8
---

# CRUD APIs for Discipline Association Groups

The following steps are to create, view and update Discipline Association Groups.


### Create a Discipline Association Group:

To create a discipline association group, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association`**. The name field in the request body should be unique for every association group creation.
The request body for the API is as follows:

```json
{
  "name": "Discipline Association Group",
  "description": "Description for Discipline Association Group",
}
```

A new association group with the request body details and with a new uuid(unique ID of the group) is added to the association_groups collection. After successfully adding new association group document to the collection. You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Discipline Association Group",
    "description": "Description for Discipline Association Group",
    "association_type": "discipline",
    "users": [],
    "associations": {
      "curriculum_pathways": []
    },
    "created_time": "2023-02-10 11:54:36.604328+00:00",
    "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
  }
}
```

### Get all Discipline Association Groups:

To fetch all the discipline type of association groups available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-associations`** with **`skip`**, **`limit`** and **`fetch_tree`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of Association Group array to be returned which takes a default value **`10`** if not provided and

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the association groups",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "Discipline Association Group",
      "description": "Description for Discipline Association Group",
      "association_type": "discipline",
      "users": [],
      "associations": {
        "curriculum_pathways": []
      },
      "created_time": "2023-02-10 11:54:36.604328+00:00",
      "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
    }
  ]
}
```

### Get a Discipline Association Group:

To fetch the details of a specific discipline association group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}`** where **`uuid`** is the unique ID of the discipline association group and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Discipline Association Group",
    "description": "Description for Discipline Association Group",
    "association_type": "discipline",
    "users": [],
    "associations": {
      "curriculum_pathways": []
    },
    "created_time": "2023-02-10 11:54:36.604328+00:00",
    "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
  }
}
```

If the Association Group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "AssociationGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a Discipline Association Group:

To update the details of a discipline association group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}`** where **`uuid`** is the unique ID of the discipline association group.

The request body would be as follows:

```json
{
  "name": "Updated Discipline Association Group Name",
  "description": "Updated Discipline Association Group Description"
}
```

After the validation of group for given uuid, group for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Updated Discipline Association Group Name",
    "description": "Updated Discipline Association Group Description",
    "association_type": "discipline",
    "users": [],
    "associations": {
      "curriculum_pathways": []
    },
    "created_time": "2023-02-10 11:54:36.604328+00:00",
    "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
  }
}
```

If the Association Group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "AssociationGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Discipline Association Group:

To delete a discipline association group, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}`** where **`uuid`** is the unique ID of the discipline association group.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the association group"
}
```

If the Association group is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "AssociationGroup with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
### Add users to the Discipline Association Group:

To add users to the discipline association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}/users/add`** where **`uuid`** is the unique ID of the discipline association group.
**Note: User should only belong to instructor or assessor user group**

The request body would be as follows:

```json
{
  "users": ["WZFsczmmNdgWurlBCAiJ"],
  "status": "active"
}
```

After the validation of discipline association group for given uuid and also validating the given user is of **`user_type=faculty`**. discipline association group for the given uuid is updated with the given users list and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully added the users to the discipline association group",
  "data": {
    "name": "Discipline Association Group Name",
    "description": "Description for Discipline Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "discipline",
    "users": [
      {
        "user": "WZFsczmmNdgWurlBCAiJ",
        "user_type": "instructor",
        "status": "active"
      }
    ],
    "associations": {
      "curriculum_pathways": []
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:07:50.564027+00:00"
  }
}
```


### Get Users associated with a particular Discipline:

To fetch users(instructors/assessors) belonging to a particular discipline, we would make a **GET** request to the endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/discipline/{curriculum_pathway_id}/users`** with **`user_type`** parameter, where **`curriculum_pathway_id`** is the unique id of the discipline (curriculum pathway) and **`user_type`** is an optional parameter which takes one of the two values **`instructor`, `assessor`** that defaults to None. A list of all users will be provided unless **`user_type`** parameter is used, which will return list of instructors or assessors based on the provided value. The optional **`fetch_tree`** parameter is to fetch the complete object when set to **`true`**, and return only the UUID when set to **`false`** (by default).

If value provided to **`user_type`** parameter is invalid, response returned would be:

```json
{
    "success": false,
    "message": "Validation Failed",
    "data": [
        {
            "loc": [
                "query",
                "user_type"
            ],
            "msg": "unexpected value; permitted: 'instructor', 'assessor'",
            "type": "value_error.const",
            "ctx": {
                "given": "instructors",
                "permitted": [
                    "instructor",
                    "assessor"
                ]
            }
        }
    ]
}
```

If non-existent curriculum_pathway_id is provided to **`curriculum_pathway_id`**, response would look like:

```json
{
    "success": false,
    "message": "Curriculum Pathway with uuid kp3RN3wEf3y2tKsFbWvZ not found",
    "data": null
}
```

If curriculum pathway for provided **`curriculum_pathway_id`** is not of type `discipline`, following response would be returned:

```json
{
    "success": false,
    "message": "Given curriculum pathway id kp3RN3wEf3y2tKsFbWvZ is not of discipline type",
    "data": null
}
```

If curriculum pathway for provided **`curriculum_pathway_id`** is not added in any discipline associaiton group, then the following response would be returned:

```json
{
    "success": false,
    "message": "Given curriculum pathway id kp3RN3wEf3y2tKsFbWvZ is not actively associated in any discipline association group",
    "data": null
}
```

If there are no validation errors and **`fetch_tree`** is **False**, the response will be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the users",
    "data": ["ErjRNo7Uls8qHl7g0XDP", "0jbIUVcRpZUVLL8yRRjq"]
}
```

And if **`fetch_tree`** is **True**, the response will be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the users",
    "data": [
        {
            "user_id": "ErjRNo7Uls8qHl7g0XDP",
            "first_name": "steve",
            "last_name": "jobs",
            "email": "behave-e2e-test-379a8371-4347-4268-8733-1182e0174bc7@gmail.com",
            "user_type": "learner",
            "user_type_ref": "",
            "user_groups": [],
            "status": "active",
            "is_registered": true,
            "failed_login_attempts_count": 0,
            "access_api_docs": false,
            "gaia_id": "F2GGRg5etyty",
            "photo_url": null,
            "created_time": "2023-02-10 20:34:26.627648+00:00",
            "last_modified_time": "2023-02-10 20:34:28.273407+00:00",
            "created_by": "",
            "last_modified_by": ""
        },
        {
            "user_id": "0jbIUVcRpZUVLL8yRRjq",
            "first_name": "firstname3",
            "last_name": "lastname3",
            "email": "uksybrgbkae@kusek.ajsd",
            "user_type": "instructor",
            "user_type_ref": "",
            "user_groups": [],
            "status": "active",
            "is_registered": true,
            "failed_login_attempts_count": 0,
            "access_api_docs": false,
            "gaia_id": "",
            "photo_url": null,
            "created_time": "2023-02-17 15:18:31.287558+00:00",
            "last_modified_time": "2023-02-17 15:18:31.482408+00:00",
            "created_by": "",
            "last_modified_by": ""
        }
    ]
}
```


### Remove user from the Discipline Association Group:

To remove user from the discipline association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}/user/remove`** where **`uuid`** is the unique ID of the discipline association group.

**Note: Removing instructor type of user from Discipline Association Group will cause the same instructor to get removed from Learner Association Group as well, where it exists for the same Discipline curriculum_pathway_id**

The request body would be as follows:

```json
{
  "user": "WZFsczmmNdgWurlBCAiJ"
}
```

After the validation of discipline association group for given uuid. Discipline association group for the given uuid is updated and given user is removed from the users list present in the discipline association group.
The response will look like this:

```json
{
  "success": true,
  "message": "Successfully removed the user from the discipline association group",
  "data": {
    "name": "Discipline Association Group Name",
    "description": "Description for Discipline Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "discipline",
    "users": [],
    "associations": {
      "curriculum_pathways": []
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:10:35.531185+00:00"
  }
}
```

### Update status of users and associations in Discipline Association Group:

To update the status of users or associations in a discipline association group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/discipline-association/{uuid}/user-association/status`** where **`uuid`** is the unique ID of the discipline association group.

**Note**:
  - User should only be of instructor or assessor type and belong to instructor/assessor user group
  - In `associations` field, `curriculum_pathway` will correspond to disciplines
  - De-activting a user of instructor type in Discipline Association Group will also de-activate the same instructor existing in any Learner Group Association for that curriculum_pathway_id.

The request body would be as follows:

```json
{
  "user": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "status": "inactive"
  },
  "curriculum_pathway": {
    "curriculum_pathway_id": "sgxR77QKS8uS7Zgm",
    "status": "inactive"
  }
}
```

After the validation of group for given uuid, group for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "association_type": "discipline",
    "users": [
      {
        "user": "124hsgxR77QKS8uS7Zgm",
        "user_type": "instructor",
        "status": "inactive"
      }
    ],
    "associations": {
      "curriculum_pathways": [
        {
          "pathway": "sgxR77QKS8uS7Zgm",
          "status": "inactive",
        }
      ]
    },
    "name": "Association Group Name",
    "description": "Description for Association Group",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

If the Association Group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "AssociationGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

If the User is not present for a user_id given in request body - **`Nzyh490mbPoE5St`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "User with uuid Nzyh490mbPoE5St not found",
  "data": null
}
```

If the CurriculumPathway is not present for a pathway given in request body - **`Nzyh490mbPoE5St`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "CurriculumPathway with uuid Nzyh490mbPoE5St not found",
  "data": null
}
```
