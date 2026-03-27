Feature: User Dashboard
  As a logged-in user
  I want to see my dashboard
  So that I can access my circles and content

  Background:
    Given I am on the dashboard page

  @smoke @ui
  Scenario: New user sees empty dashboard
    Given a user exists with username "<TEST_USERNAME>" and password "<TEST_PASSWORD>"
    And I am logged in as "<TEST_USERNAME>"
    Then I should see "Welcome back, <TEST_USER>! 👋"
    And I should see "You haven't joined any circles yet"
    And I should see a "Create Your First Circle" button