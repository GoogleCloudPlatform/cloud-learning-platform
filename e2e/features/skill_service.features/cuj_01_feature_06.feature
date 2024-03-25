@skill-service
Feature: Upload a textbook into the knowledge graph and create concepts from the data and organize them in knowledge graph
    
    Scenario: Ingest textbook in pdf format with correct request payload, into the knowledge graph
        Given Textbooks can be accessed in a digital format
            When A textbook is uploaded into the knowledge graph in pdf format with correct payload request
                Then That data should be ingested into the knowledge graph
    
    Scenario: Ingest textbook in pdf format with incorrect format in request payload, into the knowledge graph
        Given Textbooks is accessible in a digital format
            When A textbook is uploaded into the knowledge graph in pdf format with incorrect format value
                Then The data ingestion into the knowledge graph should fail with unsupported format
    
    Scenario: Ingest textbook in pdf format with incorrect GCS path in request payload, into the knowledge graph
        Given Textbooks can be accessed in a pdf format
            When A textbook is uploaded into the knowledge graph in pdf format with invalid GCS path
                Then The data ingestion into the knowledge graph should fail with invalid GCS path

    Scenario: Ingest textbook in pdf format with incorrect page number in request payload, into the knowledge graph
        Given We can access to textbooks in a pdf format
            When A textbook is uploaded into the knowledge graph in pdf format with invalid start or end page
                Then The data ingestion into the knowledge graph should fail with invalid start or end page
