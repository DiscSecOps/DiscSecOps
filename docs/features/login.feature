Feature: User Login 
  As a user
  I want to log into my account
  So that I can access my circles and content

  @ui @smoke
  Scenario: Login page is accessible
    Given I open the application
    When I go to the login page
    Then I should see the login form
    And I should see a link to register

  @ui @validation
  Scenario: Login button is disabled when form is empty
    Given I am on the login page
    Then the login button should be disabled
    When I enter a username
    And I enter a password
    Then the login button should be enabled

  @ui @navigation
  Scenario: Navigate to register page from login
    Given I am on the login page
    When I click the register link
    Then I should be redirected to the register page

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given a user exists with username "<TEST_USERNAME>" and password "<TEST_PASSWORD>"
    When I login with username "<TEST_USERNAME>" and password "<TEST_PASSWORD>"
    Then I should be redirected to the UserDashboard 
    And I should see my username "<TEST_USERNAME>" in the header 
    And a session cookie should be set

  @security @validation
  Scenario: Login fails with invalid password format (frontend validation)
    When I login with username "<TEST_USERNAME>" and password "testuserpass123!"
    Then I should see "Password must be at least 8 characters and include uppercase, lowercase, number, and special character" error
    And I should remain on the login page

  @ui @validation
  Scenario: Login button is disabled with missing username
    When I enter a blank username and password "<TEST_PASSWORD>"
    Then the login button should be disabled

  @ui @validation
  Scenario: Login button is disabled with missing password
    When I enter username "<TEST_USERNAME>" and a blank password
    Then the login button should be disabled