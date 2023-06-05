---
sidebar_label: Ingest data from Credential Engine
sidebar_position: 1
---

# Ingest data from Credential Engine

The following steps are to fetch and store data from Credential Engine to the skill graph


### Step 1:

(approx time taken for this step: 5 minutes)

The API url to fetch data from the credential engine is **`<APP_URL>/skill-service/api/v1/import/credential-engine`**

The request body for API is:

```json
{
  "competency_frameworks": [
    "https://credentialengineregistry.org/resources/ce-6fdd56d3-0214-4a67-b0c4-bb4c16ce9a13"
  ]
}
```

Here, we can see the key **`competency_frameworks`** in the request body accepts an array of URIs representing **`@type`** of **`ceasn:CompetencyFramework`**.

When we do send a **POST** request to the API **`<APP_URL>/skill-service/api/v1/import/credential-engine`**, an async batch job will be created in the background which will do ingestion of data in skill graph.

On a successful API hit, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully initiated the job with type 'credential_engine_ingestion'. Please use the job name to track the job status",
  "data": {
    "job_name": "34176209-39a3-42e0-bbc5-5135a525fbcb",
    "status": "active"
  }
}
```

### Step 2:

(approx time taken for this step: 1 minute)

We can check the status of the batch job using the job name that we get in response to the credential engine ingestion API.
For that, we can hit the **GET** request using the API **`<APP_URL>/skill-service/api/v1/jobs/credential_engine_ingestion/{job_name}`** where we pass the job name as path param(in this case, the API url will look like <{base_url}/skill-service/api/v1/jobs/credential_engine_ingestion/34176209-39a3-42e0-bbc5-5135a525fbcb>)

The response will look like this:

```json
{
  "success": true,
  "message": "Successfully fetched the batch job",
  "data": {
    "job_name": "34176209-39a3-42e0-bbc5-5135a525fbcb",
    "created_by": "",
    "created_time": "2022-05-26 11:53:49.900549+00:00",
    "last_modified_by": "",
    "last_modified_time": "2022-05-26 11:55:12.094668+00:00",
    "input_data": {
      "links": [
        "https://credentialengineregistry.org/resources/ce-ece7cefa-3c0f-42fe-9e51-f24e5489"
      ]
    },
    "status": "succeeded",
    "errors": {},
    "type": "credential_engine_ingestion"
  }
}
```

Here, the **`status`** in the **`data`** key shows the success status of the job which in this case is "succeeded".

If it fails for some reason, we will have **`status`** as "failed" with the explanation/data available in the **`errors`** key.

### Step 3:

(approx time taken for this step: 1 minute)

Once the batch job is succeeded, we can fetch the ingested data using the get all API that we have using url {base_url}/skill-service/api/v1/skills?skip=0&limit=10

We can add skip and limit to paginate the data we are fetching using query parameters as shown in the above API url.

Here is the example response of the get all skills API:

```json
{
    "success": true,
    "message": "Data fetched successfully",
    "data": [
        {
            "name": "Operating System Components",
            "description": "Explain the purpose of and relationship between common components of an operating system ",
            "keywords": [],
            "author": "",
            "creator": "",
            "alignments": {
                "standard_alignment": {},
                "credential_alignment": {},
                "skill_alignment": {
                    "emsi": {
                        "aligned": [
                            {
                                "id": "",
                                "name": "Information Systems",
                                "score": 1
                            }
                        ],
                        "suggested": []
                    },
                    "snhu": {},
                    "wgu": {}
                },
                "knowledge_alignment": {
                    "knowledge_nodes": {},
                    "learning_content_ids": {},
                    "learning_unit_ids": {}
                },
                "role_alignment": {
                    "onet": {}
                },
                "organizational_alignment": {}
            },
            "organizations": [],
            "certifications": [],
            "occupations": {
                "occupations_major_group": [
                    "15-1212.00"
                ],
                "occupations_minor_group": [],
                "broad_occupation": [],
                "detailed_occupation": []
            },
            "onet_job": "",
            "type": {
                "id": "",
                "name": ""
            },
            "parent_nodes": [
                "competency/IDS-20252"
            ],
            "reference_id": "IDS-20252-02",
            "source_uri": "snhu",
            "source_name": "snhu",
            "uuid": "l0ULPEbieDgYQRvHJDVy"
        },
        ...
    ]
}
```
