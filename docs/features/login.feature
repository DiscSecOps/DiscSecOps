Feature: User Login Page
  As a user
  I want to log into my account
  So that I can access my content

  @ui @smoke
  Scenario: Login page is accessible
    Given I open the application and I am not logged in
    Then I should see the login form
    And I should see a link to register

  @ui @validation
  Scenario: Login button is disabled when form is empty
    Given I am on the login page
    Then the login button should be disabled

  @ui @validation
  Scenario: Login button is enabled when username and password are entered
    Given I am on the login page
    When I enter a username
    And I enter a password
    Then the login button should be enabled

  @ui @navigation
  Scenario: Navigate to register page from login
    Given I am on the login page
    When I click the "Register here" link
    Then I should be redirected to the register page

  @security @validation
  Scenario: Login fails with invalid password format (frontend validation)
    Given I am on the login page
    When I login with username "<TEST_USERNAME>" and password "testuserpass123!"
    Then I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error
    And I should remain on the login page

  @ui @validation
  Scenario: Login button is disabled with missing username
    Given I am on the login page
    When I enter a blank username and password "<TEST_PASSWORD>"
    Then the login button should be disabled

  @ui @validation
  Scenario: Login button is disabled with missing password
    Given I am on the login page
    When I enter username "<TEST_USERNAME>" and a blank password
    Then the login button should be disabled

