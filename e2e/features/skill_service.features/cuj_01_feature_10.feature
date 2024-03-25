@skill-service
Feature: Create Learning Units from Learning Objectives in Knowledge Graph

    Scenario: Create Learning Units from Learning Objectives by triggering a batch job when correct request payload provided
        Given User has access to create LUs from LOs via Competency Management and LO from which LUs are to be created exists
            When API to create Learning Units from Learning Objectives is called by providing correct request payload
                Then Knowledge Service will trigger a batch job to create Learning Units from given Learning Objectives successfully
    
    Scenario: Unable to create Learning Units from Learning Objectives by triggering a batch job when incorrect LO ID is provided
        Given User has privilege to create Learning Units from Learning Objectives via Competency Management
            When API to create Learning Units from Learning Objectives is called by providing incorrect LO ID in request payload
                Then Knowledge Service will throw ResourceNotFoundException for the invalid Learning Objective
