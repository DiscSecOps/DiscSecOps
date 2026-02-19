# features/user-dashboard-access-control.feature
Feature: User Dashboard Access Control
  As a user
  I want to access the user dashboard only if I am authenticated
  So that unauthorized users cannot view protected content

    Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  Scenario: Redirect unauthenticated user to login
    Given the user is not authenticated
    And authentication loading has completed
    When the user navigates to "/user-dashboard"
    Then the user should be redirected to "/login"

  Scenario: Show loading while authentication is being checked
    Given authentication is still loading
    When the user navigates to "/user-dashboard"
    Then a loading spinner should be displayed
    And the dashboard content should not be visible

  Scenario: Allow authenticated user to view dashboard
    Given the user is authenticated
    When the user navigates to "/user-dashboard"
    Then the dashboard layout should be displayed
    And the navbar should be visible
    And the sidebar should be visible