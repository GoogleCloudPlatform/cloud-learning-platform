@skill-service
Feature:  Ingest skills from Burning Glass via API, break out skills and organize them into skill graph

    Scenario: Ingest data from EMSI Burning Glass with correct request payload
        Given Burning Glass has approved University for API usage 
            When Skill service accesses Burning Glass to download records from their registry with correct request payload
                Then records from EMSI should be ingested into skill service

    Scenario: Ingest data from EMSI Burning Glass with incorrect request payload
        Given University is approved by Burning Glass for API usage
            When Skill service accesses Burning Glass to download records from their registry with incorrect request payload
                Then Ingestion from EMSI in skill service should fail

    Scenario: Ingest data from EMSI Burning Glass
        Given University has access to Burning Glass for API usage
            When Skill service accesses Burning Glass to download records from their registry and University server is not running
                Then Skill service ingestion from EMSI should fail 