# features/user-dashboard-layout-components.feature
Feature: User Dashboard Layout
  As an authenticated user
  I want to see the user dashboard layout components
  So that I can navigate and view platform content

    Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  Scenario: Display user dashboard cards
    Given the user is authenticated
    And user dashboard data has finished loading
    When the dashboard is rendered
    Then the card "Your Circles (0)" should be displayed
    And the card "Recent Posts (0)" should be displayed
    And the card "Notifications (0)" should be displayed

  Scenario: Display raw user dashboard statistics when data exists
    Given the user is authenticated
    And user dashboard data is available
    When the user dashboard is rendered
    Then the user dashboard statistics section should be displayed
    And the statistics should be formatted as JSON