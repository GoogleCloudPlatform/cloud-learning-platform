Feature: Import achievement and learner account data from json files

    Scenario: Import learner data from a valid json file with all required fields
        Given We have access to learner data in json format with all required fields
            When SLP service accesses this learner data from given json file with all required fields
                Then learner data from given json file should get ingested into SLP service

    Scenario: Unable to import learner data from a CSV file instead of a JSON file
        Given We have access to learner data in csv format
            When SLP service accesses this learner data in csv formart instead of JSON format
                Then SLP service will throw a validation error and learner data will not get imported

    Scenario: Import learner data from a json file with invalid format
        Given We have access to learner data in json format with invalid format
            When SLP service accesses this learner data from given json file with invalid format
                Then SLP service will throw a validation error due to invalid format of the json file and learner data will not get imported

    Scenario: Import learner data from a json file with missing fields
        Given We have access to learner data in json format with missing fields
            When SLP service accesses this learner data from given json file with missing fields
                Then SLP service will throw a validation error and learner data will not get imported as some required fields are missing

    Scenario: Import achievement data from a valid json file with all required fields
        Given We have access to achievement data in json format with all required fields
            When SLP service accesses this achievement data from given json file with all required fields
                Then achievement data from given json file should get ingested into SLP service

    Scenario: Unable to import achievement data from a CSV file instead of a JSON file
        Given We have access to achievement data in csv format
            When SLP service accesses this achievement data in csv formart instead of JSON format
                Then SLP service will throw a validation error and achievement data will not get imported

    Scenario: Import achievement data from a json file with invalid format
        Given We have access to achievement data in json format with invalid format
            When SLP service accesses this achievement data from given json file with invalid format
                Then SLP service will throw a validation error due to invalid format of the json file and achievement data will not get imported

    Scenario: Import achievement data from a json file with missing fields
        Given We have access to achievement data in json format with missing fields
            When SLP service accesses this achievement data from given json file with missing fields
                Then SLP service will throw a validation error and achievement data will not get imported as some required fields are missing