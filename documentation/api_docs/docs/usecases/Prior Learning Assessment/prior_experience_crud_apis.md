---
sidebar_label: CRUD APIs for Prior Experience
sidebar_position: 3
---

# CRUD APIs for Prior Experience

The following steps are regarding the CRUD APIs for Prior Experience


### Create a Prior Experience

To create a Prior Experience, a **POST** request has to be made to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experience`** .

The request body for the API is as follows:

```json
{
    "organization": "TPSI",
    "experience_title": "Fundamentals of Accounting",
    "date_completed": "2020-09-15T00:00:00",
    "credits_earned": 6,
    "description": "",
    "url": "",
    "competencies": [
        "Fields",
        "Applied Statistics"
    ],
    "skills": [
        "Accounts",
        "Mathematics"
    ],
    "documents": [],
    "cpl": 6,
    "is_flagged": false,
    "metadata": {},
    "alignments": {},
    "type_of_experience": "Transcripts",
    "validation_type": {"email": "verification@mail.com",
                        "website": "www.quickverficiation.com"},
    "terms": [
        {
            "end_date": {
                "day": "12",
                "month": "04",
                "year": "2020"
            },
            "transfer_courses": [
                {
                    "course_title": "Coding",
                    "course_code": "COD",
                    "credits": "3",
                    "grade": "B-"
                },
                {
                    "course_title": "Economics",
                    "course_code": "ECO",
                    "credits": "2",
                    "grade": "A"
                }
            ]
        },
        {
            "end_date": {
                "day": "04",
                "month": "08",
                "year": "2014"
            },
            "transfer_courses": [
                {
                    "course_title": "Math",
                    "course_code": "MTH",
                    "credits": "2",
                    "grade": "B+"
                },
                {
                    "course_title": "Accounts",
                    "course_code": "ACC",
                    "credits": "2",
                    "grade": "A-"
                }
            ]
        }
    ]
}
```

If the response is successful then a new Prior Experience with the request body details and with a new uuid (unique ID of the Prior Experience) is added. After successfully adding new Prior Experience document to the collection, you will get a response similar to the below json:

```json
{
    "success": true,
    "message": "Successfully created the prior experience",
    "data": {
        "organization": "TPSI",
        "experience_title": "Fundamentals of Accounting",
        "date_completed": "2020-09-15T00:00:00+00:00",
        "credits_earned": 6,
        "description": "",
        "url": "",
        "competencies": [
            "Fields",
            "Applied Statistics"
        ],
        "skills": [
            "Accounts",
            "Mathematics"
        ],
        "documents": [],
        "cpl": 6,
        "is_flagged": false,
        "metadata": {},
        "alignments": {},
        "type_of_experience": "Transcripts",
        "validation_type": {"email": "verification@mail.com",
                            "website": "www.quickverficiation.com"},
        "terms": [
            {
                "end_date": {
                    "day": "12",
                    "month": "04",
                    "year": "2020"
                },
                "transfer_courses": [
                    {
                        "course_title": "Coding",
                        "course_code": "COD",
                        "credits": "3",
                        "grade": "B-"
                    },
                    {
                        "course_title": "Economics",
                        "course_code": "ECO",
                        "credits": "2",
                        "grade": "A"
                    }
                ]
            },
            {
                "end_date": {
                    "day": "04",
                    "month": "08",
                    "year": "2014"
                },
                "transfer_courses": [
                    {
                        "course_title": "Math",
                        "course_code": "MTH",
                        "credits": "2",
                        "grade": "B+"
                    },
                    {
                        "course_title": "Accounts",
                        "course_code": "ACC",
                        "credits": "2",
                        "grade": "A-"
                    }
                ]
            }
        ],
        "uuid": "RiIymL3h8qJN1gRt6Bys",
        "created_time": "2022-12-22 10:39:10.106639+00:00",
        "last_modified_time": "2022-12-22 10:39:10.592524+00:00"
    }
}
```

### Get all Prior Experience

When we need to fetch all the Prior Experiences available, then we would make a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experiences`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Prior Experience array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Prior Experiences.

The response would look something like below:

