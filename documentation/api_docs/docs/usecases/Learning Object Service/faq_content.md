---
sidebar_label: FAQ Content
sidebar_position: 7
---

# FAQ Management

### Create a FAQ

To create a faq, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/faq`**.
The request body for the API is as follows:

```json
{
    "resource_path": "some/entry/point",
    "name": "Sample FAQ",
    "curriculum_pathway_id": "uuid of linked pathway"
}
```

> **Note**
>
> The ```curriculum_pathway_id``` should be of alias type program 

After successful creation of the FAQ you will receive following response with status code ```200```

```json
    {
        "success": true,
        "message": "Successfully created FAQ",
        "data": {
            "resource_path": "some/entry/point",
            "name": "Sample FAQ",
            "curriculum_pathway_id": "Sample_pathway_id",
            "uuid": "U2DDBkl3Ayg0PWudzhI",
            "is_archived": false,
            "created_time": "2022-03-03 09:22:49.843674+00:00",
            "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
        }
    }
```

### Fetch FAQ by UUID

Make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/faq/{faq_uuid}`**.

`faq_uuid`: This is the UUID of the FAQ you want to fetch

The response will look like:

```json
    {
        "success": true,
        "message": "Successfully fetched FAQ by UUID",
        "data": {
            "resource_path": "some/entry/point",
            "name": "Sample FAQ",
            "curriculum_pathway_id": "Sample_pathway_id",
            "uuid": "U2DDBkl3Ayg0PWudzhI",
            "is_archived": false,
            "created_time": "2022-03-03 09:22:49.843674+00:00",
            "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
        }
    }

```
### Fetch FAQ by Pathway UUID

Make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/faq`**.

Query Params:

`skip`: Integer representing the number of records to be skipped

`limit`: Integer representing the step size

`curriculum_pathway_id`: This is the UUID of the pathway linked to a FAQ

The response will look like:

```json
    {
        "success": true,
        "message": "Successfully Fetched FAQs",
        "data": [{
            "resource_path": "some/entry/point",
            "name": "Sample FAQ",
            "curriculum_pathway_id": "Sample_pathway_id",
            "uuid": "U2DDBkl3Ayg0PWudzhI",
            "is_archived": false,
            "created_time": "2022-03-03 09:22:49.843674+00:00",
            "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
        }]
    }

```
### Generate Signed URL for FAQ

Make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/content-serving/{faq_uuid}`**.

Query Params:

`is_faq`: Boolean field representing if the requested data is an FAQ

The response will look like:

```json
    "success": true,
            "message": "Successfully fetched the signed url",
            "data": {
                "signed_url": "some/signed/url",
                "resource_type": "faq_html",
                "resource_uuid": "U2DDBkl3Ayg0PWudzhI"
            }

```
