@content-serving-api
Feature: User should be able to upload valid madcap SRL zip against any Learning experience

  Scenario: User wants to be able to upload a valid madcap SRL zip against any Learning experience and it will be made available for all sibling LEs
    Given that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap SRL zip against any Learning experience
      When API request is sent to upload a valid madcap SRL zip against any Learning experience
        Then LOS will return a success response for the upload and all sibling LEs get access to it

  Scenario: User wants to upload a madcap zip with invalid SRL name against any Learning experience
    Given that an LXE or CD has access to the content authoring tool and wants to upload a madcap SRL zip with invalid SRL name against any Learning experience
      When API request is sent to upload a madcap SRL zip with invalid SRL name against any Learning experience
        Then LOS will return a failure response for the upload because the file name does not follow the SRL naming convention
  
  Scenario: User wants to be able to reupload a valid madcap SRL zip against any Learning experience and it will be made available for all sibling LEs and underlying LRs resource_paths will be updated
    Given that an LXE or CD has access to the content authoring tool and wants to reupload a valid madcap SRL zip against any Learning experience
      When API request is sent to reupload a valid madcap SRL zip against any Learning experience
        Then LOS will return a success response for the upload and all LE siblings srl_resource_path is updated
          And underlying LRs resource_path will be updated
  
  Scenario: User wants to reupload a madcap SRL zip against any Learning experience with missing files
    Given that an LXE or CD has access to the content authoring tool and wants to reupload a madcap SRL zip with missing files against any Learning experience
      When API request is sent to reupload a madcap SRL zip with missing files against any Learning experience
        Then LOS will return a validation error with list of missing files in new SRL zip
