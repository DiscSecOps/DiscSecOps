# features/user-dashboard-welcome-message.feature
Feature: Personalized Welcome Message
  As an authenticated user
  I want to see a personalized welcome message
  So that the user dashboard feels customized to me

    Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  Scenario: Display username only
    Given the user is authenticated
    And the user has username "john123"
    And the user does not have a full name
    When the user dashboard loads
    Then the welcome message should display "Welcome back, john123!"

  Scenario: Display username and full name
    Given the user is authenticated
    And the user has username "john123"
    And the user has full name "John Smith"
    When the user dashboard loads
    Then the welcome message should display "Welcome back, john123! (John Smith)"