# features/user-dashboard-error-handling.feature
Feature: User Dashboard Error Handling
  As an authenticated user
  I want to be informed if user dashboard data fails to load
  So that I understand something went wrong

    Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  Scenario: Display error message on failed data fetch
    Given the user is authenticated
    And the user dashboard service request fails
    When the user dashboard page attempts to load data
    Then an error message "Failed to load user dashboard data" should be displayed
    And the loading spinner should disappear

  Scenario: Handle unauthorized API response
    Given the user is authenticated
    And the user dashboard service returns status 401
    When the user dashboard page attempts to load data
    Then an error message should be displayed
    And the user may be logged out