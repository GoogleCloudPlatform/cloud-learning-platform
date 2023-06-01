---
sidebar_label: CRUD APIs for Learners Profile
sidebar_position: 2
---

# CRUD APIs for Learners Profile

The following steps are to create, view and update Learner Profile.


### Create a learner profile for a Learner

After creating a learner, a learner profile should be created.
To create a learner_profile for a learner, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/learner-profile`** where **`learner_id`** is the unique ID of the learner.

The request body for the API is as follows:

```json
{
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
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

When we send a post request to the api **`<APP_URL>/learner-profile-service/api/v1/learner/xw4LB9j2wwhdxaJjDpJ8/learner-profile`**, first it will validate the learner for given learner_id.

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
    "employment_status": "Unemployed",
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

### Get learner profile of a Learner

When we need to fetch the details of the learner_profile of a learner then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/learner-profile/{uuid}`** where **`learner_id`** is the unique ID of the learner and **`uuid`** is the unique ID of the learner profile.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the learner profile",
  "data": {
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
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
    "uuid": "5k5OG88iCAaY56DkAk9J",
    "is_archived": false,
    "created_time": "2022-07-28 11:32:53.512086+00:00",
    "last_modified_time": "2022-07-28 11:32:53.524477+00:00"
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

### Update the learner profile for a learner

When we need to update the details of the learner profile of a learner then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/learner-profile/{uuid}`** where **`learner_id`** is the unique ID of the learner and **`uuid`** is the unique ID of the learner profile.

The request body for the Api would be as follows:

```json
{
  "learning_goals": ["Develop Communication Skills", "Teamwork"],
  "learning_constraints": {"weekly_study_time": 0},
  "learning_preferences": {},
  "patterns_of_participation": {},
  "employment_status": "Unemployed",
  "potential_career_fields":  [],
  "personal_goals": "",
  "employment_history": {},
  "education_history": {},
  "account_settings": {},
  "contact_preferences": {"email":false, "phone":false},
  "attestation_object": {},
  "is_archived": false,
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

After the validation of learner for given learner_id, learner profile for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the learner profile",
  "data": {
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
    "potential_career_fields":  [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {"email":false, "phone":false},
    "attestation_object": {},
    "is_archived": false,
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
    "uuid": "5k5OG88iCAaY56DkAk9J",
    "is_archived": false,
    "created_time": "2022-07-28 11:32:53.512086+00:00",
    "last_modified_time": "2022-07-28 17:42:00.042678+00:00"
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

If the learner profile is not present for a given uuid - **`5k5OG88iCAaY56DkAk9k`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid 5k5OG88iCAaY56DkAk9k not found",
  "data": null
}
```

:::note

For the APIs with the `learner_id` in the URL path -  
**`<APP_URL>/learner-profile-service/api/v1/learner/{learner_id}/learner-profile`**, Learner ID is validated and then an error response is sent for an invalid learner.

:::
