---
sidebar_label: Ingest external (WGU) data, break out skills and organize them in a skill graph
sidebar_position: 2
---

# Ingest external (WGU) data, break out skills and organize them in a skill graph

For ingestion and alignment of wgu skills with other skills, the following steps need to be followed.


### Step 1:

(approx time taken for this step: 2 minutes)

We can download the CSV from wgu skill library(eg. https://osmt.wgu.edu/api/collections/a6f9236c-55c3-404b-b5b2-0064195b46f7)

First step to ingest the downloaded wgu CSV data to skill graph is to convert it in the format required by our generic CSV ingestion utility API. We can check the format in API documentation <a href="/skill-service/api/v1/redoc#operation/generic_csv_import_details_import_csv_info_get" target="_blank">here</a>. Since, wgu only provides skill data, we will have only one skill CSV to ingest.

This reformated skill CSV can then be for ingesting data using generic CSV ingestion API **`<APP_URL>/skill-service/api/v1/import/csv`**.

We will add **`source`** ="wgu" in the query param of API as we are ingesting data from the wgu registry. When we do send a post request to the above API, an async batch job will be created in the background which will do ingestion of data in the skill graph.

On a successful API hit, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully initiated the job with type 'generic_csv_ingestion'. Please use the job name to track the job status",
  "data": {
    "job_name": "34176209-39a3-42e0-bbc5-5135a525fbcb",
    "status": "active"
  }
}
```

### Step 2:

(approx time taken for this step: 5 minutes)

We can check the status of the batch job using the job name that we get in response of the generic ingestion API.

For that, we can hit the **GET** request using the API **`<APP_URL>/skill-service/api/v1/jobs/generic_csv_ingestion/{job_name}`** where we pass the job name as path parameter(in this case, the API url will look like <{base_url}/skill-service/api/v1/jobs/generic_csv_ingestion/2a4803e0-8377-485b-a941-971b528ff48f>)

The response will look like this:

```json
{
  "success": true,
  "message": "Successfully fetched the batch job",
  "data": {
    "job_name": "2a4803e0-8377-485b-a941-971b528ff48f",
    "created_by": "",
    "created_time": "2022-04-19 10:42:32.550899+00:00",
    "last_modified_by": "",
    "last_modified_time": "2022-04-19 10:44:16.641083+00:00",
    "input_data": {
      "wgu_uri": "gs://bucket/skill-service/user-uploaded-csvs/wgu_data_2022_04_19-10:42:31_AM.csv"
    },
    "status": "succeeded",
    "errors": {},
    "type": "generic_csv_ingestion"
  }
}
```

Here, the **`status`** in the **`data`** key shows the status of job which in this case is "succeeded".

If it fails for some reason, we will have **`status`** as "failed" with the explanation/data available in the **`errors`** key.

### Step 3:

(approx time taken for this step: 40 minutes to 1 hour)

If we have to align wgu skill with snhu provided skill, we will be required to create embeddings for wgu sourced skills which were ingested in step 1.
To do that, we can use **`<APP_URL>/skill-service/api/v1/skill/embeddings`** API which requires the following request body:

```json
{
  "level": ["skill"],
  "source_name": ["wgu"]
}
```

Here, **`level`** denotes the node of the skill graph which in this case is "skill".

The response which we will get is details of batch job which will create embeddings and store them in db as a background process.

We can check the status of the batch job using the job name that we get in response of create embeddings API.
For that, we can hit the **GET** request using the API **`<APP_URL>/skill-service/api/v1/jobs/skill_embedding_db_update/{job_name}`** where we pass the job name as path param.

### Step 4:

(approx time taken for this step: 10 mins)

Once the batch job created in step 3 succeeds, we can move forward for doing skill alignment.

We will use **`<APP_URL>/skill-service/api/v1/unified-alignment/batch`** API which requires the following request body:

```json
{
  "source_name": ["snhu"],
  "input_type": "skill",
  "output_alignment_sources": {
    "skill_sources": ["wgu"]
  }
}
```

Here, we are providing the list of sources in the **`output_alignment_sources.skill_sources`** key where the alignment will happen with sources we provide in the **`source_name`** key. In this case, wgu skills will be aligned with snhu skills whose embeddings have been created.

When we hit the API, we get the name of the batch job of which we can track the status in the same way we did it in step 2 with API url as `<APP_URL>/skill-service/api/v1/jobs/unified_alignment/{job_name}`

### Step 5:

(approx time taken for this step: 1 minute)

When the batch job in step 4 completes, we can fetch any skill with **`source_name`** as "snhu" to check for alignments.

Let's take the below example where we can see updated alignments after the successful completion of the batch job in step 4.

```json
{
    "name": "Goal-Driven Generally Accepted Accounting Principles",
    "description": "Apply the appropriate accounting method to achieve an organizational goal",
    "keywords": [...],
    "author": "",
    "creator": "",
    "alignments": {
        "standard_alignment": {},
        "credential_alignment": {},
        "skill_alignment": {
            "wgu": {
                "suggested": [
                    {
                        "name": "Basic Accounting Principles",
                        "score": 0.868,
                        "id": "jFZcagwEr59qhDu0UCVp"
                    },
                    {
                        "name": "Corporate Accounting",
                        "id": "P7CiIPUQDN2OUKI5f14d",
                        "score": 0.108
                    },
                    {
                        "score": 0.012,
                        "name": "Accounting Regulations",
                        "id": "S2oUgG3VkFBe4pcrD4z7"
                    },
                    {
                        "score": 0.009,
                        "name": "Accounting",
                        "id": "zJ5MK0qcJzVtwIbjNYiZ"
                    },
                    {
                        "name": "Multi-Site Accounting",
                        "id": "15dfOLwZpZZFDcVNOyUl",
                        "score": 0.007
                    }
                ]
            }
        },
        "knowledge_alignment": {},
        "role_alignment": {
            "onet": {}
        },
        "organizational_alignment": {}
    },
    "organizations": [],
    "certifications": [],
    "occupations": {
        "occupations_major_group": [],
        "occupations_minor_group": [],
        "broad_occupation": [],
        "detailed_occupation": []
    },
    "onet_job": "",
    "parent_nodes": [...],
    "reference_id": "ACC-33276-04",
    "source_uri": "snhu",
    "source_name": "snhu",
    "uuid": "03BtFFltDewVGflbaA2G",
    "created_time": "2022-05-09 05:32:42.362891+00:00",
    "last_modified_time": "2022-05-24 12:58:22.057664+00:00"
}
```

Here, in key **`alignments.skill_alignment`**, we can see alignments for suggestions related to wgu with the score/percentage of the match.
