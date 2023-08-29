---
sidebar_label: CRUD APIs for Approved Experience
sidebar_position: 1
---

# CRUD APIs for Approved Experience

The following steps are regarding the CRUD APIs for Approved Experience


### Create an Approved Experience

To create a Approved Experience, a **POST** request has to be made to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience`** .

The request body for the API is as follows:

```json
{
  "title": "Machine Learning",
  "description": "Machine learning (ML) is a field devoted to understanding and building methods that let machines learn.",
  "organization": "Dummy Org",
  "type": "Certificate",
  "student_type": "Graduate",
  "class_level": "Lower level",
  "credits_range": {
    "upper_limit": 8,
    "lower_limit": 3
  },
  "status": "Active",
  "metadata": {}
}
```

If the response is successful then a new Approved Experience with the request body details and with a new uuid (unique ID of the Approved Experience) is added. After successfully adding new Approved Experience document to the collection, you will get a response similar to the below json:

```json
{
    "success": true,
    "message": "Successfully created the approved experience",
    "data": {
        "organization": "Dummy Org",
        "title": "Machine Learning",
        "description": "Machine learning (ML) is a field devoted to understanding and building methods that let machines learn.",
        "type": "Certificate",
        "student_type": "Graduate",
        "class_level": "Lower level",
        "credits_range": {
            "lower_limit": 3,
            "upper_limit": 8
        },
        "status": "Active",
        "metadata": {},
        "uuid": "4LbN01DdrSF3sMdMK1Mn",
        "created_time": "2023-05-17 10:38:15.718803+00:00",
        "last_modified_time": "2023-05-17 10:38:15.829416+00:00"
    }
}
```

### Get all Approved Experiences

When we need to fetch all the Approved Experiences available, then we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experiences`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Approved Experience array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Approved Experiences.

The response would look something like below:

```json
{
    "success": true,
    "message": "Successfully fetched the approved experiences",
    "data": {
        "records": [
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "lower_limit": 8,
                    "upper_limit": 25
                },
                "status": "Retired",
                "metadata": {},
                "uuid": "1hCs325vONuPgnpf6nX1",
                "created_time": "2023-04-25 17:37:13.564104+00:00",
                "last_modified_time": "2023-04-25 17:37:13.775941+00:00"
            },
            {
                "organization": "Penn State University",
                "title": "Spanish",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 20,
                    "lower_limit": 5
                },
                "status": "Active",
                "metadata": {},
                "uuid": "NWA9EWp6b5hT9Sm3EZKu",
                "created_time": "2023-04-25 17:37:13.102676+00:00",
                "last_modified_time": "2023-04-25 17:37:13.338416+00:00"
            },
            {
                "organization": "TPSI",
                "title": "Fundamentals of Accounting",
                "description": "",
                "type": "Certificate",
                "student_type": "Undergraduate",
                "class_level": "Lower level",
                "credits_range": {
                    "lower_limit": 5,
                    "upper_limit": 10
                },
                "status": "Active",
                "metadata": {},
                "uuid": "klf8P6Z43nbu6J9bYgps",
                "created_time": "2023-04-25 17:37:12.579670+00:00",
                "last_modified_time": "2023-04-25 17:37:12.904457+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 20,
                    "lower_limit": 5
                },
                "status": "Active",
                "metadata": {},
                "uuid": "j5MmROCF3ebVbex6jYQy",
                "created_time": "2023-04-25 15:05:46.405685+00:00",
                "last_modified_time": "2023-04-25 15:05:46.615287+00:00"
            },
            {
                "organization": "Penn State University",
                "title": "Spanish",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 20,
                    "lower_limit": 5
                },
                "status": "Active",
                "metadata": {},
                "uuid": "gSUOQVAigKd7rsMU8aYZ",
                "created_time": "2023-04-25 15:05:45.952399+00:00",
                "last_modified_time": "2023-04-25 15:05:46.176531+00:00"
            }
        ],
        "total_count": 10000
    }
}
```

### Get a specific Approved Experience

When we need to fetch the details of a specific Approved Experience, then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/{uuid}`** where **`uuid`** is the unique ID of the Approved Experience.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the approved experience",
    "data": {
        "organization": "DSU",
        "title": "Advance Mathematics",
        "description": "",
        "type": "Certificate",
        "student_type": "Graduate",
        "class_level": null,
        "credits_range": {
            "lower_limit": 8,
            "upper_limit": 25
        },
        "status": "Retired",
        "metadata": {},
        "uuid": "1hCs325vONuPgnpf6nX1",
        "created_time": "2023-04-25 17:37:13.564104+00:00",
        "last_modified_time": "2023-04-25 17:37:13.775941+00:00"
    }
}
```

If the Approved Experience is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Approved Experience with uuid zxtPzcjdkl5JvVGjl01j not found",
    "data": null
}
```

### Update an Approved Experience

When we need to update the details of an Approved Experience, then we would make a **PUT** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/{uuid}`** where **`uuid`** is the unique ID of the Approved Experience. We need to send only those fields in the request body that we want to update.

The request body would be as follows:

```json
{
  "description": "Higher level mathematics"
}
```

