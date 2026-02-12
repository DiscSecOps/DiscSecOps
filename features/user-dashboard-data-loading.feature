# features/user-dashboard-data-loading.feature
Feature: User Dashboard Data Loading
  As an authenticated user
  I want my user dashboard data to load automatically
  So that I can see my circles, posts, and notifications

    Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  Scenario: Load user dashboard data successfully
    Given the user is authenticated
    When the user dashboard page loads
    Then the system should call the user dashboard service
    And a loading spinner should be displayed
    And the user dashboard data should be stored
    And the loading spinner should disappear
    And the user dashboard cards should be displayed

  Scenario: Do not load user dashboard data if user is not authenticated
    Given the user is not authenticated
    When the user dashboard page loads
    Then the user dashboard service should not be called