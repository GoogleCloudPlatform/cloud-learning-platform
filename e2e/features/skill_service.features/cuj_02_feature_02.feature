@skill-service
Feature: Read skills and concepts within skill graph and knowledge graph respectively

    Scenario: Read a particular skill from the Skill Graph using correct skill id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the skill
            When there is a request to view a particular skill node in the skill graph with correct id
                Then Skill Service will serve up the requested skill

    Scenario: Read a particular skill and fetch tree of related skill graph nodes using correct skill id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the skill graph
            When there is a request to view a particular skill node and fetch skill graph tree with correct id
                Then Skill Service will serve up the requested skill along with tree of related nodes

    Scenario: Read a particular skill from the Skill Graph using incorrect skill id
        Given that a user can access Skill Service (via Competencies & Skill Management) and needs to view the skill
            When there is a request to view a particular skill node in the skill graph with incorrect id
                Then Skill Service will throw an error message for accessing invalid skill
    
    Scenario: Read a particular competency from the Skill Graph using correct competency id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the competency
            When there is a request to view a particular competency node in the skill graph with correct id
                Then Skill Service will serve up the requested competency

    Scenario: Read a particular competency and fetch tree of related skill graph nodes using correct competency id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch skill graph tree
            When there is a request to view a particular competency node and fetch skill graph tree related to correct competency id
                Then Skill Service will serve up the requested competency along with tree of related nodes

    Scenario: Read a particular competency from the Skill Graph using incorrect competency id
        Given that a user can access Skill Service (via Competencies & Skill Management) and needs to view the competency
            When there is a request to view a particular competency node in the skill graph with incorrect id
                Then Skill Service will throw an error message for accessing invalid competency
    
    Scenario: Read a particular category from the Skill Graph using correct category id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the category
            When there is a request to view a particular category node in the skill graph with correct id
                Then Skill Service will serve up the requested category

    Scenario: Read a particular category and fetch tree of related skill graph nodes using correct category id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view skill graph tree
            When there is a request to view a particular category node and fetch skill graph tree related to correct category id
                Then Skill Service will serve up the requested category along with tree of related nodes

    Scenario: Read a particular category from the Skill Graph using incorrect category id
        Given that a user can access Skill Service (via Competencies & Skill Management) and needs to view the category
            When there is a request to view a particular category node in the skill graph with incorrect id
                Then Skill Service will throw an error message for accessing invalid category

    Scenario: Read a particular sub-domain from the Skill Graph using correct sub-domain id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the sub-domain
            When there is a request to view a particular sub-domain node in the skill graph with correct id
                Then Skill Service will serve up the requested sub-domain

    Scenario: Read a particular sub-domain and fetch tree of related skill graph nodes using correct sub-domain id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to see skill graph tree
            When there is a request to view a particular sub-domain node and fetch skill graph tree related to correct sub-domain id
                Then Skill Service will serve up the requested sub-domain along with tree of related nodes

    Scenario: Read a particular sub-domain from the Skill Graph using incorrect sub-domain id
        Given that a user can access Skill Service (via Competencies & Skill Management) and needs to view the sub-domain
            When there is a request to view a particular sub-domain node in the skill graph with incorrect id
                Then Skill Service will throw an error message for accessing invalid sub-domain
    
    Scenario: Read a particular domain from the Skill Graph using correct domain id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the domain
            When there is a request to view a particular domain node in the skill graph with correct id
                Then Skill Service will serve up the requested domain

    Scenario: Read a particular domain and fetch tree of related skill graph nodes using correct domain id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs the skill graph tree
            When there is a request to view a particular domain node and fetch skill graph tree related to correct domain id
                Then Skill Service will serve up the requested domain along with tree of related nodes

    Scenario: Read a particular domain from the Skill Graph using incorrect domain id
        Given that a user can access Skill Service (via Competencies & Skill Management) and needs to view the domain
            When there is a request to view a particular domain node in the skill graph with incorrect id
                Then Skill Service will throw an error message for accessing invalid domain
    
    Scenario: Read a particular concept from the Knowlegde Graph using correct concept id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the concept
            When there is a request to view a particular concept node in the knowledge graph with correct concept id
                Then Skill Service will serve up the requested concept
    
    Scenario: Read a particular concept from the Knowledge Graph using incorrect concept id
        Given that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the concept
            When there is a request to view a particular concept node in the knowledge graph with incorrect concept id
                Then Skill Service will throw an error message for accessing invalid concept
    
    Scenario: Read a particular sub-concept from the Knowledge Graph using correct sub-concept id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the sub-concept
            When there is a request to view a particular sub-concept node in the knowledge graph with correct sub-concept id
                Then Skill Service will serve up the requested sub-concept
    
    Scenario: Read a particular sub-concept from the Knowledge Graph using incorrect sub-concept id
        Given that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the sub-concept
            When there is a request to view a particular sub-concept node in the knowledge graph with incorrect sub-concept id
                Then Skill Service will throw an error message for accessing invalid sub-concept
    
    Scenario: Read a particular learning-objective from the Knowledge Graph using correct learning-objective id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-objective
            When there is a request to view a particular learning-objective node in the knowledge graph with correct learning-objective id
                Then Skill Service will serve up the requested learning-objective
    
    Scenario: Read a particular learning-objective from the Knowledge Graph using incorrect learning-objective id
        Given that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-objective
            When there is a request to view a particular learning-objective node in the knowledge graph with incorrect learning-objective id
                Then Skill Service will throw an error message for accessing invalid learning-objective

    Scenario: Read a particular learning-unit from the Knowledge Graph using correct learning-unit id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-unit
            When there is a request to view a particular learning-unit node in the knowledge graph with correct learning-unit id
                Then Skill Service will serve up the requested learning-unit

    Scenario: Read a particular learning-unit from the Knowledge Graph using incorrect learning-unit id
        Given that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-unit
            When there is a request to view a particular learning-unit node in the knowledge graph with incorrect learning-unit id
                Then Skill Service will throw an error message for accessing invalid learning-unit

    Scenario: Read a particular learning-resource from the Knowledge Graph using correct learning-resource id
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-resource
            When there is a request to view a particular learning-resource node in the knowledge graph with correct learning-resource id
                Then Skill Service will serve up the requested learning-resource

    Scenario: Read a particular learning-resource from the Knowledge Graph using incorrect learning-resource id
        Given that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-resource
            When there is a request to view a particular learning-resource node in the knowledge graph with incorrect learning-resource id
                Then Skill Service will throw an error message for accessing invalid learning-resource
