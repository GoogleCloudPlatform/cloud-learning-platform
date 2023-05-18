@content-serving-api
Feature: User should be able to fetch FAQ data

  Scenario: User wants to fetch a FAQ document with UUID
    Given that an LXE or CD wants to fetch a FAQ document with valid UUID
      When API request is sent to get the FAQ by UUID
        Then the service responds a success status
          And signed URL can be generated for this faq.

  Scenario: User wants to fetch all FAQ documents
    Given that an LXE or CD wants to fetch all the FAQ documents
      When API request is sent to get the FAQ list
        Then the service responds with a success status and list of all faqs

  Scenario: User wants to fetch a FAQ document with invalid FAQ uuid
    Given that an LXE or CD wants to fetch a FAQ document with invalid FAQ uuid
      When API request is sent to get the FAQ with invalid UUID
        Then the service responds with 404 status saying the FAQ does not exists

  Scenario: User wants to fetch FAQ documents for given curriculum_pathway_id
    Given that an LXE or CD wants to fetch FAQ documents for given curriculum_pathway_id
      When API request is sent to get the FAQ list by curriculum_pathway_id
        Then the service responds with a success status and list of faqs for the given curriculum_pathway_id

  Scenario: User wants to create FAQ documents
    Given that an LXE or CD wants to create FAQ documents
      When API request is sent to create the FAQ
        Then the service responds with a success status on creating FAQ

  Scenario: User wants to create FAQ documents with an invalid name
    Given that an LXE or CD wants to create FAQ documents with an invalid name
      When API request is sent to create the FAQ with an invalid name
        Then the service fails to create FAQ
  
  Scenario: User wants to recreate FAQ for a curriculum pathway
    Given that an LXE or CD wants to recreate a FAQ for a curriculum pathway
      When API request is sent to create the new FAQ with curriculum pathway uuid which is already used
        Then the service returns validation error saying FAQ for curriculum pathway already exists

  Scenario: User wants to update FAQ with correct payload
    Given that an LXE or CD wants to update a FAQ with correct payload
      When API request is sent to update the new FAQ with correct payload
        Then the FAQ is successfully updated with correct payload
  
  Scenario: User wants to update FAQ with incorrect payload
    Given that an LXE or CD wants to update a FAQ with incorrect payload
      When API request is sent to update the new FAQ with incorrect payload
        Then the service returns error saying FAQ with incorrect payload

  Scenario: User wants to delete FAQ with correct uuid
    Given that an LXE or CD wants to delete a FAQ with correct uuid
      When API request is sent to delete the new FAQ with correct uuid
        Then the FAQ is successfully deleted

  Scenario: User wants to upload a faq file/zip with sync api
    Given that an LXE or CD has access to the content authoring tool and wants to upload a faq file/zip with sync api
      When API request is sent to upload a faq file/zip with sync api
        Then LOS will return a json response with file and folder list of the uploaded faq file/zip