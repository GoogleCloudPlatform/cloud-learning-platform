@content-serving-api
Feature: User should be able to upload a valid madcap export at learning experience level

  Scenario: User wants to upload a valid madcap export at learning experience level
    Given that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap export at learning experience level
      When API request is sent to upload a valid madcap export at learning experience level
        Then LOS will return a json response with file and folder list of the uploaded madcap zip

  Scenario: User wants to upload an invalid madcap export at learning experience level
    Given that an LXE or CD has access to the content authoring tool and wants to upload an invalid madcap export at learning experience level
      When API request is sent to upload an invalid madcap export at learning experience level
        Then LOS will return a validation error for invalid madcap export upload
  
  Scenario: User wants to reupload a valid and identical madcap export at learning experience level
    Given that an LXE or CD has access to the content authoring tool and wants to reupload a valid and identical madcap export at learning experience level
      When API request is sent to reupload a valid and identical madcap export at learning experience level
        Then LOS will return a json response with file and folder list of the reuploaded and identical zip
  
  Scenario: User wants to reupload a valid but non-identical madcap export at learning experience level
    Given that an LXE or CD has access to the content authoring tool and wants to reupload a valid but non-identical madcap export at learning experience level
      When API request is sent to reupload a valid but non-identical madcap export at learning experience level
        Then LOS will return a validation error for the missing htm files in the reuploaded zip
  
  Scenario: User wants to upload a valid madcap export against invalid learning experience
    Given that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap export against invalid learning experience
      When API request is sent to upload a valid madcap export against invalid learning experience
        Then LOS will return a validation error for the invalid learning experience
  