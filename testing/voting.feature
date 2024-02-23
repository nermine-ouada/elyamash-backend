Feature: Image voting
  As a logged in user
  I want to be able to choose between  two images 

  Scenario: Valid vote
    Given I have logged into the application
    When I make a POST request to the vote endpoint
    Then I should receive a Successful vote response
    And the response status code should be 200

    