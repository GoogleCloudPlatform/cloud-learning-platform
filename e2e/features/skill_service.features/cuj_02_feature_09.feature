@skill-service
Feature: Manage data sources

  Scenario: Successfully create a new data source
    Given Format the API request url to insert data source using object type and source
      When API request is sent to upsert the new data source using object type and source
        Then Skill Service will create a new document for given object type and source

  Scenario: Successfully update already created data source with new given source
    Given Format the API request url to add a new data source for already existing object type
      When API request is sent to upsert the new data source for already existing object type
        Then Skill Service will add the new data source to already existing document for given object type

  Scenario: Unable to insert/update due to missing source
    Given Format the API request url to update the object type with no source
      When API request is sent to upsert data sources
        Then Skill Service will throw an error message while trying to upsert the data source document

  Scenario: Successfully fetch data sources for given object type
    Given Format the API request url to fetch all data sources for given object type
      When API request is sent to fetch data sources for given object type
        Then Skill Service will return data sources for given object type

  Scenario: Successfully fetch data sources for all object types
    Given Format the API request url to fetch data sources for all object types
      When API request is sent to fetch data sources for all object types
        Then Skill Service will return data sources for all object type

  Scenario: Unable to fetch data sources due to incorrect query parameter given
    Given Format the API request url to fetch data sources for incorrect object type
      When API request is sent to fetch data sources for incorrect object type
        Then Skill Service will throw an error message while trying to fetch the data sources

  Scenario: Successfully update already existing data source with given matching engine id
    Given Format the API request url to update given matching engine id for given data source and object type
      When API request is sent to update matching engine id in corresponding data source
        Then Skill Service will update the given matching engine ID in corresponding data source

  Scenario: Unable to update already existing data source as no matching engine id provided
    Given Format the API request url to update the data source without providing matching engine ID
      When API request is sent to try updating matching engine id in corresponding data source
        Then Skill Service will throw an error message while trying to update the data source
