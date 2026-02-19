# features/user-dashboard-logout.feature
Feature: Logout from User Dashboard
  As an authenticated user
  I want to log out from the navbar
  So that I can securely end my session

  Scenario: User logs out successfully
    Given the user is authenticated
    And the user dashboard page is displayed
    When the user clicks the logout button in the navbar
    Then the logout function should be called
    And the user session should be cleared