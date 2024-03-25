@skill-service
Feature: Import Node Level Objects of Knowledge Graph from json files

    Scenario: Ingest Learning Resource data from a json file with correct request payload
        Given We have access to raw data in json format for Learning Resource
            When Skill service accesses this Learning Resource json data with correct payload request
                Then That Learning Resource json data should be ingested into skill service

    Scenario: Ingest Learning Resource data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for Learning Resource
            When Skill service accesses this Learning Resource csv data instead of the JSON
                Then ingestion of that Learning Resource data from csv file into skill service should fail


    Scenario: Ingest concept data from a json file with correct request payload
        Given We have access to raw data in json format for concept
            When Skill service accesses this concept json data with correct payload request
                Then That concept json data should be ingested into skill service

    Scenario: Ingest concept data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for concept
            When Skill service accesses this concept csv data instead of the JSON
                Then ingestion of that concept data from csv file into skill service should fail


    Scenario: Ingest sub-concept data from a json file with correct request payload
        Given We have access to raw data in json format for sub-concept
            When Skill service accesses this sub-concept json data with correct payload request
                Then That sub-concept json data should be ingested into skill service

    Scenario: Ingest sub-concept data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for sub-concept
            When Skill service accesses this sub-concept csv data instead of the JSON
                Then Ingestion of that sub-concept data from csv file into skill service should fail


    Scenario: Ingest learning objective data from a json file with correct request payload
        Given We have access to raw data in json format for learning objective
            When Skill service accesses this learning objective json data with correct payload request
                Then That learning objective json data should be ingested into skill service

    Scenario: Ingest learning objective data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for learning objective
            When Skill service accesses this learning objective csv data instead of the JSON
                Then Ingestion of that learning objective data from csv file into skill service should fail


    Scenario: Ingest learning unit data from a json file with correct request payload
        Given We have access to raw data in json format for learning unit
            When Skill service accesses this learning unit json data with correct payload request
                Then That learning unit json data should be ingested into skill service

    Scenario: Ingest learning unit data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for learning unit
            When Skill service accesses this learning unit csv data instead of the JSON
                Then Ingestion of that learning unit data from csv file into skill service should fail
