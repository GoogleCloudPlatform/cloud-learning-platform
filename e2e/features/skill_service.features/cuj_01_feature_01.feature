@skill-service
Feature: Ingest skill graph from Credential Engine via API, break out skills and organize them in skill graph.

    Scenario: Ingest data from Credential Engine with correct request payload
        Given Credential Engine has approved University for API usage
            When Skill service accesses Credential Engine to download records from their registry with correct request payload
                Then records should be ingested into skill service

    Scenario: Ingest data from Credential Engine with incorrect request payload
        Given University is approved by Credential Engine for API usage
            When Skill service accesses Credential Engine to download records from their registry with incorrect request payload
                Then Ingestion in skill service should fail

    Scenario: Ingest data from Credential Engine
        Given University has access to Credential Engine for API usage
            When Skill service accesses Credential Engine to download records from their registry and University server is not running
                Then Skill service ingestion should fail