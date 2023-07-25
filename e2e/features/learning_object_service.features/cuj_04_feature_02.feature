Feature: Establishing a relationship between the learning object and learning resource
	
	Scenario: LXE/CD wants to associate the learning resource with the learning object
    	Given that LXE or CD has access of the content authoring tool
       		When they design the learning object and the learning resource using a third-party tool
         		Then the learning object and the learning resource will be created in a third-party tool
           			And the learning resource gets associated with the learning object

  	Scenario: LXE/CD adds the incorrect reference of the given learning object in the learning resource
     	Given that an LXE or CD wants to create a learning resource providing the reference of the given learning object
       		When they design the learning resource using a third-party tool
        		Then the user will get an error message of not found the reference to the learning object

   	Scenario: LXE/CD wants to associate a single learning resource with multiple learning object
    	Given that an LXE or CD wants to add the reference of learning object in the learning resource
       		When they design the multiple learning object and the single learning resource using a third-party tool
         		Then the multiple learning object and the learning resource will be created in a third-party tool
           			And the learning resource gets associated with the multiple learning object

   	Scenario: LXE/CD wants to associate the multiple learning resource with the given learning object
     	Given that an LXE or CD wants to add the reference of a single learning object in the multiple learning resource
       		When they design the multiple learning resource using a third-party tool
         		Then the learning object will be created in a third-party tool
           			And all the learning resource gets associated with the given learning object

   	Scenario: LXE/CD wants to update the reference of the learning resource with the new learning object
     	Given that an LXE or CD wants to replace an old reference of the learning object with a new reference in the learning resource
       		When they update the new learning object using a third-party tool
		        Then the learning resource gets associated with the new learning object
   
   	Scenario: LXE/CD updating the incorrect reference of learning object in the learning resource
     	Given that an LXE or CD wants to add a reference to one more learning object in the learning resource
       		When they update the learning resource using a third-party tool
        		Then the user gets an error message of not found the reference to the learning object

   	Scenario: LXE/CD wants to update the reference from the previous learning resource with the current learning resource in the given learning object
     	Given that an LXE or CD wants to update the reference of the learning resource in the learning object
       		When they add the new reference and delete the old reference of the learning resource using a third-party tool
         		Then the old learning resource will get untagged and the new learning resource will get tagged to the learning object