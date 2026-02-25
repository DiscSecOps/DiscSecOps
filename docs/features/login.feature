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

  Background:
    # This runs before every scenario to ensure our baseline user exists
    Given a user exists with username "john_doe" and password "SecurePass123!"

  @smoke @critical @ui
  Scenario: Successful login with valid credentials
    When I login with username "john_doe" and password "SecurePass123!" [cite: 3]
    Then I should be redirected to the UserDashboard 
    And I should see my username "john_doe" in the header 
    And a session cookie should be set 

  @smoke @ui
  Scenario: Successful login with case-insensitive username
    When I login with username "JOHN_DOE" and password "SecurePass123!"
    Then I should be redirected to the UserDashboard 

  @security @validation
  Scenario Outline: Login failures with invalid or missing credentials
    When I login with username "<username>" and password "<password>"
    Then I should see "<error_message>" error
    And I should remain on the login page 

    Examples:
      | username     | password         | error_message                |
      | john_doe     | WrongPass123!    | Invalid username or password |
      | unknown_user | anypass          | Invalid username or password |
      | john_doe     | securepass123!   | Invalid username or password |
      |              | SecurePass123!   | Username is required         |
      | john_doe     |                  | Password is required         |

  @security @rate-limiting
  Scenario: Account lockout after multiple failures
    When I attempt to login with wrong password 5 times [cite: 6]
    Then I should see "Account locked. Try again in 15 minutes" message 
    And even with correct password, login should fail 

  @session @security
  Scenario: Session expires after 24 hours
    Given I am logged in as "john_doe" 
    When my session is manually expired in the backend
    And I refresh the page 
    Then I should be redirected to the login page 

  @session @security
  Scenario: Single device per user invalidates previous sessions
    # We use 'Session A' and 'Session B' to represent different browser contexts
    Given I am logged in as "john_doe" in Session A
    When I login as "john_doe" in Session B
    Then Session A should be invalidated
    And Session A should be redirected to the login page on its next action