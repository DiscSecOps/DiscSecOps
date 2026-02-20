# features/registration.feature
Feature: User Registration
  As a new user
  I want to create an account
  So that I can join Social Circles

  Business Rules:
    - Username: required, 3-50 chars, alphanumeric + underscore
    - Email: required, valid format, unique
    - Password: required, min 8 chars with 1 uppercase, 1 lowercase, 1 number, 1 special
    - Full name: optional, max 100 chars

  @smoke @critical
  Scenario: Successful registration with valid data
    Given I am on the registration page
    When I fill in:
      | username   | john_doe        |
      | full_name  | John Doe        |
      | email      | john@test.com   |
      | password   | SecurePass123!  |
      | confirm    | SecurePass123!  |
    And I click the register button
    Then I should be redirected to the login page
    And I should see "Account created successfully" message

  @security
  Scenario: Registration with existing username
    Given a user exists with username "john_doe"
    When I try to register with username "john_doe"
    Then I should see "Username already taken" error
    And I should remain on the registration page

  @security
  Scenario: Registration with mismatched passwords
    When I fill in:
      | username   | john_doe        |
      | password   | SecurePass123!  |
      | confirm    | DifferentPass!  |
    And I click the register button
    Then I should see "Passwords do not match" error

  @security
  Scenario: Registration with invalid email format
    When I fill in:
      | username   | john_doe        |
      | email      | invalid-email   |
      | password   | SecurePass123!  |
    And I click the register button
    Then I should see "Invalid email format" error

  @security
  Scenario: Registration with weak password
    When I fill in:
      | username   | john_doe         |
      | password   | weak             |
    And I click the register button
    Then I should see "Password must be at least 8 characters" error