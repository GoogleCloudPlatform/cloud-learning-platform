---
sidebar_label: CRUD APIs for Staff
sidebar_position: 9
---

# CRUD APIs for Staff

The following steps are to create, view and update Staff.


### Create a Staff:

To create a staff, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/staff`**.
The request body for the API is as follows:

```json
{
  "first_name": "Ted",
  "last_name": "Turner",
  "preferred_name": "TT",
  "bio": "",
  "pronoun": "he/him/his",
  "email": "ted.turner@email.com",
  "phone_number": "0000000000"
}
```

A new Staff with the request body details and with a new uuid (unique ID of the Staff) is added to the Staffs collection. After successfully adding new Staff document to the collection you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created staff",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "first_name": "Ted",
    "last_name": "Turner",
    "preferred_name": "TT",
    "bio": "",
    "pronoun": "he/him/his",
    "email": "ted.turner@email.com",
    "phone_number": "0000000000",
    "shared_inboxes": "",
    "office_hours": []
  }
}
```

### Get all Staffs:

To fetch all the Staffs available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staffs`** with **`skip`** and **`limit`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of staffs array to be returned which takes a default value **`10`**.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "first_name": "Ted",
      "last_name": "Turner",
      "preferred_name": "TT",
      "bio": "",
      "pronoun": "he/him/his",
      "email": "ted.turner@email.com",
      "phone_number": "0000000000",
      "shared_inboxes": "",
      "office_hours": []
    }
  ]
}
```

### Search Staff by email:

To search a Staff Record based on the `email`, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staff/search`**, where **`email`** is the email that is to be searched. This will fetch all the Staff records that has email as **`email`**. Please note - here, the exact matching is used i.e. only the Staff records whose `email` is **`email`** are fetched.

The response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the staff",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "first_name": "Ted",
      "last_name": "Turner",
      "preferred_name": "TT",
      "bio": "",
      "pronoun": "he/him/his",
      "email": "ted.turner@email.com",
      "phone_number": "0000000000",
      "shared_inboxes": "",
      "office_hours": []
    }
  ]
}
```

### Get a specific Staff:

To fetch the details of a specific Staff, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staff/{uuid}`** where **`uuid`** is the unique ID of the Staff.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the staff",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "first_name": "Ted",
    "last_name": "Turner",
    "preferred_name": "TT",
    "bio": "",
    "pronoun": "he/him/his",
    "email": "ted.turner@email.com",
    "phone_number": "0000000000",
    "shared_inboxes": "",
    "office_hours": []
  }
}
```

If the Staff is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Staff with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a Staff:

To update the details of a Staff, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staff/{uuid}`** where **`uuid`** is the unique ID of the Staff.
The request body would be as follows:

```json
{
  "preferred_name": "TED",
  "bio": "Updated bio",
}
```

After the validation of Staff for given uuid, Staff for the given uuid is updated and the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully updated the staff",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "first_name": "Ted",
    "last_name": "Turner",
    "preferred_name": "Ted",
    "bio": "Updated bio",
    "pronoun": "he/him/his",
    "email": "ted.turner@email.com",
    "phone_number": "0000000000",
    "shared_inboxes": "",
    "office_hours": []
  }
}
```

If the Staff is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Staff with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Staff:

To delete a Staff, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staff/{uuid}`** where **`uuid`** is the unique ID of the Staff.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the staff"
}
```

If the Staff is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Staff with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```

### Import Staffs From Json file

To import Staffs from JSON file, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/staff/import/json`**, along with **`json_file`** of type binary consisting of Staffs,json_schema which matches the Staff model. This will create the new Staffs for all the entries in the file.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the staffs",
  "data": [
    "124hsgxR77QKS8uS7Zgm",
    "0G92bYBw6wxdMYuvrfc1",
    "0FmHJtre1FDM0p5f7b4V"
  ]
}
```
