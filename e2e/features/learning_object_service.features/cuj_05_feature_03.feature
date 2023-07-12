Feature: Integration with 3rd Party Tool | Frost (Clone Functionality for Curriculum Pathway)

    Scenario: Clone a curriculum pathway using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to copy a curriculum pathway
            When there is a request to copy a particular curriculum pathway with correct id
                Then a copy of the requested curriculum pathway will be returned
    
    Scenario: Clone a curriculum pathway using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to copy a curriculum pathway
            When there is a request to copy a particular curriculum pathway with incorrect id
                Then Learning Object Service will fail to copy the curriculum pathway due to invalid curriculum pathway id