---
sidebar_label: Setting up a Learner
sidebar_position: 1
---

# Setting up a Learner

The following steps need to be followed to setup a new Learner.

<!-- :::note

**`APP_URL`** used in the below URLs is **<https://snhu-glidepath-dev-api.cloudpssolutions.com>**

::: -->

### Create a Learner

A new Learner needs to be created in the Learners collection to store personal details of the learner.
To create a learner, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner`**.
The request body for the API is as follows:

```json
{
    "first_name": "steve",
    "middle_name": "",
    "last_name": "jobs",
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
    "email_address": "steve.jobs@example.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "steve.jobs2@example.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "employer_id": "test_employer_id",
    "employer": "",
    "employer_email": "testid@employer.com",
    "organisation_email_id": "steve.jobs@foobar.com",
    "affiliation": ""
}
```

When we do send a **POST** request to the api **`<APP_URL>/learner-profile-service/api/v1/learner`**, first it will check if a learner with same **`email_address`** is already present in the collection.

If a learner with same **`email_address`** is present in learner collection, then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with the given email address steve.jobs@example.com already exists",
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
    "email_address": "steve.jobs@example.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "steve.jobs2@example.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "employer_id": "test_employer_id",
    "employer": "",
    "employer_email": "testid@employer.com",
    "organisation_email_id": "steve.jobs@foobar.com",
    "affiliation": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Create a learner profile for a Learner

After creating a learner, a learner profile should be created to store goals, achievements, learning progress etc.
To create a learner_profile for a learner, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/learner-profile`** where **`learner_id`** is the unique ID of the learner.

The request body for the API is as follows:

```json
{
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "unemployed",
    "potential_career_fields":  [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {"email":false, "phone":false},
    "attestation_object": {},
    "enrollment_information": {},
    "progress": {
        "curriculum_pathways": {},
        "learning_experiences": {},
        "learning_objects": {},
        "learning_resources": {},
        "assessments": {}
    },
    "achievements": [],
    "tagged_skills": [],
    "tagged_competencies": [],
    "mastered_skills": [],
    "mastered_competencies": []
}
```

When we send a post request to the api **`<APP_URL>/learner-profile-service/api/v1/learner/bISbGFDh0NXe1m5Kbu5O/learner-profile`**, first it will validate the learner for given learner_id.

If a learner with given uuid exists, then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the learner profile",
  "data": {
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "unemployed",
    "potential_career_fields":  [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {"email":false, "phone":false},
    "attestation_object": {},
    "enrollment_information": {},
    "progress": {
        "curriculum_pathways": {},
        "learning_experiences": {},
        "learning_objects": {},
        "learning_resources": {},
        "assessments": {}
    },
    "achievements": [],
    "tagged_skills": [],
    "tagged_competencies": [],
    "mastered_skills": [],
    "mastered_competencies": [],
    "uuid": "ymGSJ69MGtgoiL9wudZd",
    "is_archived": false,
    "created_time": "2022-07-28 11:08:55.066059+00:00",
    "last_modified_time": "2022-07-28 11:08:55.085461+00:00"
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

### Create a User of Learner type:

A new user with user_type as Learner has to be created in the Users collection by providing the newly created learner_id as user_type_ref to link the User to the Learner.
To create a new user of learner type, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/user`**.
The request body for the API is as follows:

```json
{
  "first_name": "steve",
  "last_name": "jobs",
  "email": "steve.jobs@example.com",
  "user_type": "learner",
  "user_type_ref": "bISbGFDh0NXe1m5Kbu5O",
  "user_groups": [
    "44qxEpc35pVMb6AkZGbi"
  ],
  "status": "active",
  "is_registered": true,
  "failed_login_attempts_count": 0,
  "access_api_docs": false,
  "gaia_id": "F2GGRg5etyty"
}
```

A new user of learner type with the request body details and new user_id (unique ID of the user) will get added to the Users collection and this user will also get added to the given usergroups. After successful execution, response will be similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the user",
  "data": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "user_type": "learner",
    "user_type_ref": "",
    "user_groups": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "status": "active",
    "is_registered": true,
    "failed_login_attempts_count": 0,
    "access_api_docs": false,
    "gaia_id": "F2GGRg5etyty"
  }
}
```

### Create an Agent

Finally, an Agent object needs to be created for the learner by providing the user_id of the newly created user.
To create an Agent, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent`**

The request body for the API is as follows:

```json
{
  "object_type": "agent",
  "name": "steve jobs",
  "mbox": "mailto:steve.jobs@example.com",
  "mbox_sha1sum": "",
  "open_id": "",
  "account_homepage": "",
  "account_name": "steve_jobs",
  "members": [],
  "user_id": "124hsgxR77QKS8uS7Zgm"
}
```

The **`user_id`** in the above input payload is the existing user's id in the firestore collection and it will be used as reference in the Agent data model. If the user is not present, a **`ResourceNotFoundException`** exception is raised. It is necessary to create a user before accessing the same user id in the Agent data model in order to prevent this.

If an agent already exists with the same **`user_id`** then **`ConflictError`** exception is raised.

If the response is successful then a new Agent with the request body details and with a new uuid(unique ID of the Agent) is added. After successfully adding new Agent document to the collection, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the agent",
  "data": {
    "object_type": "agent",
    "name": "steve.jobs@example.com",
    "mbox": "mailto:steve.jobs@example.com",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "steve_jobs",
    "members": [],
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "uuid": "AAVqfJoM6HpyV5K7kmKE",
    "created_time": "2022-09-01 07:13:34.801165+00:00",
    "last_modified_time": "2022-09-01 07:13:35.001616+00:00"
  }
}
```