# features/login.feature
Feature: User Login

  Background:
    Given the backend is running on port 8000
    And the frontend is running on port 3000

  @login @smoke @session
  Scenario: Successful login with session-based authentication
    Given I am a registered user with username "johndoe"
    When I navigate to the login page
    And I enter "johndoe" in the username field
    And I enter "SecurePass123!" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see "Welcome back, johndoe!" on the dashboard
    And my session cookie should be set

  @login @error @session
  Scenario: User sees error on invalid login
    Given I am on the login page
    When I enter "wronguser" in the username field
    And I enter "wrongpass" in the password field
    And I click the "Login" button
    Then I should see error message "Invalid credentials"
    And I should remain on the login page

  @login @protected @session
  Scenario: Unauthenticated user cannot access dashboard
    Given I am not logged in
    When I try to access the dashboard page
    Then I should be redirected to the login page
    And I should see "Login to Social Circles"