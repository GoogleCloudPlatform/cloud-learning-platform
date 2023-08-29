---
sidebar_label: CRUD APIs for PLA Record (Session)
sidebar_position: 2
---

# CRUD APIs for PLA Record (Session)

The following steps are regarding the CRUD APIs for PLA Records


### Create a PLA Record

To create a PLA Record, a **POST** request has to be made to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record`** .

The request body for the API is as follows:

```json
{
  "title": "PLA Title",
  "user_id": "user_1234",
  "type": "catalog",
  "assessor_name": "assessor_name",
  "description": "",
  "status": "In progress",
  "prior_experiences": ["PE_uuid_1", "PE_uuid_2"],
  "approved_experiences": ["AE_uuid_1"]
}
```

If there are no PriorExperience documents with the uuid that are present in the `prior_experiences` list of the request body, you will get `ResourceNotFound` error.
If there are no ApprovedExperience documents with the uuid that are present in the `approved_experiences` list of the request body, you will get `ResourceNotFound` error.

id_number will be calculated automatically while creating the PLARecord. It will be an incremental value starting with 10000, i.e. first document of PLARecord will have the id_number as 10000, second will have 10001, and so on.

If the title is not provided in the request body, it will be set as "Session #<id_number>", for eg. if the title is not provided for the first document, it will be set as "Session #10001".

If the response is successful then a new PLA Record with the request body details and with a new uuid (unique ID of the PLA Record) is added. After successfully adding new PLA Record document to the collection, you will get a response similar to the below json:

```json
{
    "success": true,
    "message": "Successfully created the PLA Record",
    "data": {
        "title": "PLA Title",
        "user_id": "user_1234",
        "type": "catalog",
        "assessor_name": "assessor_name",
        "description": "",
        "status": "In progress",
        "prior_experiences": [
            "PE_uuid_1",
            "PE_uuid_2"
        ],
        "approved_experiences": [
            "AE_uuid_1"
        ],
        "id_number": 10001,
        "progress": 20,
        "is_archived": false,
        "is_flagged": false,
        "uuid": "5kR1HTqLSMXm4TgSskf2",
        "created_time": "2022-12-21 13:28:47.238098+00:00",
        "last_modified_time": "2022-12-21 13:28:47.504235+00:00"
    }
}
```

### Get all PLA Records

When we need to fetch all the PLA Records available, then we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-records`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of PLA Record array to be returned which takes a default value **`10`** if not provided. This will fetch the list of PLA Records.

The response would look something like below:

```json
{
    "success": true,
    "message": "Successfully fetched the PLA Records",
    "data": {
        "records": [
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": [
                    "1hCs325vONuPgnpf6nX1"
                ],
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "SMMkf944kKJWa95ycQjT",
                "created_time": "2023-05-09 14:39:18.108965+00:00",
                "last_modified_time": "2023-05-09 14:39:18.295022+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": [
                    "1hCs325vONuPgnpf6nX1"
                ],
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "wQnRAcaPpwQsngypj71p",
                "created_time": "2023-05-09 13:46:49.614970+00:00",
                "last_modified_time": "2023-05-09 13:46:49.785059+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": [
                    "1hCs325vONuPgnpf6nX1"
                ],
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "R7UsFLK6zJjSJHnESqyT",
                "created_time": "2023-05-09 13:20:18.710576+00:00",
                "last_modified_time": "2023-05-09 13:20:19.216083+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "gdPQ5YtBrCCFd0ktoz4J",
                "created_time": "2023-04-25 17:43:46.699266+00:00",
                "last_modified_time": "2023-04-25 17:43:46.889213+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "5kR1HTqLSMXm4TgSskf2",
                "created_time": "2022-12-21 13:28:47.238098+00:00",
                "last_modified_time": "2022-12-21 13:28:47.504235+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "RBAOdq5nbal1Q9qmB1cf",
                "created_time": "2022-10-19 08:27:05.007527+00:00",
                "last_modified_time": "2022-10-19 08:27:05.175870+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "1BydOLzSowXPmACjEXrB",
                "created_time": "2022-10-19 08:18:04.604671+00:00",
                "last_modified_time": "2022-10-19 08:18:04.773543+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "v77lsICITt6RKtjpzQ7M",
                "created_time": "2022-10-19 08:08:13.368405+00:00",
                "last_modified_time": "2022-10-19 08:08:13.532935+00:00"
            },
            {
                "title": "PLA Title 2",
                "user_id": "user_5678",
                "type": "catalog",
                "assessor_name": "assessor_name2",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "UyC1mpXDyUJUomjzUDwa",
                "created_time": "2022-10-18 08:21:43.522784+00:00",
                "last_modified_time": "2022-10-18 08:21:43.742898+00:00"
            },
            {
                "title": "PLA Title",
                "user_id": "user_1234",
                "type": "catalog",
                "assessor_name": "assessor_name",
                "description": "",
                "status": "In progress",
                "prior_experiences": null,
                "approved_experiences": null,
                "id_number": 10001,
                "progress": 20,
                "is_archived": false,
                "is_flagged": false,
                "uuid": "XYXf0z3dzDV4E0cOKfjT",
                "created_time": "2022-10-18 08:21:42.961867+00:00",
                "last_modified_time": "2022-10-18 08:21:43.282681+00:00"
            }
        ],
        "total_count": 10000
    }
}
```

