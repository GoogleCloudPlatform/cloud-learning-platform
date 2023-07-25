Feature: Negative scenarios for CRUD APIs for managing learner, learner-profile, achievement and goal data in Student Learner Profile


    Scenario: Unable to create learner when one or more required fields is missing
      Given that no learner with same e-mail id already exists, format the API request url to create a learner with one or more required fields missing in request payload
        When API request is sent to create learner with one or more required fields missing in request payload
          Then SLP Service will throw a validation error message while trying to create the learner as required field is missing

    Scenario: Unable to update learner when trying to update a field that is non-editable
      Given that a Learner account exists, format the API request url to update non-editable field of learner in request payload
        When API request is sent to update non-editable field of the learner in request payload
          Then SLP Service will throw a validation error message while trying to update the learner as non-editable field was attempted to be updated

    Scenario: Unable to update learner when incorrect uuid is given
      Given that a Learner account exists, format the API request url to update the learner by providing incorrect uuid in request payload
        When API request is sent to update learner with incorrect uuid in request payload
          Then SLP Service will throw a validation error message while trying to update learner as incorrect uuid was provided

    Scenario: Unable to fetch learner when incorrect uuid is given
      Given that a Learner account exists, format the API request url to fetch the learner by providing incorrect uuid in request payload
        When API request is sent to fetch learner with incorrect uuid in request payload
          Then SLP Service will throw an error message while trying to fetch the learner as incorrect uuid was provided

    Scenario: Unable to delete learner when incorrect uuid is given
      Given that a Learner account exists, format the API request url to delete the learner by providing incorrect uuid in request payload
        When API request is sent to delete learner with incorrect uuid in request payload
          Then SLP Service will throw a validation error message while trying to delete learner as incorrect uuid was provided

    Scenario: Unable to create learner profile when invalid learner_id provided
      Given that a Learner account exists, format the API request url to create a learner profile by providing invalid learner_id in request payload
        When API request is sent to create learner profile with invalid learner_id in request payload
          Then SLP Service will throw a validation error message while trying to create the learner profile as invalid learner_id was provided

    Scenario: Unable to update learner profile when an invalid extra field is provided
      Given that a Learner profile exists, format the API request url to update learner profile by including invalid extra field in request payload
        When API request is sent to update a learner profile by providing invalid extra field in request payload
          Then SLP Service will throw a validation error message while trying to update the learner profile as invalid extra field was provided

    Scenario: Unable to update learner profile when trying to update a field that is non-editable
      Given that a Learner profile exists, format the API request url to update non-editable field of learner profile in request payload
        When API request is sent to update non-editable field of the learner profile in request payload
          Then SLP Service will throw a validation error message while trying to update the learner profile as non-editable field was attempted to be updated

    Scenario: Unable to fetch learner profile when incorrect learner uuid is given
      Given that a Learner profile exists, format the API request url to fetch the learner profile by providing incorrect learner uuid in request payload
        When API request is sent to fetch learner profile with incorrect learner uuid in request payload
          Then SLP Service will throw an error message while trying to fetch the learner profile as incorrect learner uuid was provided

    Scenario: Unable to delete learner profile when incorrect learner uuid is given
      Given that a Learner profile exists, format the API request url to delete the learner profile by providing incorrect learner uuid in request payload
        When API request is sent to delete learner profile with incorrect learner uuid in request payload
          Then SLP Service will throw a validation error message while trying to delete learner profile as incorrect learner uuid was provided

    Scenario: Unable to create achievement when one or more required fields is missing
      Given that a Learner account exists, format the API request url to create an achievement with one or more required fields missing in request payload
        When API request is sent to create achievement with one or more required fields missing in request payload
          Then SLP Service will throw a validation error message as one or more required fields are missing

    Scenario: Unable to update achievement when required field is missing
      Given that an Achievement exists, format the API request url to update the achievement with required field missing in request payload
        When API request is sent to update achievement with required field missing in request payload
          Then SLP Service will throw a validation error message as required field is missing

    Scenario: Unable to fetch achievement when incorrect uuid is given
      Given that an Achievement exists, format the API request url to fetch the achievement by providing incorrect uuid in request payload
        When API request is sent to fetch achievement with incorrect uuid in request payload
          Then SLP Service will throw an error message while trying to fetch achievement as incorrect uuid was provided

    Scenario: Unable to delete achievement when incorrect uuid is given
      Given that an Achievement exists, format the API request url to delete the achievement by providing incorrect uuid in request payload
        When API request is sent to delete achievement with incorrect uuid in request payload
          Then SLP Service will throw a validation error message while trying to delete achievement as incorrect uuid was provided

    Scenario: Unable to create goal when one or more required fields is missing
      Given format the API request url to create a goal with one or more required fields missing in request payload
        When API request is sent to create goal with one or more required fields missing in request payload
          Then SLP Service will throw a validation error message while creating the goal as one or more required fields are missing

    Scenario: Unable to update goal when invalid uuid is given
      Given that a goal exists, format the API request url to update the goal by providing invalid uuid in request payload
        When API request is sent to update goal by providing invalid uuid in request payload
          Then SLP Service will throw a validation error message while updating the goal as invalid uuid provided

    Scenario: Unable to fetch goal when incorrect uuid is given
      Given that a goal exists, format the API request url to fetch the goal by providing incorrect uuid in request payload
        When API request is sent to fetch goal with incorrect uuid in request payload
          Then SLP Service will throw an error message as incorrect uuid was provided

    Scenario: Unable to delete goal when incorrect uuid is given
      Given that a goal exists, format the API request url to delete the goal by providing incorrect uuid in request payload
        When API request is sent to delete goal with incorrect uuid in request payload
          Then SLP Service will throw a validation error message while trying to delete goal as incorrect uuid was provided