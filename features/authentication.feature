
Feature: User Authentication

  As a user
  I want to register and login
  So I can access the social circles app

  Scenario: Successful user registration
    Given I am on the registration page
    When I fill in valid registration details
    And I submit the registration form
    Then I should see a success message
    And I should be redirected to the login page

  Scenario: User login with valid credentials
    Given I have a registered account
    When I enter my email and password
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see my profile information"