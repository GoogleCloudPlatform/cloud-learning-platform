@skill-service
Feature: Create skills and concepts within skill graph and knowledge graph respectively
    
    Scenario: Create skills within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a skill
            When The node is created within the management interface with correct request payload
                Then That node will appear within the Skill Graph
    
    @matching-engine
    Scenario: Create and align skills within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create and align a skill
            When The node is created within the management interface with correct request payload and to be aligned
                Then That node will be created within the Skill Graph
                    And the skill node to be mapped accordingly
    
    Scenario: Create skills within skill graph from Skill Management with incorrect payload
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a skill with incorrect payload
            When The node is created within the management interface with incorrect request payload
                Then The user will get an error message for skill
    
    Scenario: Create Competencies within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a competency
            When The competency node is created within the management interface with correct request payload
                Then That competency node will appear within the Skill Graph and be mapped accordingly
    
    Scenario: Create Competencies within skill graph from Skill Management with incorrect payload
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a competency incorrect payload
            When The competency node is created within the management interface with incorrect request payload
                Then The user will get an error message for competency
    
    Scenario: Create Categories within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a category
            When The category node is created within the management interface with correct request payload
                Then That category node will appear within the Skill Graph and be mapped accordingly
    
    Scenario: Create Categories within skill graph from Skill Management with incorrect payload
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a category incorrect payload
            When The category node is created within the management interface with incorrect request payload
                Then The user will get an error message for category
    
    Scenario: Create Sub-domain within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a sub-domain
            When The Sub-domain node is created within the management interface with correct request payload
                Then That Sub-domain node will appear within the Skill Graph and be mapped accordingly
    
    Scenario: Create Sub-domain within skill graph from Skill Management with incorrect payload
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a Sub-domain incorrect payload
            When The Sub-domain node is created within the management interface with incorrect request payload
                Then The user will get an error message for Sub-domain
    
    Scenario: Create domain within skill graph from Skill Management
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a domain
            When The domain node is created within the management interface with correct request payload
                Then That domain node will appear within the Skill Graph and be mapped accordingly
    
    Scenario: Create domain within skill graph from Skill Management with incorrect payload
        Given A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a domain incorrect payload
            When The domain node is created within the management interface with incorrect request payload
                Then The user will get an error message for domain
    
    Scenario: Create concepts within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a concept
            When The concept node is created within the management interface with correct request payload
                Then That concept node will appear within the Knowledge Graph
    
    @matching-engine
    Scenario: Create and align concepts within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a concept
            When The concept node is created within the management interface with correct request payload and to be aligned
                Then That concept node will be created within the Knowledge Graph
                    And concept should be aligned
    
    Scenario: Create concepts within knowledge graph from Skill Management with incorrect payload
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a concept with incorrect payload
            When The concept node is created within the management interface with incorrect request payload
                Then The user will get an error message for concept
    
    Scenario: Create learning objectives within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning objective
            When The learning objective node is created within the management interface with correct request payload
                Then That learning objective node will appear within the Knowledge Graph

    @matching-engine
    Scenario: Create and align learning objectives within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a learning objective
            When The learning objective node is created within the management interface with correct request payload and to be aligned
                Then That learning objective node will be created within the Knowledge Graph
                    And That learning objective nodes is aligned correctly
    
    Scenario: Create learning objectives within knowledge graph from Skill Management with incorrect payload
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning objective with incorrect payload
            When The learning objective node is created within the management interface with incorrect request payload
                Then The user will get an error message for learning objective
    
    Scenario: Create learning resources within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning resource
            When The learning resource node will appear within the management interface with correct request payload
                Then That learning resource node will appear within the Knowledge Graph
    
    Scenario: Create learning resources within knowledge graph from Skill Management with incorrect payload
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning resource with incorrect payload
            When The learning resource node is created within the management interface with incorrect request payload
                Then The user will get an error message for learning resource
    
    Scenario: Create learning units within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning unit
            When The learning unit node is created within the management interface with correct request payload
                Then That learning unit node will appear within the Knowledge Graph
    
    @matching-engine
    Scenario: Create and align learning units within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align learning unit
            When The learning unit node is created within the management interface with correct request payload and to be aligned
                Then That learning unit node will ve created within the Knowledge Graph
                    And the learning unit node to be mapped accordingly
    
    Scenario: Create learning units within knowledge graph from Skill Management with incorrect payload
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning unit with incorrect payload
            When The learning unit node is created within the management interface with incorrect request payload
                Then The user will get an error message for learning unit
    
    Scenario: Create SubConcepts within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a SubConcept
            When The SubConcept node is created within the management interface with correct request payload
                Then That SubConcept node will appear within the Knowledge Graph

    @matching-engine
    Scenario: Create and align SubConcepts within knowledge graph from Skill Management
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a SubConcept
            When The SubConcept node is created within the management interface with correct request payload and to be aligned
                Then That SubConcept node will be created within the Knowledge Graph 
                    And the subconcept node will be mapped accordingly
    
    Scenario: Create SubConcepts within knowledge graph from Skill Management with incorrect payload
        Given A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a SubConcept with incorrect payload
            When The SubConcept node is created within the management interface with incorrect request payload
                Then The user will get an error message for SubConcept

