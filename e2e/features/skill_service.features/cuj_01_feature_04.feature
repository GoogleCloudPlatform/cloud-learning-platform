@skill-service
Feature: Ingest data from non-API Sources, break out skills and organize them in skill graph

    Scenario: Ingest skill data from a gcs csv file with correct request payload
        Given We have access to raw data in csv format available on a gcs bucket
            When Skill service accesses this gcs csv data with correct payload request
                Then That gcs csv data should be ingested into skill service

    Scenario: Ingest skill data from a csv file with incorrect request payload
        Given We have access to raw data of csv type available on a gcs bucket
            When Skill service accesses this gcs csv data with incorrect payload request
                Then Gcs csv ingestion into skill service should fail

    Scenario: Ingest skill data from a csv file with incorrect request payload (without a file or GCS URI)
        Given We have access to raw data (csv file) available on a gcs bucket
            When Skill service accesses this gcs csv data with incorrect payload request (without a file or GCS URI)
                Then Gcs csv ingestion into skill service should fail due to incorrect payload request (without a file or GCS URI)

    Scenario: Ingest skill data from a csv file with incorrect request payload (with both file & GCS URI)
        Given We have access to a csv file available on a gcs bucket
            When Skill service accesses this gcs csv data with incorrect payload request (with both file & GCS URI)
                Then Gcs csv ingestion into skill service should fail due to incorrect payload request (with both file & GCS URI)

    Scenario: Ingest skill data from a CSV file URI with missing fields
        Given We have access to raw data for skill in a csv file with missing fields available on a gcs bucket
            When Skill service accesses this csv file with skill data from gcs with missing fields
                Then Gcs csv ingestion into skill service should fail as csv skill data has missing fields

    Scenario: Ingest competency data from a CSV file URI with missing fields
        Given We have access to raw data for competency in a csv file with missing fields available on a gcs bucket
            When Skill service accesses this csv file with competency data from gcs with missing fields
                Then Gcs csv ingestion into skill service should fail as csv competency data has missing fields

    Scenario: Ingest category data from a CSV file URI with missing fields
        Given We have access to raw data for category in a csv file with missing fields available on a gcs bucket
            When Skill service accesses this csv file with category data from gcs with missing fields
                Then Gcs csv ingestion into skill service should fail as csv category data has missing fields

    Scenario: Ingest sub-domain data from a CSV file URI with missing fields
        Given We have access to raw data for sub-domain in a csv file with missing fields available on a gcs bucket
            When Skill service accesses this csv file with sub-domain data from gcs with missing fields
                Then Gcs csv ingestion into skill service should fail as csv sub-domain data has missing fields

    Scenario: Ingest domain data from a CSV file URI with missing fields
        Given We have access to raw data for domain in a csv file with missing fields available on a gcs bucket
            When Skill service accesses this csv file with domain data from gcs with missing fields
                Then Gcs csv ingestion into skill service should fail as csv domain data has missing fields

    Scenario: Ingest skill data from a local csv file with correct request payload
        Given We have access to raw data in csv format available on our local system
            When Skill service accesses this local csv data with correct payload request
                Then That local csv data should be ingested into skill service

    Scenario: Ingest skill data from a local csv file with invalid/wrong extension
        Given We have access to raw data (non-csv format) available on our local system
            When Skill service accesses this local csv data with invalid/wrong extension
                Then local csv ingestion into skill service should fail due to csv data with invalid/wrong extension

    Scenario: Ingest skill data from a local csv file with missing fields
        Given We have access to raw skill data in csv format available on our local system
            When Skill service accesses this local csv skill data with missing fields
                Then local csv ingestion into skill service should fail due to skill data missing some fields

    Scenario: Ingest competency data from a local csv file with missing fields
        Given We have access to raw competency data in csv format available on our local system
            When Skill service accesses this local csv competency data with missing fields
                Then local csv ingestion into skill service should fail due to competency data missing some fields

    Scenario: Ingest category data from a local csv file with missing fields
        Given We have access to raw category data in csv format available on our local system
            When Skill service accesses this local csv category data with missing fields
                Then local csv ingestion into skill service should fail due to category data missing some fields

    Scenario: Ingest sub-domain data from a local csv file with missing fields
        Given We have access to raw sub-domain data in csv format available on our local system
            When Skill service accesses this local csv sub-domain data with missing fields
                Then local csv ingestion into skill service should fail due to sub-domain data missing some fields

    Scenario: Ingest domain data from a local csv file with missing fields
        Given We have access to raw domain data in csv format available on our local system
            When Skill service accesses this local csv domain data with missing fields
                Then local csv ingestion into skill service should fail due to domain data missing some fields

    Scenario: Ingest skill data from a json file with correct request payload
        Given We have access to raw data in json format for skill
            When Skill service accesses this skill json data with correct payload request
                Then That skill json data should be ingested into skill service

    Scenario: Ingest skill data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for skill
            When Skill service accesses this skill json data with invalid json schema
                Then Ingestion of that skill json data with invalid json schema into skill service should fail

    Scenario: Ingest skill data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for skill
            When Skill service accesses this skill csv data instead of the JSON
                Then ingestion of that skill data from csv file into skill service should fail

    Scenario: Ingest competency data from a json file with correct request payload
        Given We have access to raw data in json format for competency
            When Skill service accesses this competency json data with correct payload request
                Then That competency json data should be ingested into skill service

    Scenario: Ingest competency data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for competency
            When Skill service accesses this competency json data with invalid json schema
                Then Ingestion of that competency json data with invalid json schema into skill service should fail

    Scenario: Ingest competency data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for competency
            When Skill service accesses this competency csv data instead of the JSON
                Then ingestion of that competency data from csv file into skill service should fail

    Scenario: Ingest category data from a json file with correct request payload
        Given We have access to raw data in json format for category
            When Skill service accesses this category json data with correct payload request
                Then That category json data should be ingested into skill service

    Scenario: Ingest category data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for category
            When Skill service accesses this category json data with invalid json schema
                Then Ingestion of that category json data with invalid json schema into skill service should fail

    Scenario: Ingest category data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for category
            When Skill service accesses this category csv data instead of the JSON
                Then Ingestion of that category data from csv file into skill service should fail

    Scenario: Ingest sub-domain data from a json file with correct request payload
        Given We have access to raw data in json format for sub-domain
            When Skill service accesses this sub-domain json data with correct payload request
                Then That sub-domain json data should be ingested into skill service

    Scenario: Ingest sub-domain data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for sub-domain
            When Skill service accesses this sub-domain json data with invalid json schema
                Then Ingestion of that sub-domain json data with invalid json schema into skill service should fail

    Scenario: Ingest sub-domain data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for sub-domain
            When Skill service accesses this sub-domain csv data instead of the JSON
                Then Ingestion of that sub-domain data from csv file into skill service should fail

    Scenario: Ingest domain data from a json file with correct request payload
        Given We have access to raw data in json format for domain
            When Skill service accesses this domain json data with correct payload request
                Then That domain json data should be ingested into skill service

    Scenario: Ingest domain data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for domain
            When Skill service accesses this domain json data with invalid json schema
                Then Ingestion of that domain json data with invalid json schema into skill service should fail

    Scenario: Ingest domain data from a CSV file as input instead of a JSON file
        Given We have access to raw data of csv type for domain
            When Skill service accesses this domain csv data instead of the JSON
                Then Ingestion of that domain data from csv file into skill service should fail
