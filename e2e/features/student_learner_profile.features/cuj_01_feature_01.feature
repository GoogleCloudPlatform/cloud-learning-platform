Feature: Learner can track current employer information in student learner profile

    Scenario: Learner can view Employer information
        Given A learner is employed by a sponsoring employer partner
            When The Learner Account is created
                Then the employer information (name, address, and contact info) is ingested into the SLP from the admin Salesforce record of the learner account
                And made visible to the learner through the learner-facing profile interface.

    Scenario: Learner cannot view Employer information
	    Given A learner is not employed by a sponsoring employer partner
	        When The Learner Account is added
	            Then the employer information (name, address, and contact info) is not ingested into the SLP from the admin Salesforce record of the learner account
	            And Employer information is not visible to the learner through the learner-facing profile interface.