Feature: User Registration
  As a new user
  I want to create an account
  So that I can access the application

   Background:
    Given I open the application and I am not logged in
    And I am on the register page

  @ui @smoke
  Scenario: Register page is accessible
    Given I am on the register page
    Then I should see the "Create Account" title
    And I should see the registration form
    And I should see a "Login here" link

  @ui @validation
  Scenario: Submit button is disabled when required fields are empty
    Given I am on the register page
    Then the "Create Account" button should be disabled
    When I enter a username
    And I enter an email
    And I enter a password
    And I enter a confirm password
    Then the "Create Account" button should be enabled

  @ui @navigation
  Scenario: Navigate to login page from register
    Given I am on the register page
    When I click the "Login here" link
    Then I should be redirected to the login page

  @security @validation
  Scenario: Registration fails with invalid email format
    Given I am on the register page
    When I enter a username
    And I enter an invalid email
    And I enter a password
    And I enter a confirm password
    And I click the "Create Account" button
    Then I should see an email error message
    And I should remain on the register page

  @security @validation
  Scenario: Registration fails with mismatched passwords
    Given I am on the register page
    When I enter a username
    And I enter an email
    And I enter a password
    And I enter a different confirm password
    And I click the "Create Account" button
    Then I should see a confirm password error message
    And I should remain on the register page