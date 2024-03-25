@skill-service
Feature: Update skills and concepts within skill graph and knowledge graph respectively

    Scenario: Update Concept from Knowledge Graph with correct request payload
        Given that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a concept
            When the concept is updated within the management interface with correct request payload
                Then that concept should be updated within the knowledge graph successfully 

    @matching-engine
    Scenario: Update Concept from Knowledge Graph and recompute the alignments
        Given that a user has access to Knowledge Service and needs to update a concept
            When that concept is updated within the management interface with correct request payload
                Then that concept should be updated successfully
                And the concept alignments should be recalculated successfully
    
    Scenario: Update Concept from Knowledge Graph with incorrect request payload
        Given a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a concept
            When the concept is updated within the management interface with incorrect request payload
                Then concept update process should fail
    
    Scenario: Update SubConcept from Knowledge Graph with correct request payload
        Given that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a subconcept
            When the subconcept is updated within the management interface with correct request payload
                Then that subconcept should be updated within the knowledge graph successfully

    @matching-engine
    Scenario: Update SubConcept from Knowledge Graph and recompute the alignments
        Given that a user has access to Knowledge Service and needs to update a subconcept
            When that subconcept is updated within the management interface with correct request payload
                Then that subconcept should be updated successfully
                And its alignments should be recalculated successfully
    
    Scenario: Update SubConcept from Knowledge Graph with incorrect request payload
        Given a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a subconcept
            When the subconcept is updated within the management interface with incorrect request payload
                Then subconcept update process should fail

    Scenario: Update Learning Objective from Knowledge Graph with correct request payload
        Given that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning objective
            When the learning objective is updated within the management interface with correct request payload
                Then that learning objective should be updated within the knowledge graph successfully 

    @matching-engine
    Scenario: Update Learning Objective from Knowledge Graph and recompute the alignments
        Given that a user has access to Knowledge Service and needs to update a learning objective
            When the learning objective is updated with correct request payload
                Then that learning objective should be updated successfully 
                And learning objective alignments should be recalculated successfully
    
    Scenario: Update Learning Objective from Knowledge Graph with incorrect request payload
        Given a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning objective
            When the learning objective is updated within the management interface with incorrect request payload
                Then learning objective update process should fail
    
    Scenario: Update Learning Unit from Knowledge Graph with correct request payload
        Given that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning unit
            When the learning unit is updated within the management interface with correct request payload
                Then that learning unit should be updated within the knowledge graph successfully

    @matching-engine
    Scenario: Update Learning Unit from Knowledge Graph and recompute the alignments
        Given that a user has access to Knowledge Service and needs to update a learning unit
            When the learning unit is updated with correct request payload
                Then that learning unit should be updated successfully
                And learning unit alignments should be recalculated successfully
    
    Scenario: Update Learning Unit from Knowledge Graph with incorrect request payload
        Given a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning unit
            When the learning unit is updated within the management interface with incorrect request payload
                Then learning unit update process should fail

    Scenario: Update Domain from Skill Graph with correct request payload
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a domain
            When the domain is updated within the management interface with correct request payload
                Then that domain should be updated within the skill graph successfully

    Scenario: Update Domain from Skill Graph with incorrect request payload
        Given that a user has access to Skill Service and needs to update a domain
            When the domain is updated within the management interface with incorrect request payload
                Then domain update process should fail
    
    Scenario: Update SubDomain from Skill Graph with correct request payload
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a subdomain
            When the subdomain is updated within the management interface with correct request payload
                Then that subdomain should be updated within the skill graph successfully
    
    Scenario: Update SubDomain from Skill Graph with incorrect request payload
        Given that a user has access to Skill Service and needs to update a subdomain
            When the subdomain is updated within the management interface with incorrect request payload
                Then subdomain update process should fail

    Scenario: Update Category from Skill Graph with correct request payload
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a category
            When the category is updated within the management interface with correct request payload
                Then that category should be updated within the skill graph successfully

    Scenario: Update Category from Skill Graph with incorrect request payload
        Given that a user has access to Skill Service and needs to update a category
            When the category is updated within the management interface with incorrect request payload
                Then category update process should fail

    Scenario: Update Competency from Skill Graph with correct request payload
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a competency
            When the competency is updated within the management interface with correct request payload
                Then that competency should be updated within the skill graph successfully
    
    Scenario: Update Competency from Skill Graph with incorrect request payload
        Given that a user has access to Skill Service and needs to update a competency
            When the competency is updated within the management interface with incorrect request payload
                Then competency update process should fail
    
    Scenario: Update Skill from Skill Graph with correct request payload
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a skill
            When the skill is updated within the management interface with correct request payload
                Then that skill should be updated within the skill graph successfully

    @matching-engine
    Scenario: Update Skill from Skill Graph and recompute the alignments
        Given that a user has access to Skill Service and needs to update a skill
            When that skill is updated with correct request payload
                Then that skill should be updated successfully
                And skill alignments should be recalculated successfully
    
    Scenario: Update Skill from Skill Graph with incorrect request payload
        Given a user has access to Skill Service (via Competencies & Skill Management) and needs to update a skill
            When the skill is updated within the management interface with incorrect request payload
                Then skill update process should fail