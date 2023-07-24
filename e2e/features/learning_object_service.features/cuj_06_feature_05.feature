@content-serving-api
Feature: User should be able to list content from GCS bucket

  Scenario: User wants to list content from GCS bucket
    Given that an LXE or CD has access to the content authoring tool and wants to list content from GCS bucket
      When API request is sent to list content from GCS bucket
        Then LOS will return a json response with file and folder list

  Scenario: User wants to list content from GCS bucket with no prefix
    Given that an LXE or CD has access to the content authoring tool and wants to list content from GCS bucket without a prefix
      When API request is sent to list content from GCS bucket without prefix
        Then LOS will return data present at the root of the bucket