### Get a specific PLA Record

When we need to fetch the details of a specific PLA Record, then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/{uuid}`** where **`uuid`** is the unique ID of the PLA Record.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the PLA Record",
    "data": {
        "title": "PLA Title",
        "user_id": "user_1234",
        "type": "catalog",
        "assessor_name": "assessor_name",
        "description": "",
        "status": "In progress",
        "prior_experiences": [
            "bUMOvE2M5FKLjLJe6aNN"
        ],
        "approved_experiences": [
            "TbHBfaGQHG2anT66uOwL"
        ],
        "id_number": 10001,
        "progress": 20,
        "is_archived": false,
        "is_flagged": false,
        "uuid": "gKfsJ980EHTbaRLcDOQy",
        "created_time": "2022-10-10 14:33:57.738941+00:00",
        "last_modified_time": "2022-10-10 14:33:57.928141+00:00"
    }
}
```

If the PLA Record is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
    "success": false,
    "message": "PLA Record with uuid zxtPzcjdkl5JvVGjl01j not found",
    "data": null
}
```

### Update a PLA Record

When we need to update the details of a PLA Record, then we would make a **PUT** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/{uuid}`** where **`uuid`** is the unique ID of the PLA Record.

The request body would be as follows:

```json
{
    "title": "Updated Title"
}
```

After the validation of PLA Record for given uuid, PLA Record for the given uuid is updated and the response will look like this:

```json
{
    "success": true,
    "message": "Successfully updated the PLA Record",
    "data": {
        "title": "Updated Title",
        "user_id": "user_1234",
        "type": "catalog",
        "assessor_name": "assessor_name",
        "description": "",
        "status": "In progress",
        "prior_experiences": [
            "bUMOvE2M5FKLjLJe6aNN"
        ],
        "approved_experiences": [
            "TbHBfaGQHG2anT66uOwL"
        ],
        "id_number": 10001,
        "progress": 20,
        "is_archived": false,
        "is_flagged": false,
        "uuid": "gKfsJ980EHTbaRLcDOQy",
        "created_time": "2022-10-10 14:33:57.738941+00:00",
        "last_modified_time": "2022-12-22 09:08:16.336831+00:00"
    }
}
```

If the PLA Record is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
    "success": false,
    "message": "PLA Record with uuid o1nv13n6sbu0ny not found",
    "data": null
}
```

### Delete a PLA Record

When we need to delete a PLA Record, then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/{uuid}`** where **`uuid`** is the unique ID of the PLA Record.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully deleted the PLA Record"
}
```

If the PLA Record is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
    "success": false,
    "message": "PLA Record with uuid 1HFXhcO7A384fdcq not found",
    "data": null
}
```

### Search PLA Records

When we want to search PLA Records based on the `title` of the PLA Record, then we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/search?title={search_title}`**, where **`search_title`** is the title that is to be searched. This will fetch all the PLA Records that has title as **`search_title`**. Please note - here, the exact matching is used i.e. only the PLA records whose `title` is **`search_title`** are fetched.

The response would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the PLA Records",
    "data": [
        {
            "title": "PLA Title",
            "user_id": "user_1234",
            "type": "catalog",
            "assessor_name": "assessor_name",
            "description": "",
            "status": "In progress",
            "prior_experiences": [
                "Ckc7FwVLROaVVbg1ccn0"
            ],
            "approved_experiences": [
                "TbHBfaGQHG2anT66uOwL"
            ],
            "id_number": 10001,
            "progress": 20,
            "is_archived": false,
            "is_flagged": false,
            "uuid": "1BydOLzSowXPmACjEXrB",
            "created_time": "2022-10-19 08:18:04.604671+00:00",
            "last_modified_time": "2022-10-19 08:18:04.773543+00:00"
        },
        {
            "title": "PLA Title",
            "user_id": "user_1234",
            "type": "catalog",
            "assessor_name": "assessor_name",
            "description": "",
            "status": "In progress",
            "prior_experiences": [
                "Lqbb6SNexSIFtGGROCJW",
                "Ckc7FwVLROaVVbg1ccn0"
            ],
            "approved_experiences": [],
            "id_number": 10001,
            "progress": 20,
            "is_archived": false,
            "is_flagged": false,
            "uuid": "5kR1HTqLSMXm4TgSskf2",
            "created_time": "2022-12-21 13:28:47.238098+00:00",
            "last_modified_time": "2022-12-21 13:28:47.504235+00:00"
        }
    ]
}
```

### Import PLA Records From Json file

To import PLA Records from JSON file, we would make a **POST** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/import/json`**, along with **`json_file`** of type binary consisting of PLA Records, json_schema which matches the PLARecord model. This will create the new PLA Records for all the entries in the file.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the pla_records",
  "data": [
    "124hsgxR77QKS8uS7Zgm",
    "0G92bYBw6wxdMYuvrfc1",
    "0FmHJtre1FDM0p5f7b4V"
  ]
}
```

### Get list of all unique Assessor names

To fetch the list of all unique Assessor names from all the PLA_Records, we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/pla-record/assessors/unique`**. This API doesn't require any parameter.

The reponse would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the unique list of Assessor names",
    "data": [
        "Kevin",
        "Peter",
        "Ben"
    ]
}
```
