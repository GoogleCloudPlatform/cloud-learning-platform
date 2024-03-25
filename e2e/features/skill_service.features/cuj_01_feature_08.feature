@skill-service
Feature:  Ingest external (OSN) data, break out skills and organize them in skill graph

    @matching-engine
    Scenario: Map internal skills to external OSN skills with correct request payload 
        Given the OSN skill data set can be accessed
            When the OSN skill data set is uploaded into the skill graph
                Then that data should be ingested into the skill graph in csv format
                And mapped with internal skills using correct request payload

    Scenario: Map internal skills to external OSN skills with incorrect request payload during ingestion
        Given the OSN skill data set can be accessed by University
            When the OSN skill data set is uploaded into the skill graph with incorrect request payload
                Then the data ingestion into the skill graph should fail due to incorrect request payload

    Scenario: Map internal skills to external OSN skills with incorrect request payload during alignment
        Given University has access to OSN for API usage
            When the OSN skill data set is uploaded into the skill graph with correct payload
                Then that data should be ingested into the skill graph in csv format with correct request payload
                And mapped with internal skills should fail due to incorrect request payload