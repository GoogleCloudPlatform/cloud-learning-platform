---
sidebar_label: CRUD APIs for Association Groups
sidebar_position: 9
---

# CRUD APIs for Association Groups

The following steps are to fetch Association Groups.


### Get all Association Groups:

To fetch all the association groups available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups`** with **`skip`**, **`limit`** and **`association_type`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of Association Group array to be returned which takes a default value **`10`** if not provided and **`association_type`** is the type of the association type to be returned which takes NONE as a default value. also, the **sort_by** parameter allows sorting the association groups based on a this field **name, association_type**, and the sort_order parameter defines the order of sorting **ASCENDING/DESCENDING**. 

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the association groups",
  "data": {
    "records": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "Discipline Association Group",
      "description": "Description for Discipline Association Group",
      "association_type": "discipline",
      "created_time": "2023-02-10 11:54:36.604328+00:00",
      "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
    }
  ],
    "total_count": 10000
  }
}
```

### Search Association Groups by name and description:

To fetch all the association groups by name and description, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/association-groups/search`** with **`skip`**, **`limit`** and **`search_query`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of Association Group array to be returned which takes a default value **`10`** if not provided and **`search_query`** is the key to be searched against name and desciption of association groups.

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
      "created_time": "2023-02-10 11:54:36.604328+00:00",
      "last_modified_time": "2023-02-10 11:57:11.611761+00:00"
    }
  ],
    "total_count": 10000
  }
}