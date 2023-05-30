---
sidebar_label: CRUD APIs for Learners
sidebar_position: 1
---

# CRUD APIs for Learners

The following steps are to create, view and update Learner.


### Create a Learner

To create a learner, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner`**.
The request body for the API is as follows:

```json
{
    "first_name": "Jon",
    "middle_name": "Jon",
    "last_name": "Doe",
    "suffix": "",
    "prefix": "",
    "preferred_name": "",
    "preferred_first_name": "",
    "preferred_middle_name": "",
    "preferred_last_name": "",
    "preferred_name_type": "PreferredName",
    "preferred_pronoun": "",
    "student_identifier": "",
    "student_identification_system": "",
    "personal_information_verification": "",
    "personal_information_type": "",
    "address_type": "",
    "street_number_and_name": "",
    "apartment_room_or_suite_number": "",
    "city": "",
    "state_abbreviation": "",
    "postal_code": "",
    "country_name": "",
    "country_code": "",
    "latitude": "",
    "longitude": "",
    "country_ansi_code": 10000,
    "address_do_not_publish_indicator": "Yes",
    "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
        },
    "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
        }
    },
    "email_address_type": "Work",
    "email_address": "jon.doe@gmail.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "jon.doe2@gmail.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "employer_id": "test_employer_id",
    "employer": "",
    "employer_email": "testid@employer.com",
    "organisation_email_id": "jon.doe@foobar.com",
    "affiliation": ""
}
```

When we do send a **POST** request to the api **`<APP_URL>/learner-profile-service/api/v1/learner`**, first it will check if a learner with same **`email_address`** is already present in the collection.

If a learner with same **`email_address`** is present in learner collection, then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with the given email address jon.doe@gmail.com already exists",
  "data": null
}
```

Only if no learner with same **`email_address`** exists in learner collection, a new learner with the request body details and with a new uuid(unique ID of the learner) is created. After successfully adding new learner document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the learner",
  "data": {
    "uuid": "bISbGFDh0NXe1m5Kbu5O",
    "first_name": "Jon",
    "middle_name": "Jon",
    "last_name": "Doe",
    "suffix": "",
    "prefix": "",
    "preferred_name": "",
    "preferred_first_name": "",
    "preferred_middle_name": "",
    "preferred_last_name": "",
    "preferred_name_type": "PreferredName",
    "preferred_pronoun": "",
    "student_identifier": "",
    "student_identification_system": "",
    "personal_information_verification": "",
    "personal_information_type": "",
    "address_type": "",
    "street_number_and_name": "",
    "apartment_room_or_suite_number": "",
    "city": "",
    "state_abbreviation": "",
    "postal_code": "",
    "country_name": "",
    "country_code": "",
    "latitude": "",
    "longitude": "",
    "country_ansi_code": 10000,
    "address_do_not_publish_indicator": "Yes",
    "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      },
    "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      }
    },
    "email_address_type": "Work",
    "email_address": "jon.doe@gmail.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "jon.doe2@gmail.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "employer_id": "test_employer_id",
    "employer": "",
    "employer_email": "testid@employer.com",
    "organisation_email_id": "jon.doe@foobar.com",
    "affiliation": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Get a Learner

When we need to fetch the details of a learner then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{uuid}`** where **`uuid`** is the unique ID of the learner.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the learner",
  "data": {
    "first_name": "Jon",
    "middle_name": "Jon",
    "last_name": "Doe",
    "suffix": "",
    "prefix": "",
    "preferred_name": "",
    "preferred_first_name": "",
    "preferred_middle_name": "",
    "preferred_last_name": "",
    "preferred_name_type": "PreferredName",
    "preferred_pronoun": "",
    "student_identifier": "",
    "student_identification_system": "",
    "personal_information_verification": "",
    "personal_information_type": "",
    "address_type": "",
    "street_number_and_name": "",
    "apartment_room_or_suite_number": "",
    "city": "",
    "state_abbreviation": "",
    "postal_code": "",
    "country_name": "",
    "country_code": "",
    "latitude": "",
    "longitude": "",
    "country_ansi_code": 10000,
    "address_do_not_publish_indicator": "Yes",
    "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      },
    "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      }
    },
    "email_address_type": "Work",
    "email_address": "jon.doe@gmail.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "jon.doe2@gmail.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "organisation_email_id": "jon.doe@foobar.com",
    "employer_id": "test_employer_id",
    "affiliation": "",
    "employer": "",
    "employer_email": "testid@employer.com",
    "uuid": "bISbGFDh0NXe1m5Kbu5O",
    "is_archived": false,
    "created_time": "2022-07-27 13:52:17.979950+00:00",
    "last_modified_time": "2022-07-27 13:52:18.009353+00:00"
  }
}
```

