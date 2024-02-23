Feature: User Authentication
  As a registered user
  I want to be able to log in to the system
  So that I can access protected resources

  Scenario: Successful Login
    Given I have user authentication credentials
    When I make a POST request to the login endpoint
    Then I should receive a valid access token
    And the response status code should be 200

    