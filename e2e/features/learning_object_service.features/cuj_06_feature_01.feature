@content-serving-api
Feature: Create Signed URls for video and HTML5 content

  Scenario: User wants a Signed URl to access video/HTML content and expecting response in json format
    Given that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content and wants response in json format 
      When API request is sent to create Signed Url with valid learning resource uuid and redirect as False
        Then LOS will return a json response with signed URl

  Scenario: User wants to redirect to a Signed URl to access video or HTML content 
    Given that an LXE or CD has access to the content authoring tool and wants to redirect to signed url 
      When API request is sent to create Signed Url with valid learning resource uuid and redirect as True
        Then LOS will serve the redirect response with signed url

  Scenario: User wants a Signed URl to access video/HTML content with incorrect learning resource uuid
    Given that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content providing invalid uuid
      When API request is sent to create Signed Url with invalid learning resource uuid
        Then LOS will not return signed url and throws ResourceNotFound error for learning resource

  Scenario: User wants a Signed URl to access video/HTML content with correct learning resource uuid which has incorrect resource path
    Given that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content which has incorrect resource path
      When API request is sent to create Signed Url with valid learning resource uuid which has incorrect resource path
        Then LOS will not return signed url and throws ResourceNotFound error for video/html5 content

  Scenario: User wants a Signed URl to access video/HTML content with correct learning resource uuid with empty resource path
    Given that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 for which resource path is empty
      When API request is sent to create Signed Url with valid learning resource uuid which has empty resource path
        Then LOS will not return signed url and throws ResourceNotFound error for resource path  
  
