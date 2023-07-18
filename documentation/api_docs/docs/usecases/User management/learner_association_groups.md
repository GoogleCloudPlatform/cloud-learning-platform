---
sidebar_label: CRUD APIs for Learner Association Groups
sidebar_position: 7
---

# CRUD APIs for Learner Association Groups

The following steps are to create, view and update Learner Association Groups.


### Create a Learner Association Group:

To create a learner association group, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association`**. The name field in the request body should be unique for every association group creation.
The request body for the API is as follows:

```json
{
  "name": "Learner Association Group",
  "description": "Description for Learner Association Group",
}
```

A new association group with the request body details and with a new uuid(unique ID of the group) is added to the association_groups collection. After successfully adding new association group document to the collection. You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Learner Association Group",
    "description": "Description for Learner Association Group",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [], "instructors": [], "curriculum_pathway_id": ""
    },
    "created_time": "2023-02-10 11:54:36.604328+00:00",
    "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
  }
}
```

### Get all Learner Association Groups:

To fetch all the learner type of association groups available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-associations`** with **`skip`**, **`limit`** and **`fetch_tree`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of Association Group array to be returned which takes a default value **`10`** if not provided and

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the association groups",
  "data": {
    "records": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "Learner Association Group",
      "description": "Description for Learner Association Group",
      "association_type": "learner",
      "users": [],
      "associations": {
        "coaches": [], "instructors": [], "curriculum_pathway_id": ""
      },
      "created_time": "2023-02-10 11:54:36.604328+00:00",
      "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a Learner Association Group:

To fetch the details of a specific learner association group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}`** where **`uuid`** is the unique ID of the learner association group and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Learner Association Group",
    "description": "Description for Learner Association Group",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [], "instructors": [], "curriculum_pathway_id": ""
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

### Get learners of a Learner Association Group:

