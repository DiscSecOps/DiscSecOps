# features/authentication.feature
Feature: User Authentication
  
  @auth @smoke
  Scenario: Existing user can login
    Given I am an existing user with username "alex"
    When I go to login page
    And I enter username "alex" and password "secret123"
    And I submit login form
    Then I should see my feed page
    And I should see my username "alex" displayed

  @auth @registration
  Scenario: New user is redirected to registration
    Given I am not a registered user
    When I go to login page
    And I enter username "newuser" and password "pass123"
    And I submit login form
    Then I should see message "User not found"
    And I should see link "Create an account"
    When I click "Create an account"
    Then I should be on registration page