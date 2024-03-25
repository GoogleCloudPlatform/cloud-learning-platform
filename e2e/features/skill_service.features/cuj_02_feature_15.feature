@skill-service
Feature: Fetch child nodes

    Scenario: Fetch all child skills of list of valid competencies
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch all the child skills of a list of valid competencies
            When there is a request to fetch all the child skills of a list of valid competencies
                Then Skill Service will return all the child skill nodes associated to their respective competencies

    Scenario: Fetch all child skills of list of invalid competencies
        Given that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch all the child skills of a list of invalid competencies
            When there is a request to fetch all the child skills of a list of invalid competencies
                Then Skill Service will throw an error message for invalid competency
