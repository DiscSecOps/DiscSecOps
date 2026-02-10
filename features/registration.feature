# features/registration.feature
Feature: User Registration

  Background:
    Given the backend is running on port 5000
    And the frontend is running on port 3000

  @registration @smoke @session
  Scenario: New user can register an account
    Given I am not a registered user
    When I navigate to the registration page
    And I enter "newuser" in the username field 
    And I enter "New User" in the full name field
    And I enter "SecurePass123!" in the password field
    And I enter "SecurePass123!" in the confirm password field
    And I click the "Create Account" button
    Then I should see message "Account created for newuser!"
    And I should be able to login with username "newuser"

  @registration @validation @session
  Scenario: Registration shows error on password mismatch
    Given I am on the registration page
    When I enter "user123" in the username field
    And I enter "Password123!" in the password field
    And I enter "Different123!" in the confirm password field
    And I click the "Create Account" button
    Then I should see error message "Passwords do not match"
    And I should remain on the registration page

  @registration @validation @session
  Scenario: Registration validates required fields
    Given I am on the registration page
    Then the "Create Account" button should be disabled
    When I enter only a username
    Then the button should still be disabled
    When I enter username and password
    Then the button should still be disabled
    When I confirm the password
    Then the button should be enabled