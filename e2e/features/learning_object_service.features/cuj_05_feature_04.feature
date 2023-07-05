Feature: Establishing a relationship between the curriculum pathway and learning experience
   
   Scenario: LXE/CD wants to associate the learning experience with the curriculum pathway
     Given that LXE or CD has access to the content authoring tool
       When they design the curriculum pathway and the learning experience using a third-party tool
         Then the curriculum pathway and the learning experience will be created in a third-party tool
           And the learning experience gets associated with the curriculum pathway
   
   Scenario: LXE/CD adds the incorrect reference of the given curriculum pathway in the learning experience
     Given that an LXE or CD wants to create a learning experience providing the reference of the given curriculum pathway with incorrect uuid
       When they design the learning experience using a third-party tool
         Then the user will get an error message of not found the reference to the curriculum pathway

   Scenario: LXE/CD wants to associate a single learning experience with multiple curriculum pathways
     Given that an LXE or CD wants to add the reference of curriculum pathway in the learning experience
       When they design the multiple curriculum pathways and the single learning experience using a third-party tool
         Then the multiple curriculum pathways and the learning experience will be created in a third-party tool
           And the learning experience gets associated with the multiple curriculum pathways

   Scenario: LXE/CD wants to associate the multiple learning experiences with the given curriculum pathway
     Given that an LXE or CD wants to add the reference of a single curriculum pathway in the multiple learning experiences
       When they design the multiple learning experiences using a third-party tool
         Then the multiple learning experiences will be created in a third-party tool
           And all the learning experiences gets associated with the given curriculum pathways

   Scenario: LXE/CD wants to update the reference of the learning experience with the new curriculum pathway
     Given that an LXE or CD wants to replace an old reference of the curriculum pathway with a new reference in the learning experience
       When they update the new curriculum pathway using a third-party tool
         Then the learning experience gets associated with the new curriculum pathway
   
   Scenario: LXE/CD updating the incorrect reference of curriculum pathway in the learning experience
     Given that an LXE or CD wants to add a reference to one more curriculum pathway in the learning experience
       When they update the learning experience using a third-party tool by adding incorrect reference of the curriculum pathway
         Then the user gets an error message of not found the reference to the curriculum pathway

   Scenario: LXE/CD wants to update the reference from the previous learning experience with the current learning experience in the given curriculum pathway
     Given that an LXE or CD wants to update the reference of the learning experience in the curriculum pathway
       When they add the new reference and delete the old reference of the learning experience using a third-party tool
         Then the old learning experience will get untagged and the new learning experience will get tagged to the curriculum pathway

    Scenario: LXE/CD wants to associate the child curriculum pathway with the parent curriculum pathway
     Given that LXE or CD has access to the content authoring tool to associate the child curriculum pathway with the parent curriculum pathway
       When they design the parent curriculum pathway and the child curriculum pathway using a third-party tool
         Then the parent curriculum pathway and the child curriculum pathway will be created in a third-party tool
           And the child curriculum pathway gets associated with the parent curriculum pathway

    Scenario: LXE/CD adds the incorrect reference of the given parent curriculum pathway in the child curriculum pathway
      Given that an LXE or CD wants to create a child curriculum pathway providing the reference of the given parent curriculum pathway with incorrect uuid
        When they design the child curriculum pathway using a third-party tool
          Then the user will get an error message of not found the reference to the parent curriculum pathway

    Scenario: LXE/CD wants to associate a single child curriculum pathway with multiple parent curriculum pathways
      Given that an LXE or CD wants to add the reference of parent curriculum pathway in the child curriculum pathway
        When they design the multiple parent curriculum pathways and the single child curriculum pathway using a third-party tool
          Then the multiple parent curriculum pathways and the child curriculum pathway will be created in a third-party tool
            And the child curriculum pathway gets associated with the multiple parent curriculum pathways