To fetch the learner details of a specific learner association group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/learners`** where **`uuid`** is the unique ID of the learner association group and the query parameter  **`fetch_tree`** is to fetch the complete user object when set **`true`** if not it takes the default value **`false`** returning only UUID. Other query parameters include **`status`**, **`skip`** and **`limit`**, where **`status`** is the status of the learner(active or inactive), **`skip`** is the number of objects to be skipped and it takes a default value **`0`** if not provided, **`limit`** is the size of learners array to be returned which takes a default value **`10`** if not provided.

Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["first_name", "last_name", "email", "created_time"] | field by which the submitted assessments will be sorted. (default="created_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="descending") |

If `fetch_tree` is `false`, then the response would be as follows: 

```json
{
    "success": true,
    "message": "Successfully fetched the learners",
    "data": {
    "records": [
        {
            "user": "zYyqFBPWM8jbwoZw6veQ",
            "status": "active"
        },
        {
            "user": "1qAF5rPScDNKTDzYqrYe",
            "status": "active"
        }
    ],
    "total_count": 10000
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

If the Association Group is not of type `learner`, then the response would be as follows:

```json
{
    "success": false,
    "message": "AssociationGroup for given uuid: JAnZNzyh490mbPoE5StZ is not learner type",
    "data": null
}
```

### Get coaches of a Learner Association Group:

To fetch the learner details of a specific learner association group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/coaches`** where **`uuid`** is the unique ID of the learner association group and the query parameter  **`fetch_tree`** is to fetch the complete user object when set **`true`** if not it takes the default value **`false`** returning only UUID. Other query parameters include **`status`**, **`skip`** and **`limit`**, where **`status`** is the status of coach(active or inactive), **`skip`** is the number of objects to be skipped and it takes a default value **`0`** if not provided, **`limit`** is the size of coaches array to be returned which takes a default value **`10`** if not provided

Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["first_name", "last_name", "email", "created_time"] | field by which the submitted assessments will be sorted. (default="created_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="descending") |

If `fetch_tree` is `true`, then the response would be as follows: 

```json
{
    "success": true,
    "message": "Successfully fetched the coaches",
    "data": {
    "records": [
        {
            "coach": {
                "user_id": "iwIYtB9kiliMCPTUvBKS",
                "first_name": "steve",
                "last_name": "jobs",
                "email": "4622df74-70b9-496d-9748-e096fffdc947@gmail.com",
                "user_type": "coach",
                "user_type_ref": "",
                "user_groups": [],
                "status": "active",
                "is_registered": true,
                "failed_login_attempts_count": 0,
                "access_api_docs": false,
                "gaia_id": "F2GGRg5etyty",
                "photo_url": "//lh3.googleusercontent.com/a/default-user",
                "inspace_user": {},
                "is_deleted": false,
                "created_time": "2023-05-08 21:07:50.131893+00:00",
                "last_modified_time": "2023-05-08 21:07:50.788793+00:00",
                "created_by": "",
                "last_modified_by": ""
            },
            "status": "active"
        }
    ],
    "total_count": 10000
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

If the Association Group is not of type `learner`, then the response would be as follows:

```json
{
    "success": false,
    "message": "AssociationGroup for given uuid: JAnZNzyh490mbPoE5StZ is not learner type",
    "data": null
}
```

### Get instructors of a Learner Association Group:

To fetch the learner details of a specific learner association group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/instructors`** where **`uuid`** is the unique ID of the learner association group and the query parameter  **`fetch_tree`** is to fetch the complete user object when set **`true`** if not it takes the default value **`false`** returning only UUID. Other query parameters include  **`status`**, **`skip`** and **`limit`**, where **`status`** is the status of instructor(active or inactive), **`skip`** is the number of objects to be skipped and it takes a default value **`0`** if not provided, **`limit`** is the size of instructors array to be returned which takes a default value **`10`** if not provided

Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["first_name", "last_name", "email", "created_time"] | field by which the submitted assessments will be sorted. (default="created_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="descending") |

If `fetch_tree` is `false`, then the response would be as follows: 

```json
{
    "success": true,
    "message": "Successfully fetched the instructors",
    "data": {
      "records": [
        {
            "instructor": "1AZ9XzTXXahaCbPOSrep",
            "curriculum_pathway_id": "0JDAEH6cvbNFLHxxsDN8",
            "status": "active"
        },
        {
            "instructor": "EYisVWuCleVE0A2JIH86",
            "curriculum_pathway_id": "0KdLQDPxe3SLTGJOvoAQ",
            "status": "active"
        }
    ],
      "total_count": 10000
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

If the Association Group is not of type `learner`, then the response would be as follows:

```json
{
    "success": false,
    "message": "AssociationGroup for given uuid: JAnZNzyh490mbPoE5StZ is not learner type",
    "data": null
}
```

### Update a Learner Association Group:

To update the details of a learner association group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}`** where **`uuid`** is the unique ID of the learner association group.

The request body would be as follows:

```json
{
  "name": "Updated Learner Association Group Name",
  "description": "Updated Learner Association Group Description"
}
```

After the validation of group for given uuid, group for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the association group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "Updated Learner Association Group Name",
    "description": "Updated Learner Association Group Description",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [], "instructors": [], "curriculum_pathway_id": ""
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

### Delete a Learner Association Group:

To delete a learner association group, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}`** where **`uuid`** is the unique ID of the learner association group.

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

### Add users to the Leaner Association Group:

To add users to the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/users/add`** where **`uuid`** is the unique ID of the learner association group.

The request body would be as follows:

```json
{
  "users": ["WZFsczmmNdgWurlBCAiJ"],
  "status": "active"
}
```

After the validation of learner association group for given uuid and also validating the given users is of **`user_type=learner`**. learner association group for the given uuid is updated with the given users list and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully added the users to the learner association group",
  "data": {
    "name": "Learner Association Group Name",
    "description": "Description for Learner Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "learner",
    "users": [
      {
        "user": "WZFsczmmNdgWurlBCAiJ",
        "status": "active"
      }
    ],
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": ""
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:07:50.564027+00:00"
  }
}
```


### Remove user from the learner Association Group:

To remove user from the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/user/remove`** where **`uuid`** is the unique ID of the learner association group.

The request body would be as follows:

```json
{
  "user": "WZFsczmmNdgWurlBCAiJ"
}
```

After the validation of learner association group for given uuid. learner association group for the given uuid is updated and given user is removed from the users list present in the learner association group.
The response will look like this:

```json
{
  "success": true,
  "message": "Successfully removed the user from the learner association group",
  "data": {
    "name": "Learner Association Group Name",
    "description": "Description for Learner Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": ""
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:10:35.531185+00:00"
  }
}
```

### Add coaches to the Leaner Association Group:

To add coaches to the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/coaches/add`** where **`uuid`** is the unique ID of the learner association group.
**Currently, single coach can be associated to the Learner Association Group**

The request body would be as follows:

```json
{
  "coaches": ["WZFsczmmNdgWurlBCAiJ"],
  "status": "active"
}
```

After the validation of learner association group for given uuid and also validating the given coach is of **`user_type=faculty`**. learner association group for the given uuid is updated with the given coaches list and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully added the coaches to the learner association group",
  "data": {
    "name": "Learner Association Group Name",
    "description": "Description for Learner Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [
        {
        "coach": "WZFsczmmNdgWurlBCAiJ",
        "status": "active"
        }
      ],
      "instructors": [],
      "curriculum_pathway_id": ""
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:07:50.564027+00:00"
  }
}
```


### Remove coach from the learner Association Group:

To remove coach from the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/coach/remove`** where **`uuid`** is the unique ID of the learner association group.

The request body would be as follows:

```json
{
  "coach": "WZFsczmmNdgWurlBCAiJ"
}
```

After the validation of learner association group for given uuid. learner association group for the given uuid is updated and given coach is removed from the coaches list present in the learner association group.
The response will look like this:

```json
{
  "success": true,
  "message": "Successfully remove the coach from the learner association group",
  "data": {
    "name": "Learner Association Group Name",
    "description": "Description for Learner Association Group",
    "uuid": "xQ0FXfQBMm7Mv41vrMIh",
    "association_type": "learner",
    "users": [],
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": ""
    },
    "created_time": "2023-02-21 12:06:46.278255+00:00",
    "last_modified_time": "2023-02-21 12:07:50.564027+00:00"
  }
}
```

### Add Instructor to the Leaner Association Group:

To add an instructor to the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/instructor/add`** where **`uuid`** is the unique ID of the learner association group.

**Note**:
  - Currently, only one Instructor can be associated to one discipline in the Learner Association Group.
  - Given `instructor_id` for given `curriculum_pathway_id` will get added to the Learner Association Group only if the instructor is actively associated to the `curriculum_pathway_id` in any of Discipline Association Groups.

The request body would be as follows:

```json
{
    "instructor": ["12sdfhbejv21212"],
    "curriculum_pathway_id": "1212eruirthvschkdsvv",
    "status": "active"
}
```

After the validation of the learner association group for given uuid and also validating of the given Instructor. Learner association group for the given uuid is updated with the given Instructor and the response will look like this:

```json
{
    "success": true,
    "message": "Instructor added successfully",
    "data": {
        "uuid": "uu6gV6N27X2CmJ4hmEA4",
        "name": "Association Group Name",
        "association_type": "learner",
        "description": "Description for Association Group",
        "users": [],
        "associations": {
            "instructors": [
                {
                    "status": "active",
                    "curriculum_pathway_id": "1212erui34uvv",
                    "instructor": "12sdfh231212"
                }
            ],
            "coaches": [],
            "curriculum_pathway_id": ""
        },
        "created_time": "2023-02-23 17: 39: 34.747210+00: 00",
        "last_modified_time": "2023-02-23 17: 39: 34.787425+00: 00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

If the given instructor_id **`JAnZNzyh490mbPoE5StZ`** is NOT actively associated to the curriculum_pathway_id  **`Nzyh490mbPoE5St`** in any of the Discipline Association Groups, then the following response would be returned:

```json
{
  "success": false,
  "message": "Instructors for given instructor_ids ['JAnZNzyh490mbPoE5StZ'] are not actively associated to the given curriculum_pathway_id Nzyh490mbPoE5St in discipline association group",
  "data": null
}
```

### Update status of Users and Associations in Learner Association Group:

To update the status of users or associations in a learner association group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/user-association/status`** where **`uuid`** is the unique ID of the learner association group.

**Note**: User should only be of learner type and belong to learner user group.

**Note**:
  - User should only be of learner type and belong to learner user group.
  - Given `instructor_id` for given `curriculum_pathway_id` will get activated in the Learner Association Group only if the instructor is actively associated to the curriculum_pathway_id in any of Discipline Association Groups.

The request body would be as follows:

```json
{
  "user": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "status": "inactive"
  },
  "coach": {
    "coach_id": "85sgxR77QKS8uS7Zg",
    "status": "inactive"
  },
  "instructor": {
    "instructor_id": "sgxR77QKS8uS7Zgm",
    "curriculum_pathway_id": "1sgxR72QKS8uS7Zmlk",
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
    "association_type": "learner",
    "users": [
      {
        "user": "124hsgxR77QKS8uS7Zgm",
        "status": "inactive"
      }
    ],
    "associations": {
      "coaches": [
        {
          "user": "85sgxR77QKS8uS7Zg",
          "status": "inactive"
        }
      ],
      "instructors": [
        {
          "instructor": "sgxR77QKS8uS7Zgm",
          "status": "inactive",
          "curriculum_pathway_id": "1sgxR72QKS8uS7Zmlk"
        }
      ],
      "curriculum_pathway_id": ""
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

If the given instructor_id **`JAnZNzyh490mbPoE5StZ`** is NOT actively associated to the curriculum_pathway_id  **`Nzyh490mbPoE5St`** in any of the Discipline Association Groups, then the following response would be returned:

```json
{
  "success": false,
  "message": "Instructor for given instructor_id JAnZNzyh490mbPoE5StZ is not actively associated to the given curriculum_pathway_id Nzyh490mbPoE5St in discipline association group",
  "data": null
}
```

### Remove Instructor from the Leaner Association Group:

To remove an instructor from the learner association group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/{uuid}/instructor/remove`** where **`uuid`** is the unique ID of the learner association group.
**Currently, single Instructor can be associated with one discipline in the Learner Association Group**

The request body would be as follows:

```json
{
    "instructor": "12sdfhbejv21212",
    "curriculum_pathway_id": "1212eruirthvschkdsvv"
}
```

After the validation of the learner association group for given uuid and also validating of the given Instructor. learner association group for the given uuid is updated with the given Instructor and the response will look like this:

```json
{
    "success": true,
    "message": "Instructor removed successfully",
    "data": {
        "uuid": "uu6gV6N27X2CmJ4hmEA4",
        "name": "Association Group Name",
        "association_type": "learner",
        "description": "Description for Association Group",
        "users": [],
        "associations": {
            "instructors": [],
            "coaches": [],
            "curriculum_pathway_id": ""
        },
        "created_time": "2023-02-23 17: 39: 34.747210+00: 00",
        "last_modified_time": "2023-02-23 17: 39: 34.787425+00: 00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

### Get all Learners for given Instructor :

To fetch the details of all learners for given Instructor, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/instructor/{user_id}/learners`** where **`user_id`** is the unique ID of the user having user_type instructor and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the learners for the given instructor",
  "data": ["GDAuFBlir7AyWJjvDipD"]
}
```

### Get all Learners for given Coach :

To fetch the details of all learners for given Coach, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/learner-association/coach/{user_id}/learners`** where **`user_id`** is the unique ID of the user having user_type coach and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the learners for the given coach",
  "data": ["GDAuFBlir7AyWJjvDipD"]
}
```
