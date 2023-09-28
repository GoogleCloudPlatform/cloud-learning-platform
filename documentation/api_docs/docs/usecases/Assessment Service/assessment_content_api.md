---
sidebar_label: File Upload API for Assessment and Submitted Assessment
sidebar_position: 5
---

# Assessment Authoring File Upload API

An LXE can upload extra files for an Assessment using the endpoint **`<API_URL>/assessment/service/api/v1/assessment-authoring/upload-sync/{user_id}`** with a **POST** request

#### Request Parameters
1. `user_id`: User id of the LXE user

#### Request Body
1. `content_file`: The content file should be a Binary File.


#### API Response
```json
    {
        "success": True,
        "message": "Successfully uploaded file",
        "data": {
            "resource_path": <location_of_uploaded_file>
        }
    }
```

When data is successfully uploaded via the API it will be placed in a `temp` folder. When the Assessment create API is called, these files will be moved from the `temp` folder to the folder identified by `Assessment ID`.

#### File Storage Structure on GCS
```
    CONTENT_SERVING_BUCKET
        |
        + assessments
            |
            + <USER_ID>
                |
                + temp
                |   |
                |   + file_1.txt
                |   + file_2.txt
                |
                + <Assessment_1_ID>
                |   |
                |   + file_3.txt
                |
                + <Assessment_2_ID>
                    |
                    + file_4.txt
```

Note: Relocating the Files from `temp` folder to the required Assessment folder will be done internally by the service when the Assessment is created.

---

# Assessment Submission File Upload API

A Learner can upload files for Assessment using te following endpoint**`<API_URL>/assessment/service/api/v1/assessment-submission/upload-sync/{learner_id}/{assessment_id}`** with a **POST** request

#### Request Parameters
1. `learner_id`: User id of the Learner
2. `assessment_id`: UUID of the Assessment for which submission is to being done

#### Request Body
1. `content_file`: The content file should be a Binary File.

#### API Response
```json
    {
        "success": True,
        "message": "Successfully uploaded file",
        "data": {
            "resource_path": <location_of_uploaded_file>
        }
    }
```

When data is successfully uploaded via the API it will be placed in a `temp` folder. When the Assessment Submit API is called, these files will be moved from the `temp` folder to the folder identified by `Assessment ID`.

#### File Storage Structure on GCS
```
    CONTENT_SERVING_BUCKET
        |
        + submissions
            |
            + <LEARNER_ID>
                |
                + <ASSESSMENT_ID>
                    |
                    + temp
                    |   |
                    |   + file_1.txt
                    |   + file_2.txt
                    |
                    + <Assessment_1_ID>
                    |   |
                    |   + file_3.txt
                    |
                    + <Assessment_2_ID>
                        |
                        + file_4.txt
```

Note: Relocating the Files from `temp` folder to the required Assessment folder will be done internally by the service when a submission is made for an Assessment.
---

# API to generate Signed URL for Assessment Content

The files attached to the Assessment and Submitted Assessment can be accessed using Signed URL. Since Assessment and Submitted Assessment can have multiple files attached, the response of the below endpoint is a list of signed urls.

Make a **GET** request to the **`<API_URL>/assessment/service/api/v1/assessment-content/<assessment_content_uuid>/signed-url`**


#### Request Parameters
1. `assessment_content_uuid`: UUID of Assessment or Submitted Assessment

#### Query Parameters
1. `is_submitted_assessment`: if `true`, the API will infer `assessment_content_uuid` as UUID of the Submitted Assessment. Default value is `false`, which means by default `assessment_content_uuid` will be treated as Assessment uuid.

#### API Response 1
If signed URLs are generated successfully for all the `file_paths` then the following response will be returned with a **`200`** status code. 

```json
    {
        "success": True,
        "message": "Successfully generated signed urls for all files",
        "data": [
            {
                "file_path": <location_of_attached_file>,
                "signed_url": <signed_url>,
                "status": "Signed url generated successfully"
            },{
                "file_path": <location_of_attached_file>,
                "signed_url": <signed_url>,
                "status": "Signed url generated successfully"
            },
        ]
    }
```

#### API Response 2
If signed URLs for some files were not generated successfully because of missing files, then the following response will be returned with a **`200`** status code. 

```json
    {
        "success": True,
        "message": "Could not generate urls for some files",
        "data": [
            {
                "file_path": <location_of_attached_file>,
                "signed_url": <signed_url>,
                "status": "Signed url generated successfully"
            },{
                "file_path": <location_of_attached_file>,
                "signed_url": null,
                "status": "File Not Found"
            },
        ]
    }
```
Notice that the `status` of the second file is mentioned as `File Not Found`, yet the Status code is **`200`**. This is because the API is responsible for generation of multiple signed urls, and if the process fails for a few files, it is still a partial success.


#### API response 3
If signed URLs generation failed for all the files, then the API will respond with a **`500`** status code.

```json
    {
        "success": False,
        "message": "Some error occurred while generating signed urls",
        "data": [
            {
                "file_path": <location_of_attached_file>,
                "signed_url": null,
                "status": "File Not Found"
            },{
                "file_path": <location_of_attached_file>,
                "signed_url": null,
                "status": "File Not Found"
            },
        ]
    }
```
Notice that the `status` of both the files is `File Not Found`. Which means, it was a complete failure, hence the response status is **`500`**