```json
{
    "success": true,
    "message": "Successfully fetched the prior experiences",
    "data": {
        "records": [
            {
                "organization": "DDU",
                "experience_title": "Accounts",
                "date_completed": "2019-05-15T00:00:00+00:00",
                "credits_earned": 6,
                "description": "",
                "url": "",
                "competencies": [
                    "Fields",
                    "Applied Statistics"
                ],
                "skills": [
                    "Accounts",
                    "Mathematics"
                ],
                "documents": [],
                "cpl": 6,
                "is_flagged": false,
                "metadata": {},
                "alignments": {},
                "type_of_experience": "Transcripts",
                "validation_type": {},
                "terms": [
                    {
                        "end_date": {
                            "year": "2020",
                            "month": "June",
                            "day": "12"
                        },
                        "transfer_courses": [
                            {
                                "course_title": "Coding",
                                "course_code": "COD",
                                "credits": "3",
                                "grade": "B-"
                            },
                            {
                                "course_title": "Economics",
                                "course_code": "ECO",
                                "credits": "2",
                                "grade": "A"
                            }
                        ]
                    },
                    {
                        "end_date": {
                            "year": "2014",
                            "month": "March",
                            "day": "04"
                        },
                        "transfer_courses": [
                            {
                                "course_title": "Math",
                                "course_code": "MTH",
                                "credits": "2",
                                "grade": "B+"
                            },
                            {
                                "course_title": "Accounts",
                                "course_code": "ACC",
                                "credits": "2",
                                "grade": "A-"
                            }
                        ]
                    }
                ],
                "uuid": "QTsx299k0j7OGbWAoys1",
                "created_time": "2023-05-18 06:11:09.870765+00:00",
                "last_modified_time": "2023-05-18 06:11:10.036996+00:00"
            },
            {
                "organization": "DDU",
                "experience_title": "Accounts",
                "date_completed": "2019-05-15T00:00:00+00:00",
                "credits_earned": 6,
                "description": "",
                "url": "",
                "competencies": [
                    "Fields",
                    "Applied Statistics"
                ],
                "skills": [
                    "Accounts",
                    "Mathematics"
                ],
                "documents": [],
                "cpl": 6,
                "is_flagged": false,
                "metadata": {},
                "alignments": {},
                "type_of_experience": "Transcripts",
                "validation_type": {
                    "phone": "123-321-9900",
                    "email": "www.verify.com"
                },
                "terms": [
                    {
                        "end_date": {
                            "year": "2020",
                            "month": "June",
                            "day": "12"
                        },
                        "transfer_courses": [
                            {
                                "course_title": "Coding",
                                "course_code": "COD",
                                "credits": "3",
                                "grade": "B-"
                            },
                            {
                                "course_title": "Economics",
                                "course_code": "ECO",
                                "credits": "2",
                                "grade": "A"
                            }
                        ]
                    },
                    {
                        "end_date": {
                            "year": "2014",
                            "month": "March",
                            "day": "04"
                        },
                        "transfer_courses": [
                            {
                                "course_title": "Math",
                                "course_code": "MTH",
                                "credits": "2",
                                "grade": "B+"
                            },
                            {
                                "course_title": "Accounts",
                                "course_code": "ACC",
                                "credits": "2",
                                "grade": "A-"
                            }
                        ]
                    }
                ],
                "uuid": "IP5BZx81GHCWsfPQeFA1",
                "created_time": "2023-05-18 06:10:51.903253+00:00",
                "last_modified_time": "2023-05-18 06:10:52.073427+00:00"
            }
        ],
        "total_count": 10000
    }
}
```

### Get a specific Prior Experience

When we need to fetch the details of a specific Prior Experience, then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experience/{uuid}`** where **`uuid`** is the unique ID of the Prior Experience.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully fetched the prior experience",
    "data": {
        "organization": "TPSI",
        "experience_title": "Fundamentals of Accounting",
        "date_completed": "2020-09-15T00:00:00+00:00",
        "credits_earned": 6,
        "description": "",
        "url": "",
        "competencies": [
            "Fields",
            "Applied Statistics"
        ],
        "skills": [
            "Accounts",
            "Mathematics"
        ],
        "documents": [
            "gs://core-learning-services-dev/pla/user-transcripts/test.pdf"
        ],
        "cpl": 6,
        "is_flagged": false,
        "metadata": {},
        "alignments": {},
        "type_of_experience": "Transcripts",
        "validation_type": {},
        "terms": [],
        "uuid": "bUMOvE2M5FKLjLJe6aNN",
        "created_time": "2022-10-10 14:33:54.131484+00:00",
        "last_modified_time": "2022-10-10 14:33:54.574399+00:00"
    }
}
```

If the Prior Experience is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Prior Experience with uuid zxtPzcjdkl5JvVGjl01j not found",
    "data": null
}
```

### Update a Prior Experience

When we need to update the details of a Prior Experience, then we would make a **PUT** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experience/{uuid}`** where **`uuid`** is the unique ID of the Prior Experience.

The request body would be as follows:

```json
{
    "organization": "CGSI"
}
```

After the validation of Prior Experience for given uuid, Prior Experience for the given uuid is updated and the response will look like this:

```json
{
    "success": true,
    "message": "Successfully updated the prior experience",
    "data": {
        "organization": "CGSI",
        "experience_title": "Fundamentals of Accounting",
        "date_completed": "2020-09-15T00:00:00+00:00",
        "credits_earned": 6,
        "description": "",
        "url": "",
        "competencies": [
            "Fields",
            "Applied Statistics"
        ],
        "skills": [
            "Accounts",
            "Mathematics"
        ],
        "documents": [
            "gs://core-learning-services-dev/pla/user-transcripts/test.pdf"
        ],
        "cpl": 6,
        "is_flagged": false,
        "metadata": {},
        "alignments": {},
        "type_of_experience": "Transcripts",
        "validation_type": {},
        "terms": [],
        "uuid": "bUMOvE2M5FKLjLJe6aNN",
        "created_time": "2022-10-10 14:33:54.131484+00:00",
        "last_modified_time": "2022-12-22 10:51:29.822262+00:00"
    }
}
```

If the Prior Experience is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Prior Experience with uuid o1nv13n6sbu0ny not found",
    "data": null
}
```

### Delete a Prior Experience

When we need to delete a Prior Experience, then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experience/{uuid}`** where **`uuid`** is the unique ID of the Prior Experience.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Successfully deleted the prior experience"
}
```

If the Prior Experience is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
    "success": false,
    "message": "Prior Experience with uuid 1HFXhcO7A384fdcq not found",
    "data": null
}
```

### Import Prior Experiences From Json file

To import Prior Experiences from JSON file, we would make a **POST** request to the API endpoint - **`<APP_URL>/prior-learning-assessment/api/v1/prior-experience/import/json`**, along with **`json_file`** of type binary consisting of Prior Experiences, json_schema which matches the PriorExperience model. This will create the new Prior Experiences for all the entries in the file.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the prior experiences",
  "data": [
    "124hsgxR77QKS8uS7Zgm",
    "0G92bYBw6wxdMYuvrfc1",
    "0FmHJtre1FDM0p5f7b4V"
  ]
}
```
