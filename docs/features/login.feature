# features/login.feature
Feature: User Login
  As a user of Social Circles
  I want to log into my account
  So that I can access my circles and content

  Business Rules:
    - Valid username and password required
    - After 5 failed attempts, account locked for 15 minutes
    - Session lasts 24 hours
    - One device per user

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given a user exists with:
      | username | john_doe        |
      | password | SecurePass123!  |
    When I login with username "john_doe" and password "SecurePass123!"
    Then I should be redirected to the UserDashboard
    And I should see my username "john_doe" in the header
    And a session cookie should be set

  @security
  Scenario: Login with wrong password
    Given a user exists with:
      | username | john_doe        |
      | password | SecurePass123!  |
    When I login with username "john_doe" and password "WrongPass123!"
    Then I should see "Invalid username or password" error
    And I should remain on the login page

  @security
  Scenario: Login with non-existent user
    When I login with username "unknown_user" and password "anypass"
    Then I should see "Invalid username or password" error
    And I should remain on the login page

  @security @rate-limiting
  Scenario: Account lockout after multiple failures
    Given a user exists with username "john_doe" and password "SecurePass123!"
    When I attempt to login with wrong password 5 times
    Then I should see "Account locked. Try again in 15 minutes" message
    And even with correct password, login should fail

  @session
  Scenario: Session persists for 24 hours
    Given I am logged in as "john_doe"
    When I wait for 24 hours
    And I refresh the page
    Then I should be redirected to the login page

  @session
  Scenario: Single device per user
    Given I am logged in as "john_doe" on Chrome
    When I login as "john_doe" on Firefox
    Then the Chrome session should be invalidated
    And Chrome should be redirected to login page on next action