@skill-service @matching-engine
Feature: Matching engine operations

    Scenario: Fetch all indexes stored in matching engine when correct URL provided
        Given that there are indexes present in matching engine and user has access to fetch all indexes from matching engine
            When API to fetch all indexes is called by providing correct URL
                Then Matching Engine will retrieve and return all indexes stored in the matching engine
    
    Scenario: Fetch index stored in matching engine when corresponding to index ID is provided in URL
        Given that there are indexes present in matching engine and user has access to fetch index from matching engine
            When API to fetch index is called by providing an index id in the URL
                Then Matching Engine will retrieve and return the indexes stored in the matching engine corresponding to given index id
    
    Scenario: Unable to fetch index stored in matching engine when invalid index ID is given
        Given that there are indexes present in matching engine and user has privilege to fetch index from matching engine
            When API to fetch index is called by providing an invalid index id in the URL
                Then Matching Engine will throw an internal error as invalid index id was provided

    Scenario: Fetch all index endpoints stored in matching engine when correct URL provided
        Given that there are index endpoints present in matching engine and user has access to fetch all index endpoints from matching engine
            When API to fetch all index endpoints is called by providing correct URL
                Then Matching Engine will retrieve and return all index endpoints stored in the matching engine
    
    Scenario: Fetch index endpoint stored in matching engine when corresponding to index endpoint ID is provided in URL
        Given that there are index endpoints present in matching engine and user has access to fetch index endpoint from matching engine
            When API to fetch index endpoint is called by providing an index endpoint id in the URL
                Then Matching Engine will retrieve and return the index endpoint stored in the matching engine corresponding to given index endpoint id
    
    Scenario: Unable to fetch index endpoint stored in matching engine when invalid index endpoint ID is given
        Given that there are index endpoints present in matching engine and user has privilege to fetch index endpoint from matching engine
            When API to fetch index endpoint is called by providing an invalid index endpoint id in the URL
                Then Matching Engine will throw an internal error as invalid index endpoint id was provided

    Scenario: Fetch all nearest neighbors for given query stored in matching engine when correct request payload provided
        Given that nearest neighbors exist in matching engine and user has access to fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors from matching engine is called by providing correct request payload
                Then Matching Engine will retrieve and return all nearest neighbors stored in the matching engine corresponding to index_id and query_embeddings given in request payload

    Scenario: Unable to Fetch nearest neighbors stored in matching engine when invalid index id given
        Given that nearest neighbors exist in matching engine and user can fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors from matching engine is called by providing invalid index id
                Then Matching Engine will throw a validation error while trying to fetch neighbors as invalid index id was given

    Scenario: Unable to Fetch nearest neighbors stored in matching engine when invalid query_embeddings given
        Given that nearest neighbors exist in matching engine and user has privilege to fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors from matching engine is called by providing invalid query_embeddings
                Then Matching Engine will throw a validation error while trying to fetch neighbors as invalid query_embeddings was given

    Scenario: Unable to Fetch nearest neighbors stored in matching engine when index id is missing
        Given that nearest neighbors exist in matching engine and user can access functionality fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors from matching engine is called with missing index id
                Then Matching Engine will throw a validation error while trying to fetch neighbors as index id is missing

    Scenario: Unable to Fetch nearest neighbors stored in matching engine when query_embeddings is missing
        Given that nearest neighbors exist in matching engine and user has ability to fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors from matching engine is called with missing query_embeddings
                Then Matching Engine will throw a validation error while trying to fetch neighbors as query_embeddings is missing

    Scenario: Fetch nearest neighbors for all given queries stored in matching engine when correct request payload provided
        Given that nearest neighbors exist in matching engine and user has access to fetch nearest neighbors from matching engine by giving multiple queries
            When API to fetch nearest neighbors from matching engine is called by providing correct request payload with multiple queries at once
                Then Matching Engine will retrieve and return all nearest neighbors stored in the matching engine corresponding to all queries given in request payload

    Scenario: Unable to Fetch nearest neighbors stored in matching engine for multiple queries when invalid index id given
        Given that nearest neighbors exist in matching engine for multiple queries and user can fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors for multiple queries from matching engine is called by providing invalid index id
                Then Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as invalid index id was given

    Scenario: Unable to Fetch nearest neighbors stored in matching engine for multiple queries when invalid batch_query_embeddings given
        Given that nearest neighbors exist in matching engine for multiple queries and user has privilege to fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors for multiple queries from matching engine is called by providing invalid batch_query_embeddings
                Then Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as invalid batch_query_embeddings was given

    Scenario: Unable to Fetch nearest neighbors stored in matching engine for multiple queries when index id is missing
        Given that nearest neighbors exist in matching engine for multiple queries and user can access functionality fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors for multiple queries from matching engine is called with missing index id
                Then Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as index id is missing

    Scenario: Unable to Fetch nearest neighbors stored in matching engine for multiple queries when batch_query_embeddings is missing
        Given that nearest neighbors exist in matching engine for multiple queries and user has ability to fetch nearest neighbors from matching engine by giving query
            When API to fetch nearest neighbors for multiple queries from matching engine is called with missing batch_query_embeddings
                Then Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as batch_query_embeddings is missing