After the validation of Approved Experience for given uuid, Approved Experience for the given uuid is updated and the response will look like this:

```json
{
    "success": true,
    "message": "Successfully updated the approved experience",
    "data": {
        "organization": "DSU",
        "title": "Advance Mathematics",
        "description": "Higher level mathematics",
        "type": "Certificate",
        "student_type": "Graduate",
        "class_level": null,
        "credits_range": {
            "lower_limit": 8,
            "upper_limit": 25
        },
        "status": "Retired",
        "metadata": {},
        "uuid": "1hCs325vONuPgnpf6nX1",
        "created_time": "2023-04-25 17:37:13.564104+00:00",
        "last_modified_time": "2023-05-18 05:13:53.674560+00:00"
    }
}
```

If the Approved Experience is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Approved Experience with uuid o1nv13n6sbu0ny not found",
    "data": null
}
```

### Delete an Approved Experience

When we need to delete an Approved Experience, then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/{uuid}`** where **`uuid`** is the unique ID of the Approved Experience.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully deleted the approved experience"
}
```

If the Approved Experience is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Approved Experience with uuid 1HFXhcO7A384fdcq not found",
    "data": null
}
```

### Search Approved Experiences

When we want to perform search on Approved Experiences based on the `title` and `description` of the Approved Experiences, then we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/search?keyword={search_keyword}`**, where **`search_keyword`** is the keyword that is to be searched. This will fetch all the Approved Experience that has **`search_keyword`** in `title` or `description`. The search is case-insensitive.

Other optional parameters for sorting, filter, and pagination are:

`skip`: int (default=0)
`limit`: int (default=6)
`type`: list (default=None)
`student_type`: list (default=None)
`class_level`: list (default=None)
`status`: list (default=None)
`organization`: list (default=None),
`credits_range_lower_limit`: int (default=None)
`credits_range_upper_limit`: int (default=None)
`sort_by`: str : allowed values=["total_credit", "experience_name"] : (default="total_credit")
`sort_order`: str : allowed values=["ascending", "descending"] : (default="descending")

The response would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the Approved Experiences",
    "data": {
        "records": [
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "Higher level mathematics",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 25,
                    "lower_limit": 8
                },
                "status": "Retired",
                "metadata": {},
                "uuid": "1hCs325vONuPgnpf6nX1",
                "created_time": "2023-04-25 17:37:13.564104+00:00",
                "last_modified_time": "2023-05-18 05:13:53.674560+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "lower_limit": 5,
                    "upper_limit": 20
                },
                "status": "Active",
                "metadata": {},
                "uuid": "4dNipL5j9aCL01IHIJxj",
                "created_time": "2023-04-25 14:49:18.625099+00:00",
                "last_modified_time": "2023-04-25 14:49:18.813187+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 20,
                    "lower_limit": 5
                },
                "status": "Active",
                "metadata": {},
                "uuid": "OykFrw2G5w8SiB6CNe0f",
                "created_time": "2023-04-25 14:34:25.063838+00:00",
                "last_modified_time": "2023-04-25 14:34:25.195473+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "upper_limit": 20,
                    "lower_limit": 5
                },
                "status": "Active",
                "metadata": {},
                "uuid": "Zav5YzRQh56z4QKFIdYm",
                "created_time": "2023-04-25 15:01:45.510306+00:00",
                "last_modified_time": "2023-04-25 15:01:45.714404+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "lower_limit": 5,
                    "upper_limit": 20
                },
                "status": "Active",
                "metadata": {},
                "uuid": "j5MmROCF3ebVbex6jYQy",
                "created_time": "2023-04-25 15:05:46.405685+00:00",
                "last_modified_time": "2023-04-25 15:05:46.615287+00:00"
            },
            {
                "organization": "DSU",
                "title": "Advance Mathematics",
                "description": "",
                "type": "Certificate",
                "student_type": "Graduate",
                "class_level": null,
                "credits_range": {
                    "lower_limit": 5,
                    "upper_limit": 20
                },
                "status": "Active",
                "metadata": {},
                "uuid": "nelG7vCNxel1ZCrxGnzt",
                "created_time": "2023-04-25 14:20:56.449400+00:00",
                "last_modified_time": "2023-04-25 14:20:56.644353+00:00"
            }
        ],
        "total_count": 10000
    }
}
```

### Import Approved Experiences From Json file

To import Approved Experiences from JSON file, we would make a **POST** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/import/json`**, along with **`json_file`** of type binary consisting of Approved Experiences, json_schema which matches the ApprovedExperience model. This will create the new Approved Experiences for all the entries in the file.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the approved experiences",
  "data": [
    "124hsgxR77QKS8uS7Zgm",
    "0G92bYBw6wxdMYuvrfc1",
    "0FmHJtre1FDM0p5f7b4V"
  ]
}
```

### Get list of Unique Organizations

To fetch the list of all unique organizations from all the Approved Experiences, we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/approved-experience/organisations/unique`**. This API doesn't require any parameter.

The reponse would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the unique list of approved organisations",
    "data": [
        "DSU",
        "Penn State University",
        "TPSI"
    ]
}
```
