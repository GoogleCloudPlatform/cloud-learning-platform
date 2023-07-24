Feature: Establishing a relationship between the learning experience and learning objects
   
   Scenario: LXE/CD wants to associate the learning object with the learning experience
     Given that LXE or CD has access to the content authoring tool to copy learning experience
       When they design the learning experience and the learning object using a third-party tool
         Then the learning experience and the learning object will be created in a third-party tool
           And the learning object gets associated with the learning experience
   
   Scenario: LXE/CD adds the incorrect reference of the given learning experience in the learning object
     Given that an LXE or CD wants to create a learning object providing the reference of the given learning experience
       When they design the learning object using a third-party tool
         Then the user will get an error message of not found the reference to the learning experience

   Scenario: LXE/CD wants to associate a single learning object with multiple learning experiences
     Given that an LXE or CD wants to add the reference of learning experience in the learning object
       When they design the multiple learning experiences and the single learning object using a third-party tool
         Then the multiple learning experiences and the learning object will be created in a third-party tool
           And the learning object gets associated with the multiple learning experiences

   Scenario: LXE/CD wants to associate the multiple learning objects with the given learning experience
     Given that an LXE or CD wants to add the reference of a single learning experience in the multiple learning objects
       When they design the multiple learning objects using a third-party tool
         Then the learning objects will be created in a third-party tool
           And all the learning objects gets associated with the given learning experiences

   Scenario: LXE/CD wants to update the reference of the learning object with the new learning experience
     Given that an LXE or CD wants to replace an old reference of the learning experience with a new reference in the learning object
       When they update the new learning experience using a third-party tool
         Then the learning object gets associated with the new learning experience
   
   Scenario: LXE/CD updating the incorrect reference of learning experience in the learning object
     Given that an LXE or CD wants to add a reference to one more learning experience in the learning object
       When they update the learning object using a third-party tool
         Then the user gets an error message of not found the reference to the learning experience

   Scenario: LXE/CD wants to update the reference from the previous learning object with the current learning object in the given learning experience
     Given that an LXE or CD wants to update the reference of the learning object in the learning experience
       When they add the new reference and delete the old reference of the learning object using a third-party tool
         Then the old learning object will get untagged and the new learning object will get tagged to the learning experience