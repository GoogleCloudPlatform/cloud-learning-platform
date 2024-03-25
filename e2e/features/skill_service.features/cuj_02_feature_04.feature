@skill-service
Feature: Delete skills or concepts from skill graph or knowledge graph respectively

    Scenario: Successfully delete skill from skill-graph
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a skill.
            When the skill is deleted within the management interface with correct skill id.
                Then that skill will be deleted from the Skill graph and its subtree will also get deleted.

    Scenario: Unable to delete skill successfully 
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a skill
            When the skill is deleted within the management interface with incorrect skill id
                Then the Skill Service will throw an error message while trying to delete skill

    Scenario: Successfully delete Competency from skill-graph
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a competency.
            When the competency is deleted within the management interface with correct competency id.
                Then that competency will be deleted from the Skill graph and its subtree will also get deleted.

    Scenario: Unable to delete Competency successfully 
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a competency
            When the competency is deleted within the management interface with incorrect competency id
                Then the Skill Service will throw an error message while trying to delete competency

    Scenario: Successfully delete Category from skill-graph
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a category.
            When the category is deleted within the management interface with correct category id.
                Then that category will be deleted from the Skill graph and its subtree will also get deleted.

    Scenario: Unable to delete Category successfully
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a category
            When the category is deleted within the management interface with incorrect category id
                Then the Skill Service will throw an error message while trying to delete category

    Scenario: Successfully delete Domain from skill-graph
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a domain.
            When the domain is deleted within the management interface with correct domain id.
                Then that domain will be deleted from the Skill graph and its subtree will also get deleted.

    Scenario: Unable to delete Domain successfully
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a domain
            When the domain is deleted within the management interface with incorrect domain id
                Then the Skill Service will throw an error message while trying to delete domain

    Scenario: Successfully delete Sub-Domain from skill-graph
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a sub_domain.
            When the sub_domain is deleted within the management interface with correct sub_domain id.
                Then that sub_domain will be deleted from the Skill graph and its subtree will also get deleted.

    Scenario: Unable to delete Sub-Domain successfully
        Given that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a sub_domain
            When the sub_domain is deleted within the management interface with incorrect sub_domain id
                Then the Skill Service will throw an error message while trying to delete sub-domain



    Scenario: Successfully delete concept from knowledge-graph
        Given that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a concept.
            When the concept is deleted within the management interface with correct concept id.
                Then that concept will be deleted from the knowledge graph and its subtree will also get deleted.

    Scenario: Unable to delete concept successfully 
        Given that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a concept
            When the concept is deleted within the management interface with incorrect concept id
                Then the knowledge Service will throw an error message to the user while trying to delete concept

    Scenario: Successfully delete Sub-Concept from knowledge-graph
        Given that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a sub_concept.
            When the sub_concept is deleted within the management interface with correct sub_concept id.
                Then that sub_concept will be deleted from the knowledge graph and its subtree will also get deleted.

    Scenario: Unable to delete Sub-Concept successfully
        Given that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a sub_concept
            When the sub_concept is deleted within the management interface with incorrect sub_concept id
                Then the knowledge Service will throw an error message to the user while trying to delete sub-concept

    Scenario: Successfully delete Learning Objective from knowledge-graph
        Given that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_objective.
            When the learning_objective is deleted within the management interface with correct learning_objective id.
                Then that learning_objective will be deleted from the knowledge graph and its subtree will also get deleted.

    Scenario: Unable to delete Learning Objective successfully
        Given that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_objective
            When the learning_objective is deleted within the management interface with incorrect learning_objective id
                Then the knowledge Service will throw an error message to the user while trying to delete learning-objective

    Scenario: Successfully delete Learning Unit from knowledge-graph
        Given that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_unit.
            When the learning_unit is deleted within the management interface with correct learning_unit id.
                Then that learning_unit will be deleted from the knowledge graph and its subtree will also get deleted.

    Scenario: Unable to delete Learning Unit successfully
        Given that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_unit
            When the learning_unit is deleted within the management interface with incorrect learning_unit id
                Then the knowledge Service will throw an error message to the user while trying to delete learning-unit

    Scenario: Successfully delete Learning Resource from knowledge-graph
        Given that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_resource.
            When the learning_resource is deleted within the management interface with correct learning_resource id.
                Then that learning_resource will be deleted from the knowledge graph and its subtree will also get deleted.

    Scenario: Unable to delete Learning Resource successfully
        Given that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_resource
            When the learning_resource is deleted within the management interface with incorrect learning_resource id
                Then the knowledge Service will throw an error message to the user while trying to delete learning-resource