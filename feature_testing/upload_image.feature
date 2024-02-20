Feature: Image uploading
  As a logged in uploader or admin
  I want to be able to upload images

  Scenario: Valid vote
    Given I have logged into the application as uploader or admin
    When I make a POST request to the upload image endpoint
    Then I should receive a Successful upload response
    And the response status code should be 200
 