If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

### Update a Learner

When we need to update the details of a learner then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{uuid}`** where **`uuid`** is the unique ID of the learner.
The request body would be as follows:

```json
{
  "preferred_name": "",
  "preferred_first_name": "",
  "preferred_middle_name": "",
  "preferred_last_name": "",
  "preferred_name_type": "PreferredName",
  "preferred_pronoun": "",
  "address_type": "",
  "street_number_and_name": "",
  "apartment_room_or_suite_number": "",
  "city": "",
  "state_abbreviation": "",
  "postal_code": "",
  "country_name": "",
  "country_code": "",
  "latitude": "",
  "longitude": "",
  "country_ansi_code": 10000,
  "address_do_not_publish_indicator": "Yes",
  "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
    },
  "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
    }
  },
  "email_address_type": "Work",
  "email_address": "jon.doe@gmail.com",
  "email_do_not_publish_indicator": "Yes",
  "backup_email_address": "jon.doe2@gmail.com",
  "gender": "NotSelected",
  "country_of_birth_code": "",
  "ethnicity": "",
  "employer_id": "test_employer_id",
  "employer": "",
  "employer_email": "testid@employer.com",
  "organisation_email_id": "jon.doe@foobar.com",
  "affiliation": "",
  "is_archived": false
}
```

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully updated the learner",
  "data": {
    "first_name": "Jon",
    "middle_name": "Jon",
    "last_name": "Doe",
    "suffix": "",
    "prefix": "",
    "preferred_name": "",
    "preferred_first_name": "",
    "preferred_middle_name": "",
    "preferred_last_name": "",
    "preferred_name_type": "PreferredName",
    "preferred_pronoun": "",
    "student_identifier": "",
    "student_identification_system": "",
    "personal_information_verification": "",
    "personal_information_type": "",
    "address_type": "",
    "street_number_and_name": "",
    "apartment_room_or_suite_number": "",
    "city": "",
    "state_abbreviation": "",
    "postal_code": "",
    "country_name": "",
    "country_code": "",
    "latitude": "",
    "longitude": "",
    "country_ansi_code": 10000,
    "address_do_not_publish_indicator": "Yes",
    "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      },
    "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
      }
    },
    "email_address_type": "Work",
    "email_address": "jon.doe@gmail.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "jon.doe2@gmail.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "organisation_email_id": "jon.doe@foobar.com",
    "employer_id": "test_employer_id",
    "affiliation": "",
    "employer": "",
    "employer_email": "testid@employer.com",
    "uuid": "bISbGFDh0NXe1m5Kbu5O",
    "is_archived": false,
    "created_time": "2022-07-27 13:52:17.979950+00:00",
    "last_modified_time": "2022-07-27 16:24:41.260904+00:00"
  }
}
```

If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

### Get Learning Hierarchy

When we need to get a learning hierarchy of the particular learner then we would make a  **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/curriculum-pathway/{curriculum_pathway_id}?frontend_response=true`** where **`learner_id`** is the unique ID of the learner and **curriculum_pathway_id** is the unique ID of the learning hierarchy.
Then the response body would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the curriculum pathway",
  "data": [{
      "label": "Program",
      "type": "curriculum_pathways",
      "data": {
        "name": "Program",
        "display_name": "Program",
        "description": "Next Step Pathway",
        "references": {
          "competencies": [],
          "skills": []
        },
        "child_nodes": {
          "learning_experiences": [],
          "curriculum_pathways": [
            "2VuPBz7Z1mHhcJ2Qvarb"
          ]
        },
        "achievements": [],
        "earned_achievements": [],
        "prerequisites": {
          "curriculum_pathways": [],
          "learning_experiences": [],
          "learning_objects": [],
          "learning_resources": [],
          "assessments": []
        },
        "is_locked": false,
        "uuid": "a1O2bogMGBToc8SpyTOb",
        "version": 1,
        "is_archived": false,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "created_time": "2022-11-17 12:56:25.713996+00:00",
        "last_modified_time": "2022-11-17 12:56:25.748592+00:00",
      },
      "children": [
        {
          "type": "curriculum_pathways",
          "data": {
            "uuid": "2VuPBz7Z1mHhcJ2Qvarb",
            "name": "HUM102",
            "display_name": "HUM102",
            "description": "Cluster A1 Pathway",
            "references": {},
            "parent_nodes": {
              "curriculum_pathways": [
                "a1O2bogMGBToc8SpyTOb"
              ]
            },
            "version": 1,
            "parent_version_uuid": "",
            "root_version_uuid": "",
            "is_archived": false,
            "is_deleted": false,
            "achievements": [],
            "earned_achievements": [],
            "prerequisites": {},
            "is_locked": false,
            "created_time": "2022-11-17 12:56:25.733674+00:00",
            "last_modified_time": "2022-11-17 12:56:25.770688+00:00",
            "created_by": "",
            "last_modified_by": "",
            "child_nodes": {
              "curriculum_pathways": [
                "6bM4QBvgdzMrFlx7Wj24"
              ]
            }
          },
          "label": "HUM102",
          "children": []
        }
      ]
    }]
}
```
### To get the curriculum pathway for the given learner

