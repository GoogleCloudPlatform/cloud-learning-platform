---
sidebar_label: Upload and Parse transcript(s)
sidebar_position: 4
---

# Upload and Parse transcript(s)

The following steps are regarding uploading and parsing transcript(s)


### Step 1: Upload transcript(s)

**Please note**: If you already have the GCS path(s) of the transcript(s) that you want to parse to extract the Prior Experience(s), you can directly go to step 2.

To upload documents(s) to extract the Prior Experience(s), a **POST** request has to be made to API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/upload`**. Use the **Choose file** button to upload a file.

If the response is successful then the transcript(s) will be uploaded to GCS bucket and the response body will have the GCS path(s) of the uploaded transcript(s).

The successful response will be as follows:

```json
{
  "success": true,
  "message": "Successfully uploaded the transcripts",
  "data": [
    "gs://aitutor-dev/pla/user-transcripts/test_3.pdf",
    "gs://aitutor-dev/pla/user-transcripts/test_2.pdf"
  ]
}
```

If any of the input files is greater than 2MB in size, you will get **PayloadTooLarge** error as response, in which case the response body will be as follows:

```json
{
  "success": false,
  "message": "File size is too large: large_test_file.pdf",
  "data": null
}
```

If any of the input files is other than the allowed file types (pdf, csv, docx, xlsx, zip, jpeg, jpg), you will get **BadRequest** error, in which case the response body will be as follows:

```json
{
  "success": false,
  "message": "Invalid document type. Allowed types are: ['.pdf', '.csv', '.docx', '.xlsx', '.zip', '.jpeg', '.jpg']",
  "data": null
}
```

### Step 2: Parsing the Transcript(s)

(approx time taken for this step: 1-2 minutes)

To parse the transcript(s) to extract Prior Experience(s), a **POST** request has to be made to API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/extract`**.
The request body takes 3 parameters - 
`doc_class`: transcript or any other type of document.
`context`: additional specific information that might help in extraction - like organsiation name/degree type, etc.
`gcs_urls`: GCS path(s) of the document(s) from which Prior Experiences are to be extracted.

For now, only "transcripts" is allowed as `doc_class` and "generic" is allowed as `context`.

The request body will be as follows:

```json
{
  "doc_class": "transcripts",
  "context": "generic",
  "gcs_urls": [
    "gs://aitutor-dev/pla/user-transcripts/Transcript_Example.pdf"
  ]
}
```

On a successful API hit, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully parsed the transcript",
  "data": [
    {
      "name": {
        "text": "John Smith",
        "score": 0.9
      },
      "skills": {
        "text": null,
        "score": null
      },
      "competencies": {
        "text": null,
        "score": null
      },
      "organization": {
        "text": null,
        "score": null
      },
      "experience_title": {
        "text": "13120 American Literature (Honors)",
        "score": 1
      },
      "date_completed": {
        "text": "Jun 15, 2018",
        "score": 0.83
      },
      "credits_earned": {
        "text": "0.50",
        "score": 1
      },
      "description": {
        "text": null,
        "score": null
      },
      "url": {
        "text": null,
        "score": null
      }
    }
  ]
}
```

If any of the input GCS path does not exist, you will get `ResourceNotFound` error, in which case the reponse will be as follows:

```json
{
  "success": false,
  "message": "Could not find the file. Please check the gcs_url",
  "data": null
}
```
