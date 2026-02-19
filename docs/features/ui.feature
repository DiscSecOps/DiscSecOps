# features/ui.feature
Feature: Authentication UI
  
  @ui @smoke
  Scenario: Login page is accessible
    Given I open the application
    When I go to the login page
    Then I should see the login form

  @ui @smoke  
  Scenario: Register page is accessible
    Given I open the application
    When I go to the register page
    Then I should see the registration form

  @ui @validation
  Scenario: Login button is disabled when form is empty
    Given I am on the login page
    Then the login button should be disabled
    When I enter a username
    And I enter a password
    Then the login button should be enabled