A **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/curriculum-pathway`**. where learner_id is the unique ID of the learner.

Then the response would be as follows:
```json
{
  "success": true,
  "message": "Successfully fetch the curriculum pathway id for the learner",
  "data": {
    "curriculum_pathway_id": "44qxEpc35pVMb6AkZGbi"
  }
}
```
If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

**`Note:`** To get the curriculum pathway for the given learner. We need to make sure that the given learner should added in the **learner association group**.


### To get the instructor of the given learner for the particular discipline

A **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/curriculum-pathway/{curriculum_pathway_id}/instructor`**. where learner_id is the unique ID of the learner and curriculum_pathway_id is the unique ID of the discipline.

Then the response would be as follows:
```json
{
  "success": true,
  "message": "Successfully fetched instructor details",
  "data": {
    "instructor_id": "44qxEpc35pVMb6AkZGbi"
  }
}
```

If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

### To get all instructors tagged to given learner and given program

A **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/curriculum-pathway/{program_id}/instructors`**. where learner_id is the unique ID of the learner and curriculum_pathway_id is the unique ID of the program.

Then the response would be as follows:
```json
{
  "success": true,
  "message": "Successfully fetched instructor details",
  "data": [
    {
      "user_id": "VaZ8ZLOIrulM4sHNhSYc",
      "staff_id": "F0oQqV5TlzwhX28n0S2E",
      "discipline_id": "YkzFiTaYkGlqyBIzG0fk",
      "discipline_name": "Humanities"
    },
    {
      "user_id": "QEyKAOxuUDiFjKS3lfRU",
      "staff_id": "Qh49RVbvHRIRAFx304YL",
      "discipline_id": "gMXvlgMXoNQCRUKuXxLC",
      "discipline_name": "English"
    }
  ]
}
```

If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

If the user corresponding to the given learner_id **`WPXbWYopqpoTbyl9`** is not present in any learner association group, then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with User ID WPXbWYopqpoTbyl9 not found in any Association Groups",
  "data": null
}
```

If there is no active instructor in the learner association group in which the user corresponding to the given learner_id **`WPXbWYopqpoTbyl9`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "No Active Instructors Available for the given Program = WPXbWYopqpoTbyl9 in AssociationGroup = VaZ8ZLOIrulM4sHNhSYc",
  "data": null
}
```


### Get Coach Details

When we need to get details for coach linked to a particular learner then we would need to make a  **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/coach`** where **`learner_id`** is the unique ID of the learner which will return the uuid of the coach.

**Note**: To get the coach for given learner, the user_id for user corresponding to given learner must exist & have active status in any one learner association groups.

The response body would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the coach",
  "data": {
      "coach_id": "3IyvJoqJpCr1uSkLM7g4"
    }
}
```

If the learner is not present for a given learner_id - **`WPXbWYopqpoTbyl9`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid WPXbWYopqpoTbyl9 not found",
  "data": null
}
```

If the user corresponding to the given learner_id **`WPXbWYopqpoTbyl9`** is not present in any learner association group, then the response would be as follows:

```json
{
  "success": false,
  "message": "User for given learner_id WPXbWYopqpoTbyl9 is not associated in any Learner Association Group",
  "data": null
}
```

If there is no active coach in the learner association group in which the user corresponding to the given learner_id **`WPXbWYopqpoTbyl9`** exists, then the response would be as follows:

```json
{
  "success": false,
  "message": "No active coach exists in Learner Association Group for user corresponding to given learner_id WPXbWYopqpoTbyl9",
  "data": null
}